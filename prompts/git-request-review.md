---
description: Request GitHub PR or GitLab MR review only when current-head review is needed
---

Read `references/request-review.md` before acting, and one of `references/github.md` or `references/gitlab.md`.

Actor gate: continue only when the primary state is `REVIEW_REQUEST_NEEDED` and the authenticated user is the author or a current assignee. If `WRITE_NOT_AUTHORIZED`, stop without requesting review. Never invent a reviewer.
Reply rule: one `next step:` line, review handoff in `SKILL.md`.

$ARGUMENTS
