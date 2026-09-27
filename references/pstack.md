# pstack companion

Optional. git-collaboration owns forge gates and wins on conflict; pstack owns engineering rigor.

## Detection

Once per invocation, no forge call. `pstack:off` turns it off. Present when the runtime skill list names a skill from `references/pstack-compat.md`, else when one probe finds `poteto-mode/SKILL.md` or a `pstack` `plugin.json`. `pstack:required` with pstack absent: stop before the first write and name what is missing.

A hook whose skill is unavailable records `missing:<name>`. Load a hook's skill only when its trigger fires; never preload pstack skills.

## Precedence

- Autonomy never waives human-only waivers, the grill, reviewer selection, or dissent-then-wait.
- pstack never writes to the forge and runs no forge command; **Forge budget** applies.
- A delegate gets file pointers and the brief, never the forge snapshot, and makes no forge call. The parent reviews the diff before commit.
- With an Execution plan, record `how` and `architect` as `skip: brief is the work order`.
- Markers and fixed labels stay verbatim under `unslop` and `technical-writing`.
- pstack Babysit and Shipping never run under this skill.

## Hooks

Without pstack, each step runs as its mode reference says.

- Plan 3: `how` across subsystems; `why` for the introducing commit.
- Plan 5: `blast-radius` for a shared contract, schema, or config default. Handoff profile only: `architect` and **principle-sequence-verifiable-units**.
- Plan 5, Decision-card profile: record `skip: decision card` for `architect` and **principle-sequence-verifiable-units**; not a silent-skip failure.
- Plan 6: Prototype playbook for a fork observable by running code.
- Implement 10–11: bug fix uses `tdd` when cheap.
- Pre-submit: **principle-prove-it-works** fills `Proof:` from a real run; `verify-<app>` fills `Surface:`.
- Pre-submit and review: `blast-radius` when the diff changes a public signature, schema, wire shape, config default, or auth, security, or deletion path. `interrogate` when a dissent was settled by a third way, `arena` was used for this change, a thorough-review trigger fires, or the user asks. Both are readonly and use local git only.
- Revise: a second fix for the same blocker triggers **principle-attack-the-premise**; a CI fix follows **principle-fix-root-causes**.
- Conflict: run a drift sweep for target callers of symbols the source deletes, renames, or re-signs. Record the sweep result in the Proof record.

A hit trigger runs its hook or the Proof record says `skip: <reason>`. A silent skip fails the pre-submit gate. OCR is never replaced; pstack output is evidence, not a verdict, mapped to the OCR severity scale. Critical and High block. No auto-apply. No `arena` in review.

**Prose.** Default off; not in the default required set. `technical-writing`, `unslop`, `/deslop`, `/no-comments` run only for `pstack:prose`, an ask to fix prose/copy, or equivalent opt-in. Without opt-in, missing Prose is not a silent-skip failure.
