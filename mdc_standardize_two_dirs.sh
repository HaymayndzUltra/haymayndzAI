#!/usr/bin/env bash
set -euo pipefail
if [[ $# -ne 2 ]]; then echo "Usage: $0 <dirA> <dirB>" >&2; exit 2; fi
if [[ ! -f tools/mdc_linter.py ]]; then echo "tools/mdc_linter.py not found" >&2; exit 2; fi
python3 tools/mdc_linter.py --paths "$1" "$2" --write
echo "✅ Standardized MDC frontmatter in: $1 and $2"
