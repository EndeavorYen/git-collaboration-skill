---
description: Rank or aggressively run a personal GitHub/GitLab todo inbox, issue reply needs, or project PR/MR lifecycle
---

Use the installed `git-collaboration` skill in "Status or triage" mode, or in
"Aggressive triage run" mode when args request execution. Detect the forge from
the URL, remotes, or project target.

## Mode selection

Resolve triage scope and execution intent from the command arguments (and
surrounding user text):

| Intent | When |
| --- | --- |
| `todo` scope | **Default** when no project target; or args contain `todo`, `mine`, or `inbox` |
| `project` scope | Args contain `project`, `this repo`, a GitHub or GitLab project URL/path, or other project-scoped narrowing |
| `run` execution | Args contain `run`, `aggressive`, or `execute` |

If both `todo` and `project` markers appear, prefer `project` when a concrete
project target is present; otherwise prefer `todo`.

`run` may combine with either scope (`run`, `run todo`, `run project`,
`run this repo`). Without an explicit project target, `run` uses the personal
todo inbox.

Optional modifiers:

- `reviewer:USERNAME` or `reviewer USERNAME` — optional user-chosen username for owned PRs/MRs that still lack a reviewer. Never invent a reviewer. There is no hard-coded reviewer and no default reviewer.
- `no-merge` — execute lifecycle except merge
- `merge-only` — only owned ready-to-merge PRs/MRs
- `include-drafts` — include drafts in the end-of-run missing-reviewer list (still never merge drafts)
- `with-issues` — also implement ready issues via `/git-issue-pr`
- `dry-run` — classify and list planned actions with no writes

## Read-only triage (`todo` / `project` without `run`)

Keep the workflow read-only unless the user explicitly chooses a follow-up
action. Do not auto-assign issues or PRs/MRs, and never suggest self-assignment only
to unlock merge.

Build issue candidates from pending notifications plus open issues assigned to the authenticated user, open issues authored by the user, and issues where the user recently participated through a non-system issue comment. Include directly addressed or mentioned issue todos. Treat notifications as signals rather than conversational source of truth, and state pagination or timebox limits.

For each candidate compare non-system human comments chronologically. The fact that another user spoke last is necessary but insufficient: classify **Ready to reply**, **Acknowledge or route**, **No reply needed**, or **Needs semantic review** from the latest material request, later user response, state changes, and explicit ownership.

Then run the matching workflow section in `git-collaboration`:

- `todo` → **Todo triage workflow** (forge-global personal inbox)
- `project` → **Project triage workflow** (current or specified project), including hygiene buckets **Needs reviewer** and **Needs assignee**

### Output contract (read-only)

- Classify into the buckets defined by the selected workflow.
- For each actionable item: reason, live evidence, remaining gate, and exact next command (`/git-review-pr`, `/git-revise-pr`, `/git-fix-conflict`, `/git-request-review`, `/git-pr-status`, `/git-plan-issue`, `/git-issue-pr`, `/git-merge-approved`, `/git-reply-issue` with the exact issue URL).
- For merge-ready items, include **Merge handoff needed** when the authenticated user is not the PR/MR author or a current assignee, instead of suggesting self-assignment.
- Never recommend `/git-fix-conflict` or `/git-revise-pr` for a foreign PR/MR, even if the user named it. Never recommend `/git-review-pr` for an owned or `self_authored_head` PR/MR.
- End with a compact top three and ask which item to proceed with.

## Aggressive run (`run` / `aggressive` / `execute`)

When execution is requested, use the **Aggressive triage run** workflow in
`git-collaboration`. First classify with the selected scope, then execute the
complete owned/reviewer PR/MR lifecycle. Re-run live PR/MR command preflight before
every write, including the actor gate. User-named PRs/MRs, conflict lists, and
review lists never override `owned` or `self_authored_head`. Skip
`WRITE_NOT_AUTHORIZED`, `MERGE_NOT_AUTHORIZED`, and `REVIEW_NOT_AUTHORIZED`
items instead of repairing or self-reviewing them. Live state wins over the
triage snapshot. Run mode may surface issue reply candidates but must not auto-post issue replies; recommend `/git-reply-issue` instead. It may surface issues that still need an implementation brief but must not auto-post those briefs; recommend `/git-plan-issue` instead.

Default execution order:

1. **Assignee hygiene:** open PRs/MRs I authored with empty assignees → set assignee to me
2. Review PRs/MRs waiting on me, excluding PRs/MRs I own or that contain my commits
3. Fix conflicts on owned PRs/MRs only; a named foreign conflicted PR/MR is `WRITE_NOT_AUTHORIZED`
4. Revise owned PRs/MRs (feedback / failed CI)
5. Merge owned PRs/MRs that are `READY_TO_MERGE` via `/git-merge-approved` (skip with `no-merge`)
6. Re-request review only where a reviewer already exists and current-head review is needed

Author-self-assign (step 1) is required ownership hygiene. It is **not** the forbidden
"self-assign only to unlock merge" bypass used by non-authors/reviewers.

**Missing reviewer is last, not mid-sweep:**

- After the steps above, list owned open PRs/MRs that still have **no reviewer assigned**.
- If the user already passed `reviewer:USERNAME` → assign that username and request review.
- If not → list the PRs/MRs and **ask who to assign**; wait for the answer; do not guess or hard-code a name.

### Output contract (`run`)

- For each item: action taken or skipped, evidence, new head/pipeline when changed, remaining gate.
- End with a compact done / skipped / waiting summary (include assignee hygiene applied).
- If any owned PRs/MRs still lack a reviewer and none was pre-specified, end by listing them and asking who to assign.

$ARGUMENTS
