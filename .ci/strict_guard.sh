#!/usr/bin/env bash
set -euo pipefail
if [ "${CI:-}" = "true" ] && [ "${AI_ENFORCEMENT_MODE:-team}" != "team" ]; then
  echo "CI must run with AI_ENFORCEMENT_MODE=team (strict)."
  exit 1
fi
