---
description: Force-revise an owned GitHub PR or GitLab MR without waiting for NEEDS_REVISION
---

`/git-revise-pr-force`: read `references/revise.md` and `references/pre-submit.md` before push, and one of `references/github.md` or `references/gitlab.md`.

Reply rule: one `next step:` line, in `references/revise.md`.

Actor gate: continue only when the authenticated user is the author or a current assignee. If `WRITE_NOT_AUTHORIZED`, stop without editing. This command waives the `NEEDS_REVISION` gate. The PR/MR must still be open and not `CONFLICTED`.

$ARGUMENTS
