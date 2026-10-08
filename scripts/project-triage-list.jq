# Reduce one project PR/MR GraphQL list to triage rows.
# --arg kind is gh or gl. Latest notes come from comments(last:N) / notes(last:N);
# the first comment in a thread is not the latest note. A reviewer follow-up
# that is the latest comment stays in the row.
# A commit only merges the target branch in when its subject starts with
# "Merge branch" or "Merge remote-tracking branch" and quotes that target
# (or origin/<target>).
def target_merge($base):
  ((. // "") | split("\n")[0]) as $s
  | (($s | startswith("Merge branch ")) or ($s | startswith("Merge remote-tracking branch ")))
    and (($s | contains("\u0027" + $base + "\u0027")) or ($s | contains("\u0027origin/" + $base + "\u0027")));
def kept($rows):
  [$rows[]? | select(.a != null and .a != "" and .b != "")];
def pack($o; $m; $u; $c; $k; $pending; $trunc):
  {
    latestFeedback: (if ($o | length) == 0 then null else $o | max_by(.t) | {author: .a, at: .t, excerpt: .b[0:160]} end),
    authorReplyAt: (if ($m | length) == 0 then null else $m | max_by(.t) | .t end),
    unresolvedNonAuthor: ($u | length),
    latestNonMergeAt: (if ($c | length) == 0 then null else $c | max end),
    reviewRequestAt: (if ($pending | not) or ($k | length) == 0 then null else $k | max end),
    discussionsTruncated: $trunc
  };
if $kind == "gh" then
  [.data.repository.pullRequests.nodes[]? | . as $p
    | ([$p.reviews.nodes[]? | {a: .author.login, t: .submittedAt, b: (.body // "")}]
      + [$p.comments.nodes[]? | {a: .author.login, t: .createdAt, b: (.body // "")}]
      + [$p.reviewThreads.nodes[]?.comments.nodes[]? | {a: .author.login, t: .createdAt, b: (.body // "")}]) as $n
    | kept($n | map(select(.a != $p.author.login))) as $o
    | kept($n | map(select(.a == $p.author.login))) as $m
    | [$p.reviewThreads.nodes[]? | select(.isResolved | not) | select(any(.comments.nodes[]?; (.author.login // "") != "" and .author.login != $p.author.login)) | 1] as $u
    | [$p.commits.nodes[]?.commit | select((.messageHeadline | target_merge($p.baseRefName)) | not) | .committedDate] as $c
    | [$p.timelineItems.nodes[]?.createdAt | select(. != null)] as $k
    | {number, title, url, state, isDraft, author: $p.author.login, reviewDecision, mergeable, headRefOid, baseRefName}
      + pack($o; $m; $u; $c; $k; (($p.reviewRequests.totalCount // 0) > 0); ($p.reviewThreads.pageInfo.hasNextPage // false))]
elif $kind == "gl" then
  [.data.project.mergeRequests.nodes[]? | . as $p
    | [$p.discussions.nodes[]?.notes.nodes[]? | select(.system | not) | {a: .author.username, t: .createdAt, b: (.body // "")}] as $n
    | kept($n | map(select(.a != $p.author.username))) as $o
    | kept($n | map(select(.a == $p.author.username))) as $m
    | [$p.discussions.nodes[]? | select(.resolvable == true and .resolved != true) | select(any(.notes.nodes[]?; (.system | not) and (.author.username // "") != "" and .author.username != $p.author.username)) | 1] as $u
    | [$p.commits.nodes[]? | select((.message | target_merge($p.targetBranch)) | not) | .committedDate] as $c
    | [$p.discussions.nodes[]?.notes.nodes[]? | select(.system == true and ((.body // "") | contains("requested review from")) and (((.body // "") | contains("removed review request")) | not)) | .createdAt] as $k
    | {iid, title, url: .webUrl, state, draft, author: $p.author.username, approved, mergeableDiscussionsState, headRefOid: .diffHeadSha, targetBranch, mergeStatusEnum,
        reviewers: [$p.reviewers.nodes[]? | {username, reviewState: .mergeRequestInteraction.reviewState}]}
      + pack($o; $m; $u; $c; $k; true; ($p.discussions.pageInfo.hasNextPage // false))]
else
  error("kind must be gh or gl")
end
