#!/usr/bin/env bash
set -euo pipefail

# Run the FastAPI app with uvicorn
cd "$(dirname "$0")/.."

: ${HOST:=0.0.0.0}
: ${PORT:=8000}

echo "Starting uvicorn on ${HOST}:${PORT}"
uvicorn app.main:app --reload --host ${HOST} --port ${PORT}
