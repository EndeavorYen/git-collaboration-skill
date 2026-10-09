# GitLab CLI and approval APIs

Use this file after the main skill has detected GitLab. Prefer `glab`. The tool result is the pipe's stdout. If `jq` errors, fix the filter once. Do not drop the pipe or follow it with REST for approvals, commits, discussions, notes, or pipelines the query already returns.

URL-encode a path only for REST (`group/sub%2Fproject`). GraphQL `fullPath` stays plain.

## Auth and identity

Once per invocation:

```bash
glab api user | jq '{id,username,name}'
```

Compare stable `id` or exact `username` with MR author and assignees. Display names are not identity. Skip `glab auth status` when this returns the username, and skip project metadata when the URL or `git remote -v` names the project.

## Merge request snapshot

One GraphQL call. `approvedBy` is the approval evidence. REST `approved_by` is the same evidence; do not call `merge_requests/${IID}/approvals` when this payload has `approvedBy`.

```bash
glab api graphql -f query='
query($path: ID!, $iid: String!) {
  project(fullPath: $path) {
    mergeRequest(iid: $iid) {
      iid title state draft webUrl
      sourceBranch targetBranch diffHeadSha mergeStatusEnum
      author { id username }
      assignees(first: 20) { nodes { id username } }
      reviewers(first: 20) { nodes { id username } }
      approved
      approvedBy(first: 20) { nodes { id username } }
      description
      commits(first: 100) { nodes { sha author { username } authorName authorEmail committerName committerEmail } }
      headPipeline { status }
      mergeableDiscussionsState
      discussions(first: 100) { pageInfo { hasNextPage } nodes { id resolved notes(first: 20) { nodes { id system body createdAt author { username } } } } }
    }
  }
}' -f path="$PROJECT" -f iid="$IID" | jq '.data.project.mergeRequest | {iid,title,description,state,draft,webUrl,sourceBranch,targetBranch,diffHeadSha,mergeStatusEnum,mergeableDiscussionsState,hasNextPage:.discussions.pageInfo.hasNextPage,author:.author.username,assignees:[.assignees.nodes[].username],reviewers:[.reviewers.nodes[].username],approved,approvedBy:[.approvedBy.nodes[].username],pipeline:.headPipeline.status,commits:[.commits.nodes[]|{sha,author:.author.username,authorName,authorEmail,committerName,committerEmail}],notes:(([.discussions.nodes[] as $d|$d.notes.nodes[]|select(.system|not)|{discussionId:$d.id,resolved:$d.resolved,id,author:.author.username,createdAt,body}]|.[-40:]) as $w|($w|length) as $n|[$w|to_entries[]|.key as $i|.value|.body=(if ($i==($n-1) or ((.body//"")|test("git-plan-issue|git-force-review"))) then .body else (.body//"")[0:400] end)])}'
```

If GraphQL is unavailable, one REST call piped through the same kind of `jq`, then stop:

```bash
glab api "projects/${PROJECT}/merge_requests/${IID}" | jq '{iid,title,state,draft,sha,source_branch,target_branch,merge_status,web_url,author:.author.username,assignees:[.assignees[].username]}'
```

That fallback has no `approved_by`, commits, or discussions. Do not approve or merge from it.

Add one call only for a single missing gate field. Do not fan out.

Live approval evidence:

- `approved=true` and a non-empty `approvedBy` whose members are not the author and have no author or committer commits on the current MR.
- Approval-rule zeroes (`approvals_left == 0`) support the read-back; they must not override `approved=false` or an empty `approvedBy`.
- There is no default reviewer. `approvedBy` is observed live state, not a name to invent.

Diffs come from the local checkout after one `git fetch` of `diffHeadSha`.

## Resolve a discussion

One write per discussion replied on this round. Pass the snapshot `discussionId`. The write sets `resolved=true`. The resolve write response is the read-back for resolved.

```bash
glab api graphql -f query='mutation($id:DiscussionID!){discussionToggleResolve(input:{id:$id,resolve:true}){discussion{resolved}}}' -f id="$DISCUSSION_ID"
```

