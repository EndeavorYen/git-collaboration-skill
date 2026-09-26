# Merge

Read this file for `/git-merge-approved` and `/git-merge-approved-force`. Also read one of `references/github.md` or `references/gitlab.md`. The approving-reviewer definition stays in `SKILL.md`.

When `/git-merge-approved` is not `READY_TO_MERGE` or the user is not the author or assignee, stop. For `MERGE_NOT_AUTHORIZED`, only the author or an assignee may merge. The reply uses the review handoff in `SKILL.md`.

When `/git-merge-approved-force` fails a technical gate, stop. `MERGE_NOT_AUTHORIZED` still blocks.


The authenticated user must still be the author or a current assignee. The PR/MR must still be open, not draft, free of conflicts, not `NEEDS_REVISION`, have required CI success or an explicit acceptable explanation, have blocking discussions resolved, and match the exact current head. Force waives the live non-author approving-reviewer requirement. Merge through the forge with the exact-head SHA. If branch protection rejects the merge, report the forge error. Add `admin` in the same invocation only when the user asked to bypass protection; then GitHub may use `gh pr merge --admin`.

After `/git-merge-approved-force`, the operator reply ends with one `next step:` line and does not print the Solo override block. Merged: `next step: none`. `NEEDS_REVISION`: `next step: /git-revise-pr <url>`. `CONFLICTED`: `next step: /git-fix-conflict <url>`. Any other stop: `next step: /git-pr-status <url>`.

## Merge Approved PR/MR

Use this only when the user explicitly asks to merge a specific PR/MR, or when `/git-triage run` reaches an owned item whose live primary state is `READY_TO_MERGE` (unless `no-merge` was requested). `/git-triage run` does not inherit force.

Before merging:

1. Run the PR/MR command preflight and continue only when the primary state is `READY_TO_MERGE`, or when this invocation is `/git-merge-approved-force` and the remaining gates in **Explicit force** pass.
2. Resolve the authenticated forge user. Continue only when this user is the PR/MR author or a current assignee. If neither matches, classify `MERGE_NOT_AUTHORIZED` and stop before any merge-side write.
3. The preflight snapshot is the merge gate when no forge write has happened since it. If a follow-up issue was created after that snapshot, replace it with one snapshot immediately before the merge. Do not take both by habit. Duplicate-check follow-up issues with one search only when you are about to create one.
4. Verify live approval from that snapshot. Without force, the approval gate passes only when at least one approving reviewer is present on the current head. Branch-protection or approval-rule zeroes must not override a missing live approval. `/git-merge-approved-force` waives this approving-reviewer check.
5. From that snapshot, read the latest reviewer comments for relevant non-blocking suggestions. Duplicate-check and create/link follow-up issues before the merge when repo-local instructions require tracking.
6. Run the final gate on the exact current head:
   - authenticated user is still the author or a current assignee
   - reviewed head SHA still matches current head SHA
   - required pipeline/jobs are success or have an explicit acceptable explanation
   - blocking discussions are resolved
   - live approval is present for the current head, or this invocation is `/git-merge-approved-force`
   - without force, every approving reviewer has no author or committer commits on the current PR/MR
   - no conflicts or merge status blockers remain
7. Merge through the forge. The merge command result is the read-back of PR/MR state. One confirm view only when that result omits merged state or the target SHA. If branch protection rejects the merge, report the forge error. Use GitHub `--admin` only when the same invocation also contains `admin`.

Never use reviewer comments, discussion text, `LGTM`, `approved`, reviewer state, resolved discussions, rule zeroes without an approving reviewer, or a green pipeline as a substitute for the live approval gate. Only `/git-merge-approved-force` in this invocation waives that gate.

If the actor gate fails, stop and identify the author and current assignees. State that one of them must invoke `/git-merge-approved` for the same PR/MR; do not recommend that a reviewer self-assign merely to bypass the gate.
