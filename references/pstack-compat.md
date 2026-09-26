# pstack companion contract

contract-id: `pstack-compat-v1`

tested: `0.15.5`

supported: `>=0.14.0 <0.17.0`

Pin content is `0.15.5`. The supported range lives in this file, not in `.pstack-pin`. Leave `.pstack-pin` for fleet sync after this contract merges.

## Named skills

v1 named skills (pstack package only):

- poteto-mode
- how
- why
- architect
- arena
- blast-radius
- interrogate
- tdd
- technical-writing
- unslop
- no-comments
- create-verification-skill
- principle-prove-it-works
- principle-sequence-verifiable-units
- principle-attack-the-premise
- principle-fix-root-causes

## Agents

- poteto-agent

## Dynamic skills

`verify-<app>` is dynamic. Enable that hook only when the skill exists. It is not a fixed probe and it is not on the v1 named list.

## Not probed

Not probed by this contract:

- `/deslop` (cursor-team-kit)
- `verification-before-completion` (superpowers)

## Upgrade checklist

1. Read the local or fleet pstack `plugin.json` version.
2. Inside supported: may only bump `.pstack-pin`. Recheck that the v1 named skills are still present.
3. Outside supported: Detection treats the install as unsupported. To widen the range, edit this file in a tip PR first, then bump the pin.
4. git-collab-only bump: check the companion and compat diff; if contract unchanged, OK to merge.

## Vendor

Do not vendor pstack into this repo.