## Request review

Never invent a reviewer. Use `reviewer:USERNAME` or a reviewer already on the MR. If none exists, ask who to assign.

Prefer the instance's native reviewer assignment. The write response is the read-back for reviewers, head SHA, approval, and discussions.

## Issue snapshot

One GraphQL call. `relatedMergeRequests` is the issue link. Do not search open MRs for the iid.

```bash
glab api graphql -f query='
query($path: ID!, $iid: String!) {
  project(fullPath: $path) {
    issue(iid: $iid) {
      iid title state description webUrl
      author { id username }
      assignees(first: 20) { nodes { id username } }
      labels(first: 20) { nodes { title } }
      notes(first: 100) { pageInfo { hasNextPage } nodes { id system body createdAt author { username } } }
      relatedMergeRequests(first: 10) { nodes { iid state webUrl } }
    }
  }
}' -f path="$PROJECT" -f iid="$IID" | jq '.data.project.issue | {iid,title,state,description,webUrl,author:.author.username,assignees:[.assignees.nodes[].username],labels:[.labels.nodes[].title],links:[.relatedMergeRequests.nodes[]|{iid,state,webUrl}],hasNextPage:.notes.pageInfo.hasNextPage,noteCount:([.notes.nodes[]|select(.system|not)]|length),notes:([.notes.nodes[]|select(.system|not)] as $c|($c|length) as $n|[$c|to_entries[]|select(((.value.body//"")|test("git-plan-issue")) or (.key>=($n-20)))|.key as $i|.value|{id,author:.author.username,createdAt,body:(if ($i==($n-1) or ((.body//"")|test("git-plan-issue"))) then .body else (.body//"")[0:400] end)}])}'
```

The description and marker notes stay whole. Skip system notes. If `pageInfo.hasNextPage` is true and a marker is missing, fetch one more page through the same pipe. Post, then stop. The POST response is the read-back:

```bash
glab api --method POST "projects/${PROJECT}/issues/${IID}/notes" --field body="$BODY"
```

REST fallback, only when GraphQL is unavailable: `glab api "projects/${PROJECT}/issues/${IID}"`. One notes call only when that payload has no notes.

## Open or merge a merge request

```bash
git push -u origin HEAD
glab mr create --target-branch "$TARGET" --title "$TITLE" --description "$BODY"
glab api --method PUT "projects/${PROJECT}/merge_requests/${IID}/merge" \
  --field sha="${HEAD_SHA}"
```

Push options may create an MR when the user asked and the instance supports them. Creating an MR is not permission to merge it. When assignees are empty, set the authenticated author as the sole assignee. Never assign yourself elsewhere or replace a non-empty list. The create or merge result is the read-back, including assignees.

`/git-merge-approved-force` uses the same exact-head merge field. If approval rules reject the force merge, report the forge error. Do not push the source branch into the target locally.

## Inbox lists

One call per relationship.

```bash
glab api todos | jq '[.[:20][]|{action_name,target_type,target_url,updated_at,body:(.body//"")[0:120]}]'
glab api "merge_requests?scope=all&state=opened&reviewer_username=${USER}&per_page=20" | jq '[.[]|{iid,title,state,draft,updated_at,web_url,sha,author:.author.username}]'
glab api "merge_requests?scope=all&state=opened&author_username=${USER}&per_page=20" | jq '[.[]|{iid,title,state,draft,updated_at,web_url,sha,author:.author.username}]'
glab api "issues?scope=all&state=opened&assignee_username=${USER}&per_page=20" | jq '[.[]|{iid,title,state,updated_at,web_url,author:.author.username}]'
```

Treat `/todos` as signals. These lists are metadata. Do not open every row or fetch notes while ranking.

## Conflicts and mergeability

GitLab conflict flags or a merge status that requires target-branch repair is `CONFLICTED`. `mergeableDiscussionsState=false` with actionable unresolved notes is `NEEDS_REVISION`. `mergeableDiscussionsState=true` does not prove there is no outstanding feedback. Read both from the snapshot. REST calls this flag `blocking_discussions_resolved`.
