---
description: Merge a specific approved GitHub PR or GitLab MR after live final gates pass
---

Read `references/merge.md` before acting, and one of `references/github.md` or `references/gitlab.md`.

Actor gate: continue only when the authenticated user is the author or a current assignee. Otherwise classify `MERGE_NOT_AUTHORIZED` and do not merge. Do not merge unless live approval reports at least one approving reviewer on the current head.

$ARGUMENTS
