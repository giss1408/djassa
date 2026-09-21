#!/usr/bin/env bash
set -Eeuo pipefail

# Backward-compatible entry point for the VPS test deployment.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "${SCRIPT_DIR}/deploy-vps-test.sh" "$@"
