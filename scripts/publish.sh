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
fi
