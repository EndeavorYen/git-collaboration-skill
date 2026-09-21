# GitHub CLI and approval APIs

Use this file after the main skill has detected GitHub. Prefer `gh`. The command in each section is the **snapshot** from **Forge budget** and **Context budget** in `SKILL.md`. Keep the `--jq`. If it errors, fix the filter once. Do not rerun without it. Do not follow it with another call for a field that payload already contains. Do not also query the same object through GitHub MCP. Do not read repository files, blame, or trees through the forge; that work stays in the local checkout.

Commands below assume the current directory is the repository unless a `--repo owner/name` flag is shown.

## Auth and identity

Once per invocation:

```bash
gh api user --jq '{id,login,name}'
```

Compare `login` or numeric `id` with PR author and assignees. Display names are not identity. Skip `gh auth status` when this call returns the login. Skip `gh repo view` when the URL or `git remote -v` already names the project.

## Pull request snapshot

These two commands are the snapshot. The `--jq` drops commit message bodies, check annotations, and reaction payloads. It keeps the PR body, review commit OID, comment ids, and commit author login, name, and email. An empty `login` falls through to `name`. The latest review, latest conversation comment, and latest inline comment stay whole. `CHANGES_REQUESTED` review bodies and marker bodies stay whole.

```bash
gh pr view "$N" --json number,url,title,body,state,isDraft,headRefName,baseRefName,headRefOid,author,assignees,reviewRequests,reviews,reviewDecision,mergeStateStatus,mergeable,statusCheckRollup,commits,comments,files --jq '{number,url,title,body,state,isDraft,headRefName,baseRefName,headRefOid,author:.author.login,assignees:[.assignees[].login],reviewRequests:[.reviewRequests[]|{login:(if (.login//"") != "" then .login else .name end)}],reviewDecision,mergeStateStatus,mergeable,files:[.files[].path],commits:[.commits[]|{oid,authors:[.authors[]|{login,name,email}]}],checks:[.statusCheckRollup[]?|{name:(.name // .context // .workflowName),status,conclusion:(.conclusion // .state)}],reviews:((.reviews//[]) as $r|($r|length) as $n|[$r|to_entries[]|.key as $i|.value|{id,author:.author.login,state,submittedAt,oid:.commit.oid,body:(if ($i==($n-1) or .state=="CHANGES_REQUESTED" or ((.body//"")|test("git-force-review"))) then .body else (.body//"")[0:400] end)}]),comments:(((.comments//[])|.[-20:]) as $w|($w|length) as $n|[$w|to_entries[]|.key as $i|.value|{id,author:.author.login,createdAt,body:(if ($i==($n-1) or ((.body//"")|test("git-plan-issue|git-force-review"))) then .body else (.body//"")[0:400] end)}])}'
gh api "repos/${OWNER}/${REPO}/pulls/${N}/comments?per_page=100" --jq '([.[]|{id,user:.user.login,path,line,body}]|.[-40:]) as $w|($w|length) as $n|[$w|to_entries[]|.key as $i|.value|{id,user,path,line,body:(if ($i==($n-1) or ((.body//"")|test("git-force-review"))) then .body else (.body//"")[0:400] end)}]'
```

Do not also call `issues/${N}/comments`. Do not call check-runs when `checks` already has the required job's conclusion. Global `gh search` results have no `reviewDecision`, mergeable, or head SHA. Rank from them, then take this snapshot before a merge or review decision.

For a URL `https://github.com/owner/name/pull/12`, owner is `owner`, repo is `name`, number is `12`.

Live approval evidence from that payload:

- `reviewDecision` of `APPROVED` plus at least one review with `state=APPROVED` from a user who is not the author and has no commits on the current head.
- `CHANGES_REQUESTED` is `NEEDS_REVISION` when those reviews are still current.
- `REVIEW_REQUIRED` with no current-head request is `REVIEW_REQUEST_NEEDED`.
- Branch protection and required reviewers support the read-back; they do not invent a reviewer name.

Diffs and file contents come from the local checkout after one `git fetch` of `headRefOid`. Do not use `gh pr diff` or the contents API.

