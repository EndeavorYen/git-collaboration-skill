# Reduce one project PR/MR GraphQL list to triage rows.
# --arg kind is gh or gl. Latest notes come from comments(last:N) / notes(last:N);
# the first comment in a thread is not the latest note. A reviewer follow-up
# that is the latest comment stays in the row.
# A commit only merges the target branch in when its subject starts with
# "Merge branch" or "Merge remote-tracking branch" and quotes that target
# (or origin/<target>).
# Commit and note times are normalized to UTC before max. Every *At value ends in Z.
# GitLab commits(first:30) is newest-first; the max is still by UTC time.
def target_merge($base):
  ((. // "") | split("\n")[0]) as $s
  | (($s | startswith("Merge branch ")) or ($s | startswith("Merge remote-tracking branch ")))
    and (($s | contains("\u0027" + $base + "\u0027")) or ($s | contains("\u0027origin/" + $base + "\u0027")));
def utc:
  if . == null then null
  elif (type != "string") or . == "" then null
  elif test("Z$") then sub("\\.[0-9]+Z$"; "Z")
  else capture("^(?<d>.{19})(\\.[0-9]+)?(?<s>[+-])(?<h>[0-9]{2}):(?<m>[0-9]{2})$") as $x
    | ($x.d + "Z" | fromdateiso8601)
      - (($x.h | tonumber) * 3600 + ($x.m | tonumber) * 60) * (if $x.s == "+" then 1 else -1 end)
    | todate
  end;
def kept($rows):
  [$rows[]? | select(.a != null and .a != "" and .t != null and .b != "")];
def pack($o; $m; $u; $c; $req; $trunc):
  {
    latestFeedback: (if ($o | length) == 0 then null else $o | max_by(.t) | {author: .a, at: .t, excerpt: .b[0:160]} end),
    authorReplyAt: (if ($m | length) == 0 then null else $m | max_by(.t) | .t end),
    unresolvedNonAuthor: ($u | length),
    latestNonMergeAt: (if ($c | length) == 0 then null else [$c[] | select(. != null)] | if length == 0 then null else max end end),
    reviewRequestAt: $req,
    discussionsTruncated: $trunc
  };
def note_kind($b):
  if ($b | contains("removed review request")) then "remove"
  elif ($b | contains("requested review from")) then "request"
  else null end;
def review_events:
  [ .discussions.nodes[]?.notes.nodes[]?
    | select(.system == true)
    | (note_kind(.body // "")) as $kind
    | select($kind != null)
    | (.createdAt | utc) as $t
    | select($t != null)
    | ([.body | scan("@([A-Za-z0-9_.-]+)") | .[0]]) as $who
    | (if ($who | length) == 0 then [{kind: $kind, t: $t, who: null}]
       else [$who[] | {kind: $kind, t: $t, who: .}] end)[]
  ];
def pending_at:
  if length == 0 then null
  else
    [ group_by(.who)[] | sort_by(.t) | last | select(.kind == "request") | .t ]
    | if length == 0 then null else max end
  end;
if $kind == "gh" then
  {
    listTruncated: (.data.repository.pullRequests.pageInfo.hasNextPage // false),
    rows: [.data.repository.pullRequests.nodes[]? | . as $p
      | ([$p.reviews.nodes[]? | {a: .author.login, t: (.submittedAt | utc), b: (.body // "")}]
        + [$p.comments.nodes[]? | {a: .author.login, t: (.createdAt | utc), b: (.body // "")}]
        + [$p.reviewThreads.nodes[]?.comments.nodes[]? | {a: .author.login, t: (.createdAt | utc), b: (.body // "")}]) as $n
      | kept($n | map(select(.a != $p.author.login))) as $o
      | kept($n | map(select(.a == $p.author.login))) as $m
      | [$p.reviewThreads.nodes[]? | select(.isResolved | not) | select(any(.comments.nodes[]?; (.author.login // "") != "" and .author.login != $p.author.login)) | 1] as $u
      | [$p.commits.nodes[]?.commit | select((.messageHeadline | target_merge($p.baseRefName)) | not) | .committedDate | utc] as $c
      | [$p.timelineItems.nodes[]?.createdAt | utc | select(. != null)] as $k
      | {number, title, url, state, isDraft, author: $p.author.login, reviewDecision, mergeable, headRefOid, baseRefName}
        + pack($o; $m; $u; $c;
            (if (($p.reviewRequests.totalCount // 0) > 0) and ($k | length) > 0 then $k | max else null end);
            ($p.reviewThreads.pageInfo.hasNextPage // false))]
  }
elif $kind == "gl" then
  {
    listTruncated: (.data.project.mergeRequests.pageInfo.hasNextPage // false),
    rows: [.data.project.mergeRequests.nodes[]? | . as $p
      | [$p.discussions.nodes[]?.notes.nodes[]? | select(.system | not) | {a: .author.username, t: (.createdAt | utc), b: (.body // "")}] as $n
      | kept($n | map(select(.a != $p.author.username))) as $o
      | kept($n | map(select(.a == $p.author.username))) as $m
      | [$p.discussions.nodes[]? | select(.resolvable == true and .resolved != true) | select(any(.notes.nodes[]?; (.system | not) and (.author.username // "") != "" and .author.username != $p.author.username)) | 1] as $u
      | [$p.commits.nodes[]? | select((.message | target_merge($p.targetBranch)) | not) | .committedDate | utc] as $c
      | ($p | review_events | pending_at) as $req
      | {iid, title, url: .webUrl, state, draft, author: $p.author.username, approved, mergeableDiscussionsState, headRefOid: .diffHeadSha, targetBranch, mergeStatusEnum,
          reviewers: [$p.reviewers.nodes[]? | {username, reviewState: .mergeRequestInteraction.reviewState}]}
        + pack($o; $m; $u; $c; $req; ($p.discussions.pageInfo.hasNextPage // false))]
  }
else
  error("kind must be gh or gl")
end
