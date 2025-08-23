#!/usr/bin/env python3
import argparse, json, os, sys
from index_writer import INDEX_PATH, load_index, upsert_entry, write_atomic_json, recover_index

def cmd_add(args):
    entry = json.loads(args.entry)
    upsert_entry(entry, INDEX_PATH)
    print("OK: added", entry.get("id"))

def cmd_rebuild(args):
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "examples"))
    names = [
        "Action_Plan.md.sidecar.json",
        "Summary_Report.md.sidecar.json",
        "Validation_Report.md.sidecar.json",
        "Final_Implementation_Plan.md.sidecar.json",
    ]
    idx = {"version": 1, "artifacts": []}
    for n in names:
        p = os.path.join(base, n)
        if os.path.exists(p):
            idx["artifacts"].append(json.load(open(p)))
    write_atomic_json(INDEX_PATH, idx)
    print("OK: rebuilt index")

def cmd_verify(args):
    idx = load_index(INDEX_PATH)
    assert "artifacts" in idx and isinstance(idx["artifacts"], list)
    print("OK: verify; artifacts:", len(idx["artifacts"]))

def cmd_simulate_crash(args):
    # Write journal only, skip final replace, then run recovery
    idx = load_index(INDEX_PATH)
    idx["simulated"] = True
    journal_path = INDEX_PATH + ".journal"
    open(journal_path, "w", encoding="utf-8").write(json.dumps(idx, separators=(",", ":"), sort_keys=True))
    print("Wrote journal. Simulating crash before commit...")
    recovered = recover_index(INDEX_PATH)
    print("Recovered:", recovered)

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add"); a.add_argument("entry"); a.set_defaults(func=cmd_add)
    r = sub.add_parser("rebuild"); r.set_defaults(func=cmd_rebuild)
    v = sub.add_parser("verify"); v.set_defaults(func=cmd_verify)
    s = sub.add_parser("simulate_crash"); s.set_defaults(func=cmd_simulate_crash)
    args = ap.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()


