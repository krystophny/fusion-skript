#!/usr/bin/env bash
# Build, test and export every time; --release also pushes main to both
# remotes and deploys the locally built site to the gh-pages branch, which
# GitHub Pages serves without rebuilding.
# Never creates commits on main, stages files or changes existing remotes;
# each gh-pages commit is one generated site whose parent is the previous one.
set -euo pipefail
cd "$(dirname "$0")/.."
release=0
# GitHub SSH transfers from this network sometimes stall without failing:
# keepalives end a dead connection, and each network step is retried.
export GIT_SSH_COMMAND="${GIT_SSH_COMMAND:-ssh} -o ServerAliveInterval=5 -o ServerAliveCountMax=3"
retry() { local i; for i in 1 2 3; do timeout "${T:-60}" "$@" && return 0; echo "retrying: $*" >&2; done; return 1; }
# GitHub Pages sometimes times out while syncing a large site, or abandons the
# deployment, and then keeps serving the previous site. Wait for the build of
# the pushed commit and request a new one until it is live.
pages_live() {
  local sha=$1 repo=$2 attempt i status
  for attempt in 1 2 3; do
    for i in $(seq 90); do
      status=$(gh api "repos/$repo/pages/builds/latest" --jq "select(.commit == \"$sha\") | .status" 2>/dev/null || true)
      [[ "$status" == built ]] && { echo "GitHub Pages serves ${sha:0:7}"; return 0; }
      [[ "$status" == errored ]] && break
      sleep 10
    done
    echo "GitHub Pages did not deploy ${sha:0:7}; requesting a new build" >&2
    gh api -X POST "repos/$repo/pages/builds" >/dev/null
  done
  echo "GitHub Pages still serves an older site" >&2
  return 1
}
dest="${COURSE_FOLDER:-$HOME/Nextcloud/lv/fusion/2026}"
while (($#)); do
  case "$1" in
    --release) release=1; shift ;;
    --dest) dest="${2:?Missing destination}"; shift 2 ;;
    *) echo "usage: $0 [--dest folder] [--release]" >&2; exit 2 ;;
  esac
done
if ((release)); then
  [[ "$(git branch --show-current)" == main ]] || { echo "--release requires the main branch" >&2; exit 1; }
  [[ -z "$(git status --porcelain)" ]] || { echo "--release requires a clean worktree" >&2; exit 1; }
  # Validate configured remotes before build/export so a miss cannot leave a partial release.
  for entry in \
    'origin|git@gitlab.tugraz.at:plasma/proj/teaching/fusion-skript.git' \
    'github|git@github.com:krystophny/fusion-skript.git'; do
    IFS='|' read -r remote url <<<"$entry"
    git remote | rg -qx "$remote" || { echo "missing required remote: $remote" >&2; exit 1; }
    [[ "$(git remote get-url --all "$remote")" == "$url" ]]
    [[ "$(git remote get-url --push --all "$remote")" == "$url" ]]
  done
fi
# Only what changed since the last run is rebuilt or retested.
make -j"$(nproc)" site check
bash scripts/export-course-folder.sh "$dest"
if ((release)); then
  export FUSION_PUBLISH_IN_PROGRESS=1
  index=$(mktemp -u)
  GIT_INDEX_FILE="$index" git --work-tree=public add -f -A .
  tree=$(GIT_INDEX_FILE="$index" git write-tree)
  rm -f "$index"
  # The previous deploy is the parent, so the push sends only changed files;
  # an unchanged site is not pushed and Pages does not redeploy.
  parent=$(T=15 retry git ls-remote github refs/heads/gh-pages | cut -f1)
  git cat-file -e "$parent^{commit}" 2>/dev/null || retry git fetch -q github gh-pages
  site=""
  if [[ "$(git rev-parse "$parent^{tree}")" != "$tree" ]]; then
    site=$(git commit-tree "$tree" -p "$parent" -m "Site built from $(git rev-parse --short HEAD)")
  fi
  retry git push origin main & origin=$!
  retry git push github main ${site:+"$site:refs/heads/gh-pages"}
  wait "$origin"
  pages_live "$(git rev-parse "${site:-$parent}")" krystophny/fusion-skript
fi
