---
description: Force-revise an owned GitHub PR or GitLab MR without waiting for NEEDS_REVISION
---

Use the installed `git-collaboration` skill in `/git-revise-pr-force` mode. Detect the forge from the URL or remotes.

Run the skill's read-only PR/MR command preflight first, including the actor gate. Continue only when the authenticated user is the author or a current assignee. If `WRITE_NOT_AUTHORIZED`, stop without editing even when the user named this PR/MR. This dedicated command waives the `NEEDS_REVISION` state gate so an owned open PR/MR can receive further commits without actionable reviewer feedback.

The PR/MR must still be open and not `CONFLICTED`. Work on the source branch, validate, commit, and run the skill's **pre-submit gate** (`requesting-code-review` dispatching a fresh subagent that runs `open-code-review-delegate`). Stop before push if Critical/High remain unfixed and unwaived, if the file pass failed, or if `ocr` is missing. Then push and update evidence if needed. The push response is the read-back of the new head. One confirm view only when it omits the head SHA.

Do not merge from this command. After pushing, do not review or approve this PR/MR yourself. Recommend `/git-review-pr-force` or `/git-merge-approved-force` only as Solo override lines, never as the default next command.

$ARGUMENTS
