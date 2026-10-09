# Pre-submit gate

**REQUIRED SUB-SKILL:** `open-code-review-delegate` owns preview, rules, diffs, coverage, and finding shape. When pstack is present and not off, read `references/pstack.md`.

### File pass

After the actor gate and current-head checkout (or intended local submit range), run `open-code-review-delegate` on merge-base/target..head. Include uncommitted files only if in this submit. Pass issue brief, acceptance criteria, or PR/MR description with `--background`. Account for every `reviewable_files` entry as reviewed or skipped with a reason. Every changed file outside `reviewable_files` is unsupported by the tool: read its diff in this pass, name file and result on `Review tier:`, never silently. `0/N reviewable` alone is not a completed file pass. Missing `ocr`, failed `preview`/`rule`, or incomplete coverage fails the file pass.

### Pre-submit gate

Before push or PR/MR open/update on `/git-issue-pr`, `/git-revise-pr`, `/git-revise-pr-force`, `/git-fix-conflict`, and scheduled lifecycle source-branch push:

1. Finish `verification-before-completion`.
2. Run the file pass per **Review tier**. Full tier: dispatch the contract under **Full tier**. Light tier: the main session runs `open-code-review-delegate` on the same range; no subagent.
3. Critical and High findings are submit blockers until each is fixed in the tree or waived.
4. A waiver is valid only when the **human in this conversation** names path, issue, and reason. **Blanket ship language is not a waiver.** Unattended scheduled runs cannot waive.
5. Record each waiver in commit body or PR/MR description.
6. Only a Critical or High fix starts another file pass. Commit the fix; the pass covers the fix range, `<last reviewed SHA>..<new head>` plus callers the diff touches; recompute the tier on that range. Repeat until no unwaived Critical/High remain. A Medium/Low-only fix re-runs the tests, not the file pass.
7. Failed file pass, leftover unwaived Critical/High, missing waiver record or Proof record → do not push, do not open or update the PR/MR.

Medium/Low do not block submit.

### Review tier

- **Light tier**: submit range touches at most 3 files and at most 60 changed lines (`git diff --shortstat`), and no path is CI config/auth/security/secrets/schema/migration.
- **Full tier**: everything else, any unsure range. **Dispatch contract** (step 2; pre-agreed, do not ask when it matches):
  - **Grouping:** one fresh subagent per PR/MR (no implementer history) via `requesting-code-review`, never shared across MRs. A fix re-review is a new fresh subagent for the same PR/MR, one at a time.
  - **Purpose:** review only that MR's submit range (merge-base..head, or the step 6 fix range `<last reviewed SHA>..<new head>`) vs issue brief or acceptance criteria via `open-code-review-delegate`. Pass exact base and head SHAs matching Proof `Review tier:`, plus this contract; not this skill or forge snapshot.
  - **Budget:** read-only: only that diff and the call sites it touches; no commands other than `ocr` and git reads; no forge calls; no file edits, commits, or pushes.
  Outside it (cross-MR, parallel subagents, forge use, or edits): ask first.

Critical/High blocking and waivers are the same in both tiers. Scheduled runs always use the full tier.

### Proof record

Gate modes write it under `## Verification`, or in the update comment otherwise.

```
Proof: <command or skill> -> <observed result>
Evidence class: live job / real artifact bytes|executable unit tests|source-contract / regex tripwire|docs alignment
Surface: <verify skill and feature driven>|none: <reason>
Load-bearing fact: <fact> (level 1-5)|n/a
Review tier: <light|full> <base sha>..<head sha>[; <light|full> <sha>..<sha> ...][; unsupported: <file> <result>]
pstack: present [hooks]|absent|off
```

Evidence class values match `references/review.md`. Inconclusive or wrong-surface is not a pass. An unproven load-bearing fact is a remaining gate; do not close it. For user-visible output (video/image/audio/UI), the observed result names the content checked, frames viewed and what they showed. Output that only exists or is non-empty leaves it a remaining gate. User-visible change proven only by tests records `Surface: none: <reason>`.

### Optional observation

Under `## Verification`, outside the Proof record, PR/MR body may include:

```
Brief: followed|adjusted: <step ids>|dissent <comment id>
Executor-model: <id or unknown>
```

Missing line does not fail the pre-submit gate. Observation only, not a gate.

| Excuse | Reality |
| --- | --- |
| "I'll review the diff myself" | File pass is OCR coverage via `open-code-review-delegate`. Unsupported files are read manually. |
| "Tests passed so the diff is fine" | `verification-before-completion` is not the file pass. |
| "I'll waive this High finding" | Only the human in this conversation waives, with path + issue + reason. |
| "pstack is not installed, so proof is n/a" | The Proof record is required anyway. pstack only raises the ceiling. |
