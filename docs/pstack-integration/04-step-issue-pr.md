# pstack integ step 4: pstack hooks for /git-issue-pr and the PR/MR body

## Problem

With `/poteto-mode` active, `/git-issue-pr` runs two routers:

- poteto-mode copies the Feature, Bug fix, or Refactoring playbook steps into the todo list, runs `how` and `architect`, delegates to `poteto-agent`, then runs Opening a PR with its own `gh` / `origin` calls and its own PR body sections.
- `references/implement.md` says the brief's Execution plan is the work order, enforces the read-then-write gate, and owns the PR/MR create, update, and read-back.

The result is redesign against a settled brief, a second forge client, a PR body missing required fields, and no clear stop condition.

## Proposal

1. Add implement rows to `references/pstack.md`:
   - **Playbook by issue kind.** Bug uses Bug fix steps 1, 2, 4, and 5 (reproduce, root cause, verify on the same surface, failing repro committed before the fix) plus `tdd` when the test path is cheap. Feature uses Feature steps 4 to 6. Refactoring uses Refactoring step 1 (pin behavior) and step 6 (prove unchanged).
   - **Brief overrides redesign.** With an Execution plan, the playbook's `how`, `architect`, and `arena` steps are recorded as `skip: brief is the work order`. Without an Execution plan, they may run.
   - **Todo order.** `references/implement.md` steps are the outer list. Playbook steps nest under implement steps 10 and 11. The playbook's "Run Opening a PR" is replaced by implement steps 12 to 16.
   - **Delegation.** A `poteto-agent` code delegate is allowed. It gets file pointers and the brief, never the forge snapshot, and makes no forge call. Dispatching a delegate whose first action writes the failing test satisfies the read-then-write gate. The parent reviews the diff before commit.
   - **Prose.** When installed, run `technical-writing` and `unslop` on the PR/MR body and commit body, and `/deslop` and `/no-comments` on the diff, before the pre-submit gate. Marker lines and fixed labels stay verbatim.
   - **PR/MR body layout.** pstack's `## Why`, `## Scope`, `## Tradeoffs`, `## Blast Radius`, `## Verification` may be the layout. The fields this skill requires still appear: issue link, each brief Test case id and result, the Proof record under `## Verification`, known limitations, reviewer and assignee metadata, and pre-submit waivers.
   - **No pstack forge path.** No `gh` / `origin` from Opening a PR, no Babysit after opening, no merge. The stop condition is unchanged.
2. In `references/implement.md` step 10, add one anchor sentence: when `references/pstack.md` is loaded, apply its implement rows inside this step without adding, redesigning, or skipping brief steps.

## Acceptance criteria

- [ ] `references/pstack.md` has implement rows for playbook-by-kind, brief-overrides-redesign, todo order, delegation, prose, PR/MR body layout, and no pstack forge path.
- [ ] The rows state that with an Execution plan, `how`, `architect`, and `arena` are recorded as `skip: brief is the work order`.
- [ ] The rows state that a code delegate gets no forge snapshot and makes no forge call, and that the parent reviews the diff.
- [ ] The PR/MR body rule lists every field `references/implement.md` step 15 already requires, plus the Proof record.
- [ ] `references/implement.md` step 10 has one anchor sentence, and every existing `REFERENCE_PHRASES` entry for `implement.md` still matches.
- [ ] `prompts/git-issue-pr.md` is unchanged and still does not name merge, review, triage, or scheduled references.
- [ ] `scripts/validate.py` asserts `skip: brief is the work order` and the no-forge-call delegate rule in `references/pstack.md`.
- [ ] `SKILL.md` word count does not increase, and `python3 scripts/validate.py` passes.

## Out of scope

- `blast-radius` and `interrogate` in the pre-submit gate (step 5).
- Babysit, Shipping, and any merge path.
- Changing the read-then-write gate or the 8-step brief cap.

## Depends on

- Umbrella: {{UMBRELLA}}
- Step 1: {{STEP1}}
- Step 2: {{STEP2}}
