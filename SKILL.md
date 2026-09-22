---
name: git-collaboration
description: Use when working with GitHub or GitLab issues, pull/merge requests, reviews, CI, branches, commits, pushes, releases, labels, conflicts, or gh/glab workflows. Trigger especially for reviewing others' PRs/MRs, /git-review-pr-force, /git-merge-approved-force, /git-revise-pr-force, solo self-review, analyzing an issue and posting an implementation brief, implementing an issue and publishing a PR/MR, updating your own PR/MR after reviewer feedback, requesting re-review, fixing conflicts, merging approved PRs/MRs, live status or todo triage, and aggressive triage run sweeps.
---

# Git Collaboration

Use this skill for GitHub or GitLab work that changes repository state or forge state. Read `AGENTS.md` or equivalent repo guidance first when present. Local project instructions may strengthen the merge gate, but must never replace a live non-author approval with reviewer notes, reviewer state, resolved discussions, or a green pipeline. Only `/git-merge-approved-force` in this invocation waives that approval gate.

## Detect the forge

Resolve the forge before any write. The request URL wins, then `git remote -v`:

| Signal | Forge | CLI | Change request |
| --- | --- | --- | --- |
| `github.com`, GitHub Enterprise host, `gh` repo | GitHub | `gh` | Pull request |
| `gitlab.com`, other GitLab host, `glab` repo | GitLab | `glab` | Merge request |

If both remotes exist and the request has no URL, ask which forge to use. Load only the matching forge reference (`references/github.md` or `references/gitlab.md`) for the one-snapshot commands. This file owns the workflow, including **Forge budget** and **Context budget**; those files own forge-specific commands.

In this skill, **PR/MR** means the current forge's change request. Commands below use `/git-*`. Treat `/gitlab-*` and `/github-*` aliases, plus a pasted GitHub or GitLab URL, as the same mode.

## Forge budget

The forge is the mailbox for issue and PR/MR state. The local checkout is the codebase. Every `gh` invocation, `glab` invocation, forge REST call, and GitHub or GitLab MCP call counts. Use one client: `gh` on GitHub, `glab` on GitLab. Do not also query that object through MCP.

A **snapshot** is one read whose payload already contains every forge field that mode needs. Reuse a snapshot already in this conversation when the user has not said that object changed.

1. Resolve the authenticated user once per invocation and reuse that id. Skip a separate auth-status call when the user endpoint or the snapshot already returns the login. Skip a repo-metadata call when the URL or `git remote -v` already names the project.
2. Read each issue or PR/MR once. The command or commands named together in the matching forge reference are that snapshot, not a menu of extra calls. Do not add a call for a field that snapshot already contains.
3. After the snapshot, inspect code, history, diffs, tests, and repo instructions in the local checkout. `git fetch` of the one ref you will check out is allowed; do not fetch again to re-read files. If this checkout is the wrong repo or lacks the cited paths, stop and name the missing path.
4. Draft, classify, and implement from that snapshot plus the checkout. Do not re-query the forge between those steps. Do not read repository files, blame, or trees through the forge.
5. A write is one call. The write response is the read-back when it contains the new comment id, SHA, or state. Confirm with one view only when that response omits a field the stop condition requires. Do not reload comments or files after a successful write.
6. One more full snapshot is allowed immediately before a forge write that depends on the current head, approval, or mergeability, and before each write in an aggressive or scheduled run. That snapshot replaces the earlier one. It is still one call.

Triage lists stay lists. One metadata list per relationship. Classify from that payload. Open one trimmed snapshot only for an item you are about to write, or the one item the user named.

Download one failed job log when a verdict or a fix depends on that log. Keep the failing command and the error lines. Discard the rest of the log. Do not list or download jobs whose conclusions are already in the snapshot.

Related PRs/MRs come from links already in the snapshot. Do not search the forge for them unless the user asked whether a PR/MR exists and the snapshot has no link.

## Context budget

Forge budget limits how often you call the forge. Context budget limits what those calls, and the local reads, put into the conversation. One unfiltered PR/MR or issue payload is enough to blow the context window.

- Run the snapshot command in the forge reference with its `--jq` or `jq` pipe. If the filter errors, fix the filter once. Do not rerun without it, and do not page through raw JSON.
- The issue or PR/MR body stays whole. A comment or review body stays whole when it contains `git-plan-issue`, `git-plan-issue-dissent`, or `git-force-review`, or when it is the latest one. Every other body keeps author, time, id, and the first 400 characters. Also keep review commit OID, discussion resolved state, and commit author login, name, and email. Empty login is not a missing author when name or email is present.
- List calls return metadata only: number, title, state, updated time, author, assignees, url, and for a PR/MR also draft, `reviewDecision`, mergeable, and head SHA. No comment bodies, review bodies, or check logs.
- Do not paste the snapshot, this skill, or source listings into the reply, the posted comment, or the pre-submit subagent. The subagent gets the submit range and the contract. The reply reports the decision fields the mode requires.
- Search, then open the matching symbol and its test. Do not read a directory, a whole unrelated file, or both forge references into context. Load `references/scheduled-automation.md` only for a scheduled mode.
- Reuse the trimmed snapshot already in this conversation. Do not re-read it back into context to "be sure."

## Task Mode Decision

Classify the request before taking action. The mode controls which writes are allowed and which gates must pass.

