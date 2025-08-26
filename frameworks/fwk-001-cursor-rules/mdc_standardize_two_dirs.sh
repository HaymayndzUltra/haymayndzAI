#!/usr/bin/env bash
set -euo pipefail
if [[ $# -ne 2 ]]; then
  echo "Usage: $0 <dirA> <dirB>" >&2
  exit 2
fi
DIR_A="$1"
DIR_B="$2"
if [[ ! -f tools/mdc_linter.py ]]; then
  echo "tools/mdc_linter.py not found" >&2
  exit 2
fi
python3 tools/mdc_linter.py --paths "$DIR_A" "$DIR_B" --write
echo "✅ Standardized MDC frontmatter in: $DIR_A and $DIR_B"
