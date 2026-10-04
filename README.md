# git-collaboration

Forge-neutral GitHub and GitLab collaboration skill for coding agents.

This repository is a portable copy of a GitLab-first collaboration workflow,
rewritten so it works on GitHub and GitLab without company paths, personal
accounts, or a default reviewer.

## What it does

- Detects GitHub vs GitLab from the request URL, then from `git remote`.
- Reads each issue or PR/MR once, trimmed to the fields that decide the next action, then plans and edits from the local checkout.
- Reviews, revises, conflict-repairs, and merges PRs/MRs under live actor gates.
- Dedicated `/git-review-pr-force`, `/git-revise-pr-force`, and `/git-merge-approved-force` for solo self-review, owned iteration without `NEEDS_REVISION`, and second-person-approval waiver. `/git-triage-force` plans a solo project and `/git-triage-force run` runs those on the planned owned items. `/git-triage` and scheduled runs do not inherit force.
- Uses `open-code-review-delegate` for the file-by-file pass. `/git-review-pr` maps findings onto forge comments. Push and open/update PR/MR run a fail-closed pre-submit gate: a fresh `requesting-code-review` subagent, or an inline file pass for a light-tier diff (at most 3 files and 60 lines). After a Critical or High fix, the next pass covers only the fix range; a Medium/Low-only fix re-runs the tests.
- Plans an issue (`/git-plan-issue`), then implements (`/git-issue-pr`) with
  optional dissent on the issue instead of silently following a weak plan.
- Project triage writes an ordered plan to an untracked `PROGRESS.md` (merge first, then revise and conflict repair, review, review requests, issues). `run` executes only that file's rows, with plain gates; with no plan file it writes one and stops. Optional scheduled allowlist runs. Scheduled runs never invent a
  reviewer and never assign anyone.

## Layout

```text
SKILL.md                         # router: forge, budgets, mode table, load map
references/preflight.md          # actor gate, primary state, explicit force
references/handoff.md            # one next step per mode
references/work-order.md         # handoff brief recipe and checks
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
references/triage.md             # read-only triage, plan order, aggressive run
references/triage-force.md       # solo force sweep
references/scheduled-automation.md
references/pstack.md
prompts/git-*.md                 # mode name, actor gate, reference path
scripts/validate.py              # leak + contract checks
scripts/budget.py                # per-mode instruction bytes and caps
scripts/eval.py                  # behavior scenarios through claude -p
evals/scenarios/*.json           # snapshot, command, expected decision
```

## Optional pstack companion

pstack is optional. Modes keep their current behavior when it is absent, apart from the Proof record.

Detection runs once and makes no forge call. `pstack:off` turns pstack off for that invocation. `pstack:required` stops before the first write and names the missing skills when detection fails. Otherwise the runtime skill list, then one filesystem probe, decides whether pstack is present. A hook loads its pstack skill only when its trigger fires, and the supported version range is a maintainer upgrade check, not a per-run gate. git-collaboration keeps the forge gates; pstack supplies the rigor (`principle-prove-it-works`, `blast-radius`, `interrogate`, `tdd`, `principle-fix-root-causes`).

git-collaboration gates win on conflict. pstack never merges and never polls the forge under this skill.

Consumers should dual-pin the git-collaboration tip SHA and the pstack version; before upgrading either side, run the checklist in `references/pstack-compat.md`.

Prose is off by default. Add `pstack:prose`, or ask to fix prose, to run it.

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

## Behavior evals

```bash
python3 scripts/eval.py --self-test          # offline: grade the fixtures
python3 scripts/eval.py                      # live: run every scenario on this checkout
python3 scripts/eval.py --ref <sha> --out r.json
python3 scripts/eval.py --repeat 3             # min/mean/max per scenario
```

Each file in `evals/scenarios/` holds one forge snapshot, a command, and the
expected result block (`STATE:`, `WRITES:`, `NEXT:`). The live run sends it
through `claude -p` with only the Read tool and no user settings, MCP servers,
or slash commands, so nothing touches a forge. It prints pass or fail and the
input tokens per scenario. `--ref` evaluates an older commit from a temporary
worktree. `scripts/validate.py` runs the offline self-test.

