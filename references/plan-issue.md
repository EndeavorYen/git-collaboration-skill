# Plan issue

Read this file for `/git-plan-issue`. Also read one of `references/github.md` or `references/gitlab.md`. Do not read `references/pre-submit.md` for this mode.

## Plan Issue Workflow

Use this when the user explicitly invokes `/git-plan-issue` or clearly asks to analyze one issue and post an implementation brief. The write scope is one issue comment on the exact target; do not change code, commits, branches, labels, assignees, issue state, description, links, or any other forge object.

1. Resolve the exact project/issue. Reuse the authenticated user already resolved for this invocation.
2. Take one issue snapshot: state, description, labels, assignees, links already on that payload, marker comments, and the latest non-system comments. The latest body stays whole. Do not search for related PRs/MRs.
3. Read repo-local instructions and inspect the relevant code in the local checkout until the brief can name concrete files, symbols, behavior, and tests. Search, then open those symbols. Do not paste source into the brief or the reply. Stay on Forge budget steps 3 and 4 and on Context budget. Do not read repository files through the forge.
4. Classify whether a current implementation brief is still needed. A current brief exists when a comment contains `<!-- git-plan-issue -->` and later comments have not changed Goal, Recommended change, Out of scope, or Acceptance criteria. A current brief is still needed when none exists, later comments changed those fields, or the user asked to re-plan.
5. Draft one issue comment using this recipe, in the issue language or the repo's documented language:

```markdown
<!-- git-plan-issue -->
## Implementation brief

**Goal:** <one observable completion state>
**Root cause:** <file and behavior evidence>
**Recommended change:** <what to change, where, and why this shape>
**Out of scope:** <work this issue will not do>
**Acceptance criteria:**
- [ ] <checkable item with oracle: command, expected result, or observable API/UI>
**Tests:** <tests to add or required runs>
**Constraints:** <repo-local instructions or existing contracts>
**Next:** `/git-issue-pr <exact issue URL>`
```

The brief is a proposal. `/git-issue-pr` follows it when the implementer agrees, or posts a `<!-- git-plan-issue-dissent -->` and waits for a human decision.

6. An unsettled product decision is a choice among two or more product behaviors that changes Goal, Recommended change, Out of scope, or Acceptance criteria, or an acceptance item that cannot be checked until that choice is made. A deferred or open assumption in the close log is still unsettled. Do not guess an unsettled product decision into one of those four fields. Load `gentle-grill-me` only when the draft still contains an unsettled product decision. When those four fields are already settled, do not load `gentle-grill-me` and do not wait for a close log; step 7 posts that draft. When the draft still contains an unsettled product decision, use that skill's rounds and post nothing until the user confirms the close log. After that confirmation, rewrite those four fields from settled log entries only. If any of those four fields is still deferred or open, post nothing and report that open assumption. On this unsettled path, that confirmation authorizes the one brief comment in step 7 only when those four fields are settled decisions. The local grill log is not the issue comment. After the user confirms the close log, post that brief in the same session before the turn ends. `gentle-grill-me` saying this session must not implement does not skip the comment and does not end the turn at `.gentle-grill/grill-log.jsonl`. `/git-plan-issue` stops after that comment. It does not authorize code, commits, pushes, or a PR/MR. Scheduled lifecycle, scheduled merge, and `/git-triage` do not load `gentle-grill-me`; recommend `/git-plan-issue` with the exact issue URL.
7. Post one issue comment only when the issue is open, a current brief is still needed, the draft is grounded in the inspected checkout, and Goal, Recommended change, Out of scope, and Acceptance criteria are settled decisions. A draft whose four fields are already settled does not need a close log. The write response is the read-back. Report the new comment id and timestamp, current issue state from the snapshot, and `/git-issue-pr` with the exact issue URL. Do not view the issue again when the response includes the comment id.

Do not post a duplicate brief. Do not implement or open a PR/MR. Do not post a brief while an unsettled product decision remains in those four fields. If the issue is closed, a current brief already exists and the user did not ask to re-plan, an open PR/MR already covers the issue and the user did not ask to re-plan, or the evidence is too thin for a grounded brief, perform no write and report the evidence plus the exact wait or next action.


## Dissent recipe

Implement posts this comment on material disagreement, then stops. The recipe lives here.

```markdown
<!-- git-plan-issue-dissent -->
## Implementation dissent

**Brief:** comment <id>
**Disagree with:** <Goal / Recommended change / Out of scope / Acceptance criteria items>
**Why:** <file and behavior evidence>
**Alternative:** <proposed change>
**Need from you:** choose the original brief, this alternative, or a third way
**Next:** reply on this issue, then `/git-issue-pr <exact issue URL>`
```
