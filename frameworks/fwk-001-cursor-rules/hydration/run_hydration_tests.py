#!/usr/bin/env python3
import yaml, sys
from hydration_selector import select_candidate

def main(path: str) -> int:
    data = yaml.safe_load(open(path, "r", encoding="utf-8").read())
    cases = data.get("cases", [])
    failed = 0
    for case in cases:
        got = select_candidate(case.get("candidates", []))
        if got.get("path") != case.get("expect", {}).get("path"):
            failed += 1
            print("FAIL:", case.get("name"), "got=", got.get("path"), "expect=", case.get("expect"))
    if failed:
        print(f"FAILED {failed}/{len(cases)} cases")
        return 1
    print(f"OK: {len(cases)} cases")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))


