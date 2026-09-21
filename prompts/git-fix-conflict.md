---
description: Fix GitHub PR or GitLab MR conflicts on the source branch and push for re-review
---

Use the installed `git-collaboration` skill in "Fix PR/MR conflicts" mode. Detect the forge from the URL or remotes.

Run the skill's read-only PR/MR command preflight first, including the actor gate. Continue only when the primary state is `CONFLICTED` and the authenticated user is the author or a current assignee. If the user is neither, classify `WRITE_NOT_AUTHORIZED` and do not change the branch, even when the user named this PR/MR in the prompt or a conflict list. Reviewer membership is not ownership.

Otherwise do not change the branch; report the current state and recommend `/git-revise-pr`, `/git-request-review`, `/git-merge-approved`, or `/git-pr-status` according to the live evidence.

For a conflicted owned PR/MR, derive the source and target branches, protect unrelated local work, fetch both branches, and resolve the conflict on the source branch. Prefer merging the latest target branch into the source branch unless repo-local instructions explicitly prefer rebase or history rewriting is clearly authorized.

Keep the change scoped to conflict repair and any directly required validation fixes. Inspect conflict markers deliberately, preserve the PR/MR intent and current target-branch behavior, run focused validation, commit, run the skill's **pre-submit gate** (`requesting-code-review` dispatching a fresh subagent that runs `open-code-review-delegate`). Stop before push if Critical/High remain unfixed and unwaived, if the file pass failed, or if `ocr` is missing. Then push the source branch. The push response is the read-back. One confirm view only when it omits the new head SHA, conflict/mergeability state, pipeline, discussions, or reviewer state.

Do not merge the PR/MR. After pushing, do not review or approve this PR/MR yourself; recommend `/git-request-review`.

$ARGUMENTS
