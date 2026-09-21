# GitLab CLI and approval APIs

Use this file after the main skill has detected GitLab. Prefer `glab`. URL-encode project paths (`group/sub%2Fproject`) or use numeric project IDs once discovered.

## Auth and identity

```bash
glab auth status
glab api user | jq '{id,username,name}'
```

Compare stable `id` or exact `username` with MR author and assignees. Display names are not identity.

## Project orientation

```bash
repo_path="group/subgroup/project"
repo_encoded="${repo_path//\//%2F}"
glab api "projects/${repo_encoded}" | jq '{id,path_with_namespace,web_url,default_branch}'
```

## Merge request preflight

```bash
glab api "projects/${PROJECT}/merge_requests/${IID}"
glab api "projects/${PROJECT}/merge_requests/${IID}/approvals"
glab api "projects/${PROJECT}/merge_requests/${IID}/commits"
glab api "projects/${PROJECT}/merge_requests/${IID}/discussions"
glab api "projects/${PROJECT}/merge_requests/${IID}/notes"
glab api "projects/${PROJECT}/merge_requests/${IID}/pipelines"
```

Live approval evidence:

- `approved=true` and a non-empty `approved_by` whose members are not the author and have no author or committer commits on the current MR.
- Approval-rule zeroes (`approvals_left == 0`) support the read-back; they must not override `approved=false` or `approved_by=[]`.
- There is no default reviewer. `approved_by` is observed live state, not a name to invent.

## Request review

Never invent a reviewer. Use an explicit `reviewer:USERNAME` or a reviewer already assigned on the MR. If none exists, ask who to assign.

Prefer the GitLab instance's native request-review or reviewer-assignment operation. Then read back reviewers, current head SHA, approval state, and discussions.

## Issues

```bash
glab api "projects/${PROJECT}/issues/${IID}"
glab api "projects/${PROJECT}/issues/${IID}/notes?per_page=100&sort=asc"
glab api --method POST "projects/${PROJECT}/issues/${IID}/notes" --field body="$BODY"
glab api "projects/${PROJECT}/issues/${IID}/links"
```

Skip system notes when classifying material requests. Related MRs: issue links plus search of open MRs that mention the issue iid.

## Open or merge a merge request

```bash
git push -u origin HEAD
glab mr create --target-branch "$TARGET" --title "$TITLE" --description "$BODY"
glab api --method PUT "projects/${PROJECT}/merge_requests/${IID}/merge" \
  --field sha="${HEAD_SHA}"
```

Push options may create an MR when the user asked for a push/MR and the GitLab instance supports them. Creating an MR is not permission to merge it.

`/git-merge-approved-force` uses the same exact-head merge field. If approval rules reject the force merge, report the forge error. Do not push the source branch into the target locally.

## Inbox signals

```bash
glab api todos
glab api "merge_requests?scope=all&state=opened&reviewer_username=${USER}"
glab api "merge_requests?scope=all&state=opened&author_username=${USER}"
glab api "issues?scope=all&state=opened&assignee_username=${USER}"
```

Treat `/todos` as notification signals. Refresh the issue or MR before classifying reply or review need.

## Conflicts and mergeability

GitLab conflict flags or a merge status that requires target-branch repair is `CONFLICTED`. `blocking_discussions_resolved=false` with actionable unresolved notes is `NEEDS_REVISION`.
