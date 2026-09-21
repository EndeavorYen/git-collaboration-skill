# GitHub CLI and approval APIs

Use this file after the main skill has detected GitHub. Prefer `gh`. Commands below assume the current directory is the repository unless a `--repo owner/name` flag is shown.

## Auth and identity

```bash
gh auth status
gh api user --jq '{id,login,name}'
```

Compare `login` or numeric `id` with PR author and assignees. Display names are not identity.

## Project orientation

```bash
gh repo view --json nameWithOwner,url,defaultBranchRef,id
```

For a URL `https://github.com/owner/name/pull/12`, owner is `owner`, repo is `name`, number is `12`.

## Pull request preflight

```bash
gh pr view "$N" --json number,url,title,state,isDraft,headRefName,baseRefName,headRefOid,author,assignees,reviewRequests,reviews,reviewDecision,mergeStateStatus,mergeable,statusCheckRollup,commits,updatedAt
gh api "repos/${OWNER}/${REPO}/commits/${HEAD}/check-runs" --jq '.check_runs[] | {name,status,conclusion}'
gh api "repos/${OWNER}/${REPO}/pulls/${N}/comments"
gh api "repos/${OWNER}/${REPO}/issues/${N}/comments"
```

Live approval evidence:

- `reviewDecision` of `APPROVED` plus at least one review with `state=APPROVED` from a user who is not the author and has no commits on the current head.
- `CHANGES_REQUESTED` is `NEEDS_REVISION` when those reviews are still current.
- `REVIEW_REQUIRED` with no current-head request is `REVIEW_REQUEST_NEEDED`.
- Branch protection and required reviewers support the read-back; they do not invent a reviewer name.

## Request review

Never invent a reviewer. Use an explicit `reviewer:USERNAME`, a reviewer already on `reviewRequests`, or present CODEOWNERS as a list and ask who to assign.

```bash
gh api --method POST "repos/${OWNER}/${REPO}/pulls/${N}/requested_reviewers" \
  --field "reviewers[]=${USERNAME}"
```

## Post a review

```bash
gh pr review "$N" --approve --body "$BODY"
gh pr review "$N" --request-changes --body "$BODY"
gh pr review "$N" --comment --body "$BODY"
```

Inline comments use the pull-comment API on the exact changed line. After posting, read back `headRefOid`, `reviewDecision`, `reviews`, and comment threads.

## Issues

```bash
gh issue view "$N" --comments
gh api "repos/${OWNER}/${REPO}/issues/${N}/comments"
gh api --method POST "repos/${OWNER}/${REPO}/issues/${N}/comments" --field body="$BODY"
```

Related PRs: `gh pr list --search "N" --state open`. Linked PRs also appear on `gh issue view`.

## Open or merge a pull request

```bash
gh pr create --base "$TARGET" --head "$SOURCE" --title "$TITLE" --body "$BODY"
gh pr merge "$N" --match-head-commit "$HEAD"
```

Use `--merge`, `--squash`, or `--rebase` only when repo-local instructions or the user name that strategy. `--match-head-commit` keeps the merge on the exact reviewed head.

## Inbox signals

```bash
gh search prs --review-requested=@me --state open
gh search prs --author=@me --state open
gh search issues --assignee=@me --state open
gh api notifications
```

Treat notifications as signals. Refresh the issue or PR before classifying reply or review need.

## Conflicts and mergeability

GitHub `mergeable` / `mergeStateStatus` of `DIRTY` or `CONFLICTING` is `CONFLICTED`. `BLOCKED` may be missing checks or required reviews; inspect checks before classifying `BLOCKED` versus `REVIEW_REQUEST_NEEDED`.
