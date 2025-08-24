#!/usr/bin/env bash
set -Eeuo pipefail

REPO_ROOT=/workspace
OLD_LOCAL=/workspace/frameworks
OLD_SANDBOX=/workspace/frameworks
NEW="$REPO_ROOT/frameworks"

need() { command -v "$1" >/dev/null 2>&1 || { echo "Missing: $1" >&2; exit 1; }; }
need find; need sed; need xargs; need grep; command -v rg >/dev/null 2>&1 || true

echo "REPO_ROOT=$REPO_ROOT"
echo "NEW=$NEW"

mkdir -p "$REPO_ROOT/.cursor/rules" "$REPO_ROOT/.cursor"
touch "$REPO_ROOT/.cursor/analytics.md"

# Consolidate .mdc rules (no overwrite)
if [ -d "$NEW" ]; then
  if command -v rsync >/dev/null 2>&1; then
    find "$NEW" -type f -name '*.mdc' \( -path '*/rules/*' -o -path '*/system-prompt/*' \) -print0 \
    | xargs -0 -r -I{} rsync -ai --ignore-existing "{}" "$REPO_ROOT/.cursor/rules/"
  else
    find "$NEW" -type f -name '*.mdc' \( -path '*/rules/*' -o -path '*/system-prompt/*' \) -print0 \
    | xargs -0 -r -I{} cp -n "{}" "$REPO_ROOT/.cursor/rules/" 2>/dev/null || true
  fi
else
  echo "Warn: frameworks dir not found at $NEW"
fi

# Update hardcoded references OLD -> NEW
update_refs() {
  local FROM="$1"
  local LIST="/tmp/refs.$(echo -n "$FROM" | md5sum | cut -d' ' -f1).txt"

  if command -v rg >/dev/null 2>&1; then
    rg -l --hidden --no-ignore \
      -g '!**/.git/**' -g '!**/node_modules/**' -g '!**/.venv/**' -g '!**/.cursor/rules/**' \
      -F "$FROM" "$REPO_ROOT" > "$LIST" || true
  else
    grep -Rnl --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=.venv --exclude-dir=.cursor \
      -- "$FROM" "$REPO_ROOT" > "$LIST" || true
  fi

  if [ -s "$LIST" ]; then
    echo "Updating $(wc -l < "$LIST") file(s): $FROM -> $NEW"
    xargs -r -a "$LIST" sed -i "s|$FROM|$NEW|g"
  else
    echo "No references to $FROM"
  fi
}

update_refs "$OLD_LOCAL"
update_refs "$OLD_SANDBOX"

# Optional sanity checks
[ -f "$REPO_ROOT/tools/routing_drift_monitor.py" ] && python3 "$REPO_ROOT/tools/routing_drift_monitor.py" || true
if [ -f "$REPO_ROOT/frameworks/fwk-001-cursor-rules/hydration/run_hydration_tests.py" ]; then
  python3 "$REPO_ROOT/frameworks/fwk-001-cursor-rules/hydration/run_hydration_tests.py" \
          "$REPO_ROOT/frameworks/fwk-001-cursor-rules/hydration/hydration_tests.yaml" || true
fi
[ -f "$REPO_ROOT/frameworks/fwk-001-cursor-rules/security/security_gate.py" ] \
  && python3 "$REPO_ROOT/frameworks/fwk-001-cursor-rules/security/security_gate.py" || true

# Commit if needed
cd "$REPO_ROOT"
git add -A
if [ -n "$(git status --porcelain)" ]; then
  git commit -m "Consolidate frameworks; unify rules in .cursor/rules; update path refs (/workspace mapping)"
else
  echo "Nothing to commit"
fi
