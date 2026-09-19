#!/usr/bin/env bash
set -euo pipefail

# Run test suite for backend-api
cd "$(dirname "$0")/.."

echo "Running pytest..."
pytest -q
