# Pre-submit gate

Read this file for the file pass and the waiver rules. Review reads it with `references/review.md`. Implement, revise, and conflict read it before a source-branch push. Scheduled lifecycle keeps its unattended override in `references/scheduled-automation.md`. When detection says pstack is present and not off, read `references/pstack.md`.

## Structured file review

**REQUIRED SUB-SKILL:** `open-code-review-delegate` owns preview, rules, diffs, coverage, and finding shape. **REQUIRED SUB-SKILL for pre-submit:** `requesting-code-review` owns dispatching a **fresh subagent** with no implementer history; that reviewer runs `open-code-review-delegate`. This skill owns when to call them, how findings map onto forge comments, and the pre-submit gate.

### File pass

After the actor gate and a current-head checkout (or the intended local submit range):

1. Run `open-code-review-delegate` for the merge-base / target..head range. Include uncommitted files only when they are part of this submit.
2. Pass the issue brief, acceptance criteria, or PR/MR description with `--background`.
3. Account for every `reviewable_files` entry as reviewed or skipped with a reason.

Missing `ocr`, failed `preview`/`rule`, or incomplete coverage is a failed file pass.

### Pre-submit gate

Applies before push and before opening or updating a PR/MR on `/git-issue-pr`, `/git-revise-pr`, `/git-revise-pr-force`, `/git-fix-conflict`, and scheduled lifecycle source-branch push.

1. Finish `verification-before-completion` for tests and claimed validation.
2. Dispatch a fresh subagent through `requesting-code-review`. That reviewer runs `open-code-review-delegate` on the intended submit range. Pass the range and the contract, not this skill and not the forge snapshot.
3. Critical and High findings are submit blockers until each is fixed in the tree or waived.
4. A waiver is valid only when the **human in this conversation** names the path, the issue, and a reason. **Blanket ship language is not a waiver.** The agent does not waive. Unattended scheduled runs have no human in the conversation, so they cannot waive.
5. Record each waiver in the commit body or PR/MR description.
6. After fixes, run the file pass again on the new range until no unwaived Critical/High remain.
7. A failed file pass, leftover unwaived Critical/High, or a missing waiver record → do not push, do not open or update the PR/MR.

Medium and Low do not block submit. Mention them in the PR/MR description when useful.

| Excuse | Reality |
| --- | --- |
| "I'll review the diff myself" | File pass is OCR coverage via `open-code-review-delegate`. |
| "ocr isn't installed, skip review" | Missing `ocr` is a failed file pass. |
| "Tests passed so the diff is fine" | `verification-before-completion` is not the file pass. |
| "I'll waive this High finding" | Only the human in this conversation waives, with path + issue + reason. |
| "Ship it / LGTM" | Blanket ship language is not a waiver. |
| "I wrote this code, I know it's correct" | Pre-submit uses a fresh subagent. |
| "Scheduled run, no one to waive, push anyway" | Unattended runs cannot waive; leftover Critical/High stops the push. |
