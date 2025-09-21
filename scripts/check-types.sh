#!/usr/bin/env bash
cd "$(dirname "$0")/.."
set -euo pipefail

uv run pyright
