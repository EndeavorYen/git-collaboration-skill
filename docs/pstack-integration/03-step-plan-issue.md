# pstack integ step 3: pstack hooks for /git-plan-issue

## Problem

`/git-plan-issue` writes an Executor-ready brief for a possibly weaker executor. The quality of Root cause, Recommended change, and Stop and dissent when depends on how deeply the planner investigated. pstack has the tools for that (`how`, `why`, `architect`, `arena`, `blast-radius`, **principle-sequence-verifiable-units**, the Prototype playbook), but the planner does not know when to use them.

Two more gaps:

- The planner sometimes sends a fork to `gentle-grill-me` when running code would answer it. For example: which of two payloads the API returns today, or whether an option changes output.
- The brief does not tell the executor what real-surface proof counts as done, so step 2's Proof record gets filled after the fact.

## Proposal

1. Add plan rows to `references/pstack.md`:

   | Plan step | pstack skill | Runs when | Evidence in the brief |
   | --- | --- | --- | --- |
   | Step 3 inspect | `how` | The change spans more than one subsystem | Root cause cites `file:line` |
   | Step 3 inspect | `why` (local `git log` / `git blame` and the snapshot only) | The issue is a regression | Root cause names the introducing commit |
   | Step 5 Recommended change | `architect`; `arena` when two or more valid shapes exist | The change crosses a function boundary | The rejected-alternative line names a real candidate |
   | Step 5 Stop and dissent when | `blast-radius` load-bearing fact | Shared contract, wire format, schema, or config default | That fact is a checkable Stop and dissent line |
   | Step 5 Execution plan | **principle-sequence-verifiable-units** | Always when present | Each step ends in Verify (existing rule) |
   | Step 6 before the grill | Prototype playbook | A fork whose answer can be observed by running code | The run result is cited in Root cause or Recommended change |

2. In `references/plan-issue.md` step 6, add one pstack-neutral sentence: a fork whose answer can be observed by running code is settled by a recorded local run (pstack's Prototype playbook, or an equivalent script), not by the grill. Product and preference choices still load `gentle-grill-me`. Existing grill sentences stay word for word.
3. Add one optional recipe line after `**Tests:**`: `**Proof:** <verify skill and feature to drive, or command> | tests only: <reason>`. It tells the executor what real-surface proof step 2's Proof record expects.
4. pstack artifacts (arena directories, `how` writeups, prototype code) are never pasted into the brief. The brief keeps every Executor-ready rule, including no function bodies and the 8-step cap.

## Acceptance criteria

- [ ] `references/pstack.md` has the six plan rows above, each with trigger, evidence, and fallback ("current step N").
- [ ] `why` in that table is limited to local git and the existing snapshot, with no forge or MCP query.
- [ ] `references/plan-issue.md` step 6 has the observable-fork sentence, and every existing `REFERENCE_PHRASES` entry for `plan-issue.md` still matches.
- [ ] The brief recipe has an optional `**Proof:**` line, and the Executor-ready rules say when `tests only: <reason>` is allowed (no user-visible surface).
- [ ] `references/plan-issue.md` states that pstack artifacts are not pasted into the brief.
- [ ] `prompts/git-plan-issue.md` still does not name `references/pre-submit.md`, and `references/plan-issue.md` does not name it outside the existing "Do not read" sentence.
- [ ] `scripts/validate.py` asserts `**Proof:**` and the observable-fork sentence in `references/plan-issue.md`.
- [ ] `SKILL.md` word count does not increase, and `python3 scripts/validate.py` passes.

## Out of scope

- Changing what counts as an unsettled product decision for product or preference forks.
- Changing `gentle-grill-me` itself.
- Implement behavior (step 4).

## Depends on

- Umbrella: {{UMBRELLA}}
- Step 1: {{STEP1}}
- Step 2: {{STEP2}} (the `**Proof:**` line feeds the Proof record)
