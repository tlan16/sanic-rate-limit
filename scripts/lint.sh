#!/usr/bin/env bash
cd "$(dirname "$0")/.." || exit 1
set -euo pipefail

# Lint Python code
echo "Linting python code with ruff..."
uv run ruff check
uv run ruff format --check

echo "All linting completed successfully."
