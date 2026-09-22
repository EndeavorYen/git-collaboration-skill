# Triage

Read this file for `/git-triage` and `/git-triage run`. A scheduled run does not read this file.

## Status Triage Workflow

Use this when the user asks what can be handled now, asks for project status, asks for a personal todo list, or invokes `/git-triage` without `run` / `aggressive` / `execute`.

Keep this mode read-only unless the user explicitly chooses a follow-up action. Resolve the authenticated forge user first. Do not auto-assign issues or PRs/MRs. Never suggest self-assignment only to unlock merge. Never invent a reviewer.

Mode selection (same rules as the `git-triage` prompt):

- **Todo triage** (default): empty args, or `todo` / `mine` / `inbox`.
- **Project triage**: `project` / `this repo` / a forge project URL or path.
- **Aggressive run**: args contain `run` / `aggressive` / `execute`.
- If both todo and project markers appear, prefer project when a concrete project target is present; otherwise prefer todo.

### Todo triage workflow

Build a forge-global personal inbox from metadata lists only: one for notifications or todos, one for PRs/MRs where the user is a reviewer, one for PRs/MRs where the user is author or assignee, and one for open issues assigned to or authored by the user. Context budget defines the fields. Do not request comment or review bodies on a list.

Treat notifications as signals, not conversational source of truth. Another user speaking last is necessary but insufficient to require a reply. Rank from list fields. If a row still cannot be classified, take one trimmed snapshot of that one item, and only when it is in the top three you might recommend.

Classify into Ready to review, Ready to fix conflicts, Ready to revise, Ready to merge, Merge handoff needed, Ready to reply, Acknowledge or route, No reply needed, Needs semantic review, Ready to implement, Review request needed, and Waiting or blocked. A named foreign conflicted PR/MR is `WRITE_NOT_AUTHORIZED`, not ready to fix.

Ready to implement: open issues assigned to me that are not blocked, not already covered by an active PR/MR, and have a current `<!-- git-plan-issue -->` brief whose Goal, Recommended change, Out of scope, and Acceptance criteria contain no unsettled product decision. When none exists, or an unsettled product decision remains, recommend `/git-plan-issue` with the exact issue URL. An unresolved `<!-- git-plan-issue-dissent -->` waits for a human decision. `/git-triage` does not load `gentle-grill-me`.

Report each actionable item with reason, live evidence, remaining gate, and exact next command. End with a compact top three and ask which item to handle next.

### Project triage workflow

Scope to the current repository's forge project, or the project URL/path supplied in arguments. One metadata PR/MR list and one metadata issue list. Do not open each row. Apply the same relationship model inside the selected project. Include sibling repositories only when repo-local instructions identify them or the user asks.

Add hygiene buckets **Needs reviewer** and **Needs assignee**. Do not auto-assign. Prefer `/git-request-review` when the user owns the PR/MR; otherwise report who should request review. A list row has no comment body, so do not call an issue Ready to implement from the list. Recommend `/git-issue-pr` only after a trimmed snapshot shows a settled current brief. Until then the next command is `/git-plan-issue` with the exact issue URL. `/git-triage` does not load `gentle-grill-me`. Mention `/git-issue-pr` only after ownership is clear.

Suggested commands include `/git-review-pr`, `/git-revise-pr`, `/git-fix-conflict`, `/git-request-review`, `/git-pr-status`, `/git-plan-issue`, `/git-issue-pr`, `/git-merge-approved`. End with a compact top-three recommendation and ask which item to handle next.

## Aggressive Triage Run

Use this when the user invokes `/git-triage run` (aliases `aggressive` / `execute`).

1. Resolve authenticated forge user and triage scope. Honor modifiers: `no-merge`, `merge-only`, `include-drafts`, `with-issues`, `dry-run`, and optional explicit `reviewer:USERNAME` (a user-chosen username, no hard-coded reviewer). `/git-triage run` does not inherit force.
2. Classify with the matching read-only triage workflow first. If `dry-run`, stop after listing planned actions; no writes. This mode may surface reply candidates but must not auto-post issue replies; use `/git-reply-issue` separately. It may surface issues that still need an implementation brief but must not auto-post those briefs; use `/git-plan-issue` separately.
3. Capture any **explicit** reviewer from args. Do not silently invent a reviewer from memory or hard-coded names. Repo-local docs may inform later suggestions but must not auto-assign without the user stating a reviewer for this run.
4. **Assignee hygiene (early):** for open PRs/MRs where the authenticated user is the **author** and **empty assignees**, set assignee to the authenticated user. Do not assign yourself on PRs/MRs you did not author. Do not replace an existing non-empty assignee list.
5. Execute the complete lifecycle unless `merge-only`: Ready to review → `/git-review-pr`; owned conflicts → `/git-fix-conflict`; owned revision → `/git-revise-pr`; owned Ready to merge → `/git-merge-approved` (skip when `no-merge`); owned PRs/MRs that already have a reviewer and only need current-head re-request → `/git-request-review`.
6. **Defer missing-reviewer hygiene to the end.** If the user already specified `reviewer:USERNAME`, assign that reviewer and request review. If no reviewer was specified, list those PRs/MRs and **ask who to assign**. Wait for the user's answer; do not guess.
7. Before every write, take one new snapshot and re-run the PR/MR command preflight. Live state overrides the triage list. Do not issue a call per field.
8. Do not auto-implement issues unless `with-issues` is present.
9. Prefer isolated worktrees when local checkouts are dirty or belong to another branch/repo.
10. After the sweep, report each item as done / skipped / waiting with evidence.
