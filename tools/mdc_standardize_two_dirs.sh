#!/usr/bin/env bash
set -euo pipefail
shopt -s nullglob

ROOT="/workspace"
TARGETS=(
  "$ROOT/.cursor/rules"
  "$ROOT/.cursor/test"
)
REPORT="$ROOT/STD_REPORT.md"
: > "$REPORT"

echo "# MDC Standardization Report ($(date -u +%F' '%T'Z'))" >> "$REPORT"

default_globs() {
  local slug="$1"; slug="${slug,,}"
  if [[ "$slug" =~ (react|next|gatsby|remix|astro|tailwind|htmx|bootstrap|css|html) ]]; then
    echo '"**/*.tsx", "**/*.jsx", "**/*.ts", "**/*.js", "package.json", "tsconfig.json", "next.config.js"'; return
  fi
  if [[ "$slug" =~ (react-native|expo) ]]; then
    echo '"**/*.tsx", "**/*.ts", "**/*.js", "app.json", "app.config.*", "package.json"'; return
  fi
  if [[ "$slug" =~ (svelte|sveltekit) ]]; then
    echo '"**/*.svelte", "**/*.ts", "**/*.js", "package.json", "svelte.config.*"'; return
  fi
  if [[ "$slug" =~ (vue|nuxt) ]]; then
    echo '"**/*.vue", "**/*.ts", "**/*.js", "package.json", "nuxt.config.*"'; return
  fi
  if [[ "$slug" =~ (python|django|fastapi|flask|jupyter|pandas|numpy|seaborn) ]]; then
    echo '"**/*.py", "requirements.txt", "pyproject.toml", "setup.cfg"'; return
  fi
  if [[ "$slug" =~ (php|laravel|wordpress|woocommerce) ]]; then
    echo '"**/*.php", "composer.json"'; return
  fi
  if [[ "$slug" =~ (flutter|dart) ]]; then
    echo '"**/*.dart", "pubspec.yaml"'; return
  fi
  if [[ "$slug" =~ (ruby|rails|rspec) ]]; then
    echo '"**/*.rb", "Gemfile", "Gemfile.lock"'; return
  fi
  if [[ "$slug" =~ (go|golang) ]]; then
    echo '"**/*.go", "go.mod", "go.sum"'; return
  fi
  if [[ "$slug" =~ (rust) ]]; then
    echo '"**/*.rs", "Cargo.toml", "Cargo.lock"'; return
  fi
  if [[ "$slug" =~ (java|spring|quarkus) ]]; then
    echo '"**/*.java", "**/*.kt", "pom.xml", "build.gradle", "settings.gradle", "gradle.properties"'; return
  fi
  if [[ "$slug" =~ (kotlin|android) ]]; then
    echo '"**/*.kt", "**/*.java", "**/*.xml", "build.gradle", "settings.gradle", "gradle.properties"'; return
  fi
  if [[ "$slug" =~ (elixir|phoenix) ]]; then
    echo '"**/*.{ex,exs}", "mix.exs"'; return
  fi
  if [[ "$slug" =~ (prisma|sql|dbml|postgres) ]]; then
    echo '"**/*.sql", "**/*.prisma", "**/*.dbml", "schema.prisma", "migrations/**"'; return
  fi
  if [[ "$slug" =~ (terraform|iac) ]]; then
    echo '"**/*.tf", "**/*.tfvars", "**/*.hcl"'; return
  fi
  echo '"**/*"'
}

is_universal() {
  local base="$1"
  [[ "$base" == execution_orchestrator.mdc ]] && return 0
  [[ "$base" == memory_ai.mdc ]] && return 0
  [[ "$base" == rules_master_toggle.mdc ]] && return 0
  [[ "$base" == guidance_* ]] && return 0
  return 1
}

is_ai_role() {
  local base="$1"
  [[ "$base" == *_ai.mdc ]] && return 0 || return 1
}

desc_universal() {
  local base="$1"
  if [[ "$base" == execution_orchestrator.mdc ]]; then
    echo "Universal orchestration rule for coordinating multi-step executions and flows."
  elif [[ "$base" == memory_ai.mdc ]]; then
    echo "Universal memory system to enhance recall and context continuity across tasks."
  elif [[ "$base" == rules_master_toggle.mdc ]]; then
    echo "Universal control: master toggle for enabling or suppressing rule suites."
  elif [[ "$base" == guidance_* ]]; then
    echo "Universal guidance rule providing global behavioral guidance. Always active."
  else
    echo "Universal guidance rule."
  fi
}

