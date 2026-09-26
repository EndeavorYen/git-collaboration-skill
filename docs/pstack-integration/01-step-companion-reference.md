# pstack integ step 1: add references/pstack.md with detection, precedence, and hook points

## Problem

Nothing in this skill says what to do when pstack is loaded next to it. `SKILL.md` has 2 words of headroom (2998 / 3000), so the integration cannot live there. Every later step needs one home for detection, precedence, and hook rows, and that home must not load for merge, triage, or scheduled work.

## Proposal

Add `references/pstack.md` with these sections and no mode-specific hook rows yet. Steps 2 to 6 each add their own rows, so nothing points at behavior that has not landed.

1. **Detection.** Once per invocation, with no forge call:
   - `pstack:off` in the invocation turns pstack off.
   - `pstack:required` means detection must succeed. Otherwise stop before the first write and report which skills are missing.
   - If the runtime skill list includes `poteto-mode` or the hook's skill, pstack is present.
   - Otherwise run one filesystem probe: a `.cursor-plugin/plugin.json` with `name` `pstack` in the runtime plugin cache, or a `poteto-mode/SKILL.md` under a known skills directory. Read the version when `plugin.json` has one.
   - Per-hook granularity: a missing leaf skill disables only that hook.
   - pstack skills often set `disable-model-invocation: true`, so a hook says "read the `<name>` skill in full".
2. **Precedence.** git-collaboration wins on conflict. List the named cases from the umbrella:
   - Autonomy does not waive human-only waivers, the grill, reviewer selection, or dissent-then-wait.
   - pstack forge commands do not run. Forge calls come only from the forge reference.
   - `why` and `blast-radius` use local git and the existing snapshot only.
   - A brief with an Execution plan is the work order.
   - pstack subagents never write to the forge and never receive the snapshot.
   - Marker lines and fixed labels are exempt from prose rewrites.
3. **Subagents and models.** Use `poteto-agent` only when listed, otherwise `generalPurpose` or inline. Multi-model hooks with one model record `single-model`. Models come from the `/setup-pstack` rule, not from this skill.
4. **Hook table.** Header row only: `Mode / step | pstack skill | Runs when | Evidence | Fallback`.
5. **Record line.** `pstack: present <version> [hooks run] | absent | off`, used later by the Proof record.

Add one hook sentence each to `references/pre-submit.md` and `references/plan-issue.md`: read `references/pstack.md` only when detection says present and not off. Other modes do not reference it.

## Acceptance criteria

- [ ] `references/pstack.md` exists with Detection, Precedence, Subagents and models, Hook table, and Record line sections, and is 900 words or fewer.
- [ ] Detection lists `pstack:off`, `pstack:required`, runtime skill list, and one filesystem probe in that order, and says it makes no forge call.
- [ ] `pstack:required` with pstack absent stops before the first write and names the missing skills.
- [ ] Precedence lists all six named conflict cases from the umbrella and states that git-collaboration wins.
- [ ] `references/pre-submit.md` and `references/plan-issue.md` each gain exactly one conditional hook sentence naming `references/pstack.md`.
- [ ] `SKILL.md` word count does not increase, and the five `LOAD_LINES` sentences in `scripts/validate.py` are unchanged.
- [ ] `scripts/validate.py` adds `references/pstack.md` to `REQUIRED_FILES`, adds `REFERENCE_PHRASES` for it (at least `pstack:off`, `pstack:required`, `git-collaboration wins`, `never writes to the forge`, `Forge budget`), enforces a 900-word cap on it, and fails when `references/pstack.md` appears in the merge, scheduled, or triage load lines or in `prompts/git-merge-approved*.md`, `prompts/git-scheduled-*.md`, `prompts/git-triage.md`, `prompts/git-reply-issue.md`, `prompts/git-request-review.md`, or `prompts/git-pr-status.md`.
- [ ] `python3 scripts/validate.py` passes.
- [ ] The PR description shows that with pstack absent, the pre-submit and plan-issue text reads exactly as before apart from the conditional hook sentence.

## Out of scope

- Any mode-specific hook row (steps 2 to 6).
- The Proof record (step 2).
- README changes (step 7).

## Depends on

- Umbrella: {{UMBRELLA}}
