---
description: Fix GitHub PR or GitLab MR conflicts on the source branch and push for re-review
---

Read `references/conflict.md` before acting. Before push, read `references/pre-submit.md`. Also read one of `references/github.md` or `references/gitlab.md`.

Actor gate: continue only when the primary state is `CONFLICTED` and the authenticated user is the author or a current assignee. If `WRITE_NOT_AUTHORIZED`, do not change the branch.

$ARGUMENTS
