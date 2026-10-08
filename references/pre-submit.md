# Pre-submit gate

File pass and waivers. Implement, revise, and conflict read this before a source-branch push. Scheduled lifecycle's unattended override is in `references/scheduled-automation.md`. When pstack is present and not off, read `references/pstack.md`.

## Structured file review

**REQUIRED SUB-SKILL:** `open-code-review-delegate` owns preview, rules, diffs, coverage, and finding shape. Full tier also uses `requesting-code-review` per the dispatch contract below. This skill owns when to call them, how findings map onto forge comments, and the pre-submit gate.

### File pass

After the actor gate, on the current head or the intended submit range:

1. Run `open-code-review-delegate` on merge-base..head. Include uncommitted files only if part of this submit.
2. Pass the issue brief, acceptance criteria, or PR/MR description with `--background`.
3. Account for every `reviewable_files` entry as reviewed or skipped with a reason.

Missing `ocr`, failed `preview`/`rule`, or incomplete coverage is a failed file pass.

### Pre-submit gate

Applies before push and before opening or updating a PR/MR on `/git-issue-pr`, `/git-revise-pr`, `/git-revise-pr-force`, `/git-fix-conflict`, and scheduled lifecycle source-branch push.

1. Finish `verification-before-completion` for tests and claimed validation.
2. Run the file pass at the tier from **Review tier**. Full tier: dispatch the contract under **Full tier** and do not ask when it matches. Light tier: review in the main session; no subagent.
3. Critical and High findings are submit blockers until each is fixed in the tree or waived.
4. A waiver is valid only when the **human in this conversation** names the path, the issue, and a reason. **Blanket ship language is not a waiver.** The agent does not waive. Unattended runs cannot waive.
5. Record each waiver in the commit body or PR/MR description.
6. Only a Critical or High fix starts another file pass. Commit the fix; the pass covers the fix range, `<last reviewed SHA>..<new head>` plus callers that diff touches; recompute the tier on that range. Repeat until no unwaived Critical/High remain. A Medium/Low-only fix re-runs the tests, not the file pass.
7. A failed file pass, leftover unwaived Critical/High, a missing waiver record, or a missing Proof record → do not push, do not open or update the PR/MR.

Medium and Low do not block submit.

### Review tier

- **Light tier**: the submit range touches at most 3 files and at most 60 changed lines (`git diff --shortstat`), and no path is CI config, auth, security, secrets, schema, or migration.
- **Full tier**: everything else, and any unsure range. **Dispatch contract** (step 2; pre-agreed, so do not ask when it matches):
  - **Grouping:** one fresh subagent per PR/MR through `requesting-code-review`, never shared across MRs.
  - **Purpose:** review only that MR's submit range (merge-base..head) against the issue brief or acceptance criteria, running `open-code-review-delegate`. Pass the range and this contract, not this skill or the forge snapshot.
  - **Budget:** only that diff and the call sites it touches; no forge calls; no file edits, commits, or pushes.
  Outside it (cross-MR, several subagents in parallel, forge use, or edits): ask first.

Blocking and waivers are the same in both tiers. Scheduled runs always use the full tier.

### Proof record

Write this record under `## Verification`, or in the update comment otherwise.

```
Proof: <command or skill run> -> <observed result>
Evidence class: live job / real artifact bytes | executable unit tests | source-contract / regex tripwire | docs alignment
Surface: <verify skill and feature driven> | none: <reason>
Load-bearing fact: <fact> (level 1-5) | n/a
Review tier: <light|full> <base sha>..<head sha>[; <light|full> <sha>..<sha> ...]
pstack: present [hooks] | absent | off
```

Evidence class values match `references/review.md`. Inconclusive or wrong-surface is not a pass. An unproven load-bearing fact is a remaining gate; do not write it closed. For a user-visible output, the observed result names the content checked. An output that only exists or is non-empty leaves that fact a remaining gate. Tests alone on a user-visible change record `Surface: none: <reason>`.

### Optional observation

Outside the Proof record, under `## Verification`, the body may include:

```
Brief: followed | adjusted: <step ids> | dissent <comment id>
Executor-model: <id or unknown>
```

A missing line does not fail the pre-submit gate.

| Excuse | Reality |
| --- | --- |
| "I'll review the diff myself" | The file pass is `open-code-review-delegate`. |
| "Tests passed so the diff is fine" | `verification-before-completion` is not the file pass. |
| "I'll waive this High finding" | Only the human in this conversation waives, with path, issue, and reason. |
| "pstack is absent, so proof is n/a" | The Proof record is still required. |