| Mode | User intent examples | Allowed writes | Stop condition |
| --- | --- | --- | --- |
| Review someone else's PR/MR | `plz review`, `review again`, review a PR/MR URL, `/git-review-pr-force`, solo self-review | Forge review comments, discussion resolution only when re-review proves the blocker is fixed, approve/request changes, or a `<!-- git-force-review -->` comment when self-APPROVE is rejected | Posted visible verdict and read back SHA, pipeline, discussions, and approval/request-changes state |
| Plan issue | `plan this issue`, `analyze issue`, `/git-plan-issue` | One issue comment containing the implementation brief | Live preflight proves the issue is open, a current brief is still needed, and the brief is grounded in repo evidence. An unsettled product decision waits until the user confirms the close log and those four fields are settled decisions. A deferred or open field posts no brief |
| Implement issue then PR/MR | `fix issue #N`, `resolve this issue`, issue implementation work | Code edits, tests, branch, commit, push, open/update PR/MR targeting the repo development branch; one settled brief comment when none exists; or one dissent issue comment when the current brief is materially disputed | PR/MR exists with issue links, validation evidence, reviewer/assignee metadata, and live read-back; or a dissent comment is posted and the run waits for a human decision; a deferred or open field posts no brief and does not implement; a settled brief is posted and implemented in the same session; do not merge |
| Reply to issue | `reply to issue`, answer one issue URL, `/git-reply-issue` | One issue comment on the exact target only | Live preflight proves a material unanswered request, or no write with evidence/draft is reported |
| Update own PR/MR after review | `address reviewer comment`, `fix PR feedback`, `push for re-review`, `/git-revise-pr-force` | Focused code/test/doc edits, commit, push to PR/MR branch, description/comment updates, replies to reviewer threads | Reviewer threads are answered/resolved when justified, PR/MR read-back reflects the new head; do not merge until a live non-author approval is present |
| Fix PR/MR conflicts | `fix conflict`, PR/MR reports conflicts | Checkout/worktree setup, merge or rebase target into the source branch, conflict-resolution code edits, tests, commit, push to the source branch | Source branch is pushed and live read-back shows current head, conflict/mergeability, pipeline, discussions, and reviewer state; do not merge |
| Merge approved PR/MR | `merge PR #N`, `plz merge it`, `/git-merge-approved-force`, `強制合併` | Follow-up issue creation/linking for relevant non-blocking reviewer notes, then merge | Final gate passes on the exact current head and merge read-back confirms result |
| Request PR/MR review | `request review`, `ask reviewer to review again` | Assign or re-request a reviewer the user named or that is already on the PR/MR, only when current-head review is actually needed | Request is visible on the forge and read back; do not change code or merge |
| Focused PR/MR status | `what is this PR waiting for?`, inspect one PR/MR URL | None | Read-only state, evidence, and exact next command are reported |
| Status or triage | `current status`, `todo`, `what should we do next`, `/git-triage` | Usually read-only; create/update only if explicitly requested | Live ranked todo inbox and/or project triage with next commands; no auto-assign |
| Aggressive triage run | `/git-triage run`, `aggressive`, `execute` | Execute ranked PR/MR lifecycle; author-self-assign when assignees empty; defer missing-reviewer assign to end (explicit `reviewer:` or ask user) | Done/skipped/waiting summary; ask who to assign only when owned PRs/MRs still lack a reviewer and none was pre-specified |
| Scheduled lifecycle | unattended scheduled lifecycle run | Only review/approval, owned-or-assigned revision, conflict repair, validation, commit, and source-branch push; never assigns reviewers or assignees | Stable result buckets; never asks a question or waits for input |
| Scheduled approved merge | unattended scheduled approved-merge run | Only delegation to the exact-head `/git-merge-approved` workflow; never assigns reviewers or assignees | Stable result buckets; never asks a question or waits for input |

When the wording is ambiguous, choose the safer mode. A review-only request never implies permission to push, update the PR/MR description, create follow-up issues, or merge. Plain `/git-triage` stays read-only; only `run` / `aggressive` / `execute` authorizes the aggressive sweep.

For either scheduled mode, read `references/scheduled-automation.md` in full before acting. Its scheduled profile overrides interactive aggressive-triage behavior: it never assigns reviewers or assignees and never asks a question or waits for input. Scheduled lifecycle cannot merge or implement issues; Scheduled approved merge cannot review, revise, repair conflicts, or perform preparatory writes.

## Prompt Commands

Use these global prompt commands when available. They intentionally do not define `argument-hint`.

- `/git-review-pr`: review another person's PR/MR and post the visible forge verdict.
- `/git-review-pr-force`: force-review an owned or self-authored PR/MR and post a visible verdict.
- `/git-plan-issue`: analyze one issue against current code, post an implementation brief with acceptance criteria, and stop without implementing.
- `/git-issue-pr`: implement a GitHub or GitLab issue, validate it, push, and open/update the PR/MR.
- `/git-revise-pr`: address reviewer feedback on an existing PR/MR and push for re-review.
- `/git-revise-pr-force`: force-revise an owned PR/MR without waiting for `NEEDS_REVISION`.
- `/git-fix-conflict`: resolve PR/MR source-branch conflicts and push for re-review.
- `/git-merge-approved`: merge a specific approved PR/MR only after live final gates pass.
- `/git-merge-approved-force`: force-merge an owned PR/MR after remaining technical gates pass.
- `/git-request-review`: request review or re-review only when the current head needs it.
- `/git-pr-status`: inspect one PR/MR read-only and report its current state and exact next command.
- `/git-triage`: default personal todo inbox, project-scoped triage, or aggressive `run` mode.
- `/git-scheduled-lifecycle`: run the non-interactive scheduled lifecycle capability boundary.
- `/git-scheduled-merge`: run scheduled approved merge by delegating only to the exact-head approved-merge workflow.
- `/git-reply-issue`: inspect one issue conversation and post a focused response only when a material reply is still needed.

## PR/MR Command Preflight

Every PR/MR-scoped command starts with one read-only snapshot, as **Forge budget** defines. Requested command does not override live conflict, draft, CI, discussion, or mergeability state. Dedicated `*-force` commands are the exception named in **Explicit force**. Do not edit code, create commits, push, post comments, request review, resolve discussions, approve, or merge until the PR/MR is classified and the requested command is valid for that state.

