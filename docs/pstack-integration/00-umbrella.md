# Umbrella: deep-integrate pstack into git-collaboration

## Problem

pstack (the Cursor plugin by Lauren Tan: `/poteto-mode`, its playbooks, the `principle-*` skills, `arena`, `swarm`, `interrogate`, `blast-radius`, `create-verification-skill`) and this skill overlap on planning, implementation, review, and PR work. Neither knows about the other.

- An agent in `/poteto-mode` that runs `/git-issue-pr` gets two routers. poteto-mode wants the Feature or Bug fix playbook plus Opening a PR. `references/implement.md` wants the brief as the work order and its own PR steps. Nothing says who owns forge writes, the PR body, or the stop condition.
- pstack's Autonomy section ("Just do it", **principle-never-block-on-the-human**) contradicts gates here: human-only pre-submit waivers, `gentle-grill-me` for unsettled product decisions, asking the user for a reviewer, and dissent-then-wait.
- pstack's Babysit, Shipping, and Opening a PR playbooks issue their own `gh` / `origin` / `watch-pr` calls. That bypasses **Forge budget**, does not work on GitLab, and Shipping merges.
- `why` and `blast-radius` step 1 pull PRs and commits through forge or MCP queries. That is a second forge client.
- Our evidence rules (`verification-before-completion`, review **Evidence class**) have no link to pstack's stronger proof tools. "Tests passed" can still pass a user-visible change that was never driven.
- Team4 `poteto-dispatch` is a one-line dispatch wrapper. The integration has to live upstream, in this skill.

## Goal

When a git-collaboration mode runs and pstack is available, the agent knows which pstack skill or playbook to run at which step, and what evidence counts as done. When pstack is absent or turned off, every mode behaves as it does today, apart from the one pstack-neutral **Proof record** that step 2 adds. No gate gets weaker.

## Design

### 1. Architecture: one companion reference, hooked from mode references

| Option | Verdict |
| --- | --- |
| A. Add pstack triggers to `SKILL.md` | Rejected. `SKILL.md` is at 2998 of 3000 words. It would also load pstack text for merge, triage, and scheduled runs. |
| B. New `/git-*-pstack` modes | Rejected. Doubles the mode table, prompts, actor-gate rows, and validator contracts. Users have to pick a fork of every command. |
| C. One optional `references/pstack.md`, loaded by a one-sentence hook in the mode references that already own the step | **Chosen.** |

Shape of option C:

- `references/pstack.md` (new, validator cap about 900 words). It holds detection, precedence, the per-mode hook table, fallbacks, and the record line. It names pstack skills and playbooks by name only. It never copies pstack text.
- Hook sentences go in `references/pre-submit.md` and `references/plan-issue.md`. Implement, revise, conflict, and review already read `pre-submit.md`, so two hooks reach all five modes. A mode reference gets its own anchor sentence only when a numbered step needs one (steps 4 to 6).
- The gate stays in this skill. Step 2 adds a pstack-neutral **Proof record** to the pre-submit gate and the PR/MR description. pstack skills are the preferred way to produce that proof. They are not the gate.
- `SKILL.md`: zero net words and no change to the load-line sentences. The validator asserts that the merge, scheduled, triage, reply, request-review, and status paths never name `references/pstack.md`.

### Precedence (every step inherits this)

1. git-collaboration owns forge detection, every forge read and write, actor gates, force, **Forge budget**, **Context budget**, the merge gate, reviewer policy, the brief and dissent recipes, waivers, stop conditions, and reply shape (`next step:`).
2. pstack owns how the local work is done between the snapshot and the write: investigation, design, the fix, proof, adversarial review, and prose polish.
3. On conflict, git-collaboration wins. Named cases:
   - pstack Autonomy does not waive human-only pre-submit waivers, the grill for unsettled product decisions, asking for a reviewer, or dissent-then-wait.
   - pstack forge commands (`gh` / `origin` in Opening a PR, Babysit polling, `watch-pr`, Shipping merge) do not run. Forge calls come only from `references/github.md` or `references/gitlab.md`, so GitLab keeps working.
   - `why` and `blast-radius` read local `git log` / `git blame` and the snapshot already in context. They do not query the forge or a forge MCP.
   - An Executor-ready brief with an Execution plan is the work order. Playbook steps that redesign (`how`, `architect`, `arena` in Feature) are recorded as `skip: brief is the work order`. The read-then-write gate holds.
   - pstack subagents (`poteto-agent`, arena runners, interrogate reviewers, swarm workers) never write to the forge. They get file pointers, the submit range, and the contract, never the forge snapshot or credentials.
   - Marker lines and fixed field labels (`<!-- git-plan-issue -->`, `**Goal:**`, `verdict:`, `next step:`, the Proof record labels) are exempt from `unslop` and `technical-writing` rewrites.

