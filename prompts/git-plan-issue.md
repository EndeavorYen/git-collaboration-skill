---
description: Analyze one GitHub or GitLab issue, post an implementation brief with acceptance criteria, and stop without implementing
---

Use the installed `git-collaboration` skill in "Plan issue" mode. Detect the forge from the URL or remotes.

This action is explicitly invoked and authorizes at most one issue comment on the exact supplied issue. It does not authorize code changes, commits, pushes, label or assignee changes, state transitions, description edits, issue links, or changes to any other forge object.

Obey **Forge budget** and **Context budget** before drafting or posting. One trimmed issue snapshot, then the local checkout. Do not paste source into the brief.

1. Resolve the exact project/issue from the URL, path plus iid, or another unambiguous target. Reuse the authenticated user already resolved for this invocation.
2. Take one issue snapshot: state, description, labels, assignees, links on that payload, marker notes, and the latest non-system notes. The latest body stays whole. Do not search for related PRs/MRs.
3. Read repo-local instructions and inspect the relevant code in the local checkout until the brief names concrete files, behavior, and tests. Do not read repository files through the forge.
4. Classify whether a current implementation brief is still needed. A current brief is a comment that contains `<!-- git-plan-issue -->` whose Goal, Recommended change, Out of scope, and Acceptance criteria have not been changed by later comments. A current brief is still needed when none exists, later comments changed those fields, or the user asked to re-plan.
5. Draft the issue comment from the skill's Plan Issue Workflow recipe. The brief is a proposal. `/git-issue-pr` follows it when the implementer agrees, or posts a dissent and waits for a human decision.

Do not post a duplicate brief. Do not implement or open a PR/MR. Do not guess an unsettled product decision. Do not post a brief while an unsettled product decision remains in Goal, Recommended change, Out of scope, or Acceptance criteria. A deferred or open assumption is still unsettled. When those four fields are already settled, post the brief without loading `gentle-grill-me` and do not wait for a close log. Load `gentle-grill-me` only when an unsettled product decision remains, and post nothing until the user confirms the close log. After that confirmation, rewrite those four fields from settled log entries only. If any field is still deferred or open, post nothing. Scheduled runs and `/git-triage` do not load `gentle-grill-me`; recommend `/git-plan-issue`.

Post one issue comment only when the issue is open, a current brief is still needed, the draft is grounded in the local checkout, and those four fields are settled decisions. The write response is the read-back: report its comment id and timestamp, the issue state from the snapshot, and `/git-issue-pr` with the exact issue URL. Do not view the issue again when that response includes the comment id. If no write is justified, perform no write and report the evidence and exact wait or next action.

$ARGUMENTS
