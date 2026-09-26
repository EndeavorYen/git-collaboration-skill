#!/usr/bin/env python3
"""Fail closed on company/personal leaks and missing dual-forge contracts."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []

LEAK_PATTERNS = [
    ("email address", re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)),
    ("unix home path", re.compile(r"(?<![\w$])/(?:home|Users)/[A-Za-z0-9._-]+")),
    ("windows home path", re.compile(r"(?i)\b[A-Z]:\\Users\\[A-Za-z0-9._-]+")),
    ("forge token", re.compile(r"glpat-[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}")),
    ("private key", re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----")),
]

REQUIRED_FILES = [
    ROOT / "SKILL.md",
    ROOT / "references" / "github.md",
    ROOT / "references" / "gitlab.md",
    ROOT / "references" / "scheduled-automation.md",
    ROOT / "references" / "pre-submit.md",
    ROOT / "references" / "review.md",
    ROOT / "references" / "plan-issue.md",
    ROOT / "references" / "implement.md",
    ROOT / "references" / "revise.md",
    ROOT / "references" / "conflict.md",
    ROOT / "references" / "merge.md",
    ROOT / "references" / "reply.md",
    ROOT / "references" / "request-review.md",
    ROOT / "references" / "status.md",
    ROOT / "references" / "triage.md",
    ROOT / "references" / "pstack.md",
    ROOT / "references" / "pstack-compat.md",
    ROOT / "prompts" / "git-review-pr.md",
    ROOT / "prompts" / "git-issue-pr.md",
    ROOT / "prompts" / "git-plan-issue.md",
    ROOT / "prompts" / "git-reply-issue.md",
    ROOT / "prompts" / "git-revise-pr.md",
    ROOT / "prompts" / "git-fix-conflict.md",
    ROOT / "prompts" / "git-merge-approved.md",
    ROOT / "prompts" / "git-request-review.md",
    ROOT / "prompts" / "git-pr-status.md",
    ROOT / "prompts" / "git-triage.md",
    ROOT / "prompts" / "git-scheduled-lifecycle.md",
    ROOT / "prompts" / "git-scheduled-merge.md",
    ROOT / "prompts" / "git-review-pr-force.md",
    ROOT / "prompts" / "git-merge-approved-force.md",
    ROOT / "prompts" / "git-revise-pr-force.md",
]

SKILL_PHRASES = [
    "Detect the forge",
    "GitHub",
    "GitLab",
    "Never invent a reviewer",
    "no hard-coded reviewer",
    "approving reviewer",
    "READY_TO_MERGE",
    "REVIEW_NOT_AUTHORIZED",
    "WRITE_NOT_AUTHORIZED",
    "MERGE_NOT_AUTHORIZED",
    "self_authored_head",
    "/git-review-pr-force",
    "/git-merge-approved-force",
    "/git-revise-pr-force",
    "<!-- git-force-review -->",
    "Solo override",
    "next step:",
    "does not print the Solo override block",
    "does not inherit force",
    "Forge budget",
    "Context budget",
    "local checkout",
    "write response is the read-back",
    "Do not read repository files",
    "Explicit force",
]

SKILL_WORD_LIMIT = 3000

REFERENCE_PHRASES = {
    "pre-submit.md": [
        "open-code-review-delegate",
        "requesting-code-review",
        "pre-submit gate",
        "fresh subagent",
        "human in this conversation",
        "Blanket ship language is not a waiver",
        "Critical and High findings are submit blockers",
        "do not push, do not open or update the PR/MR",
    ],
    "review.md": [
        "references/pre-submit.md",
        "OCR Step 7 Fix stays off",
        "<!-- git-force-review -->",
        "Evidence class",
        "verdict: approve",
        "verdict: request-changes",
        "forge approval: absent",
        "forge approval: present",
        "next step:",
        "同意",
        "不同意",
        "agree or disagree",
        "Re-run the `Proof:` command on the current review head",
        "cannot re-run",
        "An Evidence class mismatch is `verdict: request-changes` with severity High",
        "Do not require rerunning a protected live job before approval",
    ],
    "plan-issue.md": [
        "<!-- git-plan-issue -->",
        "<!-- git-plan-issue-dissent -->",
        "The brief is a proposal",
        "gentle-grill-me",
        "confirms the close log",
        "unsettled product decision",
        "Do not post a brief while an unsettled product decision remains",
        "already settled",
        "Load `gentle-grill-me` only when",
        "The local grill log is not the issue comment",
        "material disagreement",
        "human decision",
        "write that contract into the issue description",
        "### Exceptions",
        "**Original:**",
        "**This issue:**",
        "**Still elsewhere:**",
        "description holds the checkable acceptance checklist",
        "do not duplicate the full checklist",
        'status: "follow_up"',
        'open a forge issue for each confirmed close log record with `status: "follow_up"`',
        'fails this mode when a `follow_up` record has no issue URL',
        "## Executor-ready brief",
        "**Planned at:**",
        "### Execution plan",
        "### Interfaces",
        "### Test cases",
        "### Stop and dissent when",
        "Do not write function bodies",
        "No vague verbs",
        "more than 8 steps",
        "never the line's text",
        "also an unsettled product decision about Out of scope",
    ],
    "implement.md": [
        "Do not ask the user to invoke `/git-issue-pr` again",
        "same session",
        "references/plan-issue.md",
        "references/pre-submit.md",
        "stale description checklist is a failed plan",
        "description holds the checkable acceptance checklist",
        "read-then-write gate",
        "out of mode",
        "at most one focused search",
        "it is the work order",
        "planned-at",
        "Stop and dissent when",
        "every brief Test case",
        "do not revert them",
    ],
    "revise.md": [
        "NEEDS_REVISION",
        "pre-submit gate",
        "references/pre-submit.md",
        "next step:",
    ],
    "conflict.md": [
        "CONFLICTED",
        "pre-submit gate",
        "references/pre-submit.md",
    ],
    "merge.md": [
        "approving reviewer",
        "MERGE_NOT_AUTHORIZED",
        "exact current head",
        "next step:",
    ],
    "reply.md": [
        "No reply needed",
    ],
    "request-review.md": [
        "Never invent a reviewer",
        "REVIEW_REQUEST_NEEDED",
    ],
    "status.md": [
        "Solo override",
    ],
    "triage.md": [
        "does not inherit force",
        "/git-plan-issue",
        "ask who to assign",
    ],
    "pstack.md": [
        "pstack:off",
        "pstack:required",
        "git-collaboration wins",
        "never writes to the forge",
        "Forge budget",
    ],
}

PSTACK_WORD_LIMIT = 900

PSTACK_FORBIDDEN_PROMPTS = (
    "git-merge-approved.md",
    "git-merge-approved-force.md",
    "git-scheduled-lifecycle.md",
    "git-scheduled-merge.md",
    "git-triage.md",
    "git-reply-issue.md",
    "git-request-review.md",
    "git-pr-status.md",
)

TRIAGE_LOAD_LINE = "Status or triage, including the aggressive run: read `references/triage.md`."

# Numbered-procedure sentences. Prompts point at the home; they do not copy it.
PROCEDURE_SENTENCES = [
    "Critical and High findings are submit blockers",
    "The brief is a proposal",
    "Load `gentle-grill-me` only when",
    "OCR Step 7 Fix stays off",
    "Do not ask the user to invoke `/git-issue-pr` again",
    "Blanket ship language is not a waiver",
]

PROMPT_PHRASES = {
    "git-review-pr.md": [
        "REVIEW_NOT_AUTHORIZED",
        "references/review.md",
        "references/pre-submit.md",
        "references/github.md",
        "references/gitlab.md",
    ],
    "git-review-pr-force.md": [
        "/git-review-pr-force",
        "references/review.md",
        "references/pre-submit.md",
        "next step:",
    ],
    "git-plan-issue.md": [
        "references/plan-issue.md",
        "references/github.md",
        "references/gitlab.md",
    ],
    "git-issue-pr.md": [
        "references/implement.md",
        "references/plan-issue.md",
        "references/pre-submit.md",
        "stop without implementing",
        "read-then-write gate",
    ],
    "git-reply-issue.md": [
        "references/reply.md",
    ],
    "git-revise-pr.md": [
        "WRITE_NOT_AUTHORIZED",
        "NEEDS_REVISION",
        "references/revise.md",
        "references/pre-submit.md",
    ],
    "git-revise-pr-force.md": [
        "/git-revise-pr-force",
        "WRITE_NOT_AUTHORIZED",
        "references/revise.md",
        "references/pre-submit.md",
        "next step:",
    ],
    "git-fix-conflict.md": [
        "WRITE_NOT_AUTHORIZED",
        "CONFLICTED",
        "references/conflict.md",
        "references/pre-submit.md",
    ],
    "git-merge-approved.md": [
        "approving reviewer",
        "MERGE_NOT_AUTHORIZED",
        "references/merge.md",
        "references/github.md",
        "references/gitlab.md",
    ],
    "git-merge-approved-force.md": [
        "/git-merge-approved-force",
        "MERGE_NOT_AUTHORIZED",
        "references/merge.md",
        "next step:",
    ],
    "git-request-review.md": [
        "WRITE_NOT_AUTHORIZED",
        "Never invent a reviewer",
        "references/request-review.md",
    ],
    "git-pr-status.md": [
        "Solo override",
        "/git-review-pr-force",
        "/git-merge-approved-force",
        "/git-revise-pr-force",
        "references/status.md",
    ],
    "git-triage.md": [
        "Never invent a reviewer",
        "does not inherit force",
        "references/triage.md",
    ],
    "git-scheduled-lifecycle.md": [
        "does not inherit force",
        "references/scheduled-automation.md",
    ],
    "git-scheduled-merge.md": [
        "does not inherit force",
        "references/scheduled-automation.md",
    ],
}

LOAD_LINES = {
    "review": (
        "Review someone else's PR/MR: read `references/review.md` and `references/pre-submit.md`, and one of `references/github.md` or `references/gitlab.md`.",
        ("references/plan-issue.md", "references/implement.md", "references/merge.md", "references/triage.md"),
    ),
    "plan": (
        "Plan issue: read `references/plan-issue.md` and one of `references/github.md` or `references/gitlab.md`.",
        ("references/pre-submit.md",),
    ),
    "implement": (
        "Implement issue then PR/MR: read `references/implement.md`, `references/plan-issue.md` for the brief and dissent recipe, and `references/pre-submit.md` before push.",
        ("references/merge.md", "references/review.md", "references/triage.md", "references/scheduled-automation.md"),
    ),
    "merge": (
        "Merge approved PR/MR: read `references/merge.md` and one of `references/github.md` or `references/gitlab.md`.",
        ("references/pre-submit.md", "references/review.md"),
    ),
    "scheduled": (
        "Scheduled lifecycle or scheduled approved merge: read `references/scheduled-automation.md`.",
        ("references/triage.md", "references/review.md"),
    ),
}


def fail(message: str) -> None:
    ERRORS.append(message)


def iter_text_files() -> list[Path]:
    skip_parts = {".git", "__pycache__"}
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in skip_parts for part in path.parts):
            continue
        if path.suffix.lower() not in {".md", ".yml", ".yaml", ".py", ".txt"} and path.name != "LICENSE":
            continue
        files.append(path)
    return files


def validate_files_exist() -> None:
    for path in REQUIRED_FILES:
        if not path.exists():
            fail(f"missing {path.relative_to(ROOT)}")


def validate_no_leaks() -> None:
    for path in iter_text_files():
        rel = path.relative_to(ROOT).as_posix()
        if rel == "LICENSE":
            continue
        text = path.read_text(encoding="utf-8")
        for label, pattern in LEAK_PATTERNS:
            if pattern.search(text):
                fail(f"{rel}: possible {label} leak ({pattern.pattern})")


def validate_skill_contract() -> None:
    skill = ROOT / "SKILL.md"
    if not skill.exists():
        return
    text = skill.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail("SKILL.md: missing YAML frontmatter")
    if "name: git-collaboration" not in text.split("---", 2)[1]:
        fail("SKILL.md: name must be git-collaboration")
    for phrase in SKILL_PHRASES:
        if phrase not in text:
            fail(f"SKILL.md: missing {phrase!r}")
    if "expected reviewer" in text:
        fail("SKILL.md: still names an expected reviewer; use an approving reviewer with no default")
    if "Traditional Chinese" in text:
        fail("SKILL.md: drop language-forced review text; match the issue/PR or repo language")
    if "draft that still contains an unsettled product decision is posted" in text:
        fail("SKILL.md: do not post a draft that still contains an unsettled product decision")
    words = len(text.split())
    if words > SKILL_WORD_LIMIT:
        fail(f"SKILL.md: {words} words exceeds {SKILL_WORD_LIMIT}")
    for key, (sentence, banned) in LOAD_LINES.items():
        rows = [row for row in text.splitlines() if sentence in row]
        if not rows:
            fail(f"SKILL.md: missing {key} load line")
            continue
        for row in rows:
            for path in banned:
                if path in row:
                    fail(f"SKILL.md: {key} load line names {path}")


def validate_prompts() -> None:
    for name, phrases in PROMPT_PHRASES.items():
        path = ROOT / "prompts" / name
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        if "$ARGUMENTS" not in text:
            fail(f"prompts/{name}: missing $ARGUMENTS")
        for phrase in phrases:
            if phrase not in text:
                fail(f"prompts/{name}: missing {phrase!r}")
        if "expected reviewer" in text:
            fail(f"prompts/{name}: still names an expected reviewer")
        for sentence in PROCEDURE_SENTENCES:
            if sentence in text:
                fail(f"prompts/{name}: copies procedure sentence {sentence!r}")
    review = (ROOT / "prompts" / "git-review-pr.md").read_text(encoding="utf-8") if (ROOT / "prompts" / "git-review-pr.md").exists() else ""
    for banned in ("references/plan-issue.md", "references/implement.md", "references/merge.md", "references/triage.md"):
        if banned in review:
            fail(f"prompts/git-review-pr.md names {banned}")
    plan = (ROOT / "prompts" / "git-plan-issue.md").read_text(encoding="utf-8") if (ROOT / "prompts" / "git-plan-issue.md").exists() else ""
    if "references/pre-submit.md" in plan:
        fail("prompts/git-plan-issue.md names references/pre-submit.md")
    merge = (ROOT / "prompts" / "git-merge-approved.md").read_text(encoding="utf-8") if (ROOT / "prompts" / "git-merge-approved.md").exists() else ""
    for banned in ("references/pre-submit.md", "references/review.md"):
        if banned in merge:
            fail(f"prompts/git-merge-approved.md names {banned}")
    for name in ("git-scheduled-lifecycle.md", "git-scheduled-merge.md"):
        path = ROOT / "prompts" / name
        if not path.exists():
            continue
        scheduled = path.read_text(encoding="utf-8")
        for banned in ("references/triage.md", "references/review.md"):
            if banned in scheduled:
                fail(f"prompts/{name} names {banned}")
    implement = (ROOT / "prompts" / "git-issue-pr.md").read_text(encoding="utf-8") if (ROOT / "prompts" / "git-issue-pr.md").exists() else ""
    for banned in ("references/merge.md", "references/review.md", "references/triage.md", "references/scheduled-automation.md"):
        if banned in implement:
            fail(f"prompts/git-issue-pr.md names {banned}")


DEFAULT_PROMPT_FORBIDDEN = {
    "git-review-pr.md": ("/git-review-pr force",),
    "git-merge-approved.md": ("/git-merge-approved force",),
    "git-revise-pr.md": ("/git-revise-pr force",),
}


def validate_default_prompts_stay_strict() -> None:
    for name, phrases in DEFAULT_PROMPT_FORBIDDEN.items():
        path = ROOT / "prompts" / name
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for phrase in phrases:
            if phrase in text:
                fail(f"prompts/{name}: default command must stay strict; found {phrase!r}")


def validate_reference_phrases() -> None:
    for name, phrases in REFERENCE_PHRASES.items():
        path = ROOT / "references" / name
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for phrase in phrases:
            if phrase not in text:
                fail(f"references/{name}: missing {phrase!r}")
    plan = ROOT / "references" / "plan-issue.md"
    if plan.exists():
        recipe_bodies = (
            "**Disagree with:**",
            "**Goal:** <one observable completion state>",
            "### Execution plan",
            "**Planned at:**",
        )
        for name in ("review.md", "implement.md", "revise.md", "conflict.md", "merge.md", "triage.md", "reply.md"):
            path = ROOT / "references" / name
            if not path.exists():
                continue
            text = path.read_text(encoding="utf-8")
            for body in recipe_bodies:
                if body in text:
                    fail(f"references/{name}: recipe body belongs only in references/plan-issue.md")


def validate_forge_references() -> None:
    github = ROOT / "references" / "github.md"
    gitlab = ROOT / "references" / "gitlab.md"
    if github.exists():
        text = github.read_text(encoding="utf-8")
        for phrase in ("gh pr", "gh issue", "reviewDecision", "requested_reviewers", "--admin", "--jq"):
            if phrase not in text:
                fail(f"references/github.md: missing {phrase!r}")
    if gitlab.exists():
        text = gitlab.read_text(encoding="utf-8")
        for phrase in ("glab api", "merge_requests", "approved_by", "force merge"):
            if phrase not in text:
                fail(f"references/gitlab.md: missing {phrase!r}")


def validate_scheduled_ocr_gate() -> None:
    path = ROOT / "references" / "scheduled-automation.md"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    for phrase in (
        "pre-submit gate",
        "open-code-review-delegate",
        "cannot waive Critical/High",
        "do not push",
        "does not inherit force",
    ):
        if phrase not in text:
            fail(f"references/scheduled-automation.md: missing {phrase!r}")


def validate_implement_profile() -> None:
    readme = ROOT / "README.md"
    if not readme.exists():
        fail("README.md: missing file")
        return
    text = readme.read_text(encoding="utf-8")
    for phrase in (
        "Minimal implement profile",
        "references/implement.md",
        "references/plan-issue.md",
        "references/pre-submit.md",
        "is not permission to merge",
        "chat reply has one `next step:` line",
    ):
        if phrase not in text:
            fail(f"README.md: minimal implement profile missing {phrase!r}")


def validate_pstack() -> None:
    path = ROOT / "references" / "pstack.md"
    if not path.exists():
        fail("references/pstack.md: missing file")
        return
    text = path.read_text(encoding="utf-8")
    words = len(text.split())
    if words > PSTACK_WORD_LIMIT:
        fail(f"references/pstack.md: {words} words exceeds {PSTACK_WORD_LIMIT}")
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8") if (ROOT / "SKILL.md").exists() else ""
    for key in ("merge", "scheduled"):
        sentence, _banned = LOAD_LINES[key]
        for row in skill.splitlines():
            if sentence in row and "references/pstack.md" in row:
                fail(f"SKILL.md: {key} load line names references/pstack.md")
    for row in skill.splitlines():
        if TRIAGE_LOAD_LINE in row and "references/pstack.md" in row:
            fail("SKILL.md: triage load line names references/pstack.md")
    for name in PSTACK_FORBIDDEN_PROMPTS:
        prompt = ROOT / "prompts" / name
        if not prompt.exists():
            continue
        if "references/pstack.md" in prompt.read_text(encoding="utf-8"):
            fail(f"prompts/{name} names references/pstack.md")
    pre = (ROOT / "references" / "pre-submit.md").read_text(encoding="utf-8")
    for label in ("Proof:", "Evidence class:", "Surface:", "Load-bearing fact:", "pstack:"):
        if label not in pre:
            fail(f"references/pre-submit.md: missing Proof record label {label!r}")
    if "Inconclusive or wrong-surface is not a pass" not in pre:
        fail("references/pre-submit.md: missing inconclusive-surface rule")
    scheduled = (ROOT / "references" / "scheduled-automation.md").read_text(encoding="utf-8")
    if "pstack: off" not in scheduled:
        fail("references/scheduled-automation.md: missing 'pstack: off'")
    plan = (ROOT / "references" / "plan-issue.md").read_text(encoding="utf-8")
    if "**Proof:**" not in plan:
        fail("references/plan-issue.md: missing **Proof:**")
    fork = (
        "A fork whose answer can be observed by running code is settled by a recorded "
        "local run (pstack's Prototype playbook, or an equivalent script), not by the grill."
    )
    if fork not in plan:
        fail("references/plan-issue.md: missing observable-fork sentence")
    if plan.count("references/pre-submit.md") != 1 or "Do not read `references/pre-submit.md`" not in plan:
        fail("references/plan-issue.md: pre-submit mention must stay the Do not read sentence")
    if "skip: brief is the work order" not in text:
        fail("references/pstack.md: missing skip: brief is the work order")
    if "never the forge snapshot, and makes no forge call" not in text:
        fail("references/pstack.md: missing no-forge-call delegate rule")
    if "The parent reviews the diff" not in text:
        fail("references/pstack.md: delegate rule must say the parent reviews the diff")
    if "A silent skip fails the pre-submit gate" not in text:
        fail("references/pstack.md: missing silent-skip rule")
    review = (ROOT / "references" / "review.md").read_text(encoding="utf-8")
    if "An unproven load-bearing fact is a remaining gate" not in review:
        fail("references/review.md: missing remaining-gate ladder rule")
    routing = "pstack Babysit and Shipping never run under this skill."
    if routing not in text:
        fail("references/pstack.md: missing routing sentence")
    drift = "Record the sweep result in the Proof record."
    if "run a drift sweep" not in text or drift not in text:
        fail("references/pstack.md: missing drift-sweep sentence")
    readme = (ROOT / "README.md").read_text(encoding="utf-8") if (ROOT / "README.md").exists() else ""
    for phrase in ("pstack:off", "pstack:required", "references/pstack.md", "references/pstack-compat.md"):
        if phrase not in readme:
            fail(f"README.md: missing {phrase!r}")
    for phrase in (
        "references/pstack-compat.md",
        "unsupported",
        "Out of range",
        "unreadable version",
        "not `present`",
        "all hooks absent",
        "v1 named list",
    ):
        if phrase not in text:
            fail(f"references/pstack.md: missing {phrase!r}")
    compat_path = ROOT / "references" / "pstack-compat.md"
    if not compat_path.exists():
        fail("references/pstack-compat.md: missing file")
        return
    compat = compat_path.read_text(encoding="utf-8")
    for phrase in (
        "contract-id: `pstack-compat-v1`",
        "tested: `0.15.5`",
        "supported: `>=0.14.0 <0.17.0`",
        "## Named skills",
        "## Agents",
        "poteto-agent",
        "## Upgrade checklist",
        ".pstack-pin",
        "named skills",
        "tip PR",
        "contract unchanged",
        "Do not vendor pstack",
        "verify-<app>",
    ):
        if phrase not in compat:
            fail(f"references/pstack-compat.md: missing {phrase!r}")


def main() -> int:
    validate_files_exist()
    validate_no_leaks()
    validate_skill_contract()
    validate_prompts()
    validate_default_prompts_stay_strict()
    validate_reference_phrases()
    validate_forge_references()
    validate_scheduled_ocr_gate()
    validate_implement_profile()
    validate_pstack()
    if ERRORS:
        print("Validation failed:", file=sys.stderr)
        for error in ERRORS:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("git-collaboration skill validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
