---
name: git-collaboration
description: Use when working with GitHub or GitLab issues, pull/merge requests, reviews, CI, branches, commits, pushes, releases, labels, conflicts, or gh/glab workflows. Trigger for /git-review-pr, /git-review-pr-force, /git-plan-issue, /git-issue-pr, /git-reply-issue, /git-revise-pr, /git-revise-pr-force, /git-fix-conflict, /git-merge-approved, /git-merge-approved-force, /git-request-review, /git-pr-status, /git-triage, /git-scheduled-lifecycle, and /git-scheduled-merge.
---

# Git Collaboration

Use this skill for GitHub or GitLab work that changes repository state or forge state. Local project instructions may strengthen the merge gate, but must never replace a live non-author approval with reviewer notes, reviewer state, resolved discussions, or a green pipeline. Only `/git-merge-approved-force` in this invocation waives that approval gate.

## Detect the forge

Resolve the forge before any write. The request URL wins, then `git remote -v`:

| Signal | Forge | CLI | Change request |
| --- | --- | --- | --- |
| `github.com`, GitHub Enterprise host, `gh` repo | GitHub | `gh` | Pull request |
| `gitlab.com`, other GitLab host, `glab` repo | GitLab | `glab` | Merge request |

If both remotes exist and the request has no URL, ask which forge to use. Load only the matching forge reference (`references/github.md` or `references/gitlab.md`) for the one-snapshot commands. This file owns the workflow, including **Forge budget** and **Context budget**; those files own forge-specific commands.

In this skill, **PR/MR** means the current forge's change request. Commands below use `/git-*`. Treat `/gitlab-*` and `/github-*` aliases, plus a pasted GitHub or GitLab URL, as the same mode.

## Forge budget

Every `gh` invocation, `glab` invocation, forge REST call, and GitHub or GitLab MCP call counts. Use one client: `gh` on GitHub, `glab` on GitLab. Do not also query that object through MCP.

A **snapshot** is one read whose payload already contains every forge field that mode needs. Reuse a snapshot already in this conversation when the user has not said that object changed.

1. Resolve the authenticated user once per invocation and reuse that id. Skip a separate auth-status call when the user endpoint or the snapshot already returns the login. Skip a repo-metadata call when the URL or `git remote -v` already names the project.
2. Read each issue or PR/MR once. The command or commands named together in the matching forge reference are that snapshot, not a menu of extra calls. Do not add a call for a field that snapshot already contains.
3. After the snapshot, inspect code, history, diffs, tests, and repo instructions in the local checkout. `git fetch` of the one ref you will check out is allowed; do not fetch again to re-read files. If this checkout is the wrong repo or lacks the cited paths, stop and name the missing path.
4. Draft, classify, and implement from that snapshot plus the checkout. Do not re-query the forge between those steps. Do not read repository files, blame, or trees through the forge.
5. A write is one call. The write response is the read-back when it contains the new comment id, SHA, or state. Confirm with one view only when that response omits a field the stop condition requires. Do not reload comments or files after a successful write.
6. One more full snapshot is allowed immediately before a forge write that depends on the current head, approval, or mergeability, and before each write in an aggressive or scheduled run. That snapshot replaces the earlier one. It is still one call.

Triage lists stay lists. One metadata list per relationship. Classify from that payload. Open one trimmed snapshot only for an item you are about to write, or the one item the user named.

Download one failed job log when a verdict or a fix depends on it. Keep the failing command and the error lines.

Related PRs/MRs come from links already in the snapshot. Do not search the forge for them unless the user asked whether a PR/MR exists and the snapshot has no link.

## Context budget

- Run the snapshot command in the forge reference with its `--jq` or `jq` pipe. If the filter errors, fix the filter once. Do not rerun without it, and do not page through raw JSON.
- The issue or PR/MR body stays whole. A comment or review body stays whole when it contains `git-plan-issue`, `git-plan-issue-dissent`, or `git-force-review`, or when it is the latest one. Every other body keeps author, time, id, and the first 400 characters. Also keep review commit OID, discussion resolved state, and commit author login, name, and email. Empty login is not a missing author when name or email is present.
- List calls return metadata only: number, title, state, updated time, author, assignees, url, and for a PR/MR also draft, `reviewDecision`, mergeable, and head SHA. No comment bodies, review bodies, or check logs.
- Do not paste the snapshot, this skill, or source listings into the reply, the posted comment, or the pre-submit subagent. The subagent gets the submit range and the contract. The reply reports the decision fields the mode requires.
- Search, then open the matching symbol and its test. Do not read a directory, a whole unrelated file, or both forge references into context.
- Reuse the trimmed snapshot already in this conversation. Do not re-read it back into context to "be sure."

