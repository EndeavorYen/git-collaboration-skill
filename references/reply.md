# Reply to issue

Read this file for `/git-reply-issue`.

## Focused Issue Reply Workflow

Use this only when the user explicitly invokes `/git-reply-issue` or clearly asks to post a response to one exact issue. The write scope is one issue comment on the exact target; do not change code, commits, branches, labels, assignees, issue state, description, links, or any other forge object.

1. Resolve the exact project/issue. Reuse the authenticated user already resolved for this invocation.
2. Take one issue snapshot: state, description, labels, assignees, links on that payload, marker comments, and the latest non-system comments. The latest body stays whole.
3. Identify the latest material request, the latest material response by the authenticated user, and any later response or state change that superseded it. Draft from that snapshot and repo-local instructions in the checkout.
4. Classify the response as a decision, requested information, acknowledgment, routing, or `No reply needed`.
5. Post one issue comment only when a material unanswered request remains.
6. The write response is the read-back. Report the new comment id/time, current state, assignees, and remaining owner or blocker from that response and the snapshot. Do not view the issue again when the response includes the comment id.

Do not post a duplicate response. Ambiguous product decisions stop with a draft and a request for user direction; write nothing.
