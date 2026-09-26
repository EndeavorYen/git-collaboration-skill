# pstack integ step 5: blast-radius and interrogate in pre-submit and review, without soft-pass

## Problem

The OCR file pass reviews the diff file by file. It does not look for breakage outside the diff, such as a caller in another package, a JSON consumer, or a config default another service reads. It is also one model's view.

pstack's `blast-radius` finds the one load-bearing fact and proves it by running code. `interrogate` runs a multi-model adversarial review. Neither is wired in. If they were wired in loosely, two soft-pass risks appear:

- A clean pstack writeup gets treated as a pass.
- An "optional" hook quietly never runs.

## Proposal

1. **Deterministic triggers** in `references/pstack.md`:
   - `blast-radius` runs when the diff changes an exported or public signature, a schema or migration, a wire or JSON payload shape, a config default or CLI flag, or auth, security, or data-deletion paths, deletes or renames a symbol used from another module, or when the user asks for blast radius.
   - `interrogate` runs when a dissent was settled by a third way, `arena` was used for this change, a thorough-review trigger from `references/review.md` is present, or the user asks for interrogate or adversarial review.
   - With pstack present and a trigger hit, the hook runs, or the Proof record says `skip: <reason>`. A silent skip fails the pre-submit gate.
2. **Order and isolation.** The fresh-subagent OCR file pass runs first and stays required. `interrogate` is additive. Its reviewers are readonly and get the submit range, the stated intent, and the contract, never the forge snapshot. Rerun `interrogate` only when an earlier run produced Critical or High and the range changed.
3. **Severity mapping.** The parent maps each `blast-radius` risk and `interrogate` finding onto the OCR scale:
   - In pre-submit, Critical and High are submit blockers with the existing human-only waiver.
   - In `/git-review-pr`, the existing mapping table turns them into blocking inline discussions or follow-up comments.
   - Consensus from two or more models is noted as higher signal. It does not replace the parent's severity call.
4. **Evidence class to ladder.** In `references/review.md`:
   - Map `blast-radius` levels onto Evidence class: 5 is live job / real artifact bytes, 4 is executable unit tests, 2 and 3 are source-contract / regex tripwire, 1 is no evidence.
   - An unproven load-bearing fact is a remaining gate. Approve must not write it as closed.
   - Fill `Load-bearing fact:` in the Proof record with the fact and its level.
5. **Review stays read-only.** No auto-apply from `interrogate`. OCR Step 7 Fix stays off. No `arena` in review.
6. Add the remaining umbrella excuse rows to `references/pre-submit.md`: "pstack says it is fine", "interrogate found nothing, skip OCR", "interrogate called it Medium", and "The blast-radius writeup explains it".

## Acceptance criteria

- [ ] `references/pstack.md` lists the `blast-radius` and `interrogate` trigger conditions above as concrete, checkable conditions.
- [ ] The text states that a trigger hit with pstack present either runs the hook or records `skip: <reason>`, and that a silent skip fails the pre-submit gate.
- [ ] The text states that the OCR file pass runs first and is never replaced, and that `interrogate` reviewers are readonly and receive no forge snapshot.
- [ ] Findings from both skills map onto Critical / High / Medium / Low. Critical and High block pre-submit with the human-only waiver unchanged.
- [ ] `references/review.md` maps ladder levels 1 to 5 onto the existing Evidence class names, and states that an unproven load-bearing fact is a remaining gate.
- [ ] `references/review.md` still contains "OCR Step 7 Fix stays off" and every existing `REFERENCE_PHRASES` entry.
- [ ] `references/pre-submit.md` excuse table has the four new rows.
- [ ] `scripts/validate.py` asserts the silent-skip rule and the "remaining gate" ladder rule.
- [ ] `SKILL.md` word count does not increase, and `python3 scripts/validate.py` passes.

## Out of scope

- Auto-applying fixes from `interrogate` or `blast-radius`.
- A new severity scale.
- `swarm` verification lanes and Shipping-style per-PR verdicts.

## Depends on

- Umbrella: {{UMBRELLA}}
- Step 1: {{STEP1}}
- Step 2: {{STEP2}}
