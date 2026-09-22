---
description: Force-merge an owned GitHub PR or GitLab MR after remaining technical gates pass
---

`/git-merge-approved-force`: read `references/merge.md` and one of `references/github.md` or `references/gitlab.md`.

This command waives the live non-author approving-reviewer gate. Continue only when the authenticated user is the author or a current assignee. If neither matches, classify `MERGE_NOT_AUTHORIZED` and do not merge. `/git-triage run` does not inherit force.

$ARGUMENTS
