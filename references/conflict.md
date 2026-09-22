# Conflict repair

Read this file for `/git-fix-conflict`. Before push: `references/pre-submit.md`. Do not read `references/revise.md`.

When the PR/MR is not `CONFLICTED` or the user is not the author or assignee, stop without changing the branch. For `WRITE_NOT_AUTHORIZED`, name the author or assignee and do not repair a foreign PR/MR.

## Fix PR/MR Conflicts

Use this when the user asks to fix a conflict or invokes `/git-fix-conflict`.

1. Run the PR/MR command preflight and continue only when the primary state is `CONFLICTED` and the PR/MR is `owned`. If `WRITE_NOT_AUTHORIZED`, stop without changing the branch even when the user named this PR/MR.
2. Read repo-local instructions, inspect `git status --short --branch`, and use the preflight snapshot as the PR/MR record. Do not snapshot it again before the push.
3. Confirm the write boundary is only the source branch.
4. Work in a clean checkout or isolated worktree when the main checkout has unrelated changes.
5. Check out the source branch tracking origin. Prefer a non-rewriting merge of the target branch into the source branch unless repo-local instructions explicitly prefer rebase.
6. Resolve conflict markers deliberately by preserving the PR/MR intent and current target-branch behavior.
7. Run focused tests, formatters, builds, or generation checks proportional to the conflicted areas.
8. Commit with the repo's normal style. Run the **pre-submit gate**. Stop before push if Critical/High remain unfixed and unwaived. Then push the source branch.
9. The push response is the read-back for the new head SHA. One confirm view only when it omits head SHA, conflict or mergeability state, pipeline, unresolved discussions, or reviewer state. Bundle any missing fields into that one view.

After resolving conflicts, still do not merge until live approval reports an approving reviewer on the current head, or the user separately invokes `/git-merge-approved-force`.
