# Scheduled GitHub / GitLab automation

This contract applies to both scheduled modes in the git-collaboration skill. It is non-interactive, allowlist-only, and subordinate to the main skill's live-state model and exact-head merge gate.

## Local configuration preflight

Load `.git-scheduled-automation.yml` from the repository root before any write. The machine owns this file: keep it untracked and exclude it locally with `.git/info/exclude`; do not change the repository `.gitignore`. Exclude the configured state directory locally as well.

The tracked schema example is deliberately empty and contains no real project or personal path:

```yaml
version: 1
timezone: UTC
schedules:
  lifecycle:
    rrule: "RRULE:FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR;BYHOUR=9,11,14,16;BYMINUTE=0"
  approved_merge:
    rrule: "RRULE:FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR;BYHOUR=17;BYMINUTE=30"
safety:
  dry_run: true
  merge_enabled: false
state_dir: .git-scheduled-state
projects: []
```

Set `timezone` to the operator's timezone. Each `projects` entry contains `url` and may contain `checkout_path`. The local file must contain canonical HTTPS GitHub or GitLab project URLs, no duplicates, and no credentials.

A write-enabled run fails closed unless all of these checks pass:

- the file exists, parses, uses version `1`, contains a timezone, both schedule entries, and both safety flags;
- `projects` is non-empty and duplicate-free;
- Git reports the file as untracked; and
- when the file is inside the repository, `git check-ignore` proves that `.git/info/exclude` ignores it.

A read-only dry run reports all configuration errors. Any failed preflight puts the run in `failed` before a forge or branch write.

## Project allowlist enforcement

Resolve every configured URL through the matching forge and compare both stable project ID and canonical `web_url` / `html_url` to the project allowlist entry. Reject redirects, sibling projects, remotes, API responses, and checkout paths whose canonical identity is not an exact allowlist match. Never infer additional projects from local remotes, links, orgs, groups, or prior runs.

If `checkout_path` is present, verify its remote resolves to that same allowlisted identity before fetch, checkout, commit, or push. Identity or access uncertainty is a per-project `failed` result and authorizes no write.

## Non-interactive assignment policy

The scheduled profile overrides interactive aggressive triage: it never writes reviewer or assignee fields, including author self-assignment. A PR/MR missing a reviewer or assignee, or an issue missing an assignee, is `waiting-human-assignment`. Never invent a reviewer.

Record each gap under `assignment-gaps` with project, object type, IID, title, URL, missing role, and suggested human next action. Continue independent eligible work. End without asking a question or waiting for input.

## Lifecycle order and write boundary

After configuration, identity, access, and allowlist checks, enumerate and classify live candidates per project. Scheduled lifecycle processes eligible PRs/MRs in this order:

1. strict review and approval when all review gates pass;
2. conflict repair for PRs/MRs owned by or assigned to the authenticated user;
3. focused revision for PRs/MRs owned by or assigned to the authenticated user; and
4. live reclassification and reporting.

Scheduled lifecycle may only review or approve, revise an owned-or-assigned source branch, repair its conflicts, validate, commit, and push that source branch. It never merges, implements issues, changes target branches, broadens PR/MR scope, or performs assignment writes.

## Strict review and required test gate

Review correctness and regression risk; automated tests and reproducible validation; APIs, schemas, generated artifacts, and data contracts; security; required CI; deployment and operations; and agreement between documentation and behavior. A substantive unverified risk blocks approval. Style-only preferences stay non-blocking unless repository policy requires them.

Any new behavior or behavior change without corresponding automated tests is blocking. The only exception is reproducible alternative validation whose strength is proportionate to risk. That evidence must state the exact environment, steps, inputs, expected observable result, captured output or artifact, why automation is impractical, and why the evidence is sufficient for the risk. A green pipeline, small diff, authority, deadline, or screenshots alone do not satisfy this exception.

Post a concrete blocking finding when the evidence is insufficient. Do not approve with a test follow-up. Do not duplicate feedback when the same head has already been reviewed and no material code, CI, discussion, or validation evidence changed.

## Per-write allowlist and live-state preflight

Before every forge or branch write, reload the configured project allowlist and re-resolve the candidate's stable project ID and canonical URL. Then refresh the PR/MR and rerun the main skill's PR/MR command preflight. Refresh at least the current head, actor relationship, live approval, pipeline and required jobs, discussions, draft state, conflicts, mergeability, source and target branches, and assignment state.

