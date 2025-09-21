#!/usr/bin/env bash
cd "$(dirname "$0")/.." || exit 1
set -euo pipefail

. scripts/up.sh
docker compose exec dev uv run tests/test_main.py
docker compose down --remove-orphans --volumes
