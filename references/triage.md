# Triage

Read this file for `/git-triage` and `/git-triage-force`.

## Status Triage Workflow

No forge write unless the user picks a follow-up. Do not auto-assign issues or PRs/MRs. Never suggest self-assignment only to unlock merge.

Mode selection:

- **Todo triage** (default): empty args, or `todo` / `mine` / `inbox`.
- **Project triage**: `project` / `this repo` / a forge project URL or path.
- **Issue triage**: args name only issues; read `references/triage-issues.md`.
- **Aggressive run**: args contain `run` / `aggressive` / `execute`.
- With both todo and project markers, prefer project when a concrete project target is present; otherwise todo.

### Todo triage workflow

Build a forge-global personal inbox from metadata lists only: notifications or todos, PRs/MRs where the user is reviewer, author, or assignee, and open issues assigned to or authored by the user. Open one trimmed snapshot only for an item you are about to write, or the one item the user named.

Notifications are signals, not source of truth. Another user speaking last is necessary but insufficient to require a reply. Rank from list fields. Snapshot an unclassifiable row only if it may make the top three.

Classify into Ready to review, Ready to fix conflicts, Ready to revise, Ready to merge, Merge handoff needed, Ready to reply, Acknowledge or route, No reply needed, Needs semantic review, Ready to implement, Review request needed, and Waiting or blocked. A named foreign conflicted PR/MR is `WRITE_NOT_AUTHORIZED`, not ready to fix.

Ready to implement: an open issue assigned to me, not blocked, not covered by an active PR/MR, with a current `<!-- git-plan-issue -->` brief whose Goal, Recommended change, Out of scope, and Acceptance criteria hold no unsettled product decision. Otherwise recommend `/git-plan-issue` with the exact issue URL. An unresolved `<!-- git-plan-issue-dissent -->` waits for a human decision.

Report each actionable item with reason, evidence, remaining gate, and next command. End with a top three and ask which to handle next.

### Project triage workflow

Scope to the current repository's forge project, or the project URL/path in arguments. One metadata PR/MR list and one metadata issue list; do not open each row. Include sibling repositories only when repo instructions or the user name them.

Add hygiene buckets **Needs reviewer** and **Needs assignee**. Prefer `/git-request-review` when the user owns the PR/MR; otherwise report who should request review. A list row has no comment body, so: recommend `/git-issue-pr` only after a trimmed snapshot shows a settled current brief and ownership is clear; until then `/git-plan-issue` with the exact issue URL.

Write the actionable items to the **Plan file** in **Plan order**; issue rows plain `run` skips are `manual`. Ask to run only with a `todo` row.

### Plan file

`PROGRESS.md` at the root of the main checkout, added to `.git/info/exclude`, never committed. Its first line is `<!-- git-triage-plan -->`; never overwrite a `PROGRESS.md` without it, stop and ask. Header: planner (`/git-triage` or `/git-triage-force`), repo, target (default) branch, planned-at time. One row per item: item URL, its next command, status (`todo` / `done` / `waiting` / `skip` / `manual`), evidence. Todo triage writes no file.

### Plan order

Merging moves the target branch, so:

1. Owned Ready to merge.
2. Owned Ready to revise, then owned Ready to fix conflicts.
3. Ready to review.
4. Owned Review request needed.
5. Issues: `/git-plan-issue` before `/git-issue-pr`.

Within a step, oldest first. A PR/MR whose base branch is another open PR/MR's head, or that says it depends on one, comes after it. Mark a PR/MR that touches the same files as an earlier step **may conflict after #N**.

## Aggressive Triage Run

`/git-triage run` does not inherit force.

1. Resolve the authenticated user. Scope is project triage: the current repo, or a project in arguments. Modifiers: `no-merge`, `merge-only`, `include-drafts`, `with-issues`, and an explicit `reviewer:USERNAME`. `dry-run` means the bare command.
2. No **Plan file**: write it and stop with no forge write. One from another planner, repo, or target branch: stop and ask before rewriting it.
3. Otherwise the file is the only target list. Run its rows in file order from the first row not `done`; skip rows the owner deleted or marked `skip`. Do not touch an item missing from the file; report it as **new since plan**. Plain `run` never runs a `*-force` row or auto-posts replies or briefs. A `scope: issues` plan follows `references/triage-issues.md` over steps 1, 3, and 8.
4. **Assignee hygiene (early):** assign yourself to planned PRs/MRs you **authored** with **empty assignees**. Never assign yourself elsewhere or replace a non-empty list.
5. Row commands unless `merge-only`: Ready to review → `/git-review-pr`; owned conflicts → `/git-fix-conflict`; owned revision → `/git-revise-pr`; owned Ready to merge → `/git-merge-approved` (skip on `no-merge`); owned current-head re-request with an existing reviewer → `/git-request-review`.
6. **Missing reviewers last.** With `reviewer:USERNAME`, assign and request review. Otherwise list those PRs/MRs and **ask who to assign**; wait, do not guess.
7. Before every write, take one new snapshot and re-run the command preflight. Live state overrides the row: reroute within that item or mark it `waiting`.
8. Do not auto-implement issues unless `with-issues` is present.
9. After each command, write status and evidence to its row. If the item's next command is runnable, set it and go on.
10. Skip an unchanged `waiting` row. No `todo` left: say what each needs; do not suggest `run`.