### 2. Mode mapping

| git-collaboration mode / step | pstack skill or playbook | Runs when | Evidence it must produce | Fallback when absent |
| --- | --- | --- | --- | --- |
| `/git-plan-issue` step 3 (inspect) | `how`; `why` limited to local git | Brief spans more than one subsystem, or root cause is a regression | Root cause cites `file:line` | Current step 3 |
| `/git-plan-issue` step 5 (Recommended change) | `architect`; `arena` when two or more valid shapes exist | Change crosses a function boundary | Rejected alternative comes from a real candidate | Current step 5 |
| `/git-plan-issue` step 5 (Stop and dissent when) | `blast-radius` load-bearing fact | Change touches a shared contract, wire format, schema, or config default | That fact is a checkable Stop and dissent line | Current step 5 |
| `/git-plan-issue` step 5 (Execution plan) | **principle-sequence-verifiable-units** | Always when present | Each step ends in a Verify (already required) | Current rule |
| `/git-plan-issue` step 6 (before the grill) | Prototype playbook | A fork whose answer is observable by running code | The fork is settled by a recorded run | `gentle-grill-me` as today |
| `/git-issue-pr` step 10 | Bug fix (reproduce first), Feature, or Refactoring (pin first); `tdd` | Matches the issue kind. The brief's Execution plan overrides redesign steps | Failing-then-passing output, or the refactor pin | Current TDD rule |
| `/git-issue-pr` step 11 | **principle-prove-it-works**; the repo's `verify-<app>` skill when present | Always when present | Proof record; real surface when the change is user-visible | `verification-before-completion` plus Proof record from tests |
| `/git-issue-pr` step 15 | Opening a PR section layout, `technical-writing`, `unslop`, `/deslop`, `/no-comments` when installed | Writing the PR/MR body and commit body | Why / Scope / Blast Radius / Verification plus every field this skill requires | Current description |
| Pre-submit gate | `blast-radius` | Deterministic trigger list (step 5) | Load-bearing fact with ladder level; unproven means a remaining gate | OCR file pass only |
| Pre-submit gate | `interrogate` | Contested design or thorough request (step 5) | Findings mapped to Critical / High / Medium / Low | OCR file pass only |
| `/git-review-pr`, `/git-review-pr-force` | `blast-radius`, `interrogate` (read-only, no auto-apply) | PR claims a fix; thorough-review triggers | Evidence class mapped to the ladder in the verdict | Current review |
| `/git-revise-pr`, `/git-revise-pr-force` | Bugbot triage rubric (fix / dismiss / ask), **principle-fix-root-causes**, **principle-attack-the-premise** | Bot or automated review threads; a second fix for the same blocker | Each thread reply names a fix SHA or a dismissal reason | Current revise |
| `/git-fix-conflict` | Babysit drift sweep, **principle-migrate-callers-then-delete-legacy-apis**, `blast-radius` | Target added callers of code the source deletes, renames, or re-signs | Drift sweep result in the Proof record | Current conflict repair |
| `/git-pr-status`, `/git-merge-approved(-force)`, `/git-request-review`, `/git-reply-issue`, triage, scheduled | none | | | |

Routing inside a repo that uses this skill: "check on PR X", "babysit", and "get it green" go to `/git-pr-status`, or to `/git-revise-pr` / `/git-fix-conflict` when owned. "Land" and "ship" go to `/git-merge-approved` per PR/MR. pstack Babysit and Shipping do not run.

