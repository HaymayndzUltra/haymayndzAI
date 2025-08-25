#!/usr/bin/env python3
"""
Detect framework markers in the repository and emit rule_attach_log.json.

Supported frameworks (initial set):
- frontend: react, vue, angular, svelte
- backend: node, python, php, go, dotnet
- mobile: flutter, react-native, ionic

The detector scans for common markers and maps them to corresponding
`.cursor/frameworks/<group>/<name>.mdc` rule files if present.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple


@dataclass
class MarkerSpec:
    description: str
    # (kind, path_or_regex)
    # kind ∈ {"file", "glob", "regex", "json-dep"}
    checks: List[Tuple[str, str]]


def read_text_safe(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def json_has_dep(pkg_json: Path, dep_name: str) -> bool:
    try:
        data = json.loads(pkg_json.read_text(encoding="utf-8"))
    except Exception:
        return False
    for key in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
        if isinstance(data.get(key), dict) and dep_name in data[key]:
            return True
    return False


def glob_count(root: Path, pattern: str, limit: int = 1000) -> Tuple[int, List[str]]:
    try:
        matches = [str(p) for p in root.rglob(pattern)][:limit]
        return len(matches), matches
    except Exception:
        return 0, []


def file_exists(root: Path, relative: str) -> bool:
    return (root / relative).exists()


def regex_anywhere(
    root: Path,
    pattern: str,
    exts: Tuple[str, ...] = (".md", ".mdx", ".py", ".ts", ".tsx", ".js", ".jsx", ".go", ".php", ".cs", ".json", ".yml", ".yaml"),
) -> bool:
    rx = re.compile(pattern, re.IGNORECASE)
    for p in root.rglob("*"):
        if p.is_file() and p.suffix.lower() in exts and p.stat().st_size < 2_000_000:
            try:
                if rx.search(read_text_safe(p)):
                    return True
            except Exception:
                continue
    return False


def build_specs() -> Dict[str, MarkerSpec]:
    specs: Dict[str, MarkerSpec] = {
        # Frontend
        "frontend/react": MarkerSpec(
            description="React app markers",
            checks=[
                ("file", "package.json"),
                ("json-dep", "react"),
                ("glob", "**/*.tsx"),
                ("glob", "**/*.jsx"),
            ],
        ),
        "frontend/vue": MarkerSpec(
            description="Vue app markers",
            checks=[("file", "package.json"), ("json-dep", "vue"), ("glob", "**/*.vue")],
        ),
        "frontend/angular": MarkerSpec(
            description="Angular markers",
            checks=[("file", "angular.json"), ("glob", "**/*.ts")],
        ),
        "frontend/svelte": MarkerSpec(
            description="Svelte markers",
            checks=[("file", "package.json"), ("json-dep", "svelte"), ("glob", "**/*.svelte")],
        ),
        # Backend
        "backend/node": MarkerSpec(
            description="Node/Express markers",
            checks=[("file", "package.json"), ("regex", r"express|koa|fastify")],
        ),
        "backend/python": MarkerSpec(
            description="Python markers",
            checks=[("glob", "**/*.py"), ("file", "pyproject.toml"), ("file", "requirements.txt")],
        ),
        "backend/php": MarkerSpec(
            description="PHP markers",
            checks=[("glob", "**/*.php"), ("file", "composer.json")],
        ),
        "backend/go": MarkerSpec(
            description="Go markers",
            checks=[("file", "go.mod"), ("glob", "**/*.go")],
        ),
        "backend/dotnet": MarkerSpec(
            description=".NET/C# markers",
            checks=[("glob", "**/*.cs"), ("glob", "**/*.sln")],
        ),
        # Mobile
        "mobile/flutter": MarkerSpec(
            description="Flutter markers",
            checks=[("file", "pubspec.yaml"), ("glob", "**/*.dart")],
        ),
        "mobile/react-native": MarkerSpec(
            description="React Native markers",
            checks=[("file", "package.json"), ("json-dep", "react-native"), ("glob", "**/*.tsx")],
        ),
        "mobile/ionic": MarkerSpec(
            description="Ionic markers",
            checks=[("file", "package.json"), ("json-dep", "@ionic"), ("glob", "**/*.ts")],
        ),
    }
    return specs


def rule_file_for(framework_key: str, root: Path) -> Optional[str]:
    base = root / ".cursor" / "frameworks"
    group, name = framework_key.split("/", 1)
    if group not in {"frontend", "backend", "mobile", "specialized"}:
        path = base / framework_key
        path = path.with_suffix(".mdc")
    else:
        path = base / group / f"{name}.mdc"
    return str(path.relative_to(root)) if path.exists() else None


def detect(root: Path, key: str, spec: MarkerSpec) -> Tuple[bool, List[Dict[str, object]], List[str]]:
    evidence: List[Dict[str, object]] = []
    matched_files: List[str] = []
    positives = 0
    any_glob_match = False
    has_glob_spec = False
    json_dep_results: List[bool] = []
    has_json_dep_spec = False

    for kind, arg in spec.checks:
        if kind == "file":
            exists = file_exists(root, arg)
            evidence.append({"type": kind, "path": arg, "present": exists})
            if exists:
                positives += 1
        elif kind == "glob":
            has_glob_spec = True
            count, matches = glob_count(root, arg)
            evidence.append({"type": kind, "path": arg, "matches": count})
            matched_files.extend(matches[:5])
            if count > 0:
                positives += 1
                any_glob_match = True
        elif kind == "regex":
            found = regex_anywhere(root, arg)
            evidence.append({"type": kind, "pattern": arg, "present": found})
            if found:
                positives += 1
        elif kind == "json-dep":
            has_json_dep_spec = True
            pj = root / "package.json"
            ok = pj.exists() and json_has_dep(pj, arg)
            evidence.append({"type": kind, "dep": arg, "present": ok})
            if ok:
                positives += 1
            json_dep_results.append(ok)
        else:
            evidence.append({"type": kind, "detail": arg, "present": False})

    # Detection policy
    json_ok = (not has_json_dep_spec) or all(json_dep_results)
    if not json_ok:
        detected = False
    else:
        if has_glob_spec:
            detected = any_glob_match
        else:
            detected = positives >= 2
    rule_path = rule_file_for(key, root)
    confidence = "high" if detected and rule_path else ("medium" if detected else "low")
    return detected, evidence, matched_files[:10]


def atomic_write_json(path: Path, payload: dict) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def main() -> int:
    parser = argparse.ArgumentParser(description="Rule attach detector")
    parser.add_argument("--output", default="rule_attach_log.json", help="Output JSON path")
    args = parser.parse_args()

    root = Path.cwd()
    specs = build_specs()
    entries: List[Dict[str, object]] = []

    for key, spec in specs.items():
        detected, markers, matched_files = detect(root, key, spec)
        rule_file = rule_file_for(key, root)
        entries.append({
            "framework": key,
            "rule_file": rule_file,
            "detected": detected,
            "confidence": "high" if detected and rule_file else ("medium" if detected else "low"),
            "markers": markers,
            "matched_files": matched_files,
        })

    out = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repo_root": str(root.resolve()),
        "entries": entries,
    }

    out_path = Path(args.output)
    if not out_path.is_absolute():
        out_path = Path.cwd() / out_path
    atomic_write_json(out_path, out)
    print(f"✅ Wrote {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())