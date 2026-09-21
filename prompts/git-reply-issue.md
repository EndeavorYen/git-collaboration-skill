---
description: Reply to one GitHub or GitLab issue after checking whether a material response is still needed
---

Use the installed `git-collaboration` skill in "Reply to issue" mode. Detect the forge from the URL or remotes.

This action is explicitly invoked and authorizes at most one issue comment on the exact supplied issue. It does not authorize code changes, commits, pushes, label or assignee changes, state transitions, description edits, issue links, or changes to any other forge object.

Obey **Forge budget** in the skill before drafting or posting. One issue snapshot, then repo-local instructions in the checkout.

1. Resolve the exact project/issue from the URL, path plus iid, or another unambiguous target. Reuse the authenticated user already resolved for this invocation.
2. Take one issue snapshot: state, description, labels, assignees, links on that payload, marker comments, and the latest non-system comments. The latest body stays whole.
3. Identify the latest material request, the latest material response by the authenticated user, and any later comment or state change that superseded the request.
4. Classify the needed response as a decision, requested information, acknowledgment, routing, or `No reply needed`.
5. Draft concise text from that snapshot and repo-local instructions.

Do not post a duplicate response. Do not comment merely because another user spoke last. Do not guess product or ownership decisions, expose sensitive evidence, or imply work was completed without verification. Ambiguous product decisions stop with a draft and a concise request for user direction; write nothing.

Post one issue comment only when a material unanswered request remains and the response does not require missing user direction. The write response is the read-back: report its comment id and timestamp, plus state, assignees, and any remaining owner or blocker from the snapshot. Do not view the issue again when that response includes the comment id. If no material reply remains, perform no write and report the evidence and exact wait or next action.

$ARGUMENTS