The snapshot covers:

- PR/MR state, draft status, current head SHA, source/target branches, author, assignees, requested reviewers, and current user relationship; resolve the authenticated forge user and compare stable user IDs or usernames rather than display names
- commit SHAs and authors from the trimmed snapshot, not commit message bodies; record whether any commit author or committer matches the authenticated user
- live approval evidence from the forge (see `references/github.md` / `references/gitlab.md`); use branch-protection or approval-rule counts only as supporting evidence
- latest pipeline/checks and required jobs, conflict and mergeability state, and whether blocking discussions are resolved
- all unresolved discussions, latest non-system reviewer comments, latest author replies, and whether feedback was addressed by a later commit
- latest material author update on the current head and latest review-request event, so a request made before a newer push is not treated as current

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

On an actor-gate failure, perform no code edit, commit, push, comment, approval, discussion resolve, or review request. Report `Requested command`, `Current state`, `Actor`, `Evidence`, `Why the action was blocked`, and `Recommended next command`. For `WRITE_NOT_AUTHORIZED` or `MERGE_NOT_AUTHORIZED`, name the author and current assignees and tell them to run the command; do not recommend that a reviewer self-assign as a bypass. For `REVIEW_NOT_AUTHORIZED` on an owned PR/MR, recommend `/git-request-review` and print the Solo override lines. For `REVIEW_NOT_AUTHORIZED` because of `self_authored_head`, recommend another reviewer and `/git-pr-status`, and print the Solo override lines.

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

Command routing:

| Requested command | Allowed primary state | Otherwise |
| --- | --- | --- |
| `/git-review-pr` | not `REVIEW_NOT_AUTHORIZED`, and the PR/MR is open | Stop without posting review feedback. For `REVIEW_NOT_AUTHORIZED`, do not approve. Recommend `/git-request-review` when the user owns the PR/MR, or another reviewer plus `/git-pr-status` when `self_authored_head`. Print Solo override. |
| `/git-review-pr-force` | the PR/MR is open | Stop without posting review feedback. `MERGED_OR_CLOSED` stays blocked. |
| `/git-merge-approved` | `READY_TO_MERGE`, and the authenticated user is the author or a current assignee | Stop. For `MERGE_NOT_AUTHORIZED`, report that only the author or an assignee may merge. Otherwise recommend `/git-revise-pr` for `NEEDS_REVISION`, `/git-fix-conflict` for `CONFLICTED`, `/git-request-review` for `REVIEW_REQUEST_NEEDED`, or `/git-pr-status` plus waiting guidance for `WAITING_FOR_REVIEW`/`BLOCKED`. Print Solo override when the remaining gate is a second-person reviewer. |
| `/git-merge-approved-force` | `owned`, open, not draft, not `CONFLICTED`, not `NEEDS_REVISION`, required CI passing or explained, blocking discussions resolved, exact current head | Stop. `MERGE_NOT_AUTHORIZED` still blocks. Remaining technical gates still block. |
| `/git-revise-pr` | `NEEDS_REVISION`, and the authenticated user is the author or a current assignee | Stop without editing. For `WRITE_NOT_AUTHORIZED`, name the author or assignee. Recommend `/git-request-review`, `/git-merge-approved`, `/git-fix-conflict`, or waiting plus `/git-pr-status` according to state. Print Solo override for `/git-revise-pr-force`. |
| `/git-revise-pr-force` | `owned`, open, not `CONFLICTED`, not `MERGED_OR_CLOSED` | Stop without editing. `WRITE_NOT_AUTHORIZED` still blocks. Conflicts still go to `/git-fix-conflict`. |
| `/git-fix-conflict` | `CONFLICTED`, and the authenticated user is the author or a current assignee | Stop without changing the branch. For `WRITE_NOT_AUTHORIZED`, name the author or assignee and do not repair a foreign PR/MR even when the user named it. Otherwise recommend the command matching the classified state. |
| `/git-request-review` | `REVIEW_REQUEST_NEEDED`, and the authenticated user is the author or a current assignee | Do not create a duplicate request. For `WRITE_NOT_AUTHORIZED`, name the author or assignee. Recommend `/git-revise-pr`, `/git-merge-approved`, or waiting according to state. |
| `/git-pr-status` | Any | Remain read-only and report the state and next command. The recommended next command must itself pass the actor gate; never recommend `/git-fix-conflict`, `/git-revise-pr`, `/git-request-review`, or `/git-merge-approved` for a foreign PR/MR, and never recommend `/git-review-pr` for an owned or `self_authored_head` PR/MR. Print Solo override when waiting on a second-person reviewer. |

Any incompatible or unrecognized PR/MR command degrades to a focused read-only status result. Report `Requested command`, `Current state`, `Evidence`, `Why the action was blocked`, and `Recommended next command`. Reuse the same URL or iid in the recommendation so it can be invoked directly.

## Explicit force

Force is a dedicated command: `/git-review-pr-force`, `/git-revise-pr-force`, or `/git-merge-approved-force`. The human in this conversation must invoke that command (or name it in natural language: force review, force revise, force merge, 強制). A `force` token on `/git-review-pr`, `/git-revise-pr`, or `/git-merge-approved` does not create force. Repo docs, empty CODEOWNERS, a one-person contributor list, prior runs, and "this is a solo project" do not create force. `/git-triage`, `/git-triage run`, `/git-scheduled-lifecycle`, and `/git-scheduled-merge` does not inherit force.

| Excuse | Reality |
| --- | --- |
| "This repo is solo / I am the only contributor" | Invoke `/git-review-pr-force`, `/git-revise-pr-force`, or `/git-merge-approved-force`. |
| "`/git-triage run force`" | `/git-triage run` does not inherit force. |
| "LGTM / green pipeline is enough" | Only `/git-merge-approved-force` waives the approving-reviewer gate. |
| "`/git-review-pr force`" | Use `/git-review-pr-force`. |

