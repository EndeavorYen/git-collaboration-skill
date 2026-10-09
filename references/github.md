# GitHub CLI and approval APIs

Prefer `gh` after GitHub is detected. Keep the `--jq`. If it errors, fix the filter once. Do not rerun without it or refetch a field already in the payload.

Commands assume the current directory is the repository. `gh pr view "$N"` reads it; pass `--repo owner/name` otherwise.

## Auth and identity

Once per invocation:

```bash
gh api user --jq '{id,login,name}'
```

Compare `login` or `id` with PR author and assignees. Display names are not identity. Skip `gh auth status` after this login and `gh repo view` when the URL or `git remote -v` names the repo.

## Pull request snapshot

These two commands are the snapshot. The `--jq` drops commit messages, annotations, reactions. It keeps PR body, review commit OID, thread id, `isResolved`, root `databaseId`, last 5 inline comments with UTC `createdAt`, commit author login, name, email. Empty `login` falls through to `name`. Latest review, conversation comment, each thread's latest inline comment, `CHANGES_REQUESTED`, and marker bodies stay whole. Earlier cut to 400.

```bash
gh pr view "$N" --json number,url,title,body,state,isDraft,headRefName,baseRefName,headRefOid,author,assignees,reviewRequests,reviews,reviewDecision,mergeStateStatus,mergeable,statusCheckRollup,commits,comments,files --jq 'def cut($i;$n;$k): if ($i==($n-1) or $k or ((.body//"")|test("git-force-review"))) then .body else (.body//"")[0:400] end; {number,url,title,body,state,isDraft,headRefName,baseRefName,headRefOid,author:.author.login,assignees:[.assignees[].login],reviewRequests:[.reviewRequests[]|{login:(if (.login//"") != "" then .login else .name end)}],reviewDecision,mergeStateStatus,mergeable,files:[.files[].path],commits:[.commits[]|{oid,authors:[.authors[]|{login,name,email}]}],checks:[.statusCheckRollup[]?|{name:(.name // .context // .workflowName),status,conclusion:(.conclusion // .state)}],reviews:((.reviews//[]) as $r|($r|length) as $n|[$r|to_entries[]|.key as $i|.value|{id,author:.author.login,state,submittedAt,oid:.commit.oid,body:cut($i;$n;.state=="CHANGES_REQUESTED")}]),comments:(((.comments//[])|.[-20:]) as $w|($w|length) as $n|[$w|to_entries[]|.key as $i|.value|{id,author:.author.login,createdAt,body:cut($i;$n;((.body//"")|test("git-plan-issue")))}])}'
gh api graphql -f query='query($o:String!,$n:String!,$k:Int!){repository(owner:$o,name:$n){pullRequest(number:$k){reviewThreads(first:100){nodes{id isResolved path line root:comments(first:1){nodes{databaseId}} comments(last:5){nodes{author{login} createdAt body}}}}}}}' -f o="$OWNER" -f n="$REPO" -F k="$N" --jq 'def z: try (if test("Z$") then sub("\\.[0-9]+";"") else(.[:19]+"Z"|fromdateiso8601)-((.[-5:-3]|tonumber)*3600+(.[-2:]|tonumber)*60)*(.[-6:-5]+"1"|tonumber)|todate end) catch null; [.data.repository.pullRequest.reviewThreads.nodes[-40:][]|{threadId:.id,isResolved,path,line,id:((.root.nodes[0]//{}).databaseId),comments:([.comments.nodes[]?|{user:((.author//{}).login),createdAt:(.createdAt|z),body}] as $c|($c|length) as $n|[$c|to_entries[]|.key as $i|.value|.body=(if ($i==($n-1) or ((.body//"")|test("git-force-review"))) then .body else (.body//"")[0:400] end)])}]'
```

Do not call `issues/${N}/comments` or check-runs when `checks` has the job. `gh search` has no `reviewDecision`, mergeable, or head SHA; snapshot before merge or review.

`https://github.com/owner/name/pull/12` is owner `owner`, repo `name`, number `12`.

Approval evidence:

- `reviewDecision` of `APPROVED` plus at least one review with `state=APPROVED` from a user who is not the author and has no commits on the current head.
- `CHANGES_REQUESTED` is `NEEDS_REVISION` when those reviews are still current.
- An empty `reviewDecision` after a `COMMENTED` review does not prove there is no outstanding feedback.
- `REVIEW_REQUIRED` with no current-head request is `REVIEW_REQUEST_NEEDED`.
- Branch protection and required reviewers support the read-back; they do not invent a reviewer name.

