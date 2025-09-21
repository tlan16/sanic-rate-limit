#!/usr/bin/env bash
cd "$(dirname "$0")/.." || exit 1
set -euo pipefail

SERVICE="dev"

# Check if the service is running
is_running=$(docker compose ps --services --filter "status=running" | grep -Fx "$SERVICE" || true)

# If not running, start it
if [[ -z "$is_running" ]]; then
    echo "Service '$SERVICE' is not running. Starting..."
    . scripts/up.sh
fi

docker compose exec dev uv run tests/test_main.py
docker compose down --remove-orphans --volumes
