#!/usr/bin/env bash
set -euo pipefail

# Simple deploy script for a PoC on a freshly provisioned Ubuntu server.
# Usage: copy this repo to the server or git clone, then run: ./deploy-poc.sh

# Warning: this script is intentionally minimal for PoC use. Review .env values
# before running in any environment accessible from the Internet.

COMPOSE_FILE=docker-compose.poc.yml

function ensure_binary() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "$1 not found. Please install it first."
    exit 1
  fi
}

ensure_binary docker
ensure_binary docker-compose

# Ensure env file exists
if [ ! -f .env ]; then
  echo ".env file not found. Creating a minimal .env"
  cat > .env <<EOF
DATABASE_URL=postgresql+asyncpg://djassa:djassa@db:5432/djassa
CELERY_BROKER_URL=redis://redis:6379/0
SECRET_KEY=please-change-me
MOBILE_MONEY_SECRETS=change-me
EOF
  echo "Created .env — edit it before starting for production use."
fi

echo "Starting PoC stack using $COMPOSE_FILE"
docker compose -f "$COMPOSE_FILE" up -d --build

echo "Deployment finished. Services status:"
docker compose -f "$COMPOSE_FILE" ps

echo "To view logs: docker compose -f $COMPOSE_FILE logs -f web"