### 3. Verification without soft-pass

- The gate belongs to this skill. pstack output is evidence. It never decides a pass. It never replaces the OCR file pass, the fresh `requesting-code-review` subagent, or `verification-before-completion`.
- Step 2 adds a pstack-neutral **Proof record** to the PR/MR description for implement, revise, and conflict. It is required with or without pstack:

  ```
  Proof: <command or skill run> -> <observed result>
  Evidence class: live job / real artifact bytes | executable unit tests | source-contract / regex tripwire | docs alignment
  Surface: <verify skill and feature driven> | none: <reason>
  Load-bearing fact: <fact> (level 1-5) | n/a
  pstack: present <version> [hooks run] | absent | off
  ```

- The Evidence class names are the ones in `references/review.md`. They map onto the `blast-radius` ladder: level 5 is live job / real artifact, level 4 is executable tests, levels 2 and 3 are source-contract, level 1 is no evidence.
- `blast-radius` and `interrogate` use deterministic trigger lists, so "optional" cannot drift into "never". When pstack is present and a trigger hits, the hook runs, or the Proof record says `skip: <reason>`. A silent skip fails the gate.
- `create-verification-skill` never runs inside `/git-issue-pr` unless the issue asks for it. When a user-visible change has no `verify-<app>` skill, the Proof record says `Surface: none: no verify skill` and the chat report recommends `/create-verification-skill` as separate work. No new write scope.

| Excuse | Reality |
| --- | --- |
| "pstack says it is fine" | pstack output is evidence, not a verdict. |
| "interrogate found nothing, skip OCR" | The OCR file pass is still required. |
| "interrogate called it Medium" | The parent maps severity on the OCR scale. Critical and High block. Only the human in this conversation waives. |
| "Inconclusive on the real surface" | Inconclusive or wrong-surface is not a pass. Record `Surface: none: <reason>`. |
| "The blast-radius writeup explains it" | An unproven load-bearing fact is a remaining gate in the description. Review must not write it closed. |
| "pstack is not installed, so proof is n/a" | The Proof record is required anyway. pstack only raises the ceiling. |
| "I will create the verify skill in this PR" | That is its own issue unless this issue asks for it. |
| "Never block on the human, I will waive it" | Waivers stay human-only. |

Scheduled runs never load pstack. They have no human to answer an `ask`, and multi-model fan-out is out of budget. Their Proof record says `pstack: off`.

### 4. Detection and fallback

Once per invocation, with no forge calls:

1. Invocation token. `pstack:off` means off. `pstack:required` means detection must succeed, otherwise stop before the first write and report the missing skills.
2. Runtime skill list. If the agent's available skills include `poteto-mode` or the specific hook skill, pstack is present. This signal is authoritative.
3. One filesystem probe. Look for a `.cursor-plugin/plugin.json` whose `name` is `pstack` in the runtime plugin cache (for example under `~/.cursor/plugins/`), or a `poteto-mode/SKILL.md` under a known skills directory (`~/.cursor/skills`, `${CLAUDE_HOME:-~/.claude}/skills`, `${CODEX_HOME:-~/.codex}/skills`, repo `.cursor/skills`). Read the version from `plugin.json` when present.
4. Otherwise pstack is absent.

- Each hook checks its own skill, so a partial or older install degrades one hook at a time.
- Many pstack skills set `disable-model-invocation: true`. Each hook therefore tells the agent to read that skill's `SKILL.md` in full, not to wait for auto-invocation.
- Use `poteto-agent` only when the runtime lists it. Otherwise use `generalPurpose`, or run inline when the runtime has no subagents.
- `interrogate` or `arena` with a single available model records `single-model` and claims no model diversity.
- Model choice follows the `/setup-pstack` rule (`~/.cursor/rules/pstack-models.mdc`). This skill does not pick models.

### 5. Word budget and load plan

