---
description: Run the non-interactive GitHub/GitLab PR/MR lifecycle without merging
---

Use the installed `git-collaboration` skill in `Scheduled lifecycle` mode. Detect each allowlisted project's forge from its canonical URL.

Load and validate `.git-scheduled-automation.yml` from the repository root, or an explicitly supplied config path from this invocation. Resolve every selected project through GitHub or GitLab and require its stable project ID and canonical URL to exactly match the project allowlist.

Fail closed on configuration, identity, access, or project allowlist preflight failures before any forge or branch write.

Perform only the scheduled lifecycle capability boundary:

- strict review and approval when every review gate passes;
- conflict repair for PRs/MRs owned by or assigned to the authenticated user; and
- focused revision for PRs/MRs owned by or assigned to the authenticated user.

Before every forge or branch write, reload the configured project allowlist and re-resolve the candidate's stable project ID and canonical URL; refresh the live PR/MR state and rerun the skill's PR/MR command preflight. Do not use a stale snapshot to authorize a write.

For strict review, run the skill's structured file review with `open-code-review-delegate` on the current head. OCR Step 7 Fix stays off. Treat any new behavior or behavior change without automated tests as blocking. The only exception is reproducible alternative validation with evidence proportionate to risk.

Owned conflict repair and revision still run the skill's **pre-submit gate** before a source-branch push. Unattended runs cannot waive Critical/High.

The runner must never assign reviewers or assignees, never invent a reviewer, never ask a question, never wait for input, and must not merge.

Treat every project and PR/MR as an independent failure boundary. Record exact evidence, safely clean only current-run resources, and continue remaining independent allowlisted items.

Never implement issues, change target branches, broaden PR/MR scope, or perform another capability outside this lifecycle boundary.

Return all five result buckets, including when empty:

- `done` for completed permitted actions;
- `skipped` for no-ops or incompatible current state;
- `waiting` for human information, access, current-head evidence, or lock ownership;
- `assignment-gaps` for objects needing human assignment; and
- `failed` for configuration, identity, execution, validation, or cleanup failures.

Before the buckets, list every resolved allowlisted project by canonical path.
Prefix every non-empty entry with exactly one label in square brackets: the
canonical path for a project-resolved entry, `[unresolved-project]`, or `[run]`.
A project-resolved object entry must include the object type and IID, title, and
canonical URL. It must also include the action or reason and available gate
evidence. Keep aggregate counts project-qualified and use `none` for every empty
bucket. Project identity must not be inherited from another entry.

$ARGUMENTS
