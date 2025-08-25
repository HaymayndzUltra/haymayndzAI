import os, re, json
ROOT = "/workspace"
RULES_DIR = os.path.join(ROOT, ".cursor", "rules")
TEST_DIR = os.path.join(ROOT, ".cursor", "test")

UNIVERSAL_FILES = {
    "execution_orchestrator.mdc",
    "memory_ai.mdc",
    "rules_master_toggle.mdc",
    "framework_memory_bridge.mdc",
}

FM_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)
FILENAME_COMMENT_RE = re.compile(r"^#\s*.*\.mdc\s*$", re.IGNORECASE)

def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

def has_frontmatter(text: str) -> bool:
    return text.startswith("---\n")

def build_frontmatter(description: str, globs: list, always_apply: bool) -> str:
    parts = [
        "---",
        "description: >",
        "  {}".format(description),
        "globs: {}".format(json.dumps(globs)),
        "alwaysApply: {}".format(str(always_apply).lower()),
        "---",
        "",
    ]
    return "\n".join(parts)

def strip_filename_comments(text: str) -> str:
    lines = text.splitlines()
    out = []
    for ln in lines:
        if FILENAME_COMMENT_RE.match(ln.strip()):
            continue
        out.append(ln)
    res = "\n".join(out)
    if not res.endswith("\n"):
        res += "\n"
    return res

def infer_framework_and_globs(name: str):
    lower = name.lower()
    # Mobile
    if "flutter" in lower or " dart " in lower or lower.endswith("-dart.mdc"):
        return ("Framework-specific rules for Flutter/Dart. Auto-applies to Dart projects.", ["**/*.dart", "pubspec.yaml"]) 
    if "react native" in lower or "react-native" in lower or "expo" in lower:
        return ("Framework-specific rules for React Native. Auto-applies to RN projects.", ["**/*.ts", "**/*.tsx", "**/*.js", "**/*.jsx"]) 
    if "ionic" in lower or "capacitor" in lower or "cordova" in lower:
        return ("Framework-specific rules for Ionic/Capacitor. Auto-applies to hybrid mobile apps.", ["**/*.ts", "**/*.tsx", "**/*.js", "**/*.jsx"]) 
    # Frontend
    if "react" in lower or "next" in lower:
        return ("Framework-specific rules for React/Next.js. Auto-applies to TS/JS and JSX/TSX.", ["**/*.ts", "**/*.tsx", "**/*.js", "**/*.jsx", "next.config.*"]) 
    if "vue" in lower:
        return ("Framework-specific rules for Vue/Nuxt. Auto-applies to Vue SFCs and TS/JS.", ["**/*.vue", "**/*.ts", "**/*.js", "nuxt.config.*"]) 
    if "angular" in lower:
        return ("Framework-specific rules for Angular. Auto-applies to Angular workspaces.", ["**/*.ts", "**/*.js", "angular.json"]) 
    if "svelte" in lower:
        return ("Framework-specific rules for Svelte/SvelteKit. Auto-applies to Svelte projects.", ["**/*.svelte", "**/*.ts", "**/*.js", "svelte.config.*"]) 
    # Backend/languages
    if any(k in lower for k in ["python", "django", "fastapi", "flask", "odoo", "jax"]):
        return ("Framework-specific rules for Python (Django/FastAPI/Flask).", ["**/*.py", "requirements.txt", "pyproject.toml"]) 
    if any(k in lower for k in ["php", "laravel", "wordpress", "woocommerce", "drupal"]):
        return ("Framework-specific rules for PHP (Laravel/WordPress/Drupal).", ["**/*.php", "composer.json"]) 
    if any(k in lower for k in ["typescript", "node", "nest", "express", "fastify", "remix", "astro", "htmx", "bootstrap", "svelte", "vue", "react"]):
        return ("Framework-specific rules for TypeScript/JavaScript stacks.", ["**/*.ts", "**/*.tsx", "**/*.js", "**/*.jsx"]) 
    if ".net" in lower or "asp" in lower or "blazor" in lower or "unity" in lower:
        return ("Framework-specific rules for .NET/C#.", ["**/*.cs", "**/*.csproj", "**/*.sln"]) 
    if " go" in lower or lower.endswith("-go.mdc") or lower.startswith("go-") or ".go" in lower or " golang" in lower:
        return ("Framework-specific rules for Go.", ["**/*.go", "go.mod", "go.sum"]) 
    if "rust" in lower or "solana" in lower:
        return ("Framework-specific rules for Rust/Solana.", ["**/*.rs", "Cargo.toml"]) 
    if "solidity" in lower or "smart contract" in lower:
        return ("Framework-specific rules for Solidity/Smart Contracts.", ["**/*.sol", "hardhat.config.*", "foundry.toml"]) 
    if "ruby" in lower or "rails" in lower:
        return ("Framework-specific rules for Ruby on Rails.", ["**/*.rb", "Gemfile"]) 
    if "julia" in lower:
        return ("Framework-specific rules for Julia.", ["**/*.jl", "Project.toml"]) 
    if "lua" in lower:
        return ("Framework-specific rules for Lua.", ["**/*.lua"]) 
    if "arduino" in lower or "esp32" in lower or "esp8266" in lower:
        return ("Framework-specific rules for Arduino/C++.", ["**/*.c", "**/*.cpp", "**/*.h", "**/*.hpp"]) 
    if "salesforce" in lower or "apex" in lower or "trigger" in lower:
        return ("Framework-specific rules for Salesforce/Apex.", ["**/*.cls", "**/*.trigger"]) 
    if "terraform" in lower:
        return ("Framework-specific rules for Terraform.", ["**/*.tf", "**/*.tfvars"]) 
    if "ghost" in lower or "handlebars" in lower or "hbs" in lower:
        return ("Framework-specific rules for Ghost/Handlebars.", ["**/*.hbs"]) 
    if "shopify" in lower or "liquid" in lower:
        return ("Framework-specific rules for Shopify/Liquid.", ["**/*.liquid"]) 
    if "business central" in lower or lower.endswith("-al.mdc"):
        return ("Framework-specific rules for AL (Business Central).", ["**/*.al"]) 
    # Default fallback to TS/JS
    return ("Framework-specific rules for TypeScript/JavaScript stacks.", ["**/*.ts", "**/*.tsx", "**/*.js", "**/*.jsx"]) 

updates = []

# Process system/rules files
for fname in sorted(os.listdir(RULES_DIR)):
    if not fname.endswith(".mdc"):
        continue
    fpath = os.path.join(RULES_DIR, fname)
    original = read(fpath)
    content = strip_filename_comments(original)

    is_universal = (fname in UNIVERSAL_FILES) or fname.startswith("guidance_")
    is_role = fname.endswith("_ai.mdc") and fname != "memory_ai.mdc"

    if is_universal:
        base = fname[:-4]
        desc = "Universal guidance rule: {} — Always active across the workspace.".format(base)
        globs = ["**/*"]
        always = True
    elif is_role:
        role_name = fname[:-4].replace(_,
