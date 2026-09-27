#!/usr/bin/env python3
"""Print and cap the instruction bytes each mode loads.

A mode loads SKILL.md plus the references its load line in SKILL.md names.
"one of github.md or gitlab.md" counts the larger file. pstack.md counts in
the pstack column when a loaded file points at it. Tokens are bytes / 4.
CRLF counts as LF so a Windows checkout measures the same.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Bytes. Caps only go down: lower a cap when a change shrinks a mode.
MODE_CAPS = {
    "Review someone else's PR/MR": 45_908,
    "Plan issue": 44_395,
    "Implement issue then PR/MR": 51_866,
    "Reply to issue": 21_829,
    "Update own PR/MR after review": 28_651,
    "Fix PR/MR conflicts": 27_520,
    "Merge approved PR/MR": 32_540,
    "Request PR/MR review": 21_682,
    "Focused PR/MR status": 21_233,
    "Status or triage, including the aggressive run": 26_353,
    "Scheduled lifecycle or scheduled approved merge": 31_820,
}

LOAD_LINE = re.compile(r"^([A-Z][^|#\n]*?): read (.+)$", re.M)
REF = re.compile(r"`(references/[a-z0-9-]+\.md)`")
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
        refs = list(dict.fromkeys(REF.findall(rest)))
        forge = [ref for ref in refs if ref in FORGE_PAIR]
        files = [ref for ref in refs if ref not in FORGE_PAIR]
        total = size("SKILL.md") + sum(size(ref) for ref in files)
        if forge:
            total += max(size(ref) for ref in FORGE_PAIR)
        read = [ROOT / "SKILL.md", *(ROOT / ref for ref in files + forge)]
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


def main() -> int:
    loads = mode_loads()
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
