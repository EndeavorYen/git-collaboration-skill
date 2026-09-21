---
description: Review another person's GitHub PR or GitLab MR and post a visible verdict, or force-review an owned PR/MR
---

Use the installed `git-collaboration` skill in "Review someone else's PR/MR" mode. Detect the forge from the URL or remotes, then load `references/github.md` or `references/gitlab.md`.

Run the skill's read-only PR/MR command preflight first, including the actor gate. Continue only when the PR/MR is not `owned` and not `self_authored_head`, unless this invocation is `/git-review-pr force` (tokens: `force`, `強制`, `solo`, `self-review`). If the authenticated user is the author or a current assignee, or any commit on the current PR/MR was authored or committed by that user, classify `REVIEW_NOT_AUTHORIZED` and do not post review feedback or approve. A named IID, URL, or list does not authorize self-review. Under `/git-review-pr force`, continue with the structured file pass and a visible verdict. If the forge rejects a self-APPROVE, post a current-head comment that starts with `<!-- git-force-review -->` and names the SHA. Force review does not merge.

If the PR/MR is merged/closed, the same current head was already reviewed with no new evidence, or the command is incompatible with the user's relationship to the PR/MR, do not post duplicate review feedback; report the focused status and recommend `/git-pr-status` or the command matching the state.

Otherwise review the live PR/MR from current forge state. Run the skill's structured file review with `open-code-review-delegate` on the current head, map findings with the skill's `/git-review-pr` mapping, then continue CI, evidence-class, remaining-gate, and verdict rules. OCR Step 7 Fix stays off. Keep the local workflow read-only except for forge review feedback, and post a visible approve/block verdict in the issue/PR language or the repo's documented language. Read back the current head SHA, pipeline, discussion state, and approval/request-changes state before reporting.

On re-review of a claimed failed job or issue: reread that job's actual error and walk the remaining job script plus adjacent layers. Checking previously posted blockers is not enough to approve. If those adjacent layers have not been walked, must not approve.

PR/MR pipeline green is not claimed live job green. An approve or block note must list the claimed live job and whether it appeared on the current head pipeline. If it did not run, the verdict must name the remaining gate and must not write the defect as closed. Do not require rerunning a protected live job before approval.

Label the evidence class on every approve or block verdict, and must not treat tripwire as live proof. If the invocation arguments contain thorough, don't rubber-stamp, 徹底, 抓出來, 放水, or 不要放水, apply thorough-review: remaining gates, policy cost, and evidence class go in the verdict main table.

$ARGUMENTS
