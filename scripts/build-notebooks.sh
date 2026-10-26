#!/usr/bin/env bash
# Render the OJS notebooks to public/notebooks/. A staging copy adds the data
# files they read, so notebooks and Python derivations share one source.
set -euo pipefail
cd "$(dirname "$0")/.."
stage=build/notebooks
rm -rf "$stage"
mkdir -p "$stage/data"
cp notebooks/_quarto.yml notebooks/*.qmd notebooks/*.js notebooks/*.json notebooks/*.css "$stage/"
xargs -a notebooks/data-files.txt cp -t "$stage/data/"
if command -v quarto >/dev/null; then
  quarto=(quarto)
elif command -v nix >/dev/null; then
  quarto=(nix run nixpkgs#quarto --)
else
  echo "quarto not found (install it or nix)" >&2; exit 1
fi
(cd "$stage" && "${quarto[@]}" render --quiet)
rm -rf public/notebooks
mkdir -p public
cp -r "$stage/_site" public/notebooks
echo "Notebooks written to public/notebooks/"
