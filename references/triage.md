# Triage

Read this file for `/git-triage`, `/git-triage run`, and `/git-triage-force`. A scheduled run does not read this file.

## Status Triage Workflow

Use this for what can be handled now, project status, a personal todo list, or `/git-triage` without `run` / `aggressive` / `execute`.

Stay read-only unless the user picks a follow-up action. Resolve the authenticated forge user first. Do not auto-assign issues or PRs/MRs. Never suggest self-assignment only to unlock merge. Never invent a reviewer.

Mode selection:

- **Todo triage** (default): empty args, or `todo` / `mine` / `inbox`.
- **Project triage**: `project` / `this repo` / a forge project URL or path.
- **Aggressive run**: args contain `run` / `aggressive` / `execute`.
- With both todo and project markers, prefer project when a concrete project target is present; otherwise todo.

### Todo triage workflow

Build a forge-global personal inbox from metadata lists only: notifications or todos, PRs/MRs where the user is a reviewer, PRs/MRs where the user is author or assignee, and open issues assigned to or authored by the user. Context budget defines the fields. Open one trimmed snapshot only for an item you are about to write, or the one item the user named.

Notifications are signals, not conversational source of truth. Another user speaking last is necessary but insufficient to require a reply. Rank from list fields. If a row still cannot be classified, take one trimmed snapshot of it, only when it is in the top three you might recommend.

Classify into Ready to review, Ready to fix conflicts, Ready to revise, Ready to merge, Merge handoff needed, Ready to reply, Acknowledge or route, No reply needed, Needs semantic review, Ready to implement, Review request needed, and Waiting or blocked. A named foreign conflicted PR/MR is `WRITE_NOT_AUTHORIZED`, not ready to fix.

Ready to implement: an open issue assigned to me, not blocked, not covered by an active PR/MR, with a current `<!-- git-plan-issue -->` brief whose Goal, Recommended change, Out of scope, and Acceptance criteria hold no unsettled product decision. Otherwise recommend `/git-plan-issue` with the exact issue URL. An unresolved `<!-- git-plan-issue-dissent -->` waits for a human decision. `/git-triage` does not load `gentle-grill-me`.

Report each actionable item with reason, live evidence, remaining gate, and exact next command. End with a compact top three and ask which item to handle next.

### Project triage workflow

Scope to the current repository's forge project, or the project URL/path in arguments. One metadata PR/MR list and one metadata issue list; do not open each row. Apply the same relationship model. Include sibling repositories only when repo-local instructions name them or the user asks.

Add hygiene buckets **Needs reviewer** and **Needs assignee**. Prefer `/git-request-review` when the user owns the PR/MR; otherwise report who should request review. A list row has no comment body, so an issue is not Ready to implement from the list: recommend `/git-issue-pr` only after a trimmed snapshot shows a settled current brief and ownership is clear; until then `/git-plan-issue` with the exact issue URL.

Print the actionable items as one numbered plan in **Plan order**, one exact command per line, then ask which step to run or whether to run the plan.

### Plan order

Merging moves the target branch, so order the steps:

1. Owned Ready to merge.
2. Owned Ready to revise, then owned Ready to fix conflicts.
3. Ready to review.
4. Owned Review request needed.
5. Issues: `/git-plan-issue` before `/git-issue-pr`.

Within a step, oldest update first. A PR/MR whose base branch is another open PR/MR's head, or that says it depends on one, comes after it. Mark a PR/MR that touches the same files as an earlier step **may conflict after #N**.

## Aggressive Triage Run

Use this for `/git-triage run` (aliases `aggressive` / `execute`). `/git-triage run` does not inherit force; `/git-triage-force` is the solo sweep.

1. Resolve the authenticated user and scope. Modifiers: `no-merge`, `merge-only`, `include-drafts`, `with-issues`, `dry-run`, and an explicit `reviewer:USERNAME` (user-chosen, never hard-coded).
2. Classify with the matching triage workflow and build the plan in **Plan order**. `dry-run` prints it and stops with no writes. Surface reply candidates and issues that need a brief, but do not auto-post them; use `/git-reply-issue` or `/git-plan-issue` separately.
3. A reviewer comes only from `reviewer:` in this run. Repo docs may inform suggestions, never an assignment.
4. **Assignee hygiene (early):** on open PRs/MRs the authenticated user **authored** with **empty assignees**, assign the authenticated user. Never assign yourself elsewhere or replace a non-empty list.
5. Run the plan in order unless `merge-only`: Ready to review → `/git-review-pr`; owned conflicts → `/git-fix-conflict`; owned revision → `/git-revise-pr`; owned Ready to merge → `/git-merge-approved` (skip on `no-merge`); owned current-head re-request with an existing reviewer → `/git-request-review`.
6. **Missing reviewers last.** With `reviewer:USERNAME`, assign and request review. Otherwise list those PRs/MRs and **ask who to assign**; wait, do not guess.
7. Before every write, take one new snapshot and re-run the command preflight. Live state overrides the plan. After a merge, re-snapshot the next PR/MR before acting on it.
8. Do not auto-implement issues unless `with-issues` is present.
9. Prefer isolated worktrees when local checkouts are dirty or on another branch/repo.
10. Report each plan step as done / skipped / waiting with evidence. A rerun rebuilds the plan from live state, so finished steps drop out.
