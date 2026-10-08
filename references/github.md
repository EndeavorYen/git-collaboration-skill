# GitHub CLI and approval APIs

Prefer `gh` after GitHub is detected. Each command is the **snapshot** from **Forge budget** and **Context budget** in `SKILL.md`. Keep the `--jq`. If it errors, fix the filter once. Do not rerun without it or refetch a field already in the payload. Do not query that object through GitHub MCP or read repository files through the forge.

Commands assume the current directory is the repository. `gh pr view "$N"` reads it; pass `--repo owner/name` otherwise.

## Auth and identity

Once per invocation:

```bash
gh api user --jq '{id,login,name}'
```

Compare `login` or numeric `id` with PR author and assignees. Display names are not identity. Skip `gh auth status` when this returns the login, and skip `gh repo view` when the URL or `git remote -v` names the project.

## Pull request snapshot

These two commands are the snapshot. The `--jq` drops commit messages, check annotations, and reactions. It keeps the PR body, review commit OID, thread id, `isResolved`, the root `databaseId`, the last 5 inline comments, and commit author login, name, and email. Empty `login` falls through to `name`. The latest review, the latest conversation comment, and each thread's latest inline comment stay whole, as do `CHANGES_REQUESTED` and marker bodies. Earlier of those 5 are cut to 400.

```bash
gh pr view "$N" --json number,url,title,body,state,isDraft,headRefName,baseRefName,headRefOid,author,assignees,reviewRequests,reviews,reviewDecision,mergeStateStatus,mergeable,statusCheckRollup,commits,comments,files --jq '{number,url,title,body,state,isDraft,headRefName,baseRefName,headRefOid,author:.author.login,assignees:[.assignees[].login],reviewRequests:[.reviewRequests[]|{login:(if (.login//"") != "" then .login else .name end)}],reviewDecision,mergeStateStatus,mergeable,files:[.files[].path],commits:[.commits[]|{oid,authors:[.authors[]|{login,name,email}]}],checks:[.statusCheckRollup[]?|{name:(.name // .context // .workflowName),status,conclusion:(.conclusion // .state)}],reviews:((.reviews//[]) as $r|($r|length) as $n|[$r|to_entries[]|.key as $i|.value|{id,author:.author.login,state,submittedAt,oid:.commit.oid,body:(if ($i==($n-1) or .state=="CHANGES_REQUESTED" or ((.body//"")|test("git-force-review"))) then .body else (.body//"")[0:400] end)}]),comments:(((.comments//[])|.[-20:]) as $w|($w|length) as $n|[$w|to_entries[]|.key as $i|.value|{id,author:.author.login,createdAt,body:(if ($i==($n-1) or ((.body//"")|test("git-plan-issue|git-force-review"))) then .body else (.body//"")[0:400] end)}])}'
gh api graphql -f query='query($o:String!,$n:String!,$k:Int!){repository(owner:$o,name:$n){pullRequest(number:$k){reviewThreads(first:100){nodes{id isResolved path line root:comments(first:1){nodes{databaseId}} comments(last:5){nodes{author{login} body}}}}}}}' -f o="$OWNER" -f n="$REPO" -F k="$N" --jq '[.data.repository.pullRequest.reviewThreads.nodes[-40:][]|{threadId:.id,isResolved,path,line,id:((.root.nodes[0]//{}).databaseId),comments:([.comments.nodes[]?|{user:((.author//{}).login),body}] as $c|($c|length) as $n|[$c|to_entries[]|.key as $i|.value|.body=(if ($i==($n-1) or ((.body//"")|test("git-force-review"))) then .body else (.body//"")[0:400] end)])}]'
```

Do not call `issues/${N}/comments` or check-runs when `checks` has the job. `gh search` has no `reviewDecision`, mergeable, or head SHA; snapshot before a merge or review decision.

`https://github.com/owner/name/pull/12` is owner `owner`, repo `name`, number `12`.

Live approval evidence:

- `reviewDecision` of `APPROVED` plus at least one review with `state=APPROVED` from a user who is not the author and has no commits on the current head.
- `CHANGES_REQUESTED` is `NEEDS_REVISION` when those reviews are still current.
- `REVIEW_REQUIRED` with no current-head request is `REVIEW_REQUEST_NEEDED`.
- Branch protection and required reviewers support the read-back; they do not invent a reviewer name.

Diffs come from one local `git fetch` of `headRefOid`. Do not use `gh pr diff` or the contents API.

## Request review

Never invent a reviewer. Use `reviewer:USERNAME`, someone already on `reviewRequests`, or list CODEOWNERS and ask who to assign.

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

Inline comments use the pull-comment API on the changed line. The review write response is the read-back for `headRefOid`, `reviewDecision`, and the new review. Confirm once only when it omits the head SHA or approval state.

## Resolve a review thread

One write per thread replied on this round. The resolve write response is the read-back for resolved.

```bash
gh api graphql -f query='mutation($id:ID!){resolveReviewThread(input:{threadId:$id}){thread{isResolved}}}' -f id="$THREAD_ID"
```

## Issue snapshot

One call. The issue body and marker comments stay whole, including older markers. The latest comment stays whole; others in the latest 20 are cut to 400 characters. Do not follow with `gh api .../comments` or `gh pr list --search`.

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

Use `--merge`, `--squash`, or `--rebase` only when repo-local instructions or the user name that strategy. `--match-head-commit` keeps the exact reviewed head. The create or merge result is the read-back.

`/git-merge-approved-force` uses the same exact-head merge. If required reviews reject it, report the forge error. Add `--admin` only when the same invocation also contains `admin`:

```bash
gh pr merge "$N" --match-head-commit "$HEAD" --admin
```

## Inbox lists

One call per relationship, metadata only. Do not add `comments`, `reviews`, or `statusCheckRollup`. Rank with `reviewDecision` on `gh pr list`. Snapshot a row only to write it or when the user named it.

```bash
gh search prs --review-requested=@me --state open --limit 20 --json number,title,repository,url,updatedAt,state
gh search prs --author=@me --state open --limit 20 --json number,title,repository,url,updatedAt,state
gh search issues --assignee=@me --state open --limit 20 --json number,title,repository,url,updatedAt,state
gh pr list --limit 30 --json number,title,state,isDraft,updatedAt,url,author,reviewDecision,mergeable,headRefOid
gh issue list --limit 30 --json number,title,state,updatedAt,url,author,assignees
gh api notifications --jq ".[:20]|[.[]|{reason,updated_at,title:.subject.title,type:.subject.type,url:.subject.url}]"
```

## Conflicts and mergeability

`mergeable` / `mergeStateStatus` of `DIRTY` or `CONFLICTING` is `CONFLICTED`. `BLOCKED` may be missing checks or reviews; use `statusCheckRollup` from this snapshot before `BLOCKED` versus `REVIEW_REQUEST_NEEDED`.
