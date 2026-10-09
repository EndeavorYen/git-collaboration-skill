#!/usr/bin/env python3
"""Grade scripts/project-triage-list.jq against committed fixtures."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
JQ = ROOT / "project-triage-list.jq"
FIXTURES = ROOT / "testdata" / "project-triage-list.json"


def run(kind: str, payload: dict) -> dict:
    out = subprocess.check_output(
        ["jq", "--arg", "kind", kind, "-f", str(JQ)],
        input=json.dumps(payload),
        text=True,
    )
    return json.loads(out)


def ends_z(value: str | None) -> bool:
    return value is None or (value.endswith("Z") and "+" not in value)


def check(case: dict) -> list[str]:
    errors: list[str] = []
    got = run(case["kind"], case["payload"])
    expect = case["expect"]
    if got.get("listTruncated") != expect.get("listTruncated", False):
        errors.append(f"{case['id']}: listTruncated {got.get('listTruncated')!r}")
    rows = got.get("rows") or []
    index = expect.get("row", 0)
    if index >= len(rows):
        return errors + [f"{case['id']}: missing row {index}"]
    row = rows[index]
    for key in ("authorReplyAt", "latestNonMergeAt", "reviewRequestAt"):
        if key in expect and row.get(key) != expect[key]:
            errors.append(f"{case['id']}: {key} {row.get(key)!r} != {expect[key]!r}")
        if not ends_z(row.get(key)):
            errors.append(f"{case['id']}: {key} is not UTC Z")
    if "unresolvedNonAuthor" in expect and row.get("unresolvedNonAuthor") != expect["unresolvedNonAuthor"]:
        errors.append(f"{case['id']}: unresolvedNonAuthor {row.get('unresolvedNonAuthor')!r}")
    if "discussionsTruncated" in expect and row.get("discussionsTruncated") != expect["discussionsTruncated"]:
        errors.append(f"{case['id']}: discussionsTruncated {row.get('discussionsTruncated')!r}")
    feedback = row.get("latestFeedback")
    want = expect.get("latestFeedback")
    if want is None and "latestFeedback" in expect:
        if feedback is not None:
            errors.append(f"{case['id']}: latestFeedback should be null")
    elif want is not None:
        if not feedback:
            errors.append(f"{case['id']}: missing latestFeedback")
        else:
            if feedback.get("author") != want["author"]:
                errors.append(f"{case['id']}: author {feedback.get('author')!r}")
            if feedback.get("at") != want["at"]:
                errors.append(f"{case['id']}: at {feedback.get('at')!r}")
            if not ends_z(feedback.get("at")):
                errors.append(f"{case['id']}: latestFeedback.at is not UTC Z")
            prefix = want.get("excerpt_prefix")
            if prefix and not str(feedback.get("excerpt") or "").startswith(prefix):
                errors.append(f"{case['id']}: excerpt {feedback.get('excerpt')!r}")
            banned = want.get("excerpt_not")
            if banned and banned in str(feedback.get("excerpt") or ""):
                errors.append(f"{case['id']}: excerpt contains {banned!r}")
    errors.extend(shape_errors(case))
    return errors


def shape_errors(case: dict) -> list[str]:
    """Lock fixtures whose string max and UTC max must not be the same commit."""
    if case.get("id") != "string-max-diverges":
        return []
    nodes = case["payload"]["data"]["project"]["mergeRequests"]["nodes"]
    commits = nodes[0]["commits"]["nodes"]
    raw = [node["committedDate"] for node in commits if not str(node["message"]).startswith("Merge ")]
    errors: list[str] = []
    if max(raw) != "2026-10-08T14:59:27+11:00":
        errors.append(f"{case['id']}: string max is not the +11 commit")
    expect = case["expect"]
    wrong = "2026-10-08T03:59:27Z"
    right = expect.get("latestNonMergeAt")
    note = (expect.get("latestFeedback") or {}).get("at")
    if right == wrong:
        errors.append(f"{case['id']}: expected UTC max equals string-max then utc")
    if not (isinstance(note, str) and isinstance(right, str) and wrong < note < right):
        errors.append(f"{case['id']}: note must sit between the wrong UTC time and the real max")
    return errors


def main() -> int:
    cases = json.loads(FIXTURES.read_text(encoding="utf-8"))
    ids = [case["id"] for case in cases]
    for required in ("follow-up", "mixed-timezone", "string-max-diverges", "gh-request-removed", "gh-unidentified-reviewer", "gl-unidentified-reviewer"):
        if required not in ids:
            print(f"missing fixture {required}", file=sys.stderr)
            return 1
    errors: list[str] = []
    for case in cases:
        errors.extend(check(case))
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"project-triage-list fixtures passed ({len(cases)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
