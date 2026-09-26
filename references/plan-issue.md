# Plan issue

Read this file for `/git-plan-issue`. Also read one of `references/github.md` or `references/gitlab.md`. Do not read `references/pre-submit.md` for this mode. When detection says pstack is present and not off, read `references/pstack.md`.

## Plan Issue Workflow

Use this when the user explicitly invokes `/git-plan-issue` or clearly asks to analyze one issue and post an implementation brief. The write scope is updating the issue description when settled acceptance differs, opening follow-up forge issues for confirmed grill records with `status: "follow_up"`, plus one issue comment containing the implementation brief on the exact target; do not change code, commits, branches, labels, assignees, issue state, links, or any other forge object.

The planner and the executor may be different models. Write the brief for an executor that did not do this analysis and may be a weaker model: it must be able to follow the brief without re-deriving the design. See **Executor-ready brief**.

1. Resolve the exact project/issue. Reuse the authenticated user already resolved for this invocation.
2. Take one issue snapshot: state, description, labels, assignees, links already on that payload, marker comments, and the latest non-system comments. The latest body stays whole. Do not search for related PRs/MRs.
3. Read repo-local instructions and inspect the relevant code in the local checkout until the brief can name concrete files, symbols, behavior, signatures, test locations, and the validation commands the repo uses. Search, then open those symbols and their tests. Record `git rev-parse --short HEAD` and the current branch as the planned-at base. Do not paste existing source into the brief or the reply. Stay on Forge budget steps 3 and 4 and on Context budget. Do not read repository files through the forge.
4. Classify whether a current implementation brief is still needed. A current brief exists when a comment contains `<!-- git-plan-issue -->` and later comments have not changed Goal, Recommended change, Out of scope, or Acceptance criteria. A current brief is still needed when none exists, later comments changed those fields, or the user asked to re-plan.
5. Draft one issue comment using this recipe, in the issue language or the repo's documented language. Keep the bold field labels and `###` headings in English so the executor and checkers can find them:

````markdown
<!-- git-plan-issue -->
## Implementation brief

**Goal:** <one observable completion state>
**Root cause:** <file and behavior evidence>
**Recommended change:** <what to change, where, and why this shape; one line naming the rejected alternative>
**Out of scope:** <work this issue will not do>
**Acceptance criteria:** <summary of acceptance changes or deliverables; full checkable list lives in the issue description, do not duplicate the full checklist>
**Tests:** <test files to add or change, and the exact commands to run>
**Proof:** <verify skill and feature to drive, or command> | tests only: <reason>
**Constraints:** <repo-local instructions or existing contracts>
**Planned at:** `<branch>@<short SHA>`

### Execution plan
1. **<imperative step title>**
   - Files: `<path>` (edit | create)
   - Change: <symbol and the exact behavior it gains or loses>
   - Verify: `<command>` → <expected result>
2. ...

### Interfaces
```<language>
<new or changed signatures, types, config keys, or payload shapes only; no bodies>
```

### Test cases
| # | Test | Given | When | Then | Covers |
| --- | --- | --- | --- | --- | --- |
| T1 | `<file>::<test name>` | <concrete input or state> | <call or action> | <exact expected output, error, or state> | <description checklist line number, e.g. `#2`> |

### Stop and dissent when
- <an assumption this plan relies on, stated so the executor can check it>

**Next:** `/git-issue-pr <exact issue URL>`
````

The brief is a proposal. `/git-issue-pr` follows it when the implementer agrees, or posts a `<!-- git-plan-issue-dissent -->` and waits for a human decision.