## Request review

Never invent a reviewer. Use an explicit `reviewer:USERNAME`, a reviewer already on `reviewRequests`, or present CODEOWNERS as a list and ask who to assign.

```bash
gh api --method POST "repos/${OWNER}/${REPO}/pulls/${N}/requested_reviewers" \
  --field "reviewers[]=${USERNAME}"
```

The POST response is the read-back. One confirm `gh pr view` only when it omits the reviewer or `headRefOid`.

## Post a review

```bash
gh pr review "$N" --approve --body "$BODY"
gh pr review "$N" --request-changes --body "$BODY"
gh pr review "$N" --comment --body "$BODY"
```

Inline comments use the pull-comment API on the exact changed line. The review write response is the read-back for `headRefOid`, `reviewDecision`, and the new review. One confirm view only when that response omits the head SHA or approval state.

## Issue snapshot

One call. The issue body stays whole. Marker comments stay whole, including markers older than the window. The latest comment stays whole. Other comments in the latest 20 are cut to 400 characters. Do not follow with `gh api .../comments` or `gh pr list --search`.

```bash
gh issue view "$N" --json number,url,title,state,author,assignees,labels,body,comments,closedByPullRequestsReferences --jq '{number,url,title,state,author:.author.login,assignees:[.assignees[].login],labels:[.labels[].name],body,links:[.closedByPullRequestsReferences[]?|{number,url,state}],commentCount:((.comments//[])|length),comments:((.comments//[]) as $c|($c|length) as $n|[$c|to_entries[]|select(((.value.body//"")|test("git-plan-issue")) or (.key>=($n-20)))|.key as $i|.value|{id,author:.author.login,createdAt,body:(if ($i==($n-1) or ((.body//"")|test("git-plan-issue"))) then .body else (.body//"")[0:400] end)}])}'
```

Post, then stop. The POST response is the read-back:

```bash
gh api --method POST "repos/${OWNER}/${REPO}/issues/${N}/comments" --field body="$BODY"
```

## Open or merge a pull request

```bash
gh pr create --base "$TARGET" --head "$SOURCE" --title "$TITLE" --body "$BODY"
gh pr merge "$N" --match-head-commit "$HEAD"
```

Use `--merge`, `--squash`, or `--rebase` only when repo-local instructions or the user name that strategy. `--match-head-commit` keeps the merge on the exact reviewed head. The create or merge command result is the read-back.

`/git-merge-approved-force` uses the same exact-head merge. If required reviews reject it, report the forge error. Add `--admin` only when the same invocation also contains `admin`:

```bash
gh pr merge "$N" --match-head-commit "$HEAD" --admin
```

## Inbox lists

One call per relationship. Metadata only. Do not add `comments`, `reviews`, or `statusCheckRollup` to a list. For one repository, `gh pr list` already includes `reviewDecision`, which is enough to rank. Snapshot a row only when you are about to write it or the user named it.

```bash
gh search prs --review-requested=@me --state open --limit 20 --json number,title,repository,url,updatedAt,state
gh search prs --author=@me --state open --limit 20 --json number,title,repository,url,updatedAt,state
gh search issues --assignee=@me --state open --limit 20 --json number,title,repository,url,updatedAt,state
gh pr list --limit 30 --json number,title,state,isDraft,updatedAt,url,author,reviewDecision,mergeable,headRefOid
gh issue list --limit 30 --json number,title,state,updatedAt,url,author,assignees
gh api notifications --jq ".[:20]|[.[]|{reason,updated_at,title:.subject.title,type:.subject.type,url:.subject.url}]"
```

Treat notifications as signals. The next command takes the trimmed snapshot. Do not snapshot every row during ranking.

## Conflicts and mergeability

GitHub `mergeable` / `mergeStateStatus` of `DIRTY` or `CONFLICTING` is `CONFLICTED`. `BLOCKED` may be missing checks or required reviews; use `statusCheckRollup` from the same snapshot before classifying `BLOCKED` versus `REVIEW_REQUEST_NEEDED`.
