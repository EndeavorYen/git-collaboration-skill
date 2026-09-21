---
description: Merge a specific approved GitHub PR or GitLab MR after live final gates pass
---

Use the installed `git-collaboration` skill in "Merge approved PR/MR" mode. Detect the forge from the URL or remotes, then load `references/github.md` or `references/gitlab.md`.

Run the skill's read-only PR/MR command preflight for the specific PR/MR first. Merge only when its primary state is `READY_TO_MERGE`. Then track relevant non-blocking follow-ups when required, perform the final exact-head gate, merge through the forge, and read back the result.

This command is also the merge step used by `/git-triage run` for owned ready-to-merge PRs/MRs unless `no-merge` was requested. `/git-triage run` does not inherit force.

Resolve the authenticated forge user and compare its stable user ID or exact username with the PR/MR author and current assignees before any merge-side follow-up or merge-readiness work. Continue only when the authenticated user is the author or a current assignee. Reviewer status, live approval, project role, or technical API permission is not authorization to merge under this workflow. If the user is neither author nor assignee, classify `MERGE_NOT_AUTHORIZED`, perform no merge-side write, and state that the author or an assignee must invoke this command for the same PR/MR. Do not suggest self-assignment as a bypass.

Do not merge unless live approval reports at least one approving reviewer on the current head. Every approving reviewer must have no author or committer commits on the current PR/MR. There is no default reviewer. Do not merge when approval is only present as reviewer text such as `LGTM`, `approved`, or `looks good`. If live approval is absent, stop and report that the PR/MR is waiting for an approving reviewer. Print Solo override for `/git-merge-approved-force` when the remaining gate is a second-person reviewer on an owned PR/MR.

When blocked, do not perform any merge-side write. Report the current state and exact evidence, then recommend the same PR/MR target with `/git-revise-pr` for actionable feedback, `/git-fix-conflict` for conflicts, `/git-request-review` when current-head review has not been requested, or `/git-pr-status` when it is waiting or otherwise blocked.

$ARGUMENTS
