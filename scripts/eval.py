#!/usr/bin/env python3
"""Replay behavior scenarios through `claude -p` and grade the decisions.

Each scenario in evals/scenarios/ holds one forge snapshot, the command, and
the expected result block. The agent reads the skill with the Read tool only;
nothing is live. The grader reads the STATE / WRITES / NEXT block at the end
of the reply.

    python3 scripts/eval.py                 # run every scenario on this checkout
    python3 scripts/eval.py --ref f6bc3d4   # run on an older commit
    python3 scripts/eval.py --only tier-light --model sonnet
    python3 scripts/eval.py --self-test     # grade the fixtures offline
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = ROOT / "evals" / "scenarios"

PROMPT = """You are dry-running the git-collaboration skill. Its files are in {skill}.
Read {skill}/SKILL.md first, then only the files it tells you to read for this command.
Nothing is live: do not run gh, glab, git, or any other command, and do not start a subagent.
Treat the snapshot below as the one forge snapshot, and treat the extra facts as already
observed in the local checkout. Decide what the skill tells you to do.

Command: {command}
Authenticated user: {user}
Snapshot:
```json
{snapshot}
```
{extra}

Explain briefly, then end your reply with exactly this block and nothing after it:
STATE: <the one primary state you classified, or n/a>
WRITES:
- <each forge or git write command you would run, one per line, or none>
NEXT: <the `next step:` line you would print, or none>
"""


def load_scenarios(only: list[str] | None = None) -> list[dict]:
    scenarios = [json.loads(p.read_text(encoding="utf-8")) for p in sorted(SCENARIOS.glob("*.json"))]
    return [s for s in scenarios if not only or s["id"] in only]


BULLET = re.compile(r"^(?:[-*+]|\d+[.)])\s+")


def clean(line: str) -> str:
    """Drop blockquote, bold, and code marks around a result-block line."""
    return line.strip().lstrip(">").strip().replace("**", "").strip("`").strip()


def parse_block(reply: str) -> dict | None:
    """Return {state, writes, next} from the last result block, or None."""
    lines = [clean(line) for line in reply.splitlines()]
    starts = [i for i, line in enumerate(lines) if line.startswith("STATE:")]
    if not starts:
        return None
    block = lines[starts[-1]:]
    state = block[0][len("STATE:"):].strip().strip("`")
    writes: list[str] = []
    nxt = None
    for line in block[1:]:
        if line.startswith("NEXT:"):
            nxt = line[len("NEXT:"):].strip().strip("`")
            break
        bullet = BULLET.match(line)
        if bullet:
            item = line[bullet.end():].strip().strip("`")
            if item.lower() != "none":
                writes.append(item)
    if nxt is None:
        return None
    return {"state": state, "writes": writes, "next": nxt}


def grade(expect: dict, reply: str) -> list[str]:
    """Return failure reasons; an empty list is a pass."""
    failures: list[str] = []
    plain = reply.replace("**", "")
    for pattern in expect.get("reply_must_re", []):
        if not re.search(pattern, plain, re.M):
            failures.append(f"reply has no match for {pattern!r}")
    for pattern in expect.get("reply_must_not_re", []):
        if re.search(pattern, plain, re.M):
            failures.append(f"reply matches forbidden {pattern!r}")
    for text in expect.get("reply_must", []):
        if text not in reply:
            failures.append(f"reply missing {text!r}")
    for text in expect.get("reply_must_not", []):
        if text in reply:
            failures.append(f"reply contains {text!r}")
    needs_block = any(key in expect for key in ("state", "writes_must", "writes_must_not", "next"))
    block = parse_block(reply)
    if block is None:
        if needs_block:
            failures.append("no STATE/WRITES/NEXT block")
        return failures
    if "state" in expect and block["state"] not in expect["state"]:
        failures.append(f"state {block['state']!r} not in {expect['state']}")
    for pattern in expect.get("writes_must", []):
        if not any(pattern in write for write in block["writes"]):
            failures.append(f"no write matching {pattern!r}")
    for pattern in expect.get("writes_must_not", []):
        hits = [write for write in block["writes"] if pattern in write]
        if hits:
            failures.append(f"forbidden write {hits[0]!r}")
    if "next" in expect:
        got = block["next"]
        if expect["next"] not in (got, f"next step: {got}"):
            failures.append(f"next {got!r} != {expect['next']!r}")
    return failures


def self_test_errors() -> list[str]:
    errors: list[str] = []
    for scenario in load_scenarios():
        fixtures = scenario.get("self_test", {})
        if "pass" not in fixtures or "fail" not in fixtures:
            errors.append(f"evals: {scenario['id']} has no pass/fail self_test fixtures")
            continue
        failures = grade(scenario["expect"], fixtures["pass"])
        if failures:
            errors.append(f"evals: {scenario['id']} pass fixture fails: {failures[0]}")
        if not grade(scenario["expect"], fixtures["fail"]):
            errors.append(f"evals: {scenario['id']} fail fixture passes")
    return errors


def run_one(skill: Path, scenario: dict, model: str | None, workdir: Path) -> dict:
    prompt = PROMPT.format(
        skill=skill.as_posix(),
        command=scenario["command"],
        user=scenario["user"],
        snapshot=json.dumps(scenario["snapshot"], indent=2),
        extra=scenario.get("extra", ""),
    )
    claude = shutil.which("claude")
    if not claude:
        return {"id": scenario["id"], "failures": ["claude CLI not found on PATH"]}
    cmd = [
        claude, "-p", prompt,
        "--output-format", "json",
        "--tools", "Read",
        "--allowedTools", "Read",
        "--add-dir", str(skill),
        "--setting-sources", "project",
        "--strict-mcp-config",
        "--disable-slash-commands",
        "--no-session-persistence",
    ]
    if model:
        cmd += ["--model", model]
    try:
        done = subprocess.run(cmd, cwd=workdir, capture_output=True, text=True, encoding="utf-8", timeout=900)
    except (OSError, subprocess.TimeoutExpired) as error:
        return {"id": scenario["id"], "failures": [f"claude did not finish: {error}"]}
    try:
        data = json.loads(done.stdout)
    except json.JSONDecodeError:
        return {"id": scenario["id"], "failures": [f"claude exited {done.returncode}: {done.stderr.strip()[:200]}"]}
    usage = data.get("usage") or {}
    reply = data.get("result") or ""
    return {
        "id": scenario["id"],
        "failures": grade(scenario["expect"], reply),
        "input_tokens": sum(usage.get(k, 0) for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")),
        "output_tokens": usage.get("output_tokens", 0),
        "turns": data.get("num_turns"),
        "cost_usd": data.get("total_cost_usd"),
        "reply": reply,
    }


def checkout(ref: str) -> Path:
    path = Path(tempfile.mkdtemp(prefix="gitcollab-eval-"))
    try:
        subprocess.run(["git", "worktree", "add", "--detach", str(path), ref], cwd=ROOT, check=True, capture_output=True)
    except subprocess.CalledProcessError:
        shutil.rmtree(path, ignore_errors=True)
        raise
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--ref", help="evaluate the skill at this git ref instead of the checkout")
    parser.add_argument("--only", nargs="*", help="scenario ids to run")
    parser.add_argument("--model", help="model alias passed to claude --model")
    parser.add_argument("--out", help="write the full results, replies included, to this JSON file")
    parser.add_argument("--self-test", action="store_true", help="grade the fixtures offline and exit")
    parser.add_argument("--regrade", help="grade the replies saved in an --out file against the current scenarios")
    args = parser.parse_args()

    if args.regrade:
        expects = {s["id"]: s["expect"] for s in load_scenarios()}
        saved = json.loads(Path(args.regrade).read_text(encoding="utf-8"))
        passed = 0
        for result in saved:
            failures = grade(expects[result["id"]], result.get("reply", "")) if result["id"] in expects else ["unknown scenario"]
            passed += not failures
            verdict = "PASS" if not failures else "FAIL " + "; ".join(failures)
            print(f"{result['id']:<22} in={result.get('input_tokens', 0):>7} {verdict}")
        print(f"{passed}/{len(saved)} passed")
        return 0 if passed == len(saved) else 1

    if args.self_test:
        errors = self_test_errors()
        for error in errors:
            print(error, file=sys.stderr)
        print("evals self-test " + ("failed" if errors else f"passed ({len(load_scenarios())} scenarios)"))
        return 1 if errors else 0

    scenarios = load_scenarios(args.only)
    if not scenarios:
        print(f"no scenarios match {args.only}", file=sys.stderr)
        return 1
    try:
        skill = checkout(args.ref) if args.ref else ROOT
    except subprocess.CalledProcessError as error:
        print(f"git worktree add {args.ref} failed: {error.stderr.decode(errors='replace').strip()}", file=sys.stderr)
        return 1
    results = []
    try:
        with tempfile.TemporaryDirectory(prefix="gitcollab-eval-cwd-") as workdir:
            for scenario in scenarios:
                result = run_one(skill, scenario, args.model, Path(workdir))
                results.append(result)
                verdict = "PASS" if not result["failures"] else "FAIL " + "; ".join(result["failures"])
                print(
                    f"{scenario['id']:<22} in={result.get('input_tokens', 0):>7} "
                    f"turns={result.get('turns')} cost=${result.get('cost_usd') or 0:.3f} {verdict}",
                    flush=True,
                )
    finally:
        if args.ref:
            subprocess.run(["git", "worktree", "remove", "--force", str(skill)], cwd=ROOT, capture_output=True)
            subprocess.run(["git", "worktree", "prune"], cwd=ROOT, capture_output=True)
    passed = sum(1 for r in results if not r["failures"])
    total_in = sum(r.get("input_tokens", 0) for r in results)
    total_cost = sum(r.get("cost_usd") or 0 for r in results)
    print(f"{passed}/{len(results)} passed, {total_in} input tokens, ${total_cost:.3f}")
    if args.out:
        Path(args.out).write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
