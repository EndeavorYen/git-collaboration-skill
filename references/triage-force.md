# Force triage run

Read this file for `/git-triage-force`, after `triage.md`. The human must invoke this command by name; `/git-triage run`, repo docs, and "this is a solo project" do not create it. A scheduled run never uses it.

## Scope

The current repository's forge project, or the project URL/path in arguments. Modifiers: `no-merge`, `include-drafts`, `no-issues`, and `base:BRANCH` for new PRs/MRs (default: Safety Defaults).

Force covers only `owned` PRs/MRs and issues that are unassigned or assigned to the authenticated user. Every other item keeps its plain command and gate: a foreign PR/MR gets `/git-review-pr` and is never revised, conflict-repaired, or merged here. An issue assigned to someone else is skipped.

## Plan

Classify with **Project triage workflow** and order with **Plan order** in `triage.md`. Plan order step 4 becomes `/git-review-pr-force`. Each owned PR/MR gets a chain; each issue gets `/git-plan-issue` then `/git-issue-pr`, then its new PR/MR's chain.

| Live state | Next command in the chain |
| --- | --- |
| `CONFLICTED` | `/git-fix-conflict` |
| `NEEDS_REVISION`, a relevant failed job, or `verdict: request-changes` on the current head | `/git-revise-pr-force` |
| no `verdict: approve` on the current head | `/git-review-pr-force` |
| `verdict: approve` on the current head, required CI green | `/git-merge-approved-force` (skip on `no-merge`) |

Bare `/git-triage-force` (or `dry-run`) writes the **Plan file** and stops with no forge write. `run` follows **Aggressive Triage Run** steps 2, 3, 8, and 10 with the chains above.

## Run

Before each command, read that mode's load line in `SKILL.md` and follow its mode file. After a merge, re-snapshot the next PR/MR; a new conflict puts `/git-fix-conflict` at the front of its chain.

Force waives only the human gates: a second-person approval, `NEEDS_REVISION`, and the self-review actor gate. Every technical gate stays: draft, running or failed required CI, pre-submit, current-head verdict, mergeability, and the final merge gates in `merge.md`.

Never request review or assign a reviewer. Do not auto-post issue replies.

An item stops as **waiting** and the run moves to the next one when: `/git-plan-issue` posts no brief (an unsettled product decision; quote the question), a dissent is posted, required CI is running or failed outside the diff, `/git-review-pr-force` gives `verdict: request-changes` after two `/git-revise-pr-force` rounds, or a gate above fails. Stop the whole run only on missing auth.

## Report

One row per plan step: item URL, commands run, result (merged / done / waiting / skipped), and evidence (merge SHA, new head, or blocking gate). For waiting items, name what the human must decide. End with `next step: /git-triage-force run` when any item is waiting on CI, otherwise `next step: none`.
