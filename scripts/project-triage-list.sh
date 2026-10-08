#!/usr/bin/env bash
# One project-triage PR/MR list. Stdout is {listTruncated, rows}.
# GraphQL variables are bound with -f; the query text stays single-quoted.
# shellcheck disable=SC2016
# Usage: project-triage-list.sh github OWNER REPO
#        project-triage-list.sh gitlab PROJECT
set -euo pipefail
kind="${1:-}"
here="$(cd "$(dirname "$0")" && pwd)"
case "$kind" in
  github)
    owner="${2:?owner}"
    name="${3:?repo}"
    gh api graphql -f owner="$owner" -f name="$name" -f query='
query($owner:String!,$name:String!){repository(owner:$owner,name:$name){pullRequests(states:[OPEN],first:30,orderBy:{field:UPDATED_AT,direction:DESC}){pageInfo{hasNextPage} nodes{
number title state isDraft url author{login} reviewDecision mergeable headRefOid baseRefName
reviewRequests(first:5){totalCount}
reviews(last:8){nodes{author{login} state submittedAt body}}
comments(last:8){nodes{author{login} createdAt body}}
reviewThreads(last:40){pageInfo{hasNextPage} nodes{isResolved comments(last:8){nodes{author{login} createdAt body}}}}
commits(last:15){nodes{commit{committedDate messageHeadline}}}
timelineItems(last:8,itemTypes:[REVIEW_REQUESTED_EVENT]){nodes{...on ReviewRequestedEvent{createdAt}}}
}}}}' | jq --arg kind gh -f "$here/project-triage-list.jq"
    ;;
  gitlab)
    project="${2:?project}"
    glab api graphql -f path="$project" -f query='
query($path:ID!){project(fullPath:$path){mergeRequests(state:opened,first:30,sort:UPDATED_DESC){pageInfo{hasNextPage} nodes{
iid title state draft webUrl author{username} approved mergeableDiscussionsState diffHeadSha targetBranch mergeStatusEnum
reviewers(first:10){nodes{username mergeRequestInteraction{reviewState}}}
discussions(last:40){pageInfo{hasNextPage} nodes{resolvable resolved notes(last:8){nodes{system body createdAt author{username}}}}}
commits(first:30){nodes{committedDate message}}
}}}}' | jq --arg kind gl -f "$here/project-triage-list.jq"
    ;;
  *)
    echo "usage: project-triage-list.sh github OWNER REPO | gitlab PROJECT" >&2
    exit 2
    ;;
esac
