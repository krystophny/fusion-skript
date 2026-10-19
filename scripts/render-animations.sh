#!/usr/bin/env bash
# Render the Manim scenes into a flat media directory:
#   <media-dir>/<slug>.mp4, <slug>.png (poster still) and <slug>.stamp
# A scene is skipped when its stamp (hash of the scene source, style.py and
# this script) is unchanged and both outputs exist.  Scenes render in
# parallel (JOBS, default: number of CPUs).
#
# Quality: MANIM_QUALITY (default h, 1080p60; no preview renders are published).
# Usage: scripts/render-animations.sh [media-dir]
#        scripts/render-animations.sh --slugs     (print the expected slugs)
# Needs `manim` (0.21) with a TeX that has the stix2 package, and ffmpeg, on
# PATH; plasma-skript's dev shell provides both (nix develop <plasma-skript>).
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
self="$repo_root/scripts/render-animations.sh"

# source file | scene class | output slug | poster time in seconds | kin6d export
scenes=(
  "coulomb_collision.py|CoulombCollision|coulomb-collision|7.0|"
)

if [[ "${1:-}" == "--slugs" ]]; then
  for entry in "${scenes[@]}"; do
    IFS='|' read -r _ _ slug _ _ <<<"$entry"
    echo "$slug"
  done
  exit 0
fi

hash_files() {
  if command -v sha256sum >/dev/null 2>&1; then
    cat "$@" | sha256sum | cut -d' ' -f1
  else
    cat "$@" | shasum -a 256 | cut -d' ' -f1
  fi
}

# Data-driven scenes also depend on the loader and their exported data
# (animations/data/kin6d/<export>/, the optional fifth scene field).
scene_stamp() {
  local files=("$repo_root/animations/$1" "$repo_root/animations/style.py" "$self")
  # Shared model modules (e.g. radial_coulomb.py) are scene inputs too.
  while IFS= read -r f; do files+=("$f"); done < <(find "$repo_root/animations" -maxdepth 1 -name "*.py" ! -name "$1" ! -name style.py | LC_ALL=C sort)
  local data="$repo_root/animations/data/kin6d/$2"
  if [[ -n "$2" && -d "$data" ]]; then
    files+=("$repo_root/animations/kin6d_data.py")
    while IFS= read -r f; do files+=("$f"); done < <(find "$data" -type f | LC_ALL=C sort)
  fi
  hash_files "${files[@]}"
}

# Worker mode: render one scene (invoked through xargs below).
if [[ "${1:-}" == "--render-one" ]]; then
  media_dir="$2"
  IFS='|' read -r source scene slug poster data <<<"$3"
  work="$(mktemp -d "${TMPDIR:-/tmp}/fusion-manim.XXXXXX")"
  trap 'rm -rf -- "$work"' EXIT
  export XDG_CONFIG_HOME="${XDG_CONFIG_HOME:-$work/xdg}"
  export MPLCONFIGDIR="${MPLCONFIGDIR:-$work/mpl}"
  mkdir -p "$XDG_CONFIG_HOME" "$MPLCONFIGDIR"
  if ! manim render "-q${MANIM_QUALITY:-h}" --format=mp4 --progress_bar none \
    --media_dir "$work/media" "$repo_root/animations/$source" "$scene" \
    >"$work/log" 2>&1; then
    echo "render failed: $scene" >&2
    tail -n 40 "$work/log" >&2
    exit 1
  fi
  video="$(find "$work/media" -type f -name "$scene.mp4" -print -quit)"
  if [[ -z "$video" ]]; then
    echo "Manim did not produce $scene.mp4" >&2
    exit 1
  fi
  cp "$video" "$work/$slug.mp4"
  # Accurate YUV->RGB rounding keeps the poster background at the exact
  # style.py BG (the default swscale path shifts it, a visible box on the
  # slides' dark letterboxing).
  ffmpeg -loglevel error -y -ss "$poster" -i "$video" -frames:v 1 \
    -vf "scale=960:-1:flags=lanczos+accurate_rnd+full_chroma_int" "$work/$slug.png"
  mv -f "$work/$slug.mp4" "$media_dir/$slug.mp4"
  mv -f "$work/$slug.png" "$media_dir/$slug.png"
  scene_stamp "$source" "$data" >"$media_dir/$slug.stamp"
  echo "rendered $slug"
  exit 0
fi

media_dir="${1:-${MEDIA_DIR:-$repo_root/.cache/animations}}"
mkdir -p "$media_dir"
media_dir="$(cd "$media_dir" && pwd)"

todo=()
for entry in "${scenes[@]}"; do
  IFS='|' read -r source _ slug _ data <<<"$entry"
  stamp="$(scene_stamp "$source" "$data")"
  if [[ -f "$media_dir/$slug.mp4" && -f "$media_dir/$slug.png" \
    && "$(cat "$media_dir/$slug.stamp" 2>/dev/null)" == "$stamp" ]]; then
    continue
  fi
  todo+=("$entry")
done

if ((${#todo[@]} == 0)); then
  echo "All ${#scenes[@]} animations are up to date in $media_dir"
  exit 0
fi

jobs="${JOBS:-$(nproc 2>/dev/null || getconf _NPROCESSORS_ONLN 2>/dev/null || echo 2)}"
echo "Rendering ${#todo[@]} of ${#scenes[@]} animations with $jobs parallel jobs"
printf '%s\n' "${todo[@]}" \
  | xargs -P "$jobs" -I{} bash "$self" --render-one "$media_dir" {}
echo "Animations written to $media_dir"
