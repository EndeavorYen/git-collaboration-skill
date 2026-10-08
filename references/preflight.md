# PR/MR preflight and force

Read this before a PR/MR write. Handoff: `references/handoff.md`.

Local instructions may strengthen the merge gate, but must never replace a live non-author approval with notes, reviewer state, resolved discussions, or a green pipeline. Only `/git-merge-approved-force` waives that gate.

## Command preflight

One read-only snapshot, as **Forge budget** defines. Live conflict, draft, CI, discussion, and mergeability win. **Explicit force** is the exception. No edit, commit, push, comment, review, resolve, approve, or merge until classified.

Actor relationship, before any other classification:

- `owned`: authenticated user is the author or a current assignee
- `self_authored_head`: any commit, including a conflict-repair or CI-fix, has the user as author or committer
- Reviewer membership, project role, API permission, and a supplied IID, URL, or list never create `owned`

A supplied target never overrides the actor gate. Changing a conflicted PR/MR requires `owned`. Review or approval while `owned` or `self_authored_head` uses only **Explicit force**.

Actor gates, before `CONFLICTED` / `NEEDS_REVISION` / review-state routing:

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

On an actor-gate failure, do not edit, commit, push, comment, approve, resolve, or request review. For `WRITE_NOT_AUTHORIZED` or `MERGE_NOT_AUTHORIZED`, name the author and assignees. Do not recommend self-assign as a bypass. The reply has one `next step:` line and does not print the Solo override block.

One primary state:

- `MERGED_OR_CLOSED`: the PR/MR can no longer accept the requested workflow.
- `WRITE_NOT_AUTHORIZED`: the action changes the branch or owner workflow, and the user is neither author nor assignee.
- `REVIEW_NOT_AUTHORIZED`: review or approval, and the user owns the PR/MR or has a commit on it.
- `CONFLICTED`: conflicts, or the source needs target-branch repair.
- `NEEDS_REVISION`: actionable feedback, an unresolved blocker, or a relevant failed job still needs code changes.
- `MERGE_NOT_AUTHORIZED`: merge was requested, and the user is neither author nor assignee. Membership, approval, role, or API permission is not this gate.
- `READY_TO_MERGE`: at least one **approving reviewer** with no commits on this PR/MR, and every final merge gate passes.
- `BLOCKED`: draft, required CI running or externally failed, required information is missing, or another non-code gate.
- `REVIEW_REQUEST_NEEDED`: no actionable feedback and no live approval, and review is unassigned, never requested, or stale.
- `WAITING_FOR_REVIEW`: a current-head review request, no new actionable feedback, no live approval. Unopened project rows use **Project list** in `triage.md`.

An **approving reviewer** left a live forge approval (GitHub `APPROVE` / GitLab approvals API) on the current head, is not the author, and has no commits on this PR/MR. There is no hard-coded reviewer and no default reviewer. Never invent a reviewer. If none is known, ask the user in this conversation, or wait.

For a merge command, `MERGE_NOT_AUTHORIZED` comes before merge readiness.

An unresolved resolvable discussion is actionable. A comment is actionable only when it requests a change or decision that a later non-merge commit or reply has not addressed. Older feedback is `REVIEW_REQUEST_NEEDED` or `WAITING_FOR_REVIEW`, not `NEEDS_REVISION`.

An unrecognized command degrades to read-only status. Report `Requested command`, `Current state`, `Evidence`, `Why the action was blocked`, and `Recommended next command`.

## Explicit force

Force is a dedicated command: `/git-review-pr-force`, `/git-revise-pr-force`, or `/git-merge-approved-force`; `/git-triage-force` invokes them for `owned` items. The human in this conversation must invoke it (force review, force revise, force merge, 強制). A `force` token on the plain command does not create force. Repo docs, empty CODEOWNERS, a one-person list, prior runs, and "this is a solo project" do not create force. `/git-triage`, `/git-triage run`, `/git-scheduled-lifecycle`, and `/git-scheduled-merge` does not inherit force.

| Excuse | Reality |
| --- | --- |
| "This repo is solo / I am the only contributor" | Invoke a `*-force` command. |
| "`/git-triage run force`" | Use `/git-triage-force`. |
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
