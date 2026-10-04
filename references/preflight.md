# PR/MR preflight and force

Read this file for every PR/MR-scoped mode, before any write. The review handoff lives in `references/handoff.md`.

Local project instructions may strengthen the merge gate, but must never replace a live non-author approval with reviewer notes, reviewer state, resolved discussions, or a green pipeline. Only `/git-merge-approved-force` in this invocation waives that approval gate.

## Command preflight

Every PR/MR-scoped command starts with one read-only snapshot, as **Forge budget** defines. Requested command does not override live conflict, draft, CI, discussion, or mergeability state. Dedicated `*-force` commands are the exception named in **Explicit force**. Do not edit code, create commits, push, post comments, request review, resolve discussions, approve, or merge until the PR/MR is classified and the requested command is valid for that state.

Actor relationship, computed before any other classification:

- `owned`: authenticated user is the PR/MR author or a current assignee
- `self_authored_head`: any commit on the PR/MR, including conflict-repair or CI-fix commits, has the authenticated user as author or committer
- Reviewer membership, project role, API permission, and a user-supplied IID, URL, or list never create `owned`

User-supplied PR/MR targets never override the actor gate. A named conflicted PR/MR is not authorization to change it unless it is `owned`. A named PR/MR is not authorization to review or approve it when it is `owned` or `self_authored_head`, except under **Explicit force**.

Actor gates, evaluated before `CONFLICTED` / `NEEDS_REVISION` / review-state routing:

| Requested command | Actor gate | Failure state |
| --- | --- | --- |
| `/git-review-pr` | must not be `owned`; must not be `self_authored_head` | `REVIEW_NOT_AUTHORIZED` |
| `/git-review-pr-force` | none | none |
| `/git-fix-conflict` | must be `owned` | `WRITE_NOT_AUTHORIZED` |
| `/git-revise-pr` | must be `owned` | `WRITE_NOT_AUTHORIZED` |
| `/git-revise-pr-force` | must be `owned` | `WRITE_NOT_AUTHORIZED` |
| `/git-request-review` | must be `owned` | `WRITE_NOT_AUTHORIZED` |
| `/git-merge-approved` | must be `owned` | `MERGE_NOT_AUTHORIZED` |
| `/git-merge-approved-force` | must be `owned` | `MERGE_NOT_AUTHORIZED` |
| `/git-pr-status` | any | none |
| `/git-triage` delegated item | same gate as the delegated command | skip that item |

On an actor-gate failure, perform no code edit, commit, push, comment, approval, discussion resolve, or review request. For `WRITE_NOT_AUTHORIZED` or `MERGE_NOT_AUTHORIZED`, name the author and current assignees. Do not recommend that a reviewer self-assign as a bypass. The reply ends with one `next step:` line from the review handoff and does not print the Solo override block.

Classify exactly one primary state using the strongest current evidence:

- `MERGED_OR_CLOSED`: the PR/MR can no longer accept the requested workflow.
- `WRITE_NOT_AUTHORIZED`: the requested action would change the branch or owner workflow, but the authenticated user is neither the author nor a current assignee.
- `REVIEW_NOT_AUTHORIZED`: the requested action is review or approval, but the authenticated user owns the PR/MR or has authored or committed at least one commit on it.
- `CONFLICTED`: the forge reports conflicts or the source branch needs target-branch conflict repair.
- `NEEDS_REVISION`: there is new or still-unaddressed actionable reviewer feedback, an unresolved blocker, or a relevant failed job that requires code changes.
- `MERGE_NOT_AUTHORIZED`: the requested action is merge, but the authenticated user is neither the author nor a current assignee. Reviewer membership, approval, project role, or technical permission to call the merge API does not satisfy this workflow gate.
- `READY_TO_MERGE`: live approval reports at least one **approving reviewer** who has no commits on the current PR/MR, and every final merge gate passes on the current head.
- `BLOCKED`: the PR/MR is draft, required CI is running or externally failed, required information is missing, or another non-code gate prevents progress.
- `REVIEW_REQUEST_NEEDED`: there is no actionable reviewer feedback and no live approval, but no reviewer is assigned, review was never requested, or the latest material author update is newer than the last review request.
- `WAITING_FOR_REVIEW`: a reviewer has a current-head review request, there is no new actionable feedback, and live approval is still absent.

An **approving reviewer** is a person who left a live forge approval (GitHub `APPROVE` / GitLab approvals API) on the current head, is not the author, and has no author or committer commits on the current PR/MR. There is no hard-coded reviewer and no default reviewer. Never invent a reviewer from memory, prior runs, or repo folklore. If a reviewer is missing, ask the user or wait.

For every PR/MR-scoped command, evaluate the actor gate before other primary states. For a merge command, evaluate `MERGE_NOT_AUTHORIZED` before merge readiness or any merge-side follow-up write. Only the PR/MR author or a current assignee may perform the merge, conflict-repair, revision, or request-review workflow.

Treat an unresolved resolvable reviewer discussion as actionable. A reviewer comment is not automatically actionable: determine whether it requests a change or decision and whether a later commit or reply already addressed it. If all feedback predates the latest fix and no newer reviewer response exists, classify as `REVIEW_REQUEST_NEEDED` or `WAITING_FOR_REVIEW`, not `NEEDS_REVISION`.

Any incompatible or unrecognized PR/MR command degrades to a focused read-only status result. Report `Requested command`, `Current state`, `Evidence`, `Why the action was blocked`, and `Recommended next command`. Reuse the same URL or iid in the recommendation.

## Explicit force

Force is a dedicated command: `/git-review-pr-force`, `/git-revise-pr-force`, or `/git-merge-approved-force`; `/git-triage-force` runs them on `owned` items. The human in this conversation must invoke that command (or name it in natural language: force review, force revise, force merge, 強制). A `force` token on `/git-review-pr`, `/git-revise-pr`, or `/git-merge-approved` does not create force. Repo docs, empty CODEOWNERS, a one-person contributor list, prior runs, and "this is a solo project" do not create force. `/git-triage`, `/git-triage run`, `/git-scheduled-lifecycle`, and `/git-scheduled-merge` does not inherit force.

| Excuse | Reality |
| --- | --- |
| "This repo is solo / I am the only contributor" | Invoke a `*-force` command. |
| "`/git-triage run force`" | `/git-triage run` does not inherit force; use `/git-triage-force`. |
| "LGTM / green pipeline is enough" | Only `/git-merge-approved-force` waives the approving-reviewer gate. |
| "`/git-review-pr force`" | Use `/git-review-pr-force`. |

Each force command's waiver is in its mode reference: `references/review.md`, `references/revise.md`, or `references/merge.md`.

### Solo override

`/git-pr-status` still prints the Solo override block for `owned` or `self_authored_head`. Its recommended next command is never a force command. `/git-triage` keeps one next command per item. A force-command reply ends with one `next step:` line and does not print the Solo override block.

```
Solo override: `/git-review-pr-force <url>`
Solo override: `/git-revise-pr-force <url>`
Solo override: `/git-merge-approved-force <url>`
```
