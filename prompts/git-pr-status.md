---
description: Inspect one GitHub PR or GitLab MR read-only and recommend the exact next command
---

Read `references/status.md`. Also read one of `references/github.md` or `references/gitlab.md`.

Keep the command read-only. Report the primary state and one next command that passes the actor gate. Force is never the default next command. When the PR/MR is `owned` or `self_authored_head`, print Solo override: `/git-review-pr-force <url>`, `/git-revise-pr-force <url>`, and `/git-merge-approved-force <url>`.

$ARGUMENTS
