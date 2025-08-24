#!/usr/bin/env bash
set -Eeuo pipefail

ROOT=/workspace
PKG_NAME=repo
MODULE_DIR="$ROOT/src/$PKG_NAME"
TOOLS_DIR="$ROOT/tools"
APPLY="${APPLY:-0}"

mkdir -p "$MODULE_DIR" "$TOOLS_DIR"

mapfile -t files < <(find "$ROOT" -maxdepth 1 -type f -name '*.py' -printf '%f\n' | sort)
[ ${#files[@]} -eq 0 ] && { echo "No root .py files."; exit 0; }

cli_count=0; mod_count=0
echo "Plan (APPLY=$APPLY):"
for base in "${files[@]}"; do
  src="$ROOT/$base"
  if grep -qE 'if __name__ == [\"'\'']__main__[\"'\'']' "$src"; then
    dest="$TOOLS_DIR/$base"
    echo "CLI  : $src -> $dest"
    if [ "$APPLY" = "1" ]; then
      mkdir -p "$(dirname "$dest")"
      if git ls-files --error-unmatch "$src" >/dev/null 2>&1; then git mv "$src" "$dest"; else mv "$src" "$dest"; fi
      chmod +x "$dest" || true
    fi
    cli_count=$((cli_count+1))
  else
    dest="$MODULE_DIR/$base"
    echo "MOD  : $src -> $dest"
    if [ "$APPLY" = "1" ]; then
      mkdir -p "$(dirname "$dest")"
      if git ls-files --error-unmatch "$src" >/dev/null 2>&1; then git mv "$src" "$dest"; else mv "$src" "$dest"; fi
    fi
    mod_count=$((mod_count+1))
  fi
done

if [ "$APPLY" = "1" ]; then
  touch "$MODULE_DIR/__init__.py"
  cd "$ROOT"
  git add -A
  git commit -m "Organize root Python files into tools/ (CLI) and src/$PKG_NAME (modules)" || echo "Nothing to commit"
fi

echo "Summary: CLI=$cli_count, Modules=$mod_count"
