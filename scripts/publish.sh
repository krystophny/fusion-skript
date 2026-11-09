#!/usr/bin/env bash
# Build, test and export every time; --release also pushes main to both
# remotes and deploys the locally built site to the gh-pages branch, which
# GitHub Pages serves without rebuilding.
# Never creates commits on main, stages files or changes existing remotes;
# gh-pages holds one generated commit and is replaced on every release.
set -euo pipefail
cd "$(dirname "$0")/.."
release=0
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
# The derivation tests do not read public/, so they run beside the build.
log=$(mktemp)
python3 -m pytest -q >"$log" 2>&1 & tests=$!
bash scripts/build-site.sh
wait "$tests" || { cat "$log" >&2; exit 1; }
tail -1 "$log"
python3 -m pytest -q scripts/test-publishing.py
bash scripts/export-course-folder.sh "$dest"
if ((release)); then
  export FUSION_PUBLISH_IN_PROGRESS=1
  index=$(mktemp -u)
  GIT_INDEX_FILE="$index" git --work-tree=public add -f -A .
  tree=$(GIT_INDEX_FILE="$index" git write-tree)
  rm -f "$index"
  site=$(git commit-tree "$tree" -m "Site built from $(git rev-parse --short HEAD)")
  git push origin main & origin=$!
  git push github main "+$site:refs/heads/gh-pages"
  wait "$origin"
fi
