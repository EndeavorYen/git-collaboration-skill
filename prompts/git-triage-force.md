---
description: Sweep a solo-owned GitHub or GitLab project, then plan, fix, force-review, and force-merge each owned item
---

`/git-triage-force`: read `references/triage.md` and `references/triage-force.md`.

Reply rule: one `next step:` line, in `references/triage-force.md`.

Bare `/git-triage-force` only writes the plan file. `/git-triage-force run` executes that file's rows and runs the dedicated force commands only on `owned` PRs/MRs and on issues that are unassigned or assigned to the authenticated user. Foreign items keep their plain gates. Technical gates still apply. `/git-triage run` does not inherit force. Never invent a reviewer.

$ARGUMENTS
