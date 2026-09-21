---
description: Force-merge an owned GitHub PR or GitLab MR after remaining technical gates pass
---

Use the installed `git-collaboration` skill in `/git-merge-approved-force` mode. Detect the forge from the URL or remotes, then load `references/github.md` or `references/gitlab.md`.

Run the skill's read-only PR/MR command preflight for the specific PR/MR first. This dedicated command waives the live non-author approving-reviewer gate. Continue only when the authenticated user is the author or a current assignee. If neither matches, classify `MERGE_NOT_AUTHORIZED`, perform no merge-side write, and state that the author or an assignee must invoke this command for the same PR/MR. Do not suggest self-assignment as a bypass.

The PR/MR must still be owned, open, not draft, free of conflicts, have required CI success or an explicit acceptable explanation, have blocking discussions resolved, and match the exact current head. Then track relevant non-blocking follow-ups when required, merge through the forge with the exact-head SHA, and read back the result.

If branch protection rejects the merge, report the forge error. Use GitHub `--admin` only when the same invocation also contains `admin`.

`/git-triage run` does not inherit force. Scheduled approved merge does not inherit force.

When remaining technical gates fail, do not perform any merge-side write. Report the current state and exact evidence, then recommend `/git-revise-pr` or `/git-revise-pr-force` for code changes, `/git-fix-conflict` for conflicts, or `/git-pr-status` when otherwise blocked.

$ARGUMENTS
