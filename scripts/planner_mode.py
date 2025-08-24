#!/usr/bin/env python3
import argparse, os, sys, yaml

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OVR  = os.path.join(REPO, "frameworks", "fwk-001-cursor-rules", "DOCS", "changes", "routing_override.yaml")

def load_yaml(path: str):
    if not os.path.isfile(path):
        return {}
    with open(path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f) or {}
    return data

def save_yaml(path: str, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        yaml.safe_dump(data, f, sort_keys=False)

def main() -> int:
    ap = argparse.ArgumentParser(description="Toggle planner mode in routing_override.yaml")
    ap.add_argument("mode", choices=["on","off"], help="Enable or disable planner-first mode")
    args = ap.parse_args()

    data = load_yaml(OVR)
    data = data or {}
    # store under overrides.planner_mode for clarity without breaking existing keys
    ovr = data.get('overrides') or {}
    ovr['planner_mode'] = True if args.mode == 'on' else False
    data['overrides'] = ovr
    save_yaml(OVR, data)
    print(f"planner_mode set to {args.mode.upper()} in {OVR}")
    return 0

if __name__ == '__main__':
    raise SystemExit(main())

