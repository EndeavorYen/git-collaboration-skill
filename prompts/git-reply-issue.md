---
description: Reply to one GitHub or GitLab issue after checking whether a material response is still needed
---

Use the installed `git-collaboration` skill in "Reply to issue" mode. Detect the forge from the URL or remotes.

This action is explicitly invoked and authorizes at most one issue comment on the exact supplied issue. It does not authorize code changes, commits, pushes, label or assignee changes, state transitions, description edits, issue links, or changes to any other forge object.

Run a live read-only preflight before drafting or posting:

1. Resolve the authenticated forge user and exact project/issue from the URL, path plus iid, or another unambiguous target.
2. Refresh issue state, description, labels, assignees, links, and all non-system comments in chronological order.
3. Identify the latest material request, the latest material response by the authenticated user, and any later comment or state change that superseded the request.
4. Classify the needed response as a decision, requested information, acknowledgment, routing, or `No reply needed`.
5. Draft concise text grounded in live issue evidence and consistent with repo-local instructions.

Do not post a duplicate response. Do not comment merely because another user spoke last. Do not guess product or ownership decisions, expose sensitive evidence, or imply work was completed without verification. Ambiguous product decisions stop with a draft and a concise request for user direction; write nothing.

Post one issue comment only when a material unanswered request remains and the response does not require missing user direction. After posting, read the issue back and report the new comment id and timestamp, current issue state, assignees, and any remaining owner or blocker. If no material reply remains, perform no write and report the evidence and exact wait or next action.

$ARGUMENTS
