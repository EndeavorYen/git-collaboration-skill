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
    "self_authored_head",
    "<!-- git-plan-issue -->",
    "<!-- git-plan-issue-dissent -->",
    "material disagreement",
    "human decision",
    "The brief is a proposal",
    "/git-review-pr",
    "/git-issue-pr",
    "/git-plan-issue",
]

PROMPT_PHRASES = {
    "git-issue-pr.md": [
        "all non-system notes",
        "<!-- git-plan-issue -->",
        "<!-- git-plan-issue-dissent -->",
        "material disagreement",
        "human decision",
    ],
    "git-plan-issue.md": [
        "The brief is a proposal",
        "<!-- git-plan-issue -->",
        "/git-issue-pr",
    ],
    "git-request-review.md": [
        "Never invent a reviewer",
        "ask who to assign",
    ],
    "git-triage.md": [
        "Never invent a reviewer",
        "ask who to assign",
        "/git-plan-issue",
    ],
    "git-merge-approved.md": [
        "approving reviewer",
        "MERGE_NOT_AUTHORIZED",
    ],
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


def validate_forge_references() -> None:
    github = ROOT / "references" / "github.md"
    gitlab = ROOT / "references" / "gitlab.md"
    if github.exists():
        text = github.read_text(encoding="utf-8")
        for phrase in ("gh pr", "gh issue", "reviewDecision", "requested_reviewers"):
            if phrase not in text:
                fail(f"references/github.md: missing {phrase!r}")
    if gitlab.exists():
        text = gitlab.read_text(encoding="utf-8")
        for phrase in ("glab api", "merge_requests", "approved_by"):
            if phrase not in text:
                fail(f"references/gitlab.md: missing {phrase!r}")


def main() -> int:
    validate_files_exist()
    validate_no_leaks()
    validate_skill_contract()
    validate_prompts()
    validate_forge_references()
    if ERRORS:
        print("Validation failed:", file=sys.stderr)
        for error in ERRORS:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("git-collaboration skill validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
