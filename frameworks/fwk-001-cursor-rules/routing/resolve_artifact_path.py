#!/usr/bin/env python3
import json, os, sys

ROUTING_JSON = os.path.join(os.path.dirname(__file__), "artifact_routing.json")

def resolve_path(framework: str, artifact_type: str, artifact_id: str) -> str:
    cfg = json.load(open(ROUTING_JSON, "r", encoding="utf-8"))
    routes = [r for r in cfg.get("routes", []) if r.get("artifactType") == artifact_type]
    if not routes:
        raise KeyError(f"No route for artifactType={artifact_type}")
    # deterministic: sort by pathPattern
    routes.sort(key=lambda r: r.get("pathPattern", ""))
    pattern = routes[0]["pathPattern"]
    return pattern.replace("{framework}", framework).replace("{artifactId}", artifact_id)

def main(argv: list[str]) -> int:
    if len(argv) != 4:
        print("Usage: resolve_artifact_path.py <framework> <artifact_type> <artifact_id>")
        return 2
    _, fwk, typ, aid = argv
    try:
        print(resolve_path(fwk, typ, aid))
        return 0
    except Exception as e:
        print("ERROR:", e)
        return 1

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))