## Task Mode Decision

| Mode | User intent examples | Allowed writes | Stop condition |
| --- | --- | --- | --- |
| Review someone else's PR/MR | `/git-review-pr`, `/git-review-pr-force` | Forge review comments, discussion resolution only when re-review proves the blocker is fixed, approve/request changes, or a `<!-- git-force-review -->` comment when self-APPROVE is rejected | Plain `/git-review-pr`: posted visible verdict and read back SHA, pipeline, discussions, and approval/request-changes state. Force `/git-review-pr-force`: that read-back, and the reply prints `verdict:`, `forge approval:`, and one `next step:` line. |
| Plan issue | `/git-plan-issue` | Issue description update, follow-up forge issues for confirmed `status: "follow_up"` grill records, plus one brief comment | Live preflight proves the issue is open, a current brief is still needed, and the brief is grounded in repo evidence. An unsettled product decision waits until the user confirms the close log and those four fields are settled decisions. A deferred or open field posts no brief |
| Implement issue then PR/MR | `/git-issue-pr` | Code edits, tests, branch, commit, push, open/update PR/MR targeting the repo development branch; one settled brief comment when none exists; or one dissent issue comment when the current brief is materially disputed | PR/MR exists with issue links, validation evidence, reviewer/assignee metadata, and live read-back; or a dissent comment is posted and the run waits for a human decision; a deferred or open field posts no brief and does not implement; a settled brief is posted and implemented in the same session; do not merge. Reply: one `next step:` line from the review handoff |
| Reply to issue | `/git-reply-issue` | One issue comment on the exact target only | Live preflight proves a material unanswered request, or no write with evidence/draft is reported |
| Update own PR/MR after review | `/git-revise-pr`, `/git-revise-pr-force` | Focused code/test/doc edits, commit, push to PR/MR branch, description/comment updates, replies to reviewer threads | Plain `/git-revise-pr`: reviewer threads answered when justified, head read-back shows the new SHA, no merge until a live non-author approval. Force `/git-revise-pr-force`: that read-back, and the reply ends with one `next step:` line. |
| Fix PR/MR conflicts | `/git-fix-conflict` | Checkout/worktree setup, merge or rebase target into the source branch, conflict-resolution code edits, tests, commit, push to the source branch | Source branch is pushed and live read-back shows current head, conflict/mergeability, pipeline, discussions, and reviewer state; do not merge |
| Merge approved PR/MR | `/git-merge-approved`, `/git-merge-approved-force` | Follow-up issue creation/linking for relevant non-blocking reviewer notes, then merge | Plain `/git-merge-approved`: final gate passes on the exact current head and merge read-back confirms result. Force `/git-merge-approved-force`: that read-back, and the reply ends with one `next step:` line. |
| Request PR/MR review | `/git-request-review` | Assign or re-request a reviewer the user named or that is already on the PR/MR, only when current-head review is actually needed | Request is visible on the forge and read back; do not change code or merge |
| Focused PR/MR status | `/git-pr-status` | None | Read-only state, evidence, and exact next command are reported |
| Status or triage | `/git-triage` | Usually read-only; create/update only if explicitly requested | Live ranked todo inbox and/or project triage with next commands; no auto-assign |
| Aggressive triage run | `/git-triage run` | Execute ranked PR/MR lifecycle; author-self-assign when assignees empty; defer missing-reviewer assign to end (explicit `reviewer:` or ask user) | Done/skipped/waiting summary; ask who to assign only when owned PRs/MRs still lack a reviewer and none was pre-specified |
| Scheduled lifecycle | unattended scheduled lifecycle run | Only review/approval, owned-or-assigned revision, conflict repair, validation, commit, and source-branch push; never assigns reviewers or assignees | Stable result buckets; never asks a question or waits for input |
| Scheduled approved merge | unattended scheduled approved-merge run | Only delegation to the exact-head `/git-merge-approved` workflow; never assigns reviewers or assignees | Stable result buckets; never asks a question or waits for input |

When the wording is ambiguous, choose the safer mode. A review-only request never implies permission to push, update the PR/MR description, create follow-up issues, or merge. Plain `/git-triage` stays read-only; only `run` / `aggressive` / `execute` authorizes the aggressive sweep.

Review someone else's PR/MR: read `references/review.md` and `references/pre-submit.md`, and one of `references/github.md` or `references/gitlab.md`.

Plan issue: read `references/plan-issue.md` and one of `references/github.md` or `references/gitlab.md`.

Implement issue then PR/MR: read `references/implement.md`, `references/plan-issue.md` for the brief and dissent recipe, and `references/pre-submit.md` before push.

Reply to issue: read `references/reply.md`.