### `/git-review-pr-force`

Waives the review actor gate (`owned`, `self_authored_head`). The PR/MR must still be open. Run the structured file pass and post a visible verdict. If the forge rejects a self-APPROVE, post a current-head comment that starts with `<!-- git-force-review -->` and names the SHA; native approval remains absent. Force review does not merge.

### `/git-revise-pr-force`

The authenticated user must still be the author or a current assignee. The PR/MR must still be open and not `CONFLICTED`. Force waives the `NEEDS_REVISION` state gate so further commits can land without actionable reviewer feedback. Run the **pre-submit gate**. Do not merge.

### `/git-merge-approved-force`

The authenticated user must still be the author or a current assignee. The PR/MR must still be open, not draft, free of conflicts, have required CI success or an explicit acceptable explanation, have blocking discussions resolved, and match the exact current head. Force waives the live non-author approving-reviewer requirement. Merge through the forge with the exact-head SHA. If branch protection rejects the merge, report the forge error. Add `admin` in the same invocation only when the user asked to bypass protection; then GitHub may use `gh pr merge --admin`.

### Solo override

`/git-pr-status` default next command still follows the actor gate. Force is never the default recommended next command. When the PR/MR is `owned` or `self_authored_head`, also print:

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
- Prefer `gh` on GitHub and `glab` on GitLab when available.
- Before write API calls, verify auth for the detected forge. If auth is missing or the wrong account is active, ask the user to authenticate instead of guessing credentials.

## Project Orientation

Derive project identity from the repo remote or local instructions. Use the matching forge reference for encoded paths, numeric IDs, and identity APIs.

For a sibling backend/frontend repository, confirm the actual project exists before creating cross-project issues or links.

## Issue Creation

Before creating an issue, search open issues for duplicates. Follow repo-local label conventions when they exist. Typical structured sets use one area, one type, one priority, and optional status.

Issue descriptions should include background/problem, impact, expected behavior, suggested implementation direction, upstream dependency when relevant, acceptance criteria, and related PR/MR or issue links.

## Markdown Descriptions

Never create issue/PR/MR descriptions by embedding literal `\n` in a quoted shell string. Use a heredoc or a file so the forge receives real newlines. Spot-check the write response body for literal backslash-n sequences. Do not view the issue again for that check.

## Cross-Repo Dependencies

When work in one repo needs support in another:

1. Create the dependency issue in the other repo.
2. Mark the blocked issue with the repo's blocked/upstream status when it cannot proceed.
3. Link the issues through the forge's issue-link API when available.
4. Mention the dependency explicitly in the blocked issue and any PR/MR description.

Use the compatible default link type for that forge. If blocker link types exist, use them; otherwise keep a relates-to link and rely on labels/description for blocking status.

## Opening PR/MRs

- Do not open or update PRs/MRs unless requested.
- For issue implementation work, after the fix is implemented, validated, and committed on a dedicated branch, pushing and opening/updating the PR/MR is part of the requested workflow unless repo-local instructions say otherwise.
- Creating or updating a PR/MR is not permission to merge it.
- Preserve existing description content; append concise sections rather than replacing useful reviewer context.
- Known limitations should be explicit.
- Opening or updating a PR/MR, and any source-branch push from `/git-issue-pr`, `/git-revise-pr`, `/git-revise-pr-force`, `/git-fix-conflict`, or scheduled lifecycle, requires the **pre-submit gate** below.

## Structured file review

**REQUIRED SUB-SKILL:** `open-code-review-delegate` owns preview, rules, diffs, coverage, and finding shape. **REQUIRED SUB-SKILL for pre-submit:** `requesting-code-review` owns dispatching a **fresh subagent** with no implementer history; that reviewer runs `open-code-review-delegate`. This skill owns when to call them, how findings map onto forge comments, and the pre-submit gate.

### File pass

After the actor gate and a current-head checkout (or the intended local submit range):

1. Run `open-code-review-delegate` for the merge-base / target..head range. Include uncommitted files only when they are part of this submit.
2. Pass the issue brief, acceptance criteria, or PR/MR description with `--background`.
3. Account for every `reviewable_files` entry as reviewed or skipped with a reason.

Missing `ocr`, failed `preview`/`rule`, or incomplete coverage is a failed file pass.

### `/git-review-pr` mapping

The current reviewer runs the file pass on this checkout after the actor gate. Do not dispatch an implementer-session self-review as a substitute.

| OCR severity | Forge action |
| --- | --- |
| critical, high | Blocking inline discussion on the changed line |
| medium | Blocking when the finding is correctness, security, a broken contract, or missing required validation; otherwise a non-blocking follow-up comment |
| low | Omit unless thorough-review is on |

OCR coverage belongs in the review evidence. **OCR Step 7 Fix stays off.** Local workflow stays read-only except forge review writes. OCR findings do not by themselves approve or request changes. Continue CI, evidence-class, remaining-gate, and verdict rules after the file pass. A failed file pass: post no approve; treat the coverage failure as a blocker.

### Pre-submit gate

Applies before push and before opening or updating a PR/MR on `/git-issue-pr`, `/git-revise-pr`, `/git-revise-pr-force`, `/git-fix-conflict`, and scheduled lifecycle source-branch push.

1. Finish `verification-before-completion` for tests and claimed validation.
2. Dispatch a fresh subagent through `requesting-code-review`. That reviewer runs `open-code-review-delegate` on the intended submit range. Pass the range and the contract, not this skill and not the forge snapshot.
3. Critical and High findings are submit blockers until each is fixed in the tree or waived.
4. A waiver is valid only when the **human in this conversation** names the path, the issue, and a reason. **Blanket ship language is not a waiver.** The agent does not waive. Unattended scheduled runs have no human in the conversation, so they cannot waive.
5. Record each waiver in the commit body or PR/MR description.
6. After fixes, run the file pass again on the new range until no unwaived Critical/High remain.
7. A failed file pass, leftover unwaived Critical/High, or a missing waiver record → do not push, do not open or update the PR/MR.

