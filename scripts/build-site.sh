#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 derivations/energy.py
python3 derivations/chapters/ch00_energy_context.py
python3 derivations/chapters/ch00_electricity_costs.py
python3 derivations/chapters/ch02_fusion_reactions.py
python3 derivations/chapters/ch02_reactivity.py
python3 derivations/chapters/ch04_power_balance.py
python3 scripts/plot-ch00-teaching.py
python3 scripts/plot-electricity-costs.py
python3 slides/figures.py >/dev/null
python3 slides/figures_sfactor.py >/dev/null
python3 slides/figures_pp.py >/dev/null
python3 slides/figures_reactivity.py >/dev/null
python3 slides/figures_power_balance.py >/dev/null
mkdir -p public/slides public/fonts slides/build
# The site root forwards to the deck launcher (present/); there is no script.
cp src/index.html public/index.html
cp fonts/*.otf fonts/OFL.txt public/fonts/
# Registered animations: posters, checksum-verified MP4s, player pages.
python3 scripts/prepare-media.py public
bash scripts/build-slides.sh
python3 scripts/build-present.py --course "Fusion Physics" --short-name Fusion --strict-metadata
bash scripts/build-notebooks.sh
echo "Lecture decks and presenter written to public/"