6. A fork whose answer can be observed by running code is settled by a recorded local run (pstack's Prototype playbook, or an equivalent script), not by the grill. Product and preference choices still load `gentle-grill-me`. An unsettled product decision is a choice among two or more product behaviors that changes Goal, Recommended change, Out of scope, or Acceptance criteria, or an acceptance item that cannot be checked until that choice is made. A deferred or open assumption in the close log is still unsettled. Do not guess an unsettled product decision into one of those four fields. An Execution plan over the **Executor-ready brief** size limit is also an unsettled product decision about Out of scope.
   - **Already settled:** when those four fields are already settled, do not load `gentle-grill-me` and do not wait for a close log; step 7 posts that draft.
   - **Grill:** Load `gentle-grill-me` only when the draft still contains an unsettled product decision. Use that skill's rounds and post nothing until the user confirms the close log. After that confirmation, rewrite those four fields, and the Execution plan and Test cases that depend on them, from settled log entries only. If any of those four fields is still deferred or open, post nothing and report that open assumption.
   - **Follow-ups:** when work is moved to a later issue during the grill, that disposition is recorded in machine-readable form with `status: "follow_up"`. Standalone `/gentle-grill-me` does not implement and does not open issues; the caller that loaded the grill does. Do not invent follow-ups from chat memory when the close log was not confirmed. A `skipped` record or still-open assumption does not become an issue by itself. After the user confirms the close log, search open issues in that project first to prevent duplicate creation. For each non-duplicate record, open a forge issue for each confirmed close log record with `status: "follow_up"` before the turn ends, linked to the source issue. The created follow-up issue states the pending work, reason for splitting, and source issue URL. List each new follow-up issue URL in the brief comment and description update. If any required follow-up issue was not opened, the turn does not report the plan complete; ending the turn with only `grill-log.jsonl` fails this mode when a `follow_up` record has no issue URL.
   - **Same session:** on this unsettled path, that confirmation authorizes opening those follow-up issues and the one brief comment in step 7 only when those four fields are settled decisions. The local grill log is not the issue comment. After the user confirms the close log, post that brief in the same session before the turn ends. `gentle-grill-me` saying this session must not implement does not skip the comment and does not end the turn at `.gentle-grill/grill-log.jsonl`.
   - **Scope:** `/git-plan-issue` stops after that comment. It does not authorize code, commits, pushes, or a PR/MR. Scheduled lifecycle, scheduled merge, and `/git-triage` do not load `gentle-grill-me`; recommend `/git-plan-issue` with the exact issue URL.
7. When the issue is open, a current brief is still needed, the draft is grounded in the inspected checkout, the draft passes **Executor-ready brief**, and Goal, Recommended change, Out of scope, and Acceptance criteria are settled decisions, write that contract into the issue description before the turn ends whenever settled acceptance differs from the existing description. Keep the existing problem, actual-result, and expected-result sections. Replace the acceptance section so it matches the settled brief. Each checklist line must be checkable by a named test case (`T1`, ...) or an exact command. Do not leave the old checklist in place beside a contradictory comment. If any original acceptance line is no longer satisfied or satisfied only on a narrower surface, record each narrowed or dropped line in an `### Exceptions` block:

```markdown
### Exceptions
- **Original:** <existing acceptance line, quoted>
  **This issue:** <settled behavior that replaces it>
  **Still elsewhere:** <surface that keeps the original behavior, or none>
```

Rules for that block:
- One bullet per original line that the settled plan no longer fully satisfies.
- The three field labels stay in English (`**Original:**`, `**This issue:**`, `**Still elsewhere:**`) so a checker can find them. The values stay in the issue language.
- Wording that appears only in the comment, or only as prose under Out of scope, does not count.
- When every original acceptance line remains satisfied, omit the section. Do not invent an exception.

Post one issue comment containing the brief. The description holds the checkable acceptance checklist. The `<!-- git-plan-issue -->` comment remains the change record and change authorization; it summarizes acceptance changes without duplicating the full checklist. A comment-only acceptance change fails this mode. A draft whose four fields are already settled does not need a close log. The write response is the read-back. Report the updated description status, any created follow-up issue URLs, the new comment id and timestamp, current issue state from the snapshot, and `/git-issue-pr` with the exact issue URL. Do not view the issue again when the response includes the comment id.

Do not post a duplicate brief. Do not implement or open a PR/MR. Do not post a brief while an unsettled product decision remains in those four fields. If the issue is closed, a current brief already exists and the user did not ask to re-plan, an open PR/MR already covers the issue and the user did not ask to re-plan, or the evidence is too thin for a grounded brief, perform no write and report the evidence plus the exact wait or next action.

## Executor-ready brief

The brief is a work order. The executor reads it, opens the files named in step 1, and writes the first failing test. It should not need a second design pass. Check the draft against every rule before step 7:

- **Paths and symbols exist.** Every `edit` path and symbol exists at the planned-at SHA. Every `create` path names the directory it goes in, following an existing neighbor.
- **Steps are ordered and small.** The first step writes or changes the failing tests from Test cases. Each later step touches one concern and ends with a Verify command and its expected result. The last step runs the repo's full relevant check.
- **Interfaces fix the contract, not the body.** Give new or changed signatures, types, return values, error behavior, config keys, and payload shapes. Show only the new form of a changed signature; omit the old form and unchanged neighbors. Do not write function bodies and do not paste existing source. A body goes stale when the code moves, and a weaker executor copies it anyway.
- **Test cases are concrete.** Given, When, and Then use literal values, not "valid input" or "works correctly". Every acceptance line is covered by at least one test case or an exact command. `Covers` holds the description checklist line number, never the line's text, so the brief does not duplicate the checklist. Include the regression case that reproduces the root cause, and each edge case the change introduces.
- **No vague verbs.** Replace "handle", "improve", "clean up", "as needed", "appropriate", "etc.", and "similar" with the exact behavior. If you cannot state the exact behavior, the evidence is too thin or a product decision is unsettled.
- **Stop and dissent when** lists the assumptions the plan relies on that the executor can check: a symbol's current behavior, a caller count, a config default, a test that currently passes. If one fails, the executor dissents instead of improvising.
- **Proof.** `tests only: <reason>` is allowed only when the change has no user-visible surface. Do not paste pstack artifacts into the brief.
- **Size.** When the Execution plan needs more than 8 steps or touches unrelated areas, how to split the work is a scope choice: treat it as an unsettled product decision about Out of scope.

## Dissent recipe

Implement posts this comment on material disagreement, then stops. The recipe lives here.

```markdown
<!-- git-plan-issue-dissent -->
## Implementation dissent

**Brief:** comment <id>
**Disagree with:** <Goal / Recommended change / Out of scope / Acceptance criteria / Execution plan step / Stop and dissent condition items>
**Why:** <file and behavior evidence>
**Alternative:** <proposed change>
**Need from you:** choose the original brief, this alternative, or a third way
**Next:** reply on this issue, then `/git-issue-pr <exact issue URL>`
```