Medium and Low do not block submit. Mention them in the PR/MR description when useful.

| Excuse | Reality |
| --- | --- |
| "I'll review the diff myself" | File pass is OCR coverage via `open-code-review-delegate`. |
| "ocr isn't installed, skip review" | Missing `ocr` is a failed file pass. |
| "Tests passed so the diff is fine" | `verification-before-completion` is not the file pass. |
| "I'll waive this High finding" | Only the human in this conversation waives, with path + issue + reason. |
| "Ship it / LGTM" | Blanket ship language is not a waiver. |
| "I wrote this code, I know it's correct" | Pre-submit uses a fresh subagent. |
| "Scheduled run, no one to waive, push anyway" | Unattended runs cannot waive; leftover Critical/High stops the push. |

## Review Workflow

When the user asks to review a GitHub or GitLab PR/MR, treat that as permission to post the review result unless repo-local instructions say otherwise. Keep review-only work read-only: do not push, merge, update the description, or create follow-up issues unless the user explicitly asks.

Run the actor gate first. Do not review or approve a PR/MR that is `owned` or `self_authored_head` unless this invocation is `/git-review-pr-force`. Classify `REVIEW_NOT_AUTHORIZED` and stop without posting a verdict. Reviewer assignment plus a named IID does not authorize self-review. Under `/git-review-pr-force`, continue with the file pass and verdict.

For `review again`, take one new snapshot instead of continuing from the old verdict. If there is no new head or no relevant new evidence after a prior blocker, report that the PR/MR is still waiting on the same blocker instead of manufacturing a fresh verdict.

Use the current head, not remembered diffs. If the main checkout is dirty, behind, or belongs to a different repo, review in a temporary clone or detached worktree. Do not push review-only branches.

Run the structured file review pass (`open-code-review-delegate`) on that head, map findings with the `/git-review-pr` mapping, then continue the layers below. OCR Step 7 Fix stays off.

Review in this order:

1. Code behavior and user-visible/API behavior.
2. Tests and missing coverage for changed behavior.
3. Docs, generated types, schemas, and frontend/backend contracts.
4. CI, pipeline artifacts, deployment, and environment risks. Separate required PR/MR jobs from a named live job. Agents must not treat a generic verify job as named live-job success.

For forge-facing review text, match the issue/PR language or the repo's documented language. Keep comments concrete enough for the author to fix without a follow-up question.

Review comments must be specific, clear, and actionable. Each finding should name the concrete problem or open question, its impact and whether it blocks merge, the expected fix direction or decision needed, and the validation, test, command, or evidence required before re-review. When multiple findings exist, use concise bullets or a Markdown table such as `Item`, `Impact`, `Required action`, and `Validation`.

Blocking versus non-blocking:

- Block for regressions, broken contracts, misleading docs about active behavior, missing required validation, unresolved prior blockers, failed relevant CI, or risks that can affect correctness, security, deployment, or operations.
- Do not block for cleanup-only, style-only, or backlog-level suggestions unless the user asks.
- Put blockers in unresolved inline diff discussions on the exact changed line when possible.
- Put non-blocking findings in a concise PR/MR comment marked as follow-up or optional.

Evidence class. Every approve or block verdict must label the strongest evidence used. Classes, strongest first:

| Class | Meaning |
| --- | --- |
| live job / real artifact bytes | Named live job or inspected artifact bytes |
| executable unit tests | Tests that actually run the behavior |
| source-contract / regex tripwire | String or schema lock, not runtime proof |
| docs alignment | Text matches intended policy |

Approve must not treat tripwire as live proof. A policy change that keeps old host config must say in the verdict that testing scope shrinks.

Thorough-review triggers in the user text or invocation arguments include thorough, don't rubber-stamp, 徹底, 抓出來, and 不要放水. Thorough review does not promote style to blocking. It must put remaining gates, policy cost, and the evidence class in the verdict main table, and must not hide remaining gates in a non-blocking note.

A regex tripwire on an install or deploy command is not package-manager or runtime proof; a named live job that actually performs that step remains a remaining gate.

Approval rules:

- Never approve from a snapshot taken before the file pass. Immediately before approve, one snapshot must show the same head SHA you reviewed. Approve only that SHA.
- Do not approve if the PR/MR is `owned` or `self_authored_head`, except under `/git-review-pr-force`. Under force, try native approve; if the forge rejects a self-APPROVE, post `<!-- git-force-review -->` on the current SHA.
- Do not approve if any active blocker remains unresolved, blocking discussions are unresolved, or relevant CI is failed/unknown without a clear non-code explanation.
- An approve or block note must list the claimed live job and whether it appeared on the current head pipeline. If it did not run, the verdict must name the remaining gate and must not write the defect as closed.
- Do not require rerunning a protected live job before approval.

For re-review, take one new snapshot of head SHA, discussions, approvals, and pipeline. Verify each previously posted blocker against the local checkout of that SHA, or against CI evidence already in the snapshot, before resolving it or approving. Do not resolve a blocker based only on the author's explanation.

When the PR/MR claims to fix a named failed job or issue, also walk that job's remaining path. Checking previously posted blockers is not enough to approve.

1. Download the claimed failed job's log once. Keep the failing command and the error lines, then walk the script locally. Do not keep the rest of the log.
2. From the failing line, walk the remaining job script and its adjacent layers.
3. If the new commit changed only one layer, still check N-1 / N+1 on the same path.
4. If those adjacent layers of the claimed failed job script have not been walked, must not approve.

After posting blockers or approval, the write response is the read-back. Report current SHA, pipeline, unresolved blocker count, and whether approval is recorded. One confirm view only when the write response omits one of those fields.