A triage snapshot never authorizes a write. If live state differs, skip or reroute only within the current scheduled mode's capability boundary. Validation belongs to the exact head being written; evidence for an earlier head is stale.

## Idempotency

Use current forge and Git state to suppress empty commits, no-op pushes, duplicate findings, duplicate approvals, duplicate review requests, and repeated merge attempts. Record a no-op as `skipped` with the observed evidence. Never manufacture a change merely to produce output.

## Atomic local lock and isolated worktree

Before modifying a source branch, acquire an atomic local lock keyed by stable project ID and PR/MR IID. Lock metadata records task kind, run or process identity, source branch, and observed head SHA. Acquire the lock atomically before creating or reusing local branch state.

If another live run owns the lock, report the PR/MR as `waiting` and do not modify the branch. Never break, replace, or remove an uncertain or apparently stale lock during an unattended run. Report its metadata for human inspection and recovery.

Use an isolated worktree for source changes. Verify the allowlisted remote before fetching or checking out. Never reuse or alter unrelated dirty work, an existing user worktree, or another run's temporary resources. Release only locks and temporary resources that the current run provably owns, and only when safe.

## Failure isolation

Treat every project and PR/MR as its own failure boundary. Record the failure and exact evidence, safely clean up only current-run resources, and continue remaining independent allowlisted items. A project failure never expands scope to another project or turns a prohibited capability into a fallback.

## Stable result buckets

Return all five top-level buckets, including when empty:

- `done` for completed permitted actions;
- `skipped` for current-state no-ops, incompatible states, or changed-head rejection;
- `waiting` for human information, access, current-head evidence, or lock ownership;
- `assignment-gaps` for `waiting-human-assignment` objects; and
- `failed` for configuration, identity, execution, validation, or cleanup failures.

Before the buckets, list every resolved allowlisted project using its canonical path (`owner/name` or `path_with_namespace`). Prefix every non-empty result entry with exactly one label in square brackets: that canonical path, `[unresolved-project]`, or `[run]`. Do not claim a canonical project identity for either fallback label. A project-resolved object entry must include the object type and IID, title, canonical URL, action or reason, and the existing exact-head gate evidence when available. Use `none` for an empty bucket.

Make every aggregate project-qualified. Break counts down by canonical project path.

```text
scope: example-org/app, example-org/api

waiting
- [example-org/app] PR #12 -- conflict repair required -- https://github.com/example-org/app/pull/12
- [example-org/api] MR !90 -- pipeline failed -- https://gitlab.example.com/example-org/api/-/merge_requests/90

failed
- [unresolved-project] project resolution -- configured project could not be resolved -- API returned 404
- [run] configuration -- YAML parse failed -- line 12 has an invalid mapping
```

Each PR/MR entry includes, when available, project and IID/URL; attempted action or reason; observed and resulting head; pipeline and required-job evidence; live approval evidence; discussion state; conflicts, draft, and mergeability; and actor relationship. End the report without a question.

## Approved-merge delegation

Scheduled approved merge performs no review, revision, conflict repair, assignment, or preparatory write. For each allowlisted candidate it delegates only to the main skill's exact-head `/git-merge-approved` workflow.

Do not weaken or reproduce that merge gate. Immediately before the merge API call, the delegated workflow must still verify on the exact current head that:

- the authenticated user is the PR/MR author or a current assignee;
- live approval reports at least one approving reviewer;
- every approving reviewer has no author or committer commits on the current PR/MR;
- reviewed head equals current head;
- required pipeline and jobs succeeded;
- blocking discussions are resolved;
- the PR/MR is not a draft; and
- no conflict or merge-status blocker remains.

Reviewer text, green CI, resolved discussions, project role, or API permission never substitutes for live approval or the actor gate. A head mismatch yields `skipped` with evidence and no merge-side write.

## Manual dry-run and activation gate

Keep `safety.dry_run: true` and `safety.merge_enabled: false` for initial setup. Manually run each scheduled mode read-only and inspect configuration errors, canonical project identities, planned capability boundaries, assignment gaps, duplicate suppression, live-state evidence, and all five result buckets.

Activate lifecycle writes only after its dry run is correct and the local configuration remains untracked and ignored. Activate approved merges separately: require a successful merge dry run, explicit operator confirmation, `dry_run: false`, and `merge_enabled: true`. The saved scheduler recurrence and timezone must match the local YAML before activation; a mismatch fails closed.
