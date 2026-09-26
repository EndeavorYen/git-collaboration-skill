# Revise

Read this file for `/git-revise-pr` and `/git-revise-pr-force`. Before push: `references/pre-submit.md`.

When `/git-revise-pr` is not `NEEDS_REVISION` or the user is not the author or assignee, stop without editing. For `WRITE_NOT_AUTHORIZED`, name the author or assignee. The reply uses the review handoff in `SKILL.md`.

When `/git-revise-pr-force` is not owned, not open, `CONFLICTED`, or `MERGED_OR_CLOSED`, stop without editing. `WRITE_NOT_AUTHORIZED` still blocks. Conflicts go to `/git-fix-conflict`.


The authenticated user must still be the author or a current assignee. The PR/MR must still be open and not `CONFLICTED`. Force waives the `NEEDS_REVISION` state gate so further commits can land without actionable reviewer feedback. Run the **pre-submit gate**. Do not merge.

After a successful `/git-revise-pr-force` push, the operator reply ends with one `next step:` line and does not print the Solo override block. When the actor is `owned` or `self_authored_head` and no other user has a current-head review request, that line is `next step: /git-review-pr-force <url>`. When some other user has a current-head review request, that line is `next step: /git-pr-status <url>`.

## Updating An Existing PR/MR

When `references/pstack.md` is loaded, apply its revise rows.

Use this when addressing reviewer feedback on a PR/MR you authored or are maintaining.

1. Run the PR/MR command preflight and continue only when the PR/MR is `owned` and either the primary state is `NEEDS_REVISION` or this invocation is `/git-revise-pr-force`. If `WRITE_NOT_AUTHORIZED`, stop without editing.
2. Use the preflight snapshot as the PR/MR record: discussions, latest reviewer comments, source branch, target branch, head SHA, and pipeline. Do not snapshot it again before the push.
3. Identify which comments are blocking, which are non-blocking, and which need a separate tracker. Inspect the source branch in the local checkout.
4. Work on the source branch in a clean checkout or isolated worktree if the main checkout has unrelated changes.
5. Implement focused fixes and add or update tests for behavior changes.
6. Commit on the PR/MR branch, preserving unrelated user work. Run the **pre-submit gate**. Stop before push if Critical/High remain unfixed and unwaived. Then push.
7. Reply to reviewer threads with what changed and validation evidence. Resolve a thread only after the new code actually addresses it.
8. Update the description when validation evidence, known limitations, issue mappings, or the Proof record from `references/pre-submit.md` changed.
9. The push and thread-reply responses are the read-back for head, pipeline, unresolved discussions, and reviewer state. One confirm view only when those responses omit the new head SHA.

If there is no new or unaddressed actionable reviewer feedback and this invocation is `/git-revise-pr`, do not edit, commit, push, or manufacture an update. Under `/git-revise-pr-force`, continue with the owned source-branch update and the **pre-submit gate**.

After pushing fixes, still do not merge until live approval reports an approving reviewer on the current head, or the user separately invokes `/git-merge-approved-force`. Reviewer comments such as `LGTM`, `approved`, or `looks good` are useful context but are not approval evidence.
