#!/usr/bin/env bash
# Build every numbered lecture deck; helper .typ files are excluded.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p public/slides
# Deck figures (slides/build/fig) from the derivation plot data.
"${PYTHON:-python3}" slides/figures.py >/dev/null
for source in slides/[0-9]*-*.typ; do
  [[ -f "$source" ]] || continue
  stem="$(basename "$source" .typ)"
  typst compile --root . --font-path fonts --ignore-system-fonts "$source" "public/slides/$stem.pdf"
done
