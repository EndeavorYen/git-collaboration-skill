---
name: git-collaboration
description: Use for GitHub or GitLab collaboration: planning or implementing an issue, reviewing, revising, conflict-repairing, or merging a pull/merge request, its CI, review requests, issue replies, triage, a pasted issue or PR/MR URL, and any /git-* command. Local-only git (commit, branch, stash, log, diff) does not need this skill.
---

# Git Collaboration

## Detect the forge

Resolve the forge before any write. The request URL wins, then `git remote -v`:

| Signal | Forge | CLI | Change request |
| --- | --- | --- | --- |
| `github.com`, GitHub Enterprise host, `gh` repo | GitHub | `gh` | Pull request |
| `gitlab.com`, other GitLab host, `glab` repo | GitLab | `glab` | Merge request |

If both remotes exist and the request has no URL, ask which forge to use.

In this skill, **PR/MR** means the current forge's change request. Treat `/gitlab-*` and `/github-*` aliases, plus a pasted GitHub or GitLab URL, as the same mode.

## Forge budget

Every `gh` invocation, `glab` invocation, forge REST call, and GitHub or GitLab MCP call counts. Use one client: `gh` on GitHub, `glab` on GitLab. Do not also query that object through MCP.

A **snapshot** is one read whose payload already contains every forge field that mode needs. Reuse a snapshot already in this conversation when the user has not said that object changed.

1. Resolve the authenticated user once per invocation and reuse it. Skip an auth-status or repo-metadata call when the snapshot, the URL, or `git remote -v` already answers it.
2. Read each issue or PR/MR once, with the snapshot command in the forge reference. It is not a menu of extra calls.
3. After the snapshot, inspect code, history, diffs, tests, and repo instructions in the local checkout. `git fetch` of the one ref you will check out is allowed; do not fetch again to re-read files. If this checkout is the wrong repo or lacks the cited paths, stop and name the missing path.
4. Draft, classify, and implement from that snapshot plus the checkout without re-querying the forge. Do not read repository files, blame, or trees through the forge.
5. A write is one call. The write response is the read-back when it contains the new id, SHA, or state. Confirm with one view only when it omits a field the stop condition needs. Do not reload after a successful write.
6. One more full snapshot is allowed immediately before a forge write that depends on the current head, approval, or mergeability, and before each write in an aggressive or scheduled run. It replaces the earlier one.

Download one failed job log only when a verdict or fix depends on it, and keep only the failing command and error lines. Do not list jobs the snapshot already concludes.

Related PRs/MRs come from snapshot links. Search the forge only when the user asks whether one exists and the snapshot has no link.

## Context budget

- Run the snapshot command in the forge reference with its `--jq` or `jq` pipe. If the filter errors, fix the filter once. Do not rerun without it, and do not page through raw JSON.
- The issue or PR/MR body stays whole. A comment or review body stays whole when it contains `git-plan-issue`, `git-plan-issue-dissent`, or `git-force-review`, or when it is the latest one. Every other body keeps author, time, id, and the first 400 characters. Also keep review commit OID, discussion resolved state, and commit author login, name, and email. Empty login is not a missing author when name or email is present.
- List calls return metadata only: number, title, state, updated time, author, assignees, url, and for a PR/MR also draft, `reviewDecision`, mergeable, and head SHA. No comment bodies, review bodies, or check logs.
- Do not paste the snapshot, this skill, or source listings into a reply, comment, or subagent prompt. The pre-submit subagent gets the submit range and the contract.
- Search, then open the matching symbol and its test. Do not read a directory, a whole unrelated file, or both forge references into context.

## Task Mode Decision

