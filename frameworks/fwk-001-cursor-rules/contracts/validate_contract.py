#!/usr/bin/env python3
import json, os, subprocess, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
CONTRACT = os.path.join(os.path.dirname(__file__), "framework_contract_framework1.json")

def main() -> int:
    cfg = json.load(open(CONTRACT, "r", encoding="utf-8"))
    # Check required files
    missing = [p for p in cfg["requiredFiles"] if not os.path.exists(os.path.join(ROOT, p))]
    if missing:
        print("MISSING files:", missing)
        return 1
    # Hydration tests
    cmds = cfg["validation"]
    for name in ["hydrationTests", "routingConflicts", "indexVerify"]:
        cmd = cmds[name]
        print("RUN:", cmd)
        res = subprocess.run(cmd, shell=True)
        if res.returncode != 0:
            print("FAIL:", name)
            return res.returncode
    print("OK: contract validated")
    return 0

if __name__ == "__main__":
    sys.exit(main())