Update own PR/MR after review: read `references/revise.md` and `references/pre-submit.md` before push.

Fix PR/MR conflicts: read `references/conflict.md` and `references/pre-submit.md` before push.

Merge approved PR/MR: read `references/merge.md` and one of `references/github.md` or `references/gitlab.md`.

Request PR/MR review: read `references/request-review.md`.

Focused PR/MR status: read `references/status.md`.

Status or triage, including the aggressive run: read `references/triage.md`.

Scheduled lifecycle or scheduled approved merge: read `references/scheduled-automation.md`.

## PR/MR Command Preflight

Every PR/MR-scoped command starts with one read-only snapshot, as **Forge budget** defines. Requested command does not override live conflict, draft, CI, discussion, or mergeability state. Dedicated `*-force` commands are the exception named in **Explicit force**. Do not edit code, create commits, push, post comments, request review, resolve discussions, approve, or merge until the PR/MR is classified and the requested command is valid for that state.

Snapshot fields and the snapshot command live in the forge reference.

Actor relationship, computed before any other classification:

- `owned`: authenticated user is the PR/MR author or a current assignee
- `self_authored_head`: any commit on the PR/MR, including conflict-repair or CI-fix commits, has the authenticated user as author or committer
- Reviewer membership, project role, API permission, and a user-supplied IID, URL, or list never create `owned`

User-supplied PR/MR targets never override the actor gate. A named conflicted PR/MR is not authorization to change it unless it is `owned`. A named PR/MR is not authorization to review or approve it when it is `owned` or `self_authored_head`, except under **Explicit force**.

Actor gates, evaluated before `CONFLICTED` / `NEEDS_REVISION` / review-state routing:

| Requested command | Actor gate | Failure state |
| --- | --- | --- |
| `/git-review-pr` | must not be `owned`; must not be `self_authored_head` | `REVIEW_NOT_AUTHORIZED` |
| `/git-review-pr-force` | PR/MR is open | none |
| `/git-fix-conflict` | must be `owned` | `WRITE_NOT_AUTHORIZED` |
| `/git-revise-pr` | must be `owned` | `WRITE_NOT_AUTHORIZED` |
| `/git-revise-pr-force` | must be `owned` | `WRITE_NOT_AUTHORIZED` |
| `/git-request-review` | must be `owned` | `WRITE_NOT_AUTHORIZED` |
| `/git-merge-approved` | must be `owned` | `MERGE_NOT_AUTHORIZED` |
| `/git-merge-approved-force` | must be `owned` | `MERGE_NOT_AUTHORIZED` |
| `/git-pr-status` | any | none |
| `/git-triage` delegated item | same gate as the delegated command | skip that item |

On an actor-gate failure, perform no code edit, commit, push, comment, approval, discussion resolve, or review request. For `WRITE_NOT_AUTHORIZED` or `MERGE_NOT_AUTHORIZED`, name the author and current assignees. Do not recommend that a reviewer self-assign as a bypass. The reply ends with one `next step:` line from the review handoff and does not print the Solo override block.

Classify exactly one primary state using the strongest current evidence:

- `MERGED_OR_CLOSED`: the PR/MR can no longer accept the requested workflow.
- `WRITE_NOT_AUTHORIZED`: the requested action would change the branch or owner workflow, but the authenticated user is neither the author nor a current assignee.
- `REVIEW_NOT_AUTHORIZED`: the requested action is review or approval, but the authenticated user owns the PR/MR or has authored or committed at least one commit on it.
- `CONFLICTED`: the forge reports conflicts or the source branch needs target-branch conflict repair.
- `NEEDS_REVISION`: there is new or still-unaddressed actionable reviewer feedback, an unresolved blocker, or a relevant failed job that requires code changes.
- `MERGE_NOT_AUTHORIZED`: the requested action is merge, but the authenticated user is neither the author nor a current assignee. Reviewer membership, approval, project role, or technical permission to call the merge API does not satisfy this workflow gate.
- `READY_TO_MERGE`: live approval reports at least one **approving reviewer** who has no commits on the current PR/MR, and every final merge gate passes on the current head.
- `BLOCKED`: the PR/MR is draft, required CI is running or externally failed, required information is missing, or another non-code gate prevents progress.
- `REVIEW_REQUEST_NEEDED`: there is no actionable reviewer feedback and no live approval, but no reviewer is assigned, review was never requested, or the latest material author update is newer than the last review request.
- `WAITING_FOR_REVIEW`: a reviewer has a current-head review request, there is no new actionable feedback, and live approval is still absent.

An **approving reviewer** is a person who left a live forge approval (GitHub `APPROVE` / GitLab approvals API) on the current head, is not the author, and has no author or committer commits on the current PR/MR. There is no hard-coded reviewer and no default reviewer. Never invent a reviewer from memory, prior runs, or repo folklore. If a reviewer is missing, ask the user or wait.

