#!/usr/bin/env python3
import os, re, sys
from collections import defaultdict
from typing import List, Optional, Tuple

REQUIRED_PATHS = [
    "memory-bank/plan/product_backlog.yaml",
    "memory-bank/plan/client_brief.md",
]

def path_exists(root: str, rel: str) -> bool:
    return os.path.exists(os.path.join(root, rel))

def validate_root(root: str) -> bool:
    try:
        for rel in REQUIRED_PATHS:
            if not path_exists(root, rel):
                return False
        return True
    except Exception:
        return False

def choose_repo_root(argv: List[str]) -> Tuple[str, bool]:
    # Priority: --root arg > REPO_ROOT env > /workspace > /home/haymayndz
    # Returns (root, is_default_path)
    arg_root: Optional[str] = None
    for i, a in enumerate(argv):
        if a == "--root" and i + 1 < len(argv):
            arg_root = argv[i + 1]
            break
        if a.startswith("--root="):
            arg_root = a.split("=", 1)[1]
            break

    if arg_root and validate_root(arg_root):
        return arg_root, False

    env_root = os.getenv("REPO_ROOT")
    if env_root and validate_root(env_root):
        return env_root, False

    candidates = ["/workspace", "/home/haymayndz"]
    for c in candidates:
        if validate_root(c):
            return c, True

    # Last resort: current working directory
    cwd = os.getcwd()
    if validate_root(cwd):
        return cwd, True

    # Failure
    msg = [
        "Unable to locate repo root. Tried:",
        f"- --root ARG: {arg_root or '(none)'}",
        f"- REPO_ROOT env: {env_root or '(none)'}",
        "- /workspace",
        "- /home/haymayndz",
        f"- CWD: {cwd}",
        "",
        f"Each root must contain: {', '.join(REQUIRED_PATHS)}",
    ]
    print("\n".join(msg), file=sys.stderr)
    sys.exit(2)

def parse_yaml_items_fast(backlog_path: str):
    items, cur, in_items = [], None, False
    rx = {
        "id": re.compile(r"^\s*-\s+id:\s+(\S+)\s*$"),
        "title": re.compile(r"^\s*title:\s*(.+?)\s*$"),
        "priority": re.compile(r"^\s*priority:\s*(\S+)\s*$"),
        "owner_role": re.compile(r"^\s*owner_role:\s*(\S+)\s*$"),
    }
    with open(backlog_path, "r", encoding="utf-8") as f:
        for line in f:
            if not in_items and line.strip() == "items:":
                in_items = True
                continue
            if not in_items:
                continue
            m = rx["id"].match(line)
            if m:
                if cur:
                    items.append(cur)
                cur = {"id": m.group(1)}
                continue
            if cur:
                for k in ("title", "priority", "owner_role"):
                    mm = rx[k].match(line)
                    if mm:
                        cur[k] = mm.group(1).strip()
    if cur:
        items.append(cur)
    return items

def extract_brief_gaps(brief_path: str):
    lines = [l.rstrip("\n") for l in open(brief_path, "r", encoding="utf-8")]
    def collect(start_idx: int):
        out, i = [], start_idx + 1
        while i < len(lines):
            s = lines[i].strip()
            if s.startswith("## ") or s.startswith("### "):
                break
            if s.startswith("- "):
                out.append(s[2:].strip())
            i += 1
        return out
    gaps, i = {}, 0
    while i < len(lines):
        s = lines[i].strip()
        if s == "## Identified Gaps":
            gaps["Identified Gaps"] = collect(i)
        elif s.startswith("### "):
            gaps[s[4:].strip()] = collect(i)
        i += 1
    return gaps

def summarize_by_priority(items):
    buckets = defaultdict(list)
    for it in items:
        buckets[it.get("priority","P?")].append(it)
    for k in buckets:
        buckets[k] = sorted(buckets[k], key=lambda x: x.get("id",""))
    return dict(sorted(buckets.items()))

def coverage_map(backlog_titles):
    def has_title_substring(keyword):
        return any(keyword.lower() in t.lower() for t in backlog_titles)

    cov = {}
    cov["API Design Standards"] = "uncovered"
    cov["Agent Lifecycle"] = "uncovered"
    cov["Context Window Management"] = "uncovered"
    cov["Model Drift Handling"] = "uncovered"
    cov["Zero Trust Architecture"] = "uncovered"
    cov["Role Mapping Blind Spots"] = "uncovered"
    cov["Compliance Validation"] = "uncovered"

    cov["Memory & State Management"] = "partial" if has_title_substring("Memory learning loop") else "uncovered"
    cov["Dependency Security"] = "uncovered"
    cov["Infrastructure / CI-CD"] = "uncovered"
    cov["Operational Readiness"] = "uncovered"
    cov["Testing Depth"] = "partial" if (has_title_substring("Security QA") or has_title_substring("Performance")) else "uncovered"
    cov["Observability / Monitoring"] = "partial" if has_title_substring("Observability") else "uncovered"
    cov["Technology Coverage"] = "partial" if any(has_title_substring(k) for k in ["Java", "Rust", "Unity", "iOS", "E-commerce"]) else "uncovered"
    return cov

def main(argv: List[str]):
    root, is_default = choose_repo_root(argv)
    backlog_path = os.path.join(root, "memory-bank/plan/product_backlog.yaml")
    brief_path = os.path.join(root, "memory-bank/plan/client_brief.md")

    items = parse_yaml_items_fast(backlog_path)
    buckets = summarize_by_priority(items)
    backlog_titles = [it.get("title","") for it in items]

    print(f"repo_root: {root} ({'auto' if is_default else 'explicit'})")
    print("Backlog counts by priority:", {k: len(v) for k, v in buckets.items()})
    print("Top P0 IDs:", [it["id"] for it in buckets.get("P0", [])])
    print("Client Brief Coverage Map (queue-free):")
    for k, status in coverage_map(backlog_titles).items():
        print(f"- {k}: {status}")

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except SystemExit:
        raise
    except Exception as e:
        print(f"Error: {e!r}", file=sys.stderr)
        sys.exit(1)