| Mode | User intent examples | Allowed writes | Stop condition |
| --- | --- | --- | --- |
| Review someone else's PR/MR | `/git-review-pr`, `/git-review-pr-force` | Review comments and verdict, resolving a discussion once its blocker is proven fixed, or a `<!-- git-force-review -->` comment when self-APPROVE is rejected | Plain `/git-review-pr`: posted visible verdict and read back SHA, pipeline, discussions, and approval/request-changes state. Force `/git-review-pr-force`: that read-back, and the reply prints `verdict:`, `forge approval:`, and one `next step:` line. |
| Plan issue | `/git-plan-issue` | Issue description update, follow-up forge issues for confirmed `status: "follow_up"` grill records, plus one brief comment | Live preflight proves the issue is open and still needs a brief grounded in repo evidence. An unsettled product decision, or a deferred or open field, posts no brief |
| Implement issue then PR/MR | `/git-issue-pr` | Code, tests, branch, commit, push, open/update PR/MR on the development branch; one settled brief comment when none exists; or one dissent comment | PR/MR exists with issue links, validation evidence, and live read-back; or a dissent is posted and the run waits for a human; do not merge. Reply: one `next step:` line from the review handoff |
| Reply to issue | `/git-reply-issue` | One issue comment on the exact target only | Live preflight proves a material unanswered request, or no write with evidence/draft is reported |
| Update own PR/MR after review | `/git-revise-pr`, `/git-revise-pr-force` | Focused code/test/doc edits, commit, push to PR/MR branch, description/comment updates, replies to reviewer threads | Plain `/git-revise-pr`: reviewer threads answered when justified, head read-back shows the new SHA, no merge until a live non-author approval. Force `/git-revise-pr-force`: that read-back, and the reply ends with one `next step:` line. |
| Fix PR/MR conflicts | `/git-fix-conflict` | Merge or rebase the target into the source branch, resolve, test, commit, push the source branch | Source branch pushed; read-back shows head, mergeability, pipeline, discussions, and reviewers; do not merge |
| Merge approved PR/MR | `/git-merge-approved`, `/git-merge-approved-force` | Follow-up issue creation/linking for relevant non-blocking reviewer notes, then merge | Plain `/git-merge-approved`: final gate passes on the exact current head and merge read-back confirms result. Force `/git-merge-approved-force`: that read-back, and the reply ends with one `next step:` line. |
| Request PR/MR review | `/git-request-review` | Assign or re-request a reviewer the user named or that is already on the PR/MR, only when current-head review is needed | Request is visible on the forge and read back; do not change code or merge |
| Focused PR/MR status | `/git-pr-status` | None | Read-only state, evidence, and exact next command are reported |
| Status or triage | `/git-triage` | None unless the user picks a follow-up | Ranked inbox or ordered plan of next commands; no auto-assign |
| Aggressive triage run | `/git-triage run` | Plain commands in plan order; self-assign authored unassigned PRs/MRs; ask for a missing reviewer last | Done/skipped/waiting summary |
| Force triage run | `/git-triage-force` | Force commands on owned items; never request review | Merged/waiting per step; one `next step:` line |
| Scheduled lifecycle | unattended scheduled lifecycle run | Only review/approval, owned revision, conflict repair, validation, commit, and source-branch push; never assigns anyone | Stable result buckets; never asks or waits |
| Scheduled approved merge | unattended scheduled approved-merge run | Only the exact-head `/git-merge-approved` workflow; never assigns anyone | Stable result buckets; never asks or waits |

When the wording is ambiguous, choose the safer mode. A review-only request never implies permission to push, update the PR/MR description, create follow-up issues, or merge.

Read only the mode's files under `references/`, in one batch of parallel reads before acting. The forge reference is `github.md` or `gitlab.md`.

Review someone else's PR/MR: read `preflight.md`, `review.md`, `pre-submit.md`, `handoff.md`, and the forge reference.

Plan issue: read `plan-issue.md`, `handoff.md`, and the forge reference.

Implement issue then PR/MR: read `implement.md`, `plan-issue.md` for the brief and dissent recipe, `handoff.md`, and `pre-submit.md` before push.

Reply to issue: read `reply.md` and `handoff.md`.

Update own PR/MR after review: read `preflight.md`, `revise.md`, `handoff.md`, and `pre-submit.md` before push.

Fix PR/MR conflicts: read `preflight.md`, `conflict.md`, `handoff.md`, and `pre-submit.md` before push.

Merge approved PR/MR: read `preflight.md`, `merge.md`, `handoff.md`, and the forge reference.

Request PR/MR review: read `preflight.md`, `request-review.md`, and `handoff.md`.

Focused PR/MR status: read `preflight.md` and `status.md`.

Status or triage, including the aggressive run: read `preflight.md` and `triage.md`.

Force triage run: read `preflight.md`, `triage.md`, and `triage-force.md`.

Scheduled lifecycle or scheduled approved merge: read `preflight.md` and `scheduled-automation.md`.

## Gates

PR/MR modes run `references/preflight.md` before any write. Do not review or approve a PR/MR you own or have commits on, or change a foreign one. There is no default reviewer. Only a `*-force` command the human invokes waives a gate. `next step:` comes from `references/handoff.md`.

## Safety Defaults

- Inspect `git status --short --branch` before making commits, pushes, or PR/MR changes.
- Treat a dirty worktree as user-owned; do not revert changes you did not make.
- Do not push, open/update PRs/MRs, close issues, or comment unless the user asks or the request clearly requires it.
- Do not target `main` or `master` for feature work unless the user explicitly says so. Prefer the repo's documented development branch, then the default branch.
- Never store forge tokens in the repo, docs, or shell history.
- Before a write, verify auth for the detected forge. If it is missing or the wrong account, ask the user to authenticate.

