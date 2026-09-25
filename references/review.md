# Review

Read this file for `/git-review-pr` and `/git-review-pr-force`. File pass: `references/pre-submit.md`. Also read one of `references/github.md` or `references/gitlab.md`. Do not read other mode files.

When `/git-review-pr` is not open or is `REVIEW_NOT_AUTHORIZED`, stop without posting review feedback. Do not approve. Recommend `/git-request-review` when the user owns the PR/MR, or another reviewer plus `/git-pr-status` when `self_authored_head`. Print Solo override.

When `/git-review-pr-force` is not open, stop without posting. `MERGED_OR_CLOSED` stays blocked.

### `/git-review-pr-force`

Waives the review actor gate (`owned`, `self_authored_head`). The PR/MR must still be open. Run the structured file pass and post a visible verdict. Force review does not merge. A `<!-- git-force-review -->` body is not an approving reviewer. Native approval stays absent unless this invocation's `APPROVE` event is accepted.

Verdict is exactly one of these tokens. Do not print `approved`, `APPROVED`, or `reject` as the status.

- `verdict: approve` — file pass done, no unresolved blocker, relevant CI is not failed or unknown.
- `verdict: request-changes` — any remaining blocker, including a failed file pass.

Try one native review event on the reviewed SHA: `APPROVE` when the verdict is approve, `REQUEST_CHANGES` when the verdict is request-changes. If the forge accepts it, the review body starts with the opening lines below. Do not also post a comment. If the forge rejects a self-APPROVE, post one current-head comment that starts with the same lines. A comment never sets `forge approval: present`.

Opening lines:

```
<!-- git-force-review -->
verdict: approve
head: <full sha>
forge approval: absent
```

Use `verdict: request-changes` on the second line when that is the result. Use `forge approval: present` only when this invocation's native `APPROVE` was accepted.

The first visible sentence after the opening lines states the verdict. When the PR/MR language is Chinese, that sentence is `同意` for `verdict: approve` and `不同意` for `verdict: request-changes`. When the language is English, use agree or disagree: `agree` for `verdict: approve` and `disagree` for `verdict: request-changes`. When the native event was rejected, the following sentence names the rejection. For a GitHub author that sentence is: the author cannot approve their own pull request. Evidence follows those sentences.

The operator reply prints the verdict line, the `forge approval:` line, and exactly one `next step:` line. Do not print the Solo override block. No second command.

Next step, first match:

1. `verdict: request-changes` and the actor is `owned` → `next step: /git-revise-pr <url>`
2. `verdict: request-changes` and the actor is not `owned` → `next step: none`
3. `verdict: approve`, actor is `owned`, and the PR/MR is `CONFLICTED` → `next step: /git-fix-conflict <url>`
4. `verdict: approve`, actor is `owned`, and the PR/MR is draft or required CI is running or another non-code gate blocks → `next step: /git-pr-status <url>`
5. `verdict: approve`, actor is `owned`, and every merge gate passes except the missing non-author forge approval → `next step: /git-merge-approved-force <url>`
6. `verdict: approve` and the actor is not `owned` → `next step: none`

Row 5 is allowed only in this force reply. `/git-pr-status` still must not recommend a force command by default.

### `/git-review-pr` mapping

The current reviewer runs the file pass on this checkout after the actor gate. Do not dispatch an implementer-session self-review as a substitute.

| OCR severity | Forge action |
| --- | --- |
| critical, high | Blocking inline discussion on the changed line |
| medium | Blocking when the finding is correctness, security, a broken contract, or missing required validation; otherwise a non-blocking follow-up comment |
| low | Omit unless thorough-review is on |

OCR coverage belongs in the review evidence. **OCR Step 7 Fix stays off.** Local workflow stays read-only except forge review writes. OCR findings do not by themselves approve or request changes. Continue CI, evidence-class, remaining-gate, and verdict rules after the file pass. A failed file pass: post no approve; treat the coverage failure as a blocker.

## Review Workflow

When the user asks to review a GitHub or GitLab PR/MR, treat that as permission to post the review result unless repo-local instructions say otherwise. Keep review-only work read-only: do not push, merge, update the description, or create follow-up issues unless the user explicitly asks.

Run the actor gate first. Do not review or approve a PR/MR that is `owned` or `self_authored_head` unless this invocation is `/git-review-pr-force`. Classify `REVIEW_NOT_AUTHORIZED` and stop without posting a verdict. Reviewer assignment plus a named IID does not authorize self-review. Under `/git-review-pr-force`, continue with the file pass and verdict.

For `review again`, take one new snapshot instead of continuing from the old verdict. If there is no new head or no relevant new evidence after a prior blocker, report that the PR/MR is still waiting on the same blocker instead of manufacturing a fresh verdict.

