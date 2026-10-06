#!/usr/bin/env bash
# Build/tests/export every time; --release also pushes main to both remotes.
# Never creates commits, stages files, changes existing remotes, or force-pushes.
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
bash scripts/build-site.sh
python3 -m pytest -q
python3 -m pytest -q scripts/test-publishing.py
bash scripts/export-course-folder.sh "$dest"
if ((release)); then
  export FUSION_PUBLISH_IN_PROGRESS=1
  git push origin main
  git push github main
fi
