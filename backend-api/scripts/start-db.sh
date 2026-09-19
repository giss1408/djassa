#!/usr/bin/env bash
set -euo pipefail

# Start development Postgres service
cd "$(dirname "$0")/.."
echo "Starting Postgres via docker compose..."
docker compose -f docker-compose.dev.yml up -d db
echo "Postgres started."
