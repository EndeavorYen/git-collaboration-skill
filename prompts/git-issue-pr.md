---
description: Implement a GitHub or GitLab issue, validate it, push, and open or update the PR/MR
---

Read `references/implement.md` before acting. Brief and dissent recipe: `references/plan-issue.md`. Before push: `references/pre-submit.md`. Also read one of `references/github.md` or `references/gitlab.md`.

Actor gate: if the issue has assignees and the authenticated user is not among them, stop without implementing. Unassigned issues may be implemented.
Enforce the read-then-write gate: after at most one focused read round, create or edit a file; do not loop on reads.
Reply rule: one `next step:` line, review handoff in `SKILL.md`.

$ARGUMENTS
