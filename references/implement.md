# Implement issue

Read this file for `/git-issue-pr`. Brief and dissent recipe: `references/plan-issue.md`. Before push: `references/pre-submit.md`. Do not copy those procedures.

## Issue Implementation To PR/MR

Use this when the task is to fix or implement a GitHub or GitLab issue.

1. Read repo-local instructions, inspect local status, and take one issue snapshot: state, description, labels, assignees, links on that payload, marker comments, and the latest non-system comments. The latest body stays whole. Related PRs/MRs are only those links. Then inspect the local checkout. Do not read the issue again while implementing.
2. If the issue has assignees and the authenticated user is not among them, stop without implementing or posting a dissent. Unassigned issues may be implemented.
3. Collect the current proposal from that live evidence. If a current comment contains `<!-- git-plan-issue -->` and later comments have not superseded its Goal / Recommended change / Out of scope / Acceptance criteria, that comment is the current brief. A description with no current brief is not an implementation contract. Treat the updated description and the matching brief as one contract: the description holds the checkable acceptance checklist and exceptions, while the brief comment provides the change record and authorization; a stale description checklist is a failed plan, not a second contract. A `<!-- git-plan-issue-dissent -->` stays unresolved until a human decision or a newer brief supersedes it. A human decision is a later non-system comment, a newer `<!-- git-plan-issue -->` brief, or explicit direction in this invocation that selects the original brief, the posted alternative, or a third way. The invoking user's explicit choice is final.
4. If an unresolved dissent exists and this invocation carries no human decision, perform no code edit and post no duplicate dissent. Report the dissent comment id and wait.
5. Inspect the relevant current code and evaluate the current brief. When the brief has a planned-at SHA, run `git diff --stat <planned-at>..HEAD -- <every path named anywhere in the brief>`; if those paths changed, re-check every Stop and dissent when condition before agreeing. A named `edit` path that no longer exists, including one that was renamed or moved, is material disagreement. Material disagreement is a conflict on Goal, Recommended change shape, Out of scope, or Acceptance criteria, a failed Stop and dissent when condition, or an Execution plan step that cannot be done as written because a named path, symbol, or behavior is not what the brief says. Names, extra tests, and equivalent structure inside that shape stay on the agree path. Use the Plan Issue Workflow meaning of unsettled product decision.
6. If no current brief exists, follow `references/plan-issue.md` for the brief, the dissent recipe, the unsettled-decision rules, and follow-up issue creation. When `gentle-grill-me` is loaded during same-session planning, search open issues in that project first to prevent duplicate creation, and open a forge issue for each confirmed close log record with `status: "follow_up"` before the turn ends, linked to the source issue; ending the turn with only `grill-log.jsonl` fails this mode when a `follow_up` record has no issue URL. When Goal, Recommended change, Out of scope, and Acceptance criteria are settled, post the decision card only in this same session (nine bold fields, Stop and dissent when, Planned at, and Next; no Execution plan, Interfaces, or Test cases section), update the issue description when settled acceptance differs, then continue from step 8. Do not post the full work-order from this step. The full work-order recipe is only for handoff, when `/git-plan-issue` is invoked for another session, model, or agent, or the user explicitly asks for a full work-order or handoff brief. Do not add a `plan:on` / `plan:off` mode flag. Do not ask the user to invoke `/git-issue-pr` again.
7. On material disagreement with a settled brief, post the dissent comment from `references/plan-issue.md`, then stop without editing code.

8. When the implementer agrees with the settled brief, or a human decision has settled the original brief, the posted alternative, or a third way, treat that note as the implementation contract. Report the comment id that supplied the contract, or that this invocation selected the third way, before editing code.
9. Start from the current development branch unless repo-local instructions say otherwise. Create a dedicated feature branch; do not implement directly on the default or documented development branch.
10. When the brief has an Execution plan, it is the work order (handoff profile): do its steps in order, write the Test cases as written, match its Interfaces, and run each step's Verify before the next step. Do not add steps, redesign a step, or skip one. When a step fails its Verify twice for a reason the brief did not anticipate, stop editing: keep completed steps on the feature branch, do not revert them, do not commit the failing step, do not push, and post the dissent from `references/plan-issue.md` naming that step and the last passing step. This mid-implementation dissent replaces step 7's stop before editing code. A brief without an Execution plan still works; derive the steps yourself in an interleaved loop. When `references/pstack.md` is loaded, apply its implement rows inside this step without adding, redesigning, or skipping brief steps.
    Use TDD when practical: add or update a focused failing test first for bug fixes or behavior changes, then implement the smallest reasonable fix. Enforce the hard **read-then-write gate**:
    - After at most one focused search and opening the relevant symbol and its test (per Context budget), the next tool actions must **create or edit** a test or implementation file. With an Execution plan, skip the search: open the files named in step 1, then write.
    - TDD means **write** a failing test file or assertion immediately, not further exploration or grepping disguised as "finding where to put the test."
    - A run that performs only reads/greps for more than one exploration round is **out of mode**: stop, report what was missing from the brief, or write the smallest failing test from the Acceptance criteria.
11. Validate with the relevant focused tests and broader checks proportional to risk, including the description's checkable Acceptance criteria and every brief Test case (`T1`, ...).
12. Commit with a focused conventional-style message and reference the issue.
13. Run the **pre-submit gate**. Stop before push if Critical/High remain unfixed and unwaived.
14. Push the branch and open or update a PR/MR targeting the development branch when this is part of the issue workflow.
15. Keep the PR/MR description current: summary, issue link, validation evidence with each brief Test case id and its result, known limitations, reviewer/assignee metadata when available, any pre-submit waivers, and the Proof record from `references/pre-submit.md`.
16. The create or update response is the read-back. Report iid, URL, current head SHA, pipeline state, issue link, and reviewer/assignee state. One confirm view only when that response omits iid, URL, or head SHA. The operator reply ends with one `next step:` line from the review handoff in `SKILL.md`. Do not print the Solo override block.

Do not merge the PR/MR unless the user separately asks for that merge and the merge gate in `references/merge.md` passes.

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
- Opening or updating a PR/MR, and any source-branch push from `/git-issue-pr`, `/git-revise-pr`, `/git-revise-pr-force`, `/git-fix-conflict`, or scheduled lifecycle, requires the pre-submit gate in `references/pre-submit.md`.

## Commits

- Use focused, conventional-style commit messages.
- Reference issue IDs when applicable.
- Use forge closing keywords only when automatic closing on the target branch is desired and understood.
- Include validation in the commit body or PR/MR description when useful.
