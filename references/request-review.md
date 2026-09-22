# Request review

Read this file for `/git-request-review`.

When the state is not `REVIEW_REQUEST_NEEDED` or the user is not the author or assignee, do not create a duplicate request. For `WRITE_NOT_AUTHORIZED`, name the author or assignee. Otherwise recommend `/git-revise-pr`, `/git-merge-approved`, or waiting according to state.

## Request PR/MR Review

Use this when the user invokes `/git-request-review` or explicitly asks to request review or re-review.

1. Run the PR/MR command preflight and continue only when the primary state is `REVIEW_REQUEST_NEEDED` and the PR/MR is `owned`.
2. Identify the reviewer from an explicit user username, a reviewer already requested on the PR/MR, or CODEOWNERS only as a list to present. If it is ambiguous, stop and ask who to assign instead of guessing. Never invent a reviewer. Do not request yourself as reviewer of a PR/MR you own or have commits on.
3. Prefer the forge's native request-review operation. The write response is the read-back for reviewer assignment, current head SHA, approval state, and discussions. One confirm view only when that response omits the reviewer or the head SHA.

Do not change code or merge. Do not send a duplicate request when a current-head request is already pending.
