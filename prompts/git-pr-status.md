---
description: Inspect one GitHub PR or GitLab MR read-only and recommend the exact next command
---

Use the installed `git-collaboration` skill in "Focused PR/MR status" mode. Detect the forge from the URL or remotes.

Keep this command read-only. Resolve the target PR/MR from the URL, iid, or an unambiguous current branch, then run the skill's PR/MR command preflight against live forge state. Do not edit code, commit, push, post comments, request review, resolve discussions, approve, or merge.

Report `Current state`, `Head and gates`, `Evidence`, and `Recommended next command`. Include the authenticated user's relationship to the author, assignees, and reviewers, and whether any current commit was authored or committed by that user. Classify the PR/MR as `MERGED_OR_CLOSED`, `WRITE_NOT_AUTHORIZED`, `REVIEW_NOT_AUTHORIZED`, `CONFLICTED`, `NEEDS_REVISION`, `MERGE_NOT_AUTHORIZED`, `READY_TO_MERGE`, `BLOCKED`, `REVIEW_REQUEST_NEEDED`, or `WAITING_FOR_REVIEW`. Give one directly usable next command with the same target, or state the exact event to wait for when no action is currently useful. The recommended next command must pass the actor gate: never suggest `/git-fix-conflict`, `/git-revise-pr`, `/git-request-review`, or `/git-merge-approved` for a foreign PR/MR, and never suggest `/git-review-pr` for an owned or `self_authored_head` PR/MR. For `MERGE_NOT_AUTHORIZED` or `WRITE_NOT_AUTHORIZED`, identify that the author or a current assignee must perform the write; never suggest self-assignment as a bypass.

If the user entered an unknown or unsuitable command with the PR/MR target, also report `Requested command` and why it was blocked.

$ARGUMENTS
