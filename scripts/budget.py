#!/usr/bin/env python3
"""Print and cap the instruction bytes each mode loads.

A mode loads SKILL.md plus the references its load line in SKILL.md names.
"the forge reference" counts the larger of github.md and gitlab.md. pstack.md counts in
the pstack column when a loaded file points at it. Tokens are bytes / 4.
CRLF counts as LF so a Windows checkout measures the same.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Bytes. Caps only go down: lower a cap when a change shrinks a mode.
MODE_CAPS = {
    "Review someone else's PR/MR": 44_524,
    "Plan issue": 35_586,
    "Implement issue then PR/MR": 43_023,
    "Reply to issue": 13_007,
    "Update own PR/MR after review": 27_168,
    "Fix PR/MR conflicts": 26_120,
    "Merge approved PR/MR": 31_186,
    "Request PR/MR review": 20_316,
    "Focused PR/MR status": 18_632,
    "Status or triage, including the aggressive run": 23_851,
    "Scheduled lifecycle or scheduled approved merge": 29_203,
}

LOAD_LINE = re.compile(r"^([A-Z][^|#\n]*?): read (.+)$", re.M)
REF = re.compile(r"`(?:references/)?([a-z0-9-]+\.md)`")
FORGE_PAIR = ("references/github.md", "references/gitlab.md")
PSTACK = "references/pstack.md"
CRLF = bytes([13, 10])
LF = bytes([10])


def size(rel: str) -> int:
    path = ROOT / rel
    return len(path.read_bytes().replace(CRLF, LF)) if path.exists() else 0


def mode_loads() -> dict[str, tuple[int, int]]:
    """Return {mode: (bytes, bytes with pstack)}."""
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    loads: dict[str, tuple[int, int]] = {}
    for mode, rest in LOAD_LINE.findall(skill):
        refs = list(dict.fromkeys(f"references/{name}" for name in REF.findall(rest)))
        if "the forge reference" in rest:
            refs.append(FORGE_PAIR[0])
        forge = [ref for ref in refs if ref in FORGE_PAIR]
        files = [ref for ref in refs if ref not in FORGE_PAIR]
        total = size("SKILL.md") + sum(size(ref) for ref in files)
        if forge:
            total += max(size(ref) for ref in FORGE_PAIR)
        read = [ROOT / "SKILL.md", *(ROOT / ref for ref in files + (list(FORGE_PAIR) if forge else []))]
        points = PSTACK not in files and any(
            PSTACK in p.read_text(encoding="utf-8") for p in read if p.exists()
        )
        loads[mode] = (total, total + size(PSTACK) if points else total)
    return loads


def budget_errors(loads: dict[str, tuple[int, int]]) -> list[str]:
    errors: list[str] = []
    for mode, cap in MODE_CAPS.items():
        if mode not in loads:
            errors.append(f"budget: no load line for {mode!r}")
            continue
        if loads[mode][0] > cap:
            errors.append(f"budget: {mode!r} loads {loads[mode][0]} bytes, cap {cap}")
    for mode in loads:
        if mode not in MODE_CAPS:
            errors.append(f"budget: {mode!r} has no cap in scripts/budget.py")
    return errors


CAP_LINE = re.compile(r'^    "(.+?)": ([0-9_]+),$', re.M)


def base_ref() -> str:
    return os.environ.get("BUDGET_BASE", "origin/main")


def base_caps() -> dict[str, int] | None:
    """MODE_CAPS as written at the base ref, or None when unreadable."""
    try:
        text = subprocess.run(
            ["git", "show", f"{base_ref()}:scripts/budget.py"],
            cwd=ROOT, capture_output=True, text=True, encoding="utf-8", check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        return None
    caps = {mode: int(value.replace("_", "")) for mode, value in CAP_LINE.findall(text)}
    return caps or None


def cap_raise_errors(caps: dict[str, int], base: dict[str, int]) -> list[str]:
    return [
        f"budget: cap for {mode!r} rose from {base[mode]} to {cap} (caps only go down)"
        for mode, cap in caps.items()
        if mode in base and cap > base[mode]
    ]


def lower_caps(loads: dict[str, tuple[int, int]]) -> None:
    """Rewrite MODE_CAPS in this file down to the current totals. Never raises a cap."""
    path = Path(__file__)
    text = path.read_text(encoding="utf-8")
    changed = False
    for mode, cap in MODE_CAPS.items():
        if mode in loads and loads[mode][0] < cap:
            text, count = re.subn(
                rf"({re.escape(chr(34) + mode + chr(34))}: )[0-9_]+",
                lambda m: m.group(1) + f"{loads[mode][0]:_}",
                text,
            )
            if count != 1:
                raise SystemExit(f"budget: cap for {mode!r} not found in {path.name}")
            changed = True
    if changed:
        path.write_text(text, encoding="utf-8")


def main() -> int:
    loads = mode_loads()
    if "--lower-caps" in sys.argv[1:]:
        lower_caps(loads)
    print(f"{'mode':<50} {'bytes':>7} {'~tokens':>8} {'+pstack':>8}")
    for mode, (total, with_pstack) in loads.items():
        print(f"{mode:<50} {total:>7} {total // 4:>8} {with_pstack // 4:>8}")
    print(f"{'SKILL.md alone':<50} {size('SKILL.md'):>7} {size('SKILL.md') // 4:>8}")
    errors = budget_errors(loads)
    for error in errors:
        print(error, file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
