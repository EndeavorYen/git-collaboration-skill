# Pre-submit gate

This file holds the file pass and the waiver rules. Implement, revise, and conflict read it before a source-branch push. Review reads it too. When detection says pstack is present and not off, read `references/pstack.md`.

### File pass

After the actor gate and a current-head checkout (or the intended local submit range), run `open-code-review-delegate` for the merge-base / target..head range. Include uncommitted files only when they are part of this submit. Pass the issue brief, acceptance criteria, or PR/MR description with `--background`. Account for every `reviewable_files` entry as reviewed or skipped with a reason. Missing `ocr`, failed `preview`/`rule`, or incomplete coverage is a failed file pass.

### Pre-submit gate

Before push or a PR/MR open/update on `/git-issue-pr`, `/git-revise-pr`, `/git-revise-pr-force`, `/git-fix-conflict`, and scheduled lifecycle source-branch push:

1. Finish `verification-before-completion`.
2. Run the file pass at the tier from **Review tier**. Full tier: dispatch the contract under **Full tier**. Light tier: the main session runs `open-code-review-delegate` on the same range; no subagent.
3. Critical and High findings are submit blockers until each is fixed in the tree or waived.
4. A waiver is valid only when the **human in this conversation** names the path, the issue, and a reason. **Blanket ship language is not a waiver.** The agent does not waive. Unattended scheduled runs have no human in the conversation, so they cannot waive.
5. Record each waiver in the commit body or PR/MR description.
6. Only a Critical or High fix starts another file pass. Commit the fix; the pass covers the fix range, `<last reviewed SHA>..<new head>` plus callers that diff touches; recompute the tier on that range. A Medium/Low-only fix re-runs the tests, not the file pass.
7. A failed file pass, leftover unwaived Critical/High, a missing waiver record, or a missing Proof record → do not push, do not open or update the PR/MR.

Medium and Low do not block submit.

### Review tier

- **Light tier**: the submit range touches at most 3 files and at most 60 changed lines (`git diff --shortstat`), and no path is CI config, auth, security, secrets, schema, or migration.
- **Full tier**: everything else, and any unsure range. **Dispatch contract** (step 2; pre-agreed, so do not ask when it matches):
  - **Grouping:** one fresh subagent per PR/MR (no implementer history) through `requesting-code-review`, never shared across MRs. A fix re-review is a new fresh subagent for the same PR/MR, one at a time.
  - **Purpose:** review only that MR's submit range (merge-base..head, or the step 6 fix range `<last reviewed SHA>..<new head>`) against the issue brief or acceptance criteria, running `open-code-review-delegate`. Pass the exact base and head SHAs, matching the Proof record's `Review tier:` line, and this contract; not this skill or the forge snapshot.
  - **Budget:** read-only: only that diff and the call sites it touches; no commands other than `ocr` and git reads; no forge calls; no file edits, commits, or pushes.
  Outside it (cross-MR, several subagents in parallel, forge use, or edits): ask first.

Critical/High blocking and the waiver rules are the same in both tiers. Scheduled runs always use the full tier.

### Proof record

The gate modes above write this record under `## Verification`.

```
Proof: <command or skill run> -> <observed result>
Evidence class: live job / real artifact bytes | executable unit tests | source-contract / regex tripwire | docs alignment
Surface: <verify skill and feature driven> | none: <reason>
Load-bearing fact: <fact> (level 1-5) | n/a
Review tier: <light|full> <base sha>..<head sha>[; <light|full> <sha>..<sha> ...]
pstack: present [hooks] | absent | off
```

Inconclusive or wrong-surface is not a pass. An unproven load-bearing fact is a remaining gate; do not write it closed. For a user-visible output (video, image, audio, UI), the observed result names the content checked, frames viewed and what they showed. An output that only exists or is non-empty leaves that fact a remaining gate. A user-visible change proven only by tests records `Surface: none: <reason>`.

### Optional observation

Under `## Verification`, outside the Proof record, the PR/MR body may include:

```
Brief: followed | adjusted: <step ids> | dissent <comment id>
Executor-model: <id or unknown>
```

Observation only, not a gate. A missing line does not fail the pre-submit gate.

| Excuse | Reality |
| --- | --- |
| "I'll review the diff myself" | File pass is OCR coverage via `open-code-review-delegate`. |
| "Tests passed so the diff is fine" | `verification-before-completion` is not the file pass. |
| "I'll waive this High finding" | Only the human in this conversation waives, with path + issue + reason. |
| "pstack is not installed, so proof is n/a" | The Proof record is required anyway. pstack only raises the ceiling. |
