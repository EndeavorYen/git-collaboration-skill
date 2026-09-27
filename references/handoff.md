# Review handoff

Every mode that prints `next step:` takes it from this list.

First match:

1. `REVIEW_NOT_AUTHORIZED` → `next step: /git-review-pr-force <url>`
2. `WRITE_NOT_AUTHORIZED` or `MERGE_NOT_AUTHORIZED` → `next step: none`
3. `/git-plan-issue` posted a brief → `next step: /git-issue-pr <url>`
4. `/git-plan-issue` posted nothing, or `/git-reply-issue` → `next step: none`
5. `/git-request-review` recorded a reviewer → `next step: /git-pr-status <url>`
6. `/git-issue-pr` opened no PR/MR → `next step: none`
7. `/git-issue-pr`, `/git-revise-pr`, or `/git-fix-conflict`, and another user has a current-head review request → `next step: /git-pr-status <url>`
8. One of those three, and the actor is the author or `self_authored_head` → `next step: /git-review-pr-force <url>`
9. Otherwise one of those three → `next step: /git-request-review <url>`
10. Plain `/git-review-pr` → `next step: none`
11. Plain `/git-merge-approved` merged → `next step: none`. `NEEDS_REVISION` → `next step: /git-revise-pr <url>`. `CONFLICTED` → `next step: /git-fix-conflict <url>`. `REVIEW_REQUEST_NEEDED` → `next step: /git-request-review <url>`. Any other stop → `next step: /git-pr-status <url>`