## Focused PR/MR Status Workflow

Use this when the user asks about one PR/MR, supplies a URL or iid without a valid action, or invokes `/git-pr-status`.

Keep the command read-only. Run the PR/MR command preflight, classify the primary state, and report `Current state`, `Head and gates`, `Evidence`, and `Recommended next command`. Do not post a status comment to the forge. Recommended next commands must pass the actor gate. Print Solo override when the PR/MR is `owned` or `self_authored_head`.

## Status Triage Workflow

Use this when the user asks what can be handled now, asks for project status, asks for a personal todo list, or invokes `/git-triage` without `run` / `aggressive` / `execute`.

Keep this mode read-only unless the user explicitly chooses a follow-up action. Resolve the authenticated forge user first. Do not auto-assign issues or PRs/MRs. Never suggest self-assignment only to unlock merge. Never invent a reviewer.

Mode selection (same rules as the `git-triage` prompt):

- **Todo triage** (default): empty args, or `todo` / `mine` / `inbox`.
- **Project triage**: `project` / `this repo` / a forge project URL or path.
- **Aggressive run**: args contain `run` / `aggressive` / `execute`.
- If both todo and project markers appear, prefer project when a concrete project target is present; otherwise prefer todo.

### Todo triage workflow

Build a forge-global personal inbox from metadata lists only: one for notifications or todos, one for PRs/MRs where the user is a reviewer, one for PRs/MRs where the user is author or assignee, and one for open issues assigned to or authored by the user. Context budget defines the fields. Do not request comment or review bodies on a list.

Treat notifications as signals, not conversational source of truth. Another user speaking last is necessary but insufficient to require a reply. Rank from list fields. If a row still cannot be classified, take one trimmed snapshot of that one item, and only when it is in the top three you might recommend.

Classify into Ready to review, Ready to fix conflicts, Ready to revise, Ready to merge, Merge handoff needed, Ready to reply, Acknowledge or route, No reply needed, Needs semantic review, Ready to implement, Review request needed, and Waiting or blocked. A named foreign conflicted PR/MR is `WRITE_NOT_AUTHORIZED`, not ready to fix.

Ready to implement: open issues assigned to me that are not blocked, not already covered by an active PR/MR, and have a current `<!-- git-plan-issue -->` brief whose Goal, Recommended change, Out of scope, and Acceptance criteria contain no unsettled product decision. When none exists, or an unsettled product decision remains, recommend `/git-plan-issue` with the exact issue URL. An unresolved `<!-- git-plan-issue-dissent -->` waits for a human decision. `/git-triage` does not load `gentle-grill-me`.

Report each actionable item with reason, live evidence, remaining gate, and exact next command. End with a compact top three and ask which item to handle next.

### Project triage workflow

Scope to the current repository's forge project, or the project URL/path supplied in arguments. One metadata PR/MR list and one metadata issue list. Do not open each row. Apply the same relationship model inside the selected project. Include sibling repositories only when repo-local instructions identify them or the user asks.

Add hygiene buckets **Needs reviewer** and **Needs assignee**. Do not auto-assign. Prefer `/git-request-review` when the user owns the PR/MR; otherwise report who should request review. A list row has no comment body, so do not call an issue Ready to implement from the list. Recommend `/git-issue-pr` only after a trimmed snapshot shows a settled current brief. Until then the next command is `/git-plan-issue` with the exact issue URL. `/git-triage` does not load `gentle-grill-me`. Mention `/git-issue-pr` only after ownership is clear.

Suggested commands include `/git-review-pr`, `/git-revise-pr`, `/git-fix-conflict`, `/git-request-review`, `/git-pr-status`, `/git-plan-issue`, `/git-issue-pr`, `/git-merge-approved`. End with a compact top-three recommendation and ask which item to handle next.

## Aggressive Triage Run

Use this when the user invokes `/git-triage run` (aliases `aggressive` / `execute`).

1. Resolve authenticated forge user and triage scope. Honor modifiers: `no-merge`, `merge-only`, `include-drafts`, `with-issues`, `dry-run`, and optional explicit `reviewer:USERNAME` (a user-chosen username, no hard-coded reviewer). `/git-triage run` does not inherit force.
2. Classify with the matching read-only triage workflow first. If `dry-run`, stop after listing planned actions; no writes. This mode may surface reply candidates but must not auto-post issue replies; use `/git-reply-issue` separately. It may surface issues that still need an implementation brief but must not auto-post those briefs; use `/git-plan-issue` separately.
3. Capture any **explicit** reviewer from args. Do not silently invent a reviewer from memory or hard-coded names. Repo-local docs may inform later suggestions but must not auto-assign without the user stating a reviewer for this run.
4. **Assignee hygiene (early):** for open PRs/MRs where the authenticated user is the **author** and **empty assignees**, set assignee to the authenticated user. Do not assign yourself on PRs/MRs you did not author. Do not replace an existing non-empty assignee list.
5. Execute the complete lifecycle unless `merge-only`: Ready to review → `/git-review-pr`; owned conflicts → `/git-fix-conflict`; owned revision → `/git-revise-pr`; owned Ready to merge → `/git-merge-approved` (skip when `no-merge`); owned PRs/MRs that already have a reviewer and only need current-head re-request → `/git-request-review`.
6. **Defer missing-reviewer hygiene to the end.** If the user already specified `reviewer:USERNAME`, assign that reviewer and request review. If no reviewer was specified, list those PRs/MRs and **ask who to assign**. Wait for the user's answer; do not guess.
7. Before every write, take one new snapshot and re-run the PR/MR command preflight. Live state overrides the triage list. Do not issue a call per field.
8. Do not auto-implement issues unless `with-issues` is present.
9. Prefer isolated worktrees when local checkouts are dirty or belong to another branch/repo.
10. After the sweep, report each item as done / skipped / waiting with evidence.