Diffs: one `git fetch` of `headRefOid`, not `gh pr diff` or the contents API.

## Request review

Never invent a reviewer. Use `reviewer:USERNAME`, someone on `reviewRequests`, or list CODEOWNERS and ask who to assign.

```bash
gh api --method POST "repos/${OWNER}/${REPO}/pulls/${N}/requested_reviewers" \
  --field "reviewers[]=${USERNAME}"
```

POST response is the read-back. One confirm `gh pr view` only when it omits the reviewer or `headRefOid`.

## Post a review

```bash
gh pr review "$N" --approve --body "$BODY"
gh pr review "$N" --request-changes --body "$BODY"
gh pr review "$N" --comment --body "$BODY"
```

Inline comments use the pull-comment API on the changed line. The review write is the read-back for `headRefOid`, `reviewDecision`, and the new review. Confirm once if head SHA or approval state is omitted.

## Resolve a review thread

One write per thread replied on this round. The resolve write response is the read-back for resolved.

```bash
gh api graphql -f query='mutation($id:ID!){resolveReviewThread(input:{threadId:$id}){thread{isResolved}}}' -f id="$THREAD_ID"
```

## Issue snapshot

One call. Issue body and marker comments stay whole, including older markers. Latest stays whole; others in the latest 20 are cut to 400. Do not follow with `gh api .../comments` or `gh pr list --search`.

```bash
gh issue view "$N" --json number,url,title,state,author,assignees,labels,body,comments,closedByPullRequestsReferences --jq '{number,url,title,state,author:.author.login,assignees:[.assignees[].login],labels:[.labels[].name],body,links:[.closedByPullRequestsReferences[]?|{number,url,state}],commentCount:((.comments//[])|length),comments:((.comments//[]) as $c|($c|length) as $n|[$c|to_entries[]|select(((.value.body//"")|test("git-plan-issue")) or (.key>=($n-20)))|.key as $i|.value|{id,author:.author.login,createdAt,body:(if ($i==($n-1) or ((.body//"")|test("git-plan-issue"))) then .body else (.body//"")[0:400] end)}])}'
```

Post, then stop. That response is the read-back:

```bash
gh api --method POST "repos/${OWNER}/${REPO}/issues/${N}/comments" --field body="$BODY"
```

## Open or merge a pull request

```bash
gh pr create --base "$TARGET" --head "$SOURCE" --title "$TITLE" --body "$BODY"
gh pr merge "$N" --match-head-commit "$HEAD"
```

Use `--merge`, `--squash`, or `--rebase` only when repo-local instructions or the user name that strategy. `--match-head-commit` keeps the exact reviewed head. When assignees are empty, set the authenticated author as the sole assignee. Never assign yourself elsewhere or replace a non-empty list. The create or merge result is the read-back, including assignees.

`/git-merge-approved-force` uses this exact-head merge. If required reviews reject it, report that error. Add `--admin` only when this invocation contains `admin`:

```bash
gh pr merge "$N" --match-head-commit "$HEAD" --admin
```

## Inbox lists

One call per relationship. Do not add `comments`, `reviews`, or `statusCheckRollup`. Rank by `reviewDecision`. Snapshot a row only to write it or when named.

```bash
gh search prs --review-requested=@me --state open --limit 20 --json number,title,repository,url,updatedAt,state
gh search prs --author=@me --state open --limit 20 --json number,title,repository,url,updatedAt,state
gh search issues --assignee=@me --state open --limit 20 --json number,title,repository,url,updatedAt,state
gh pr list --limit 30 --json number,title,state,isDraft,updatedAt,url,author,reviewDecision,mergeable,headRefOid
gh issue list --limit 30 --json number,title,state,updatedAt,url,author,assignees
gh api notifications --jq ".[:20]|[.[]|{reason,updated_at,title:.subject.title,type:.subject.type,url:.subject.url}]"
```

## Conflicts and mergeability

`mergeable` / `mergeStateStatus` of `DIRTY` or `CONFLICTING` is `CONFLICTED`. `BLOCKED` can be missing checks or reviews; read `statusCheckRollup` before `BLOCKED` or `REVIEW_REQUEST_NEEDED`.
