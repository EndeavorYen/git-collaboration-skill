---
description: Analyze one GitHub or GitLab issue, post an implementation brief with acceptance criteria, and stop without implementing
---

Use the installed `git-collaboration` skill in "Plan issue" mode. Detect the forge from the URL or remotes.

This action is explicitly invoked and authorizes at most one issue comment on the exact supplied issue. It does not authorize code changes, commits, pushes, label or assignee changes, state transitions, description edits, issue links, or changes to any other forge object.

Run a live read-only preflight before drafting or posting:

1. Resolve the authenticated forge user and exact project/issue from the URL, path plus iid, or another unambiguous target.
2. Refresh issue state, description, labels, assignees, links, related PRs/MRs, and all non-system notes in chronological order.
3. Read repo-local instructions and inspect the relevant current code until the brief can name concrete files, behavior, and tests.
4. Classify whether a current implementation brief is still needed. A current brief is a comment that contains `<!-- git-plan-issue -->` whose Goal, Recommended change, Out of scope, and Acceptance criteria have not been changed by later comments. A current brief is still needed when none exists, later comments changed those fields, or the user asked to re-plan.
5. Draft the issue comment from the skill's Plan Issue Workflow recipe. The brief is a proposal. `/git-issue-pr` follows it when the implementer agrees, or posts a dissent and waits for a human decision.

Do not post a duplicate brief. Do not implement or open a PR/MR. Ambiguous product decisions stop with a draft and a concise request for user direction; write nothing.

Post one issue comment only when the issue is open, a current brief is still needed, and the draft is grounded in inspected code. After posting, read the issue back and report the new comment id and timestamp, current issue state, and `/git-issue-pr` with the exact issue URL. If no write is justified, perform no write and report the evidence and exact wait or next action.

$ARGUMENTS