## Focused Issue Reply Workflow

Use this only when the user explicitly invokes `/git-reply-issue` or clearly asks to post a response to one exact issue. The write scope is one issue comment on the exact target; do not change code, commits, branches, labels, assignees, issue state, description, links, or any other forge object.

1. Resolve the exact project/issue. Reuse the authenticated user already resolved for this invocation.
2. Take one issue snapshot: state, description, labels, assignees, links on that payload, marker comments, and the latest non-system comments. The latest body stays whole.
3. Identify the latest material request, the latest material response by the authenticated user, and any later response or state change that superseded it. Draft from that snapshot and repo-local instructions in the checkout.
4. Classify the response as a decision, requested information, acknowledgment, routing, or `No reply needed`.
5. Post one issue comment only when a material unanswered request remains.
6. The write response is the read-back. Report the new comment id/time, current state, assignees, and remaining owner or blocker from that response and the snapshot. Do not view the issue again when the response includes the comment id.

Do not post a duplicate response. Ambiguous product decisions stop with a draft and a request for user direction; write nothing.

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

## Issue Implementation To PR/MR

Use this when the task is to fix or implement a GitHub or GitLab issue.

1. Read repo-local instructions, inspect local status, and take one issue snapshot: state, description, labels, assignees, links on that payload, marker comments, and the latest non-system comments. The latest body stays whole. Related PRs/MRs are only those links. Then inspect the local checkout. Do not read the issue again while implementing.
2. If the issue has assignees and the authenticated user is not among them, stop without implementing or posting a dissent. Unassigned issues may be implemented.
3. Collect the current proposal from that live evidence. If a current comment contains `<!-- git-plan-issue -->` and later comments have not superseded its Goal / Recommended change / Out of scope / Acceptance criteria, that comment is the current brief. A description with no current brief is not an implementation contract. A `<!-- git-plan-issue-dissent -->` stays unresolved until a human decision or a newer brief supersedes it. A human decision is a later non-system comment, a newer `<!-- git-plan-issue -->` brief, or explicit direction in this invocation that selects the original brief, the posted alternative, or a third way. The invoking user's explicit choice is final.
4. If an unresolved dissent exists and this invocation carries no human decision, perform no code edit and post no duplicate dissent. Report the dissent comment id and wait.
5. Inspect the relevant current code and evaluate the current brief. Material disagreement is a conflict on Goal, Recommended change shape, Out of scope, or Acceptance criteria. Names, extra tests, and equivalent structure inside that shape stay on the agree path. Use the Plan Issue Workflow meaning of unsettled product decision.
6. If no current brief exists, draft one with Plan Issue Workflow steps 5 and 6. When Goal, Recommended change, Out of scope, and Acceptance criteria are already settled, post that brief without loading `gentle-grill-me` and without waiting for a close log, then continue from step 8 in this session. Load `gentle-grill-me` only when an unsettled product decision remains. After the user confirms the close log, rewrite those four fields from settled log entries only. If any field is still deferred or open, post nothing and do not implement. Do not post a brief while an unsettled product decision remains. When those four fields are settled decisions, post the brief in this same session, then continue from step 8. The local grill log is not the issue comment. Do not ask the user to invoke `/git-issue-pr` again. Plan step 7's next-command line does not end this invocation.
7. On material disagreement with a settled brief, post one issue comment using this recipe, then stop without editing code:

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

8. When the implementer agrees with the settled brief, or a human decision has settled the original brief, the posted alternative, or a third way, treat that note as the implementation contract. Report the comment id that supplied the contract, or that this invocation selected the third way, before editing code.
9. Start from the current development branch unless repo-local instructions say otherwise. Create a dedicated feature branch; do not implement directly on the default or documented development branch.
10. Use TDD when practical: add or update a focused failing test first for bug fixes or behavior changes, then implement the smallest reasonable fix.
11. Validate with the relevant focused tests and broader checks proportional to risk, including the contract's Acceptance criteria.
12. Commit with a focused conventional-style message and reference the issue.
13. Run the **pre-submit gate**. Stop before push if Critical/High remain unfixed and unwaived.
14. Push the branch and open or update a PR/MR targeting the development branch when this is part of the issue workflow.
15. Keep the PR/MR description current: summary, issue link, validation evidence, known limitations, reviewer/assignee metadata when available, and any pre-submit waivers.
16. The create or update response is the read-back. Report iid, URL, current head SHA, pipeline state, issue link, and reviewer/assignee state. One confirm view only when that response omits iid, URL, or head SHA.

Do not merge the PR/MR unless the user separately asks for that merge and the merge gate below passes.

## Updating An Existing PR/MR

Use this when addressing reviewer feedback on a PR/MR you authored or are maintaining.

1. Run the PR/MR command preflight and continue only when the PR/MR is `owned` and either the primary state is `NEEDS_REVISION` or this invocation is `/git-revise-pr-force`. If `WRITE_NOT_AUTHORIZED`, stop without editing.
2. Use the preflight snapshot as the PR/MR record: discussions, latest reviewer comments, source branch, target branch, head SHA, and pipeline. Do not snapshot it again before the push.
3. Identify which comments are blocking, which are non-blocking, and which need a separate tracker. Inspect the source branch in the local checkout.
4. Work on the source branch in a clean checkout or isolated worktree if the main checkout has unrelated changes.
5. Implement focused fixes and add or update tests for behavior changes.
6. Commit on the PR/MR branch, preserving unrelated user work. Run the **pre-submit gate**. Stop before push if Critical/High remain unfixed and unwaived. Then push.
7. Reply to reviewer threads with what changed and validation evidence. Resolve a thread only after the new code actually addresses it.
8. Update the description when validation evidence, known limitations, or issue mappings changed.
9. The push and thread-reply responses are the read-back for head, pipeline, unresolved discussions, and reviewer state. One confirm view only when those responses omit the new head SHA.

