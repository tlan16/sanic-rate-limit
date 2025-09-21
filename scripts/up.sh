#!/usr/bin/env bash
cd "$(dirname "$0")/.." || exit 1
set -euo pipefail

docker compose down --remove-orphans --volumes || true
echo "Building dev service ..."
docker compose build --quiet dev

docker compose up --wait -d dev
