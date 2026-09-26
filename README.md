# git-collaboration

Forge-neutral GitHub and GitLab collaboration skill for coding agents.

This repository is a portable copy of a GitLab-first collaboration workflow,
rewritten so it works on GitHub and GitLab without company paths, personal
accounts, or a default reviewer.

## What it does

- Detects GitHub vs GitLab from the request URL, then from `git remote`.
- Reads each issue or PR/MR once, trimmed to the fields that decide the next action, then plans and edits from the local checkout.
- Reviews, revises, conflict-repairs, and merges PRs/MRs under live actor gates.
- Dedicated `/git-review-pr-force`, `/git-revise-pr-force`, and `/git-merge-approved-force` for solo self-review, owned iteration without `NEEDS_REVISION`, and second-person-approval waiver. Triage and scheduled runs do not inherit force.
- Uses `open-code-review-delegate` for the file-by-file pass. `/git-review-pr` maps findings onto forge comments. Push and open/update PR/MR run a fail-closed pre-submit gate via a fresh `requesting-code-review` subagent.
- Plans an issue (`/git-plan-issue`), then implements (`/git-issue-pr`) with
  optional dissent on the issue instead of silently following a weak plan.
- Triage and optional scheduled allowlist runs. Scheduled runs never invent a
  reviewer and never assign anyone.

## Layout

```text
SKILL.md                         # router: forge, budgets, actor gate, force
references/github.md             # gh CLI and GitHub approval APIs
references/gitlab.md             # glab CLI and GitLab approval APIs
references/pre-submit.md         # file pass and waiver rules
references/review.md             # review and force-review
references/plan-issue.md         # brief and dissent recipe
references/implement.md          # issue to PR/MR
references/revise.md             # owned update
references/conflict.md           # conflict repair
references/merge.md              # approved merge
references/reply.md              # issue reply
references/request-review.md
references/status.md
references/triage.md             # read-only triage and aggressive run
references/scheduled-automation.md
references/pstack.md
prompts/git-*.md                 # mode name, actor gate, reference path
scripts/validate.py              # leak + contract checks
```

## Optional pstack companion

pstack is optional. Modes keep their current behavior when it is absent, apart from the Proof record.

Detection runs once and makes no forge call. `pstack:off` turns pstack off for that invocation. `pstack:required` stops before the first write and names the missing skills when detection fails. Otherwise the runtime skill list, then one filesystem probe, decides whether pstack is present.

git-collaboration gates win on conflict. pstack never merges and never polls the forge under this skill.

Consumers should dual-pin the git-collaboration tip SHA and the pstack version; before upgrading either side, run the checklist in `references/pstack-compat.md`.

## Install

Copy or symlink this directory into your agent skills folder as
`git-collaboration`. Copy `prompts/*.md` into the runtime's command or action
directory if that runtime uses separate prompt files.

Examples:

```bash
# Claude Code / compatible skills dir
ln -s "$PWD" "${CLAUDE_HOME:-$HOME/.claude}/skills/git-collaboration"

# Codex-style skills dir
ln -s "$PWD" "${CODEX_HOME:-$HOME/.codex}/skills/git-collaboration"
```

Commands are named `/git-review-pr`, `/git-issue-pr`, `/git-plan-issue`, and so
on. A pasted GitHub or GitLab URL still selects the matching mode.

## Validation

```bash
python3 scripts/validate.py
```

The validator fails closed on company paths, personal accounts, local-only
binaries, and a missing dual-forge contract.

## Reviewer policy

There is no default reviewer. A reviewer comes from an explicit
`reviewer:USERNAME`, a reviewer already requested on the PR/MR, or a question
to the user. CODEOWNERS may be listed as options. Memory, prior runs, and
hard-coded names do not create a reviewer.

Solo override is a dedicated command: `/git-review-pr-force <url>`,
`/git-revise-pr-force <url>`, and `/git-merge-approved-force <url>`. Repo docs
and "this is a solo project" do not create force.

A `/git-review-pr-force` review that GitHub will not accept as APPROVE still leaves `verdict: approve` or `verdict: request-changes` on the pull request, and the chat reply has one `next step:` line.

## Executor-ready brief

`/git-plan-issue` may run on a strong model while `/git-issue-pr` runs on a
weaker one. The brief is therefore a work order, not a summary:

- **Planned at** `branch@SHA`, so the executor can diff the planned paths and
  notice drift.
- **Execution plan**: ordered steps, each with files, the exact change, and a
  Verify command with its expected result. Tests come first.
- **Interfaces**: new or changed signatures and shapes, never function bodies.
- **Test cases**: Given / When / Then with literal values, each mapped to an
  acceptance line.
- **Stop and dissent when**: checkable assumptions. If one fails, the executor
  posts a dissent instead of improvising.

A plan that needs more than 8 steps is a scope decision and goes through the
grill instead of a longer brief.

## Read-then-write gate

During issue implementation (`/git-issue-pr`), agents must not enter read-only
exploration loops:

- **Anti-pattern:** Multiple rounds of `grep`, directory walks, and file reads
  disguised as "locating where tests live" with zero file writes.
- **Contract:** At most one focused search and symbol/test inspection round,
  followed immediately by creating or editing a test or implementation file.
  More than one read round without edits is out of mode.

## Minimal implement profile

For consumers who only need issue implementation into a PR/MR (`/git-issue-pr`), load only the minimal implement set instead of the full router or secondary workflow files:

- **Always:** Forge budget and Context budget from `SKILL.md`.
- **Mode:** `references/implement.md` + `references/plan-issue.md` (brief and dissent recipe only) + `references/pre-submit.md` + one forge reference (`references/github.md` or `references/gitlab.md`).
- **Never for implement-only:** `references/merge.md`, `references/review.md`, `references/triage.md`, `references/scheduled-automation.md`, and force variants (`/git-review-pr-force`, `/git-revise-pr-force`, `/git-merge-approved-force`).
- **Optional add-on:** `references/pstack.md`. The profile works without it. When vendored, vendor the file whole.

Opening or updating a draft PR is not permission to merge. Merge modes are a separate invocation and require their own approval gates.