If there is no new or unaddressed actionable reviewer feedback and this invocation is `/git-revise-pr`, do not edit, commit, push, or manufacture an update. Under `/git-revise-pr-force`, continue with the owned source-branch update and the **pre-submit gate**.

After pushing fixes, still do not merge until live approval reports an approving reviewer on the current head, or the user separately invokes `/git-merge-approved-force`. Reviewer comments such as `LGTM`, `approved`, or `looks good` are useful context but are not approval evidence.

## Request PR/MR Review

Use this when the user invokes `/git-request-review` or explicitly asks to request review or re-review.

1. Run the PR/MR command preflight and continue only when the primary state is `REVIEW_REQUEST_NEEDED` and the PR/MR is `owned`.
2. Identify the reviewer from an explicit user username, a reviewer already requested on the PR/MR, or CODEOWNERS only as a list to present. If it is ambiguous, stop and ask who to assign instead of guessing. Never invent a reviewer. Do not request yourself as reviewer of a PR/MR you own or have commits on.
3. Prefer the forge's native request-review operation. The write response is the read-back for reviewer assignment, current head SHA, approval state, and discussions. One confirm view only when that response omits the reviewer or the head SHA.

Do not change code or merge. Do not send a duplicate request when a current-head request is already pending.

## Fix PR/MR Conflicts

Use this when the user asks to fix a conflict or invokes `/git-fix-conflict`.

1. Run the PR/MR command preflight and continue only when the primary state is `CONFLICTED` and the PR/MR is `owned`. If `WRITE_NOT_AUTHORIZED`, stop without changing the branch even when the user named this PR/MR.
2. Read repo-local instructions, inspect `git status --short --branch`, and use the preflight snapshot as the PR/MR record. Do not snapshot it again before the push.
3. Confirm the write boundary is only the source branch.
4. Work in a clean checkout or isolated worktree when the main checkout has unrelated changes.
5. Check out the source branch tracking origin. Prefer a non-rewriting merge of the target branch into the source branch unless repo-local instructions explicitly prefer rebase.
6. Resolve conflict markers deliberately by preserving the PR/MR intent and current target-branch behavior.
7. Run focused tests, formatters, builds, or generation checks proportional to the conflicted areas.
8. Commit with the repo's normal style. Run the **pre-submit gate**. Stop before push if Critical/High remain unfixed and unwaived. Then push the source branch.
9. The push response is the read-back for the new head SHA. One confirm view only when it omits head SHA, conflict or mergeability state, pipeline, unresolved discussions, or reviewer state. Bundle any missing fields into that one view.

After resolving conflicts, still do not merge until live approval reports an approving reviewer on the current head, or the user separately invokes `/git-merge-approved-force`.

## Merge Approved PR/MR

Use this only when the user explicitly asks to merge a specific PR/MR, or when `/git-triage run` reaches an owned item whose live primary state is `READY_TO_MERGE` (unless `no-merge` was requested). `/git-triage run` does not inherit force.

Before merging:

1. Run the PR/MR command preflight and continue only when the primary state is `READY_TO_MERGE`, or when this invocation is `/git-merge-approved-force` and the remaining gates in **Explicit force** pass.
2. Resolve the authenticated forge user. Continue only when this user is the PR/MR author or a current assignee. If neither matches, classify `MERGE_NOT_AUTHORIZED` and stop before any merge-side write.
3. The preflight snapshot is the merge gate when no forge write has happened since it. If a follow-up issue was created after that snapshot, replace it with one snapshot immediately before the merge. Do not take both by habit. Duplicate-check follow-up issues with one search only when you are about to create one.
4. Verify live approval from that snapshot. Without force, the approval gate passes only when at least one approving reviewer is present on the current head. Branch-protection or approval-rule zeroes must not override a missing live approval. `/git-merge-approved-force` waives this approving-reviewer check.
5. From that snapshot, read the latest reviewer comments for relevant non-blocking suggestions. Duplicate-check and create/link follow-up issues before the merge when repo-local instructions require tracking.
6. Run the final gate on the exact current head:
   - authenticated user is still the author or a current assignee
   - reviewed head SHA still matches current head SHA
   - required pipeline/jobs are success or have an explicit acceptable explanation
   - blocking discussions are resolved
   - live approval is present for the current head, or this invocation is `/git-merge-approved-force`
   - without force, every approving reviewer has no author or committer commits on the current PR/MR
   - no conflicts or merge status blockers remain
7. Merge through the forge. The merge command result is the read-back of PR/MR state. One confirm view only when that result omits merged state or the target SHA. If branch protection rejects the merge, report the forge error. Use GitHub `--admin` only when the same invocation also contains `admin`.

Never use reviewer comments, discussion text, `LGTM`, `approved`, reviewer state, resolved discussions, rule zeroes without an approving reviewer, or a green pipeline as a substitute for the live approval gate. Only `/git-merge-approved-force` in this invocation waives that gate.

If the actor gate fails, stop and identify the author and current assignees. State that one of them must invoke `/git-merge-approved` for the same PR/MR; do not recommend that a reviewer self-assign merely to bypass the gate.

## Commits

- Use focused, conventional-style commit messages.
- Reference issue IDs when applicable.
- Use forge closing keywords only when automatic closing on the target branch is desired and understood.
- Include validation in the commit body or PR/MR description when useful.

## CI And Review

For failing CI:

- Use check conclusions already in the snapshot. Download one log for the failing job, keep the failing command and the error lines, and drop the rest.
- Distinguish forge-native jobs from external providers.
- Summarize failure context before implementing fixes.
- Do not install forge tooling with system package managers unless the user asks.

For review feedback that becomes tracked work later, separate immediate code changes from backlog/process items.
