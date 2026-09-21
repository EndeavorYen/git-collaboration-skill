---
description: Address reviewer feedback on an existing GitHub PR or GitLab MR
---

Use the installed `git-collaboration` skill in "Update own PR/MR after review" mode. Detect the forge from the URL or remotes.

Run the skill's read-only PR/MR command preflight first, including the actor gate. Continue only when the primary state is `NEEDS_REVISION` because there is new or still-unaddressed actionable reviewer feedback or a relevant failed job that requires code changes, and the authenticated user is the author or a current assignee. If `WRITE_NOT_AUTHORIZED`, stop without editing even when the user named this PR/MR.

Then implement the focused feedback on the PR/MR branch, validate, commit, run the skill's **pre-submit gate** (`requesting-code-review` dispatching a fresh subagent that runs `open-code-review-delegate`). Stop before push if Critical/High remain unfixed and unwaived, if the file pass failed, or if `ocr` is missing. Then push, reply to or resolve threads only when justified by the new code, update evidence if needed, and read back the new head state.

If there is no new actionable reviewer feedback, do not edit, commit, or push. Report the current state and exact evidence instead. Recommend `/git-request-review` when current-head review has not been requested, `/git-merge-approved` when live approval and every final gate pass, `/git-fix-conflict` for conflicts, or `/git-pr-status` plus an explicit wait condition when review is already pending. Print Solo override for `/git-revise-pr-force` when the user owns the PR/MR and wants to iterate without `NEEDS_REVISION`. Do not create an empty commit or a duplicate review request.

Do not merge from this command. After pushing, do not review or approve this PR/MR yourself.

$ARGUMENTS
