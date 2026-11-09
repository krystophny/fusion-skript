#!/usr/bin/env bash
# Thin wrapper for CI and habit: the Makefile owns the build graph.
set -euo pipefail
cd "$(dirname "$0")/.."
make -j"$(nproc)" site
echo "Lecture decks and presenter written to public/"
