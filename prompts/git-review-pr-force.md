---
description: Force-review an owned or self-authored GitHub PR or GitLab MR and post a visible verdict
---

Use the installed `git-collaboration` skill in `/git-review-pr-force` mode. Detect the forge from the URL or remotes, then load `references/github.md` or `references/gitlab.md`.

This dedicated command waives the review actor gate (`owned`, `self_authored_head`). The PR/MR must still be open. Run the skill's structured file review with `open-code-review-delegate` on the current head, map findings with the skill's `/git-review-pr` mapping, then continue CI, evidence-class, remaining-gate, and verdict rules. OCR Step 7 Fix stays off. Keep the local workflow read-only except for forge review feedback, and post a visible approve/block verdict in the issue/PR language or the repo's documented language.

If the forge rejects a self-APPROVE, post a current-head comment that starts with `<!-- git-force-review -->` and names the SHA. Native approval remains absent. `/git-review-pr-force` does not merge.

On re-review of a claimed failed job or issue: download that job log once, then walk the remaining job script plus adjacent layers locally. Checking previously posted blockers is not enough to approve. If those adjacent layers have not been walked, must not approve.

PR/MR pipeline green is not claimed live job green. An approve or block note must list the claimed live job and whether it appeared on the current head pipeline. If it did not run, the verdict must name the remaining gate and must not write the defect as closed. Do not require rerunning a protected live job before approval.

Label the evidence class on every approve or block verdict, and must not treat tripwire as live proof. If the invocation arguments contain thorough, don't rubber-stamp, 徹底, 抓出來, 放水, or 不要放水, apply thorough-review: remaining gates, policy cost, and evidence class go in the verdict main table.

Read back the current head SHA, pipeline, discussion state, and approval/request-changes state before reporting.

$ARGUMENTS
