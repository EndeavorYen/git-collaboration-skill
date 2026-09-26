# pstack integ step 7: README, eval scenarios, and consumer sync hand-off

## Problem

After steps 1 to 6, the integration exists only in references. Installers do not know pstack is an optional companion or what `pstack:off` and `pstack:required` do. The minimal implement profile does not say whether `references/pstack.md` belongs in it. `scripts/validate.py` checks text, not behavior. Consumers (Team2 `aal-git-collab-thin`, Team4 `poteto-dispatch` and `verifiable-delivery`) need a pinned commit and the final Proof record labels.

## Proposal

1. Add a short **Optional pstack companion** section to `README.md`:
   - pstack is optional.
   - How detection works, and what `pstack:off` and `pstack:required` do.
   - git-collaboration gates win on conflict.
   - pstack never merges and never polls the forge here.
   - Add `references/pstack.md` to the Layout block.
2. **Minimal implement profile.** Add `references/pstack.md` as an optional add-on. The profile works without it. When vendored, it is vendored whole.
3. **Eval scenarios.** Following pstack's Eval playbook when available, run this matrix and record each result in the PR description:

   | # | Scenario | Expected |
   | --- | --- | --- |
   | E1 | pstack absent, `/git-issue-pr` with a settled brief | Same steps as before; Proof record says `pstack: absent`; `references/pstack.md` not read |
   | E2 | pstack present, bug issue with an Execution plan | Reproduce first; `how` / `architect` recorded as `skip: brief is the work order`; PR has Proof record |
   | E3 | pstack present, `pstack:off` | Same as E1 with `pstack: off` |
   | E4 | pstack absent, `pstack:required` | Stops before the first write and names the missing skills |
   | E5 | GitLab MR, `/git-revise-pr` with pstack present | Only `glab` forge calls; no `gh`, `origin`, or `watch-pr` |
   | E6 | `/git-review-pr` on a PR that renames an exported symbol | `blast-radius` runs or records `skip: <reason>`; verdict names the ladder level |
   | E7 | `/git-merge-approved` with pstack present | `references/pstack.md` not read; merge gate unchanged |
   | E8 | Scheduled lifecycle with pstack present | pstack not loaded; Proof record says `pstack: off` |

4. **Consumer hand-off.** Post one comment on the umbrella issue with the commit SHA consumers should pin, the five final Proof record labels, and the sync notes from the umbrella's Consumer sync section. Do not edit consumer repos.

## Acceptance criteria

- [ ] `README.md` has an Optional pstack companion section that covers optional install, detection, `pstack:off`, `pstack:required`, gates-win precedence, and no merge / no forge polling.
- [ ] The `README.md` Layout block lists `references/pstack.md`.
- [ ] The Minimal implement profile lists `references/pstack.md` as optional and says the profile works without it. Every existing README phrase checked by `validate_implement_profile` still matches.
- [ ] The PR description has the E1 to E8 matrix with an observed result for each row. Any row that could not be run says why.
- [ ] `scripts/validate.py` asserts `pstack:off`, `pstack:required`, and `references/pstack.md` in `README.md`.
- [ ] The umbrella issue has a consumer hand-off comment with the pin SHA and the five Proof record labels.
- [ ] `SKILL.md` word count does not increase, and `python3 scripts/validate.py` passes.

## Out of scope

- Editing `aal-git-collab-thin`, `poteto-dispatch`, or `verifiable-delivery`.
- Automated behavior tests beyond the validator.
- Any opt-in merge or autopilot work (explicit non-goal in the umbrella).

## Depends on

- Umbrella: {{UMBRELLA}}
- Steps 1 to 6: {{STEP1}}, {{STEP2}}, {{STEP3}}, {{STEP4}}, {{STEP5}}, {{STEP6}}
