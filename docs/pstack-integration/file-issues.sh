#!/usr/bin/env bash
# File the pstack integration umbrella and its step issues from the markdown files next to this script.
# Usage: docs/pstack-integration/file-issues.sh [owner/repo]
#   DRY_RUN=1 renders every body into a temp dir and makes no forge write.
set -euo pipefail

REPO="${1:-EndeavorYen/git-collaboration-skill}"
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT="$(mktemp -d)"
DRY_RUN="${DRY_RUN:-0}"

UMBRELLA_FILE="$DIR/00-umbrella.md"
STEP_FILES=("$DIR"/0[1-9]-step-*.md)

title_of() { head -n 1 "$1" | sed 's/^# //'; }

# render <src> <dst> KEY=VALUE...  (drops the title line, replaces {{KEY}} placeholders)
render() {
  local src="$1" dst="$2"
  shift 2
  python3 - "$src" "$dst" "$@" <<'PY'
import sys
src, dst, *pairs = sys.argv[1:]
lines = open(src, encoding="utf-8").read().split("\n")
body = "\n".join(lines[2:] if len(lines) > 1 and lines[1] == "" else lines[1:])
for pair in pairs:
    key, value = pair.split("=", 1)
    body = body.replace("{{" + key + "}}", value)
open(dst, "w", encoding="utf-8").write(body)
PY
}

create_issue() {
  local title="$1" body="$2"
  if [[ "$DRY_RUN" == "1" ]]; then
    echo "https://github.com/$REPO/issues/DRY-$(echo "$title" | md5sum | cut -c1-6)"
    return
  fi
  gh issue create --repo "$REPO" --title "$title" --body-file "$body" --label enhancement --label pstack
}

umbrella_title="$(title_of "$UMBRELLA_FILE")"

if [[ "$DRY_RUN" != "1" ]]; then
  existing="$(gh issue list --repo "$REPO" --state open --search "in:title \"$umbrella_title\"" --json number --jq 'length')"
  if [[ "$existing" != "0" ]]; then
    echo "An open issue titled '$umbrella_title' already exists; refusing to file duplicates." >&2
    exit 1
  fi
  gh label create pstack --repo "$REPO" --color 5319e7 --description "pstack companion integration" 2>/dev/null || true
  gh label create enhancement --repo "$REPO" --color a2eeef --description "New feature or request" 2>/dev/null || true
fi

render "$UMBRELLA_FILE" "$OUT/00.md"
umbrella_url="$(create_issue "$umbrella_title" "$OUT/00.md")"
echo "umbrella: $umbrella_url"

subs=("UMBRELLA=$umbrella_url")
step_urls=()
for i in "${!STEP_FILES[@]}"; do
  n=$((i + 1))
  file="${STEP_FILES[$i]}"
  render "$file" "$OUT/step-$n.md" "${subs[@]}"
  url="$(create_issue "$(title_of "$file")" "$OUT/step-$n.md")"
  echo "step $n: $url"
  step_urls+=("$url")
  subs+=("STEP$n=$url")
done

render "$UMBRELLA_FILE" "$OUT/00-final.md" "${subs[@]}"
if [[ "$DRY_RUN" == "1" ]]; then
  echo "dry run: rendered bodies in $OUT"
  exit 0
fi

umbrella_number="${umbrella_url##*/}"
gh issue edit "$umbrella_number" --repo "$REPO" --body-file "$OUT/00-final.md" >/dev/null

for url in "${step_urls[@]}"; do
  child_id="$(gh api "repos/$REPO/issues/${url##*/}" --jq .id)"
  if ! gh api -X POST "repos/$REPO/issues/$umbrella_number/sub_issues" -F "sub_issue_id=$child_id" >/dev/null 2>&1; then
    echo "sub-issue link failed for $url; the umbrella checklist still links it" >&2
  fi
done

echo "done: $umbrella_url"
