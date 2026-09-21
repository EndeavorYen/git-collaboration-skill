---
description: Request GitHub PR or GitLab MR review only when current-head review is needed
---

Use the installed `git-collaboration` skill in "Request PR/MR review" mode. Detect the forge from the URL or remotes.

Run the skill's read-only PR/MR command preflight first, including the actor gate, then request review or re-review only when the primary state is `REVIEW_REQUEST_NEEDED` and the authenticated user is the author or a current assignee. If `WRITE_NOT_AUTHORIZED`, stop without requesting review and name the author or assignee.

Identify the reviewer from an explicit user username, a reviewer already requested on the PR/MR, or CODEOWNERS only as a list to present. If it is ambiguous, stop and ask who to assign instead of guessing. Never invent a reviewer. There is no hard-coded reviewer and no default reviewer. Do not request yourself as reviewer of a PR/MR you own or have commits on. Prefer the forge's native request-review operation, then read back the reviewer, current head SHA, approval state, and discussions.

Do not change code or merge. Do not send a duplicate request when a current-head request is already pending. If actionable feedback exists, recommend `/git-revise-pr`; if live approval and final gates pass, recommend `/git-merge-approved`; otherwise report the exact wait condition and `/git-pr-status`.

$ARGUMENTS