Noise (`--repeat 3` on 10 scenarios, default model, #61): input tokens vary
about 1% between runs of the same scenario, while cost per run ranged
$1.81-$2.27 (mean $1.98, about +/-13%). Compare input tokens across versions;
treat a cost change under about 15% as noise.

A new behavior rule lands with a validator check or a scenario that fails
without it. Validator checks match key phrases or parse structure, not whole
sentences, so rewording a rule does not mean editing the validator.

## Instruction budget

```bash
python3 scripts/budget.py
```

Each mode loads `SKILL.md` plus the references its load line names. The
script prints the bytes and approximate tokens (bytes / 4) per mode, and
`scripts/validate.py` fails when a mode exceeds its cap in `scripts/budget.py`.
Caps only go down: the validator compares them with `origin/main` (or `BUDGET_BASE`) and fails on a raise. After a change shrinks a mode, run `python3 scripts/budget.py --lower-caps`.

Baseline before the router and pstack cuts (#40):

| Mode | Bytes | ~Tokens | +pstack |
| --- | ---: | ---: | ---: |
| Review | 45,908 | 11,477 | 13,051 |
| Plan issue | 44,395 | 11,098 | 12,672 |
| Implement | 51,866 | 12,966 | 14,540 |
| Reply | 21,829 | 5,457 | 5,457 |
| Revise | 28,651 | 7,162 | 8,736 |
| Conflict | 27,520 | 6,880 | 8,454 |
| Merge | 32,540 | 8,135 | 8,135 |
| Request review | 21,682 | 5,420 | 5,420 |
| Status | 21,233 | 5,308 | 5,308 |
| Triage | 26,353 | 6,588 | 6,588 |
| Scheduled | 31,820 | 7,955 | 7,955 |

A new behavior rule must fit the cap. Prefer a check, a scenario, or a script
over another paragraph.

## Reviewer policy

There is no default reviewer. A reviewer comes from an explicit
`reviewer:USERNAME`, a reviewer already requested on the PR/MR, or a question
to the user. CODEOWNERS may be listed as options. Memory, prior runs, and
hard-coded names do not create a reviewer.

Solo override is a dedicated command: `/git-review-pr-force <url>`,
`/git-revise-pr-force <url>`, and `/git-merge-approved-force <url>`; `/git-triage-force` runs them across a project. Repo docs
and "this is a solo project" do not create force.

A Proof for a user-visible output (video, image, audio, UI) names the content checked; an output that only exists stays a remaining gate, and review treats a live-job claim on it as an Evidence class mismatch.

`/git-review-pr-force` skips the file pass when a full-tier pre-submit range ends at the current head, and reviews only the new commits when the head moved; the Proof re-run and gates always run.

A `/git-review-pr-force` review that GitHub will not accept as APPROVE still leaves `verdict: approve` or `verdict: request-changes` on the pull request, and the chat reply has one `next step:` line.

## Executor-ready brief

Default brief is a decision card; a handoff to another session, model, or agent gets the full work-order.

`/git-plan-issue` may run on a strong model while `/git-issue-pr` runs on a
weaker one. The handoff work-order is that full recipe:

- **Planned at** `branch@SHA`, so the executor can diff the planned paths and
  notice drift.
- **Execution plan**: ordered steps, each with files, the exact change, and a
  Verify command with its expected result. Tests come first.
- **Interfaces**: new or changed signatures and shapes, never function bodies.
- **Test cases**: Given / When / Then with literal values, each mapped to an
  acceptance line.
- **Stop and dissent when**: checkable assumptions. If one fails, the executor
  posts a dissent instead of improvising.

A handoff work-order that needs more than 8 steps is a scope decision and goes through the
grill instead of a longer brief.

Optional `Brief:` and `Executor-model:` lines under `## Verification` are observation only, not a gate.

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

- **Always:** Forge budget and Context budget from `SKILL.md`, plus `references/handoff.md` for the reply.
- **Mode:** `references/implement.md` + `references/plan-issue.md` (brief and dissent recipe only) + `references/work-order.md` (when the brief has an Execution plan) + `references/pre-submit.md` + one forge reference (`references/github.md` or `references/gitlab.md`).
- **Never for implement-only:** `references/merge.md`, `references/review.md`, `references/triage.md`, `references/scheduled-automation.md`, and force variants (`/git-review-pr-force`, `/git-revise-pr-force`, `/git-merge-approved-force`).
- **Optional add-on:** `references/pstack.md`. The profile works without it. When vendored, vendor the file whole.

Opening or updating a draft PR is not permission to merge. Merge modes are a separate invocation and require their own approval gates.


