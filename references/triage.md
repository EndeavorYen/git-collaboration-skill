# Triage

Read this file for `/git-triage` and `/git-triage-force`.

## Status Triage Workflow

No forge write unless the user picks a follow-up. Do not auto-assign issues or PRs/MRs. Never self-assign only to unlock merge.

Mode selection:

- **Todo triage** (default): empty args, or `todo` / `mine` / `inbox`.
- **Project triage**: `project` / `this repo` / a forge project URL or path.
- **Issue triage**: args name only issues; read `references/triage-issues.md`.
- **Aggressive run**: args contain `run` / `aggressive` / `execute`.
- With both markers, prefer project when a project target is present; otherwise todo.

### Todo triage workflow

Build a forge-global inbox from metadata lists only: notifications or todos; PRs/MRs where the user is reviewer, author, or assignee; open issues assigned to or authored by the user. Open one trimmed snapshot only to write or for the item the user named.

Notifications are signals, not source of truth. Another user speaking last is necessary but insufficient to require a reply. Rank from list fields. Snapshot an unclassifiable row only if it may make the top three.

Classify into Ready to review, Ready to fix conflicts, Ready to revise, Ready to merge, Merge handoff needed, Ready to reply, Acknowledge or route, No reply needed, Needs semantic review, Ready to implement, Review request needed, and Waiting or blocked. A named foreign conflicted PR/MR is `WRITE_NOT_AUTHORIZED`, not ready to fix.

Ready to implement: an open issue assigned to me, not blocked, not covered by an active PR/MR, with a current `<!-- git-plan-issue -->` brief whose Goal, Recommended change, Out of scope, and Acceptance criteria hold no unsettled product decision. Otherwise `/git-plan-issue` with the issue URL. An unresolved `<!-- git-plan-issue-dissent -->` waits for a human.

Report each item with reason, evidence, gate, and next command, then a top three and ask which to handle next.

### Project triage workflow

Scope to this repo's forge project, or the project URL/path in arguments. One PR/MR list (**Project list**) and one metadata issue list; do not open each row. Include a sibling only when instructions or the user name it.

Add **Needs reviewer** and **Needs assignee**. Prefer `/git-request-review` when the user owns the PR/MR; otherwise report who should request review. Recommend `/git-issue-pr` only after a trimmed snapshot shows a settled current brief and clear ownership; until then `/git-plan-issue` with the exact issue URL.

Write actionable items to the **Plan file** in **Plan order**. Issue rows and **Needs semantic review** rows that plain `run` skips are `manual`. Ask to run only with a `todo` row.

### Plan file

`PROGRESS.md` at the main checkout root, added to `.git/info/exclude`, never committed. First line `<!-- git-triage-plan -->`; never overwrite a `PROGRESS.md` without it, stop and ask. Header: planner, repo, target branch, time. One row: URL, command, status (`todo` / `done` / `waiting` / `skip` / `manual`), evidence. Todo triage writes no file.

### Plan order

Merging moves the target branch, so:

1. Owned Ready to merge.
2. Owned Ready to revise, then owned Ready to fix conflicts.
3. Ready to review.
4. Owned Review request needed.
5. Issues: `/git-plan-issue` before `/git-issue-pr`.

Within a step, oldest first. A PR/MR based on another open PR/MR, or that depends on one, comes after it. One that touches the same files **may conflict after #N**.

## Project list

`scripts/project-triage-list.sh` is the one PR/MR list. The issue list stays the metadata list in the forge. Todo triage keeps inbox lists. Notes use `comments(last:` / `notes(last:`. The latest non-author note is the latest comment, not the first. A reviewer follow-up that is the latest comment stays visible.

`latestFeedback` is that note (`author`, `at`, first 160). `authorReplyAt` is the author's latest note. `unresolvedNonAuthor` counts unresolved resolvable discussions with a non-author comment on that latest page. `latestNonMergeAt` skips a commit that only merges the target branch in. Times end in `Z`. `reviewRequestAt` is a pending review request; a later removal note or GitHub event clears that person, and `UNREVIEWED` is not one. A request or removal outside the last 40 discussions (when `discussionsTruncated`) or the last 8 GitHub events may be missing, so null `reviewRequestAt` does not prove none were requested. `discussionsTruncated` is not a zero count. When `listTruncated` is true, the run says the open PR/MR list was truncated.

`mergeableDiscussionsState=true` does not prove there is no outstanding feedback. Neither does `approved=false`, an empty `reviewDecision` after a `COMMENTED` review, or `UNREVIEWED`.

- A reviewer note or review newer than the latest non-merge commit, with no later author reply: **Ready to revise** (`/git-revise-pr`) when the excerpt reads as blocking, otherwise **Needs semantic review**. Never **Waiting for review**. Blocking: it asks for a change or says the work still fails.
- Any unresolved non-author resolvable discussion, or `discussionsTruncated`: not **Waiting for review**. Use the bullet above when the time test matches; otherwise **Needs semantic review**.
- **Waiting for review** requires a current-head review request (`reviewRequestAt` not older than `latestNonMergeAt`) and no reviewer note newer than the latest non-merge commit.

```bash
scripts/project-triage-list.sh github "$OWNER" "$REPO"
scripts/project-triage-list.sh gitlab "$PROJECT"
```

## Aggressive Triage Run

`/git-triage run` does not inherit force.

1. Resolve the authenticated user. Scope is project triage: the current repo, or a project in arguments. Modifiers: `no-merge`, `merge-only`, `include-drafts`, `with-issues`, and `reviewer:USERNAME`. `dry-run` means the bare command.
2. No **Plan file**: write it and stop with no forge write. One from another planner, repo, or target branch: stop and ask before rewriting it.
3. Otherwise the file is the only target list. Run rows in order from the first not `done`; skip rows the owner deleted or marked `skip`. Do not touch an item missing from the file; report it as **new since plan**. Plain `run` never runs a `*-force` row or auto-posts replies or briefs. A `scope: issues` plan follows `references/triage-issues.md` over steps 1, 3, and 8.
4. **Assignee hygiene (early):** assign yourself to planned PRs/MRs you **authored** with **empty assignees**. Never assign yourself elsewhere or replace a non-empty list.
5. Row commands unless `merge-only`: Ready to review → `/git-review-pr`; owned conflicts → `/git-fix-conflict`; owned revision → `/git-revise-pr`; owned Ready to merge → `/git-merge-approved` (skip on `no-merge`); owned current-head re-request with an existing reviewer → `/git-request-review`.
6. **Missing reviewers last.** With `reviewer:USERNAME`, assign and request review. Otherwise list those PRs/MRs and **ask who to assign**; wait, do not guess.
7. Before every write, take one new snapshot and re-run preflight. Live state overrides the row: reroute within that item or mark it `waiting`.
8. Do not auto-implement issues unless `with-issues` is present.
9. After each command, write status and evidence to its row. If the next command is runnable, set it and go on.
10. Skip an unchanged `waiting` row. No `todo` left: say what each needs; do not suggest `run`.
