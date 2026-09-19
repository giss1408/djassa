#!/usr/bin/env bash
set -euo pipefail

# Start monitoring stack in a cross-platform way.
# Detect host internal address used by Docker for Mac/Windows vs Linux.
HOST_INTERNAL=host.docker.internal
if [[ "$(uname -s)" == "Linux" ]]; then
  # On Linux, host.docker.internal may not be available; use gateway
  HOST_INTERNAL=$(ip route | awk '/default/ { print $3 }')
fi

# render prometheus config
TEMPLATE_DIR="$(cd "$(dirname "$0")/../monitoring" && pwd)"
OUT=${TEMPLATE_DIR}/prometheus.yml
sed "s/{{HOST_INTERNAL}}/${HOST_INTERNAL}/g" ${TEMPLATE_DIR}/prometheus.yml.tmpl > ${OUT}

echo "Using HOST_INTERNAL=${HOST_INTERNAL}"
docker-compose -f $(cd "$(dirname "$0")/.." && pwd)/monitoring/docker-compose.monitoring.yml up -d

echo "Grafana: http://localhost:3000, Prometheus: http://localhost:9090, Alertmanager: http://localhost:9093"
