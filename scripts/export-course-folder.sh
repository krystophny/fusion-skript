#!/usr/bin/env bash
# Usage: export-course-folder.sh [destination]
# A public Nextcloud share receives the same complete export as any destination.
set -euo pipefail
exec python3 "$(dirname "$0")/export-course-folder.py" "$@"
