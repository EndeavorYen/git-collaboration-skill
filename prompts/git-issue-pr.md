---
description: Implement a GitHub or GitLab issue, validate it, push, and open or update the PR/MR
---

Use the installed `git-collaboration` skill in "Implement issue then PR/MR" mode. Detect the forge from the URL or remotes.

Before editing code, refresh the issue state, description, labels, assignees, links, related PRs/MRs, and all non-system notes in chronological order. Identify the current `<!-- git-plan-issue -->` brief if any, and any unresolved `<!-- git-plan-issue-dissent -->`. Evaluate the current brief against inspected code.

If you agree with Goal, Recommended change, Out of scope, and Acceptance criteria, treat that note as the implementation contract, report which note id supplied it, and implement. Local details inside that shape stay on this path. A human decision in a later comment, a newer brief, or this invocation is final and becomes the implementation contract.

If there is material disagreement, post one issue comment using the skill's dissent recipe (`<!-- git-plan-issue-dissent -->`), then stop without editing code. If an unresolved dissent already exists and this invocation has no human decision, perform no write and report that the issue is waiting.

Start from the current development branch, create a dedicated feature branch, use TDD when practical, implement the focused fix, validate it against the contract's Acceptance criteria, commit with issue linkage, push, open or update the PR/MR targeting the development branch, then read the PR/MR back from the forge.

If the issue has assignees and the authenticated user is not among them, stop without implementing. Unassigned issues may be implemented. Naming the issue in the prompt does not authorize taking over another person's assigned issue.

$ARGUMENTS
