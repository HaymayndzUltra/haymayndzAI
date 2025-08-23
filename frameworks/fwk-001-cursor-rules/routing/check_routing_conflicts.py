#!/usr/bin/env python3
import json, os, sys

THIS_DIR = os.path.dirname(__file__)
ROUTING_JSON = os.path.join(THIS_DIR, "artifact_routing.json")
REPORT = os.path.abspath(os.path.join(THIS_DIR, "..", "DOCS", "changes", "routing_conflicts_report.md"))

def main() -> int:
    os.makedirs(os.path.dirname(REPORT), exist_ok=True)
    data = json.load(open(ROUTING_JSON, "r", encoding="utf-8"))
    routes = data.get("routes", [])
    # naive conflict detection: duplicate artifactType entries with differing patterns
    seen = {}
    conflicts = []
    for r in routes:
        t = r.get("artifactType")
        p = r.get("pathPattern")
        if t in seen and seen[t] != p:
            conflicts.append((t, seen[t], p))
        else:
            seen[t] = p
    with open(REPORT, "w", encoding="utf-8") as f:
        if not conflicts:
            f.write("# Routing Conflicts Report\n\nNo conflicts detected.\n")
        else:
            f.write("# Routing Conflicts Report\n\n")
            for t, a, b in conflicts:
                f.write(f"- CONFLICT for {t}: '{a}' vs '{b}'\n")
    print("OK: report written:", REPORT)
    return 0 if not conflicts else 1

if __name__ == "__main__":
    sys.exit(main())


