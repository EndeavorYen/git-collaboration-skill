# Issue triage

Read this file, after `triage.md`, when `/git-triage` or `/git-triage run` arguments name only issues (`#12 #13`, issue URLs), or when the **Plan file** header says `scope: issues`.

## Plan

Scope is exactly the named issues in the current repository's forge project. Naming an issue opts it in: a `run` of this plan may post its brief and implement it without `with-issues`. Every other gate stays: `/git-plan-issue` posts no brief while a product decision is unsettled, and nothing merges.

Take one trimmed snapshot per named issue. Write the **Plan file** with `scope: issues` in the header and one row per issue:

- No current brief → `/git-plan-issue`. When the draft has an unsettled product decision, the row is `waiting` and its evidence quotes the question and the options.
- A settled current brief → `/git-issue-pr`.
- Assigned to someone else, closed, or covered by an open PR/MR → `skip`, with that evidence.

Then report the rows and ask whether to run the plan.

## Decisions

When the user answers a waiting row's question in the conversation (`#12 option 1`), write `decision: <answer>` to that row's evidence, set it `todo`, and say so. Do not post the brief in that turn unless the user also asks for it. On the next run, `/git-plan-issue` treats the recorded decision as settled for that question; any other open question keeps the row `waiting`.

When the brief was posted outside the run, set the row to `/git-issue-pr` with status `todo`.

## Run

Follow **Aggressive Triage Run** in `triage.md`. Each row runs its command; after a brief is posted, the row becomes `/git-issue-pr` and runs on in the same pass. After `/git-issue-pr` opens the PR/MR, the row is `done` with the PR/MR URL; review and merge are separate commands.