For every PR/MR-scoped command, evaluate the actor gate before other primary states. For a merge command, evaluate `MERGE_NOT_AUTHORIZED` before merge readiness or any merge-side follow-up write. Only the PR/MR author or a current assignee may perform the merge, conflict-repair, revision, or request-review workflow.

Treat an unresolved resolvable reviewer discussion as actionable. A reviewer comment is not automatically actionable: determine whether it requests a change or decision and whether a later commit or reply already addressed it. If all feedback predates the latest fix and no newer reviewer response exists, classify as `REVIEW_REQUEST_NEEDED` or `WAITING_FOR_REVIEW`, not `NEEDS_REVISION`.

Any incompatible or unrecognized PR/MR command degrades to a focused read-only status result. Report `Requested command`, `Current state`, `Evidence`, `Why the action was blocked`, and `Recommended next command`. Reuse the same URL or iid in the recommendation.

## Explicit force

Force is a dedicated command: `/git-review-pr-force`, `/git-revise-pr-force`, or `/git-merge-approved-force`. The human in this conversation must invoke that command (or name it in natural language: force review, force revise, force merge, 強制). A `force` token on `/git-review-pr`, `/git-revise-pr`, or `/git-merge-approved` does not create force. Repo docs, empty CODEOWNERS, a one-person contributor list, prior runs, and "this is a solo project" do not create force. `/git-triage`, `/git-triage run`, `/git-scheduled-lifecycle`, and `/git-scheduled-merge` does not inherit force.

| Excuse | Reality |
| --- | --- |
| "This repo is solo / I am the only contributor" | Invoke `/git-review-pr-force`, `/git-revise-pr-force`, or `/git-merge-approved-force`. |
| "`/git-triage run force`" | `/git-triage run` does not inherit force. |
| "LGTM / green pipeline is enough" | Only `/git-merge-approved-force` waives the approving-reviewer gate. |
| "`/git-review-pr force`" | Use `/git-review-pr-force`. |

Each force command's waiver is in its mode reference: `references/review.md`, `references/revise.md`, or `references/merge.md`.

### Solo override

`/git-pr-status` still prints the Solo override block for `owned` or `self_authored_head`. Its recommended next command is never a force command. `/git-triage` keeps one next command per item. A force-command reply ends with one `next step:` line and does not print the Solo override block.

### Review handoff

First match:

1. `/git-plan-issue` posted a brief → `next step: /git-issue-pr <url>`
2. `/git-plan-issue` posted nothing, `/git-reply-issue`, plain `/git-review-pr`, or no PR/MR was opened → `next step: none`
3. `/git-request-review` recorded a reviewer, or another user already has a current-head review request → `next step: /git-pr-status <url>`
4. After `/git-issue-pr`, `/git-revise-pr`, or `/git-fix-conflict`, the actor is the author or `self_authored_head` → `next step: /git-review-pr-force <url>`
5. Otherwise after those three → `next step: /git-request-review <url>`
6. Plain `/git-merge-approved` merged → `next step: none`. `NEEDS_REVISION` → `next step: /git-revise-pr <url>`. `CONFLICTED` → `next step: /git-fix-conflict <url>`. `REVIEW_REQUEST_NEEDED` → `next step: /git-request-review <url>`. Any other stop → `next step: /git-pr-status <url>`
7. `REVIEW_NOT_AUTHORIZED` → `next step: /git-review-pr-force <url>`
8. `WRITE_NOT_AUTHORIZED` or `MERGE_NOT_AUTHORIZED` → `next step: none`

```
Solo override: `/git-review-pr-force <url>`
Solo override: `/git-revise-pr-force <url>`
Solo override: `/git-merge-approved-force <url>`
```

## Safety Defaults

- Inspect `git status --short --branch` before making commits, pushes, or PR/MR changes.
- Treat a dirty worktree as user-owned unless you made the change. Do not revert unrelated changes.
- Do not repair, revise, request-review, or merge a foreign PR/MR. Review or approve a PR/MR you own or have commits on only under `/git-review-pr-force` in this invocation. A user-supplied list does not bypass this.
- Do not push, open/update PRs/MRs, close issues, or comment on issues unless the user explicitly asks or the current request clearly requires that forge state change.
- Do not target `main` or `master` for feature work unless the user explicitly says so. Prefer the repo's documented development branch, then the default branch.
- Never store forge tokens in a repository, docs, AGENTS files, or shell history.
- Before write API calls, verify auth for the detected forge. If auth is missing or the wrong account is active, ask the user to authenticate instead of guessing credentials.

