---
description: Merge allowlisted GitHub PRs or GitLab MRs only through the exact-head approved gate
---

Use the installed `git-collaboration` skill in `Scheduled approved merge` mode. Detect each allowlisted project's forge from its canonical URL.

Load and validate `.git-scheduled-automation.yml` from the repository root, or an explicitly supplied config path from this invocation. Resolve every selected project through GitHub or GitLab and require its stable project ID and canonical URL to exactly match the project allowlist.

Consider only current merge candidates from allowlisted projects. Ignore stale candidates and anything outside the configured scope.

Before every write, refresh the canonical allowlist identity by reloading the project allowlist and re-resolving the candidate's stable project ID and canonical URL; refresh live PR/MR state and rerun the skill's PR/MR command preflight.

The sole permitted write is the merge delegated exclusively to `git-merge-approved`. Never post comments, change labels, or perform preparatory writes.

Require every gate enforced by that delegate:

- the authenticated actor is the PR/MR author or a current assignee;
- live approval reports at least one approving reviewer;
- every approving reviewer has no author or committer commits on the current PR/MR;
- the reviewed head SHA exactly equals the current head SHA;
- required CI is successful for that exact head;
- all discussions are resolved;
- the PR/MR is not a draft;
- the PR/MR has no conflicts; and
- the forge reports the PR/MR as currently mergeable.

The runner must never assign reviewers or assignees, never invent a reviewer, and must never ask a question or wait for input.

The runner must never review or post review feedback, revise the PR/MR, make source-branch changes, or repair conflicts.

Treat every project and PR/MR as an independent failure boundary. Record exact evidence, safely clean only current-run resources, and continue remaining independent allowlisted candidates.

Return all five result buckets, including when empty:

- `done` for PRs/MRs merged through `git-merge-approved`;
- `skipped` for no-ops or candidates outside the current capability boundary;
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