desc_ai_role() {
  local base="$1"; local role="${base%_ai.mdc}"; role="${role//_/ }"
  echo "AI role specialization for $role — activated when explicitly requested or selected by context."
}

desc_framework() {
  local slug="$1"; slug="${slug,,}"; local tech="the target technology/framework"
  [[ "$slug" =~ (react|next) ]] && tech="React/Next.js"
  [[ "$slug" =~ (react-native|expo) ]] && tech="React Native/Expo"
  [[ "$slug" =~ (svelte|sveltekit) ]] && tech="Svelte/SvelteKit"
  [[ "$slug" =~ (vue|nuxt) ]] && tech="Vue/Nuxt"
  [[ "$slug" =~ (python|django|fastapi|flask) ]] && tech="Python"
  [[ "$slug" =~ (php|laravel|wordpress|woocommerce) ]] && tech="PHP"
  [[ "$slug" =~ (flutter|dart) ]] && tech="Flutter/Dart"
  [[ "$slug" =~ (ruby|rails) ]] && tech="Ruby on Rails"
  [[ "$slug" =~ (go|golang) ]] && tech="Go"
  [[ "$slug" =~ (rust) ]] && tech="Rust"
  [[ "$slug" =~ (java|spring|quarkus) ]] && tech="Java/Spring/Quarkus"
  [[ "$slug" =~ (kotlin|android) ]] && tech="Kotlin/Android"
  [[ "$slug" =~ (elixir|phoenix) ]] && tech="Elixir/Phoenix"
  [[ "$slug" =~ (prisma|sql|dbml|postgres) ]] && tech="Database/SQL/Prisma"
  [[ "$slug" =~ (terraform|iac) ]] && tech="Terraform/IaC"
  echo "Framework-specific rules for $tech. Auto-applies to relevant file types via globs."
}

clean_content() {
  local f="$1"; local base="$2"; local tmp_out="$3"
  local t; t="$(mktemp)"; cp -- "$f" "$t"
  awk 'NR<=5 && tolower($0) ~ /^[[:space:]]*#?[[:space:]]*[a-z0-9._-]+[.]mdc[[:space:]]*$/ { next }
       NR<=5 && tolower($0) ~ /^[[:space:]]*#?[[:space:]]*file(name)?/ { next }
       { print }' "$t" > "$tmp_out"
  sed -E '/^[[:space:]]*(#|\/\/)[[:space:]].*\.mdc[[:space:]]*$/Id' -i "$tmp_out"
  rm -f "$t"
}

add_frontmatter() {
  local f="$1"; local base="$2"; local slug="$3"; local dir="$4"
  if head -n1 -- "$f" | grep -q '^---[[:space:]]*$'; then
    echo "SKIP: $f (already has frontmatter)" >> "$REPORT"
    return 0
  fi
  local kind globs always desc
  if [[ "$dir" == */.cursor/rules ]]; then
    if is_universal "$base"; then
      kind="universal"; globs='"**/*"'; always="true"; desc="$(desc_universal "$base")"
    elif is_ai_role "$base"; then
      kind="ai_role"; globs='"**/*"'; always="false"; desc="$(desc_ai_role "$base")"
    else
      kind="universal"; globs='"**/*"'; always="false"; desc="Universal project rule."
    fi
  else
    kind="framework"; globs="$(default_globs "$slug")"; always="false"; desc="$(desc_framework "$slug")"
  fi
  desc="${desc//"/\"}"
  local body_tmp out_tmp; body_tmp="$(mktemp)"; out_tmp="$(mktemp)"
  clean_content "$f" "$base" "$body_tmp"
  {
    printf '---\n'
    printf 'description: >\n'
    printf '  %s\n' "$desc"
    printf 'globs: [%s]\n' "$globs"
    printf 'alwaysApply: %s\n' "$always"
    printf '---\n'
    cat -- "$body_tmp"
    printf '\n'
  } > "$out_tmp"
  mv -- "$out_tmp" "$f"
  rm -f "$body_tmp"
  echo "UPDATED: $f (kind=$kind; alwaysApply=$always; globs=[$globs])" >> "$REPORT"
}

process_dir() {
  local dir="$1"
  [ -d "$dir" ] || return 0
  find "$dir" -maxdepth 1 -type f -name '*.mdc' -print0 | while IFS= read -r -d '' f; do
    local base; base="$(basename -- "$f")"
    local slug; slug="${base,,}"
    add_frontmatter "$f" "$base" "$slug" "$dir"
  done
}

for d in "${TARGETS[@]}"; do process_dir "$d"; done

echo "Done. See $REPORT"

