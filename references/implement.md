# Implement issue

Read this file for `/git-issue-pr`. Brief and dissent recipe: `references/plan-issue.md`. Before push: `references/pre-submit.md`. Do not copy those procedures.

## Issue Implementation To PR/MR

Use this when the task is to fix or implement a GitHub or GitLab issue.

1. Read repo-local instructions, inspect local status, and take one issue snapshot: state, description, labels, assignees, links on that payload, marker comments, and the latest non-system comments. The latest body stays whole. Related PRs/MRs are only those links. Then inspect the local checkout. Do not read the issue again while implementing.
2. If the issue has assignees and the authenticated user is not among them, stop without implementing or posting a dissent. Unassigned issues may be implemented.
3. Collect the current proposal from that live evidence. If a current comment contains `<!-- git-plan-issue -->` and later comments have not superseded its Goal / Recommended change / Out of scope / Acceptance criteria, that comment is the current brief. A description with no current brief is not an implementation contract. A `<!-- git-plan-issue-dissent -->` stays unresolved until a human decision or a newer brief supersedes it. A human decision is a later non-system comment, a newer `<!-- git-plan-issue -->` brief, or explicit direction in this invocation that selects the original brief, the posted alternative, or a third way. The invoking user's explicit choice is final.
4. If an unresolved dissent exists and this invocation carries no human decision, perform no code edit and post no duplicate dissent. Report the dissent comment id and wait.
5. Inspect the relevant current code and evaluate the current brief. Material disagreement is a conflict on Goal, Recommended change shape, Out of scope, or Acceptance criteria. Names, extra tests, and equivalent structure inside that shape stay on the agree path. Use the Plan Issue Workflow meaning of unsettled product decision.
6. If no current brief exists, follow `references/plan-issue.md` for the brief, the dissent recipe, and the unsettled-decision rules. When Goal, Recommended change, Out of scope, and Acceptance criteria are settled, post that brief in this same session, then continue from step 8. Do not ask the user to invoke `/git-issue-pr` again.
7. On material disagreement with a settled brief, post the dissent comment from `references/plan-issue.md`, then stop without editing code.

8. When the implementer agrees with the settled brief, or a human decision has settled the original brief, the posted alternative, or a third way, treat that note as the implementation contract. Report the comment id that supplied the contract, or that this invocation selected the third way, before editing code.
9. Start from the current development branch unless repo-local instructions say otherwise. Create a dedicated feature branch; do not implement directly on the default or documented development branch.
10. Use TDD when practical: add or update a focused failing test first for bug fixes or behavior changes, then implement the smallest reasonable fix.
11. Validate with the relevant focused tests and broader checks proportional to risk, including the contract's Acceptance criteria.
12. Commit with a focused conventional-style message and reference the issue.
13. Run the **pre-submit gate**. Stop before push if Critical/High remain unfixed and unwaived.
14. Push the branch and open or update a PR/MR targeting the development branch when this is part of the issue workflow.
15. Keep the PR/MR description current: summary, issue link, validation evidence, known limitations, reviewer/assignee metadata when available, and any pre-submit waivers.
16. The create or update response is the read-back. Report iid, URL, current head SHA, pipeline state, issue link, and reviewer/assignee state. One confirm view only when that response omits iid, URL, or head SHA.

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
