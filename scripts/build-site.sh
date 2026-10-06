#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 derivations/energy.py
python3 derivations/chapters/ch00_energy_context.py
python3 scripts/plot-ch00-teaching.py
mkdir -p public/slides slides/build
bash scripts/script-outline.sh slides/build/script-outline.json
TYPST_FEATURES=bundle,html typst compile --root . --font-path fonts --ignore-system-fonts --format bundle src/main.typ public
typst compile --root . --font-path fonts --ignore-system-fonts src/print.typ public/fusion-physics.pdf
bash scripts/build-slides.sh
python3 scripts/build-present.py --course "Fusion Physics" --short-name Fusion --strict-metadata
echo "Local fusion draft written to public/"
