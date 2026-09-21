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
SKILL.md                         # workflow (source of truth)
references/github.md             # gh CLI and GitHub approval APIs
references/gitlab.md             # glab CLI and GitLab approval APIs
references/scheduled-automation.md
prompts/git-*.md                 # slash/action sources
scripts/validate.py              # leak + contract checks
```

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
