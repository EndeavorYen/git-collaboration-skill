# Pre-submit gate

Read this file for the file pass and the waiver rules. Review reads it with `references/review.md`. Implement, revise, and conflict read it before a source-branch push. Scheduled lifecycle keeps its unattended override in `references/scheduled-automation.md`. When detection says pstack is present and not off, read `references/pstack.md`.

## Structured file review

**REQUIRED SUB-SKILL:** `open-code-review-delegate` owns preview, rules, diffs, coverage, and finding shape. **REQUIRED SUB-SKILL for a full-tier pre-submit:** `requesting-code-review` owns dispatching a **fresh subagent** with no implementer history; that reviewer runs `open-code-review-delegate`. This skill owns when to call them, how findings map onto forge comments, and the pre-submit gate.

### File pass

After the actor gate and a current-head checkout (or the intended local submit range):

1. Run `open-code-review-delegate` for the merge-base / target..head range. Include uncommitted files only when they are part of this submit.
2. Pass the issue brief, acceptance criteria, or PR/MR description with `--background`.
3. Account for every `reviewable_files` entry as reviewed or skipped with a reason.

Missing `ocr`, failed `preview`/`rule`, or incomplete coverage is a failed file pass.

### Pre-submit gate

Applies before push and before opening or updating a PR/MR on `/git-issue-pr`, `/git-revise-pr`, `/git-revise-pr-force`, `/git-fix-conflict`, and scheduled lifecycle source-branch push.

1. Finish `verification-before-completion` for tests and claimed validation.
2. Run the file pass at the tier from **Review tier**. Full tier: dispatch a fresh subagent through `requesting-code-review`; that reviewer runs `open-code-review-delegate` on the intended submit range. Pass the range and the contract, not this skill and not the forge snapshot. Light tier: the parent runs `open-code-review-delegate` inline on the same range.
3. Critical and High findings are submit blockers until each is fixed in the tree or waived.
4. A waiver is valid only when the **human in this conversation** names the path, the issue, and a reason. **Blanket ship language is not a waiver.** The agent does not waive. Unattended scheduled runs have no human in the conversation, so they cannot waive.
5. Record each waiver in the commit body or PR/MR description.
6. Only a Critical or High fix starts another file pass. Commit the fix; the pass covers the fix range, `<last reviewed SHA>..<new head>` plus callers that diff touches; recompute the tier on that range. Repeat until no unwaived Critical/High remain. A Medium/Low-only fix re-runs the tests, not the file pass.
7. A failed file pass, leftover unwaived Critical/High, a missing waiver record, or a missing Proof record → do not push, do not open or update the PR/MR.

Medium and Low do not block submit.

### Review tier

- **Light tier**: the submit range touches at most 3 files and at most 60 changed lines (`git diff --shortstat`), and no path is CI config, auth, security, secrets, schema, or migration.
- **Full tier**: everything else, and any unsure range.

Critical/High blocking and the waiver rules are the same in both tiers. Scheduled runs always use the full tier.

### Proof record

The gate modes above write this record under `## Verification`, or in the update comment otherwise.

```
Proof: <command or skill run> -> <observed result>
Evidence class: live job / real artifact bytes | executable unit tests | source-contract / regex tripwire | docs alignment
Surface: <verify skill and feature driven> | none: <reason>
Load-bearing fact: <fact> (level 1-5) | n/a
Review tier: <light|full> <range>[; <light|full> <range> ...]
pstack: present [hooks] | absent | off
```

Evidence class values match `references/review.md`. Inconclusive or wrong-surface is not a pass. An unproven load-bearing fact is a remaining gate; do not write it closed. For a user-visible output (video, image, audio, UI), the observed result names the content checked, such as frames viewed and what they showed. An output that only exists or is non-empty leaves that fact a remaining gate. A user-visible change proven only by tests records `Surface: none: <reason>`.

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