Use the current head, not remembered diffs. If the main checkout is dirty, behind, or belongs to a different repo, review in a temporary clone or detached worktree. Do not push review-only branches.

Run the structured file review pass (`open-code-review-delegate`) on that head, map findings with the `/git-review-pr` mapping, then continue the layers below. OCR Step 7 Fix stays off.

Review in this order:

1. Code behavior and user-visible/API behavior.
2. Tests and missing coverage for changed behavior.
3. Docs, generated types, schemas, and frontend/backend contracts.
4. CI, pipeline artifacts, deployment, and environment risks. Separate required PR/MR jobs from a named live job. Agents must not treat a generic verify job as named live-job success.

For forge-facing review text, match the issue/PR language or the repo's documented language. Keep comments concrete enough for the author to fix without a follow-up question.

Review comments must be specific, clear, and actionable. Each finding should name the concrete problem or open question, its impact and whether it blocks merge, the expected fix direction or decision needed, and the validation, test, command, or evidence required before re-review. When multiple findings exist, use concise bullets or a Markdown table such as `Item`, `Impact`, `Required action`, and `Validation`.

Blocking versus non-blocking:

- Block for regressions, broken contracts, misleading docs about active behavior, missing required validation, unresolved prior blockers, failed relevant CI, or risks that can affect correctness, security, deployment, or operations.
- Do not block for cleanup-only, style-only, or backlog-level suggestions unless the user asks.
- Put blockers in unresolved inline diff discussions on the exact changed line when possible.
- Put non-blocking findings in a concise PR/MR comment marked as follow-up or optional.

Evidence class. Every approve or block verdict must label the strongest evidence used. Classes, strongest first:

| Class | Meaning |
| --- | --- |
| live job / real artifact bytes | Named live job or inspected artifact bytes |
| executable unit tests | Tests that actually run the behavior |
| source-contract / regex tripwire | String or schema lock, not runtime proof |
| docs alignment | Text matches intended policy |

Approve must not treat tripwire as live proof. A policy change that keeps old host config must say in the verdict that testing scope shrinks.

Thorough-review triggers in the user text or invocation arguments include thorough, don't rubber-stamp, 徹底, 抓出來, and 不要放水. Thorough review does not promote style to blocking. It must put remaining gates, policy cost, and the evidence class in the verdict main table, and must not hide remaining gates in a non-blocking note.

A regex tripwire on an install or deploy command is not package-manager or runtime proof; a named live job that actually performs that step remains a remaining gate.

Approval rules:

- Never approve from a snapshot taken before the file pass. Immediately before approve, one snapshot must show the same head SHA you reviewed. Approve only that SHA.
- Do not approve if the PR/MR is `owned` or `self_authored_head`, except under `/git-review-pr-force`. Under force, use the `/git-review-pr-force` verdict: try native `APPROVE` or `REQUEST_CHANGES` on the reviewed SHA; if the forge rejects a self-APPROVE, post the opening lines on the current SHA.
- Do not approve if any active blocker remains unresolved, blocking discussions are unresolved, or relevant CI is failed/unknown without a clear non-code explanation.
- An approve or block note must list the claimed live job and whether it appeared on the current head pipeline. If it did not run, the verdict must name the remaining gate and must not write the defect as closed.
- Do not require rerunning a protected live job before approval.

For re-review, take one new snapshot of head SHA, discussions, approvals, and pipeline. Verify each previously posted blocker against the local checkout of that SHA, or against CI evidence already in the snapshot, before resolving it or approving. Do not resolve a blocker based only on the author's explanation.

When the PR/MR claims to fix a named failed job or issue, also walk that job's remaining path. Checking previously posted blockers is not enough to approve.

1. Download the claimed failed job's log once. Keep the failing command and the error lines, then walk the script locally. Do not keep the rest of the log.
2. From the failing line, walk the remaining job script and its adjacent layers.
3. If the new commit changed only one layer, still check N-1 / N+1 on the same path.
4. If those adjacent layers of the claimed failed job script have not been walked, must not approve.

After posting blockers or approval, the write response is the read-back. Report current SHA, pipeline, unresolved blocker count, and whether approval is recorded. One confirm view only when the write response omits one of those fields.

## CI And Review

For failing CI:

- Use check conclusions already in the snapshot. Download one log for the failing job, keep the failing command and the error lines, and drop the rest.
- Distinguish forge-native jobs from external providers.
- Summarize failure context before implementing fixes.
- Do not install forge tooling with system package managers unless the user asks.

For review feedback that becomes tracked work later, separate immediate code changes from backlog/process items.