| File | Change | Budget |
| --- | --- | --- |
| `SKILL.md` | None. Load-line sentences untouched | 0 net words (2998 / 3000 today) |
| `references/pstack.md` | New | 900 words or fewer, validator-enforced |
| `references/pre-submit.md` | Hook sentence plus Proof record section | +180 words or fewer |
| `references/plan-issue.md` | Hook sentence, optional `**Proof:**` brief line, observable-fork sentence | +90 words or fewer |
| `implement.md`, `review.md`, `revise.md`, `conflict.md` | One anchor sentence each at most | +40 words or fewer each |
| `prompts/*.md` | None. Prompts point at the home; pstack is reached through references | 0 |
| `README.md` | Optional pstack companion section; minimal implement profile note | Step 7 |

- `references/pstack.md` is read only when the mode is plan, implement, revise, conflict, or review, and detection says present and not off.
- Read a pstack leaf skill only at the hook that needs it. Never read the whole playbook directory. Never paste pstack text into forge comments or subagent prompts beyond pointers.
- The minimal implement profile keeps working without `references/pstack.md`. It is an optional add-on.

### 6. Non-goals

- **LOC chase.** Laziness Protocol and "write less code" are judgment aids, not metrics. No LOC targets, no diff-size gates, no rejecting a correct fix for size. The brief's 8-step cap stays as it is.
- **Auto-merge.** pstack Shipping, Autopilot-full, Autopilot-stack, Orchestrate, and overnight or autonomous merge are out. No step here touches merge. Any future opt-in is a separate umbrella that needs explicit operator opt-in per invocation and still goes through `/git-merge-approved` gates.
- Babysit polling loops and `watch-pr`. **Forge budget** forbids them.
- **Replacing `gentle-grill-me`.** Prototype only settles facts you can observe by running code. Product and preference calls stay with the grill and the human.
- Replacing the OCR file pass, `requesting-code-review`, or `verification-before-completion`.
- Making pstack required, except when the operator passes `pstack:required`.
- pstack in triage, scheduled lifecycle, scheduled merge, reply, request-review, status, or merge.
- Changing actor gates, force, reviewer policy, or the merge gate.
- Copying pstack text into this repo, or configuring pstack models.
- Editing consumer repos as part of this umbrella.

### 7. Consumer sync (no edits in those repos here)

- **Team2 `aal-git-collab-thin`.** If it vendors the minimal implement profile, it must pick up the step 2 Proof record in `references/pre-submit.md` to stay consistent. `references/pstack.md` is optional and self-contained: vendor it whole or not at all. Pin to the commit that closes step 7.
- **Team4 `poteto-dispatch`.** Stays a one-line wrapper. When it sends a git-collaboration mode to `poteto-agent`, this skill's precedence applies. It must not add its own Opening a PR or Babysit steps on top, which would produce a double PR body and polling. It passes `pstack:required` when the team wants a hard fail if pstack is absent.
- **Team4 `verifiable-delivery` 完成條件.** It can check the Proof record labels (`Proof:`, `Evidence class:`, `Surface:`, `Load-bearing fact:`, `pstack:`) in the PR/MR description instead of re-deriving them. The labels are fixed English so a checker can grep them. Renaming a label later is a breaking change for this consumer.

### 8. Ordered steps

Each step is one small PR/MR that keeps `python3 scripts/validate.py` green and can merge on its own, in order. Steps 3 to 6 depend only on steps 1 and 2 and may land in any order after them.

- [ ] Step 1: companion reference, detection, precedence ({{STEP1}})
- [ ] Step 2: pstack-neutral Proof record in the pre-submit gate, plus prove-it-works and verify-skill hooks ({{STEP2}})
- [ ] Step 3: `/git-plan-issue` hooks ({{STEP3}})
- [ ] Step 4: `/git-issue-pr` hooks and PR body layout ({{STEP4}})
- [ ] Step 5: `blast-radius` and `interrogate` in pre-submit and review, with no soft-pass ({{STEP5}})
- [ ] Step 6: revise and conflict hooks, plus Babysit/Shipping routing ({{STEP6}})
- [ ] Step 7: README, eval scenarios, consumer sync hand-off ({{STEP7}})

Recommended first step: Step 1. It carries no behavior change when pstack is absent, and every later step adds rows to its hook table.
