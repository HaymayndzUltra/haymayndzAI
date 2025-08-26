#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re, shutil
from pathlib import Path
from typing import Dict, List, Tuple

FRAMEWORK_KEYWORDS: Dict[str, List[str]] = {
    # frontend
    "frontend/react": ["react", "next", "tsx", "jsx"],
    "frontend/vue": ["vue", "nuxt"],
    "frontend/svelte": ["svelte"],
    "frontend/angular": ["angular"],
    # backend
    "backend/python": ["python", "fastapi", "django", "flask"],
    "backend/node": ["node", "nestjs", "fastify", "express"],
    "backend/php": ["php", "laravel", "wordpress", "woocommerce", "drupal"],
    "backend/go": ["go ", "golang"],
    "backend/java": ["java", "spring"],
    "backend/rust": ["rust"],
    # mobile
    "mobile/flutter": ["flutter", "dart"],
    "mobile/react-native": ["react native", "expo"],
    "mobile/ios": ["swift", "ios", "swiftui"],
    # specialized
    "specialized/ecommerce": ["shopify", "woocommerce", "wordpress"],
}

GLOBAL_KEYWORDS: List[Tuple[str, List[str]]] = [
    ("security", ["security", "owasp", "sast", "dast", "xss", "sqli"]),
    ("testing", ["testing", "pytest", "qa", "rspec"]),
    ("devops", ["terraform", "devops", "iac"]),
]


def select_files(source: Path, frameworks: List[str], max_per_fw: int = 2) -> Dict[str, str]:
    mapping: Dict[str, str] = {}
    files = [p for p in source.glob("*.mdc") if p.is_file()]
    lower_name: Dict[Path, str] = {p: p.name.lower() for p in files}

    picked: set[Path] = set()

    # Per-framework picks
    for fw in frameworks:
        keys = FRAMEWORK_KEYWORDS.get(fw, [])
        if not keys:
            continue
        count = 0
        for p in files:
            if p in picked:
                continue
            name = lower_name[p]
            if any(k in name for k in keys):
                picked.add(p)
                count += 1
                if count >= max_per_fw:
                    break

    # Global picks (one each if matches)
    for label, keys in GLOBAL_KEYWORDS:
        for p in files:
            if p in picked:
                continue
            name = lower_name[p]
            if any(k in name for k in keys):
                picked.add(p)
                break

    return {str(p): p.name for p in picked}


def promote(mapping: Dict[str, str], dest: Path) -> List[str]:
    dest.mkdir(parents=True, exist_ok=True)
    written: List[str] = []

    # Clean previous curated selections we managed
    idx = dest / ".selected.json"
    prev_files: List[str] = []
    if idx.exists():
        try:
            prev_files = json.loads(idx.read_text(encoding="utf-8")).get("files", [])
        except Exception:
            prev_files = []
    for fname in prev_files:
        fp = dest / fname
        if fp.exists():
            try:
                fp.unlink()
            except Exception:
                pass

    for src_str, name in mapping.items():
        src = Path(src_str)
        dst = dest / f"curated_{name}"
        shutil.copy2(src, dst)
        written.append(dst.name)

    idx.write_text(json.dumps({"files": written}, indent=2), encoding="utf-8")
    return written


def main() -> int:
    ap = argparse.ArgumentParser(description="Curated selector for promoting .cursor/test-rules based on detected frameworks")
    ap.add_argument("--attach-log", required=True)
    ap.add_argument("--source", default=".cursor/test-rules")
    ap.add_argument("--dest", default=".cursor/rules")
    ap.add_argument("--max-per-fw", type=int, default=2)
    args = ap.parse_args()

    root = Path.cwd()
    attach = json.loads(Path(args.attach_log).read_text(encoding="utf-8"))
    frameworks = [e["framework"] for e in attach.get("entries", []) if e.get("detected")]

    src = (root / args.source).resolve()
    dst = (root / args.dest).resolve()

    mapping = select_files(src, frameworks, max_per_fw=args.max_per_fw)
    written = promote(mapping, dst)

    print(json.dumps({"frameworks": frameworks, "selected": list(mapping.values()), "written": written}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())