#!/usr/bin/env bash
set -euo pipefail

# Run Alembic migrations for backend-api
cd "$(dirname "$0")/.."

: "Ensure DATABASE_URL is set or fall back to sqlite"
: ${DATABASE_URL:="sqlite+aiosqlite:///./test.db"}

echo "Running migrations with DATABASE_URL=${DATABASE_URL}"
alembic -c alembic.ini upgrade head
echo "Migrations applied."
