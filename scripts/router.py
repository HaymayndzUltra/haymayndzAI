#!/usr/bin/env python3
# router.py — minimal deterministic router for fwk-001-cursor-rules
# deps: PyYAML (pip install pyyaml)

import os, re, json, sys
from typing import Dict, Any

try:
    import yaml  # https://pyyaml.org/wiki/PyYAMLDocumentation
except Exception:
    sys.stderr.write("ERROR: PyYAML missing. Install: pip install pyyaml\n")
    sys.exit(2)

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Primary expected path
MDC = os.path.join(REPO, "frameworks", "fwk-001-cursor-rules", "system-prompt", "rules_master_toggle.mdc")
# Fallback to harvested copy if primary missing
MDC_FALLBACK = os.path.join(REPO, "frameworks", "fwk-001-cursor-rules", "DOCS", "harvested", "selection_20250824_090835", "fwk-001-cursor-rules", "system-prompt", "rules_master_toggle.mdc")
OVR  = os.path.join(REPO, "frameworks", "fwk-001-cursor-rules", "DOCS", "changes", "routing_override.yaml")


def _mdc_path() -> str:
    if os.path.isfile(MDC):
        return MDC
    if os.path.isfile(MDC_FALLBACK):
        return MDC_FALLBACK
    sys.stderr.write("ERROR: rules_master_toggle.mdc not found (primary or fallback)\n")
    sys.exit(2)


def load_yaml_blocks(path: str):
    text = open(path, "r", encoding="utf-8").read()
    blocks = re.findall(r"```yaml\n([\s\S]*?)\n```", text)
    out = []
    for b in blocks:
        try:
            out.append(yaml.safe_load(b) or {})
        except Exception:
            pass
    return out


def build_effective() -> Dict[str, Any]:
    roles, routing = {}, {}
    for y in load_yaml_blocks(_mdc_path()):
        if isinstance(y, dict):
            if isinstance(y.get("roles"), dict):
                roles = y["roles"]
            if isinstance(y.get("command_routing"), dict):
                routing = y["command_routing"]

    ovr = {}
    if os.path.isfile(OVR):
        try:
            ovr = yaml.safe_load(open(OVR, "r", encoding="utf-8")) or {}
        except Exception:
            ovr = {}

    # Shallow overrides
    ov_roles = (ovr.get("overrides") or {}).get("roles") or {}
    for rid, patch in ov_roles.items():
        base = roles.get(rid, {"enabled": True, "priority": 0, "triggers": [], "dependencies": []})
        base.update(patch or {})
        roles[rid] = base

    routing.update((ovr.get("overrides") or {}).get("command_routing") or {})
    allowlist = (ovr.get("overrides") or {}).get("allowlist_triggers") or ovr.get("allowlist_triggers") or []
    progressive_mode = bool(ovr.get("progressive_mode", False))

    return {
        "roles": roles,
        "command_routing": routing,
        "allowlist_triggers": allowlist,
        "progressive_mode": progressive_mode,
    }


def resolve(trigger: str) -> Dict[str, Any]:
    eff = build_effective()
    routing = eff["command_routing"]
    roles   = eff["roles"]
    allow   = eff["allowlist_triggers"]
    prog    = eff["progressive_mode"]

    role = routing.get(trigger)
    if role is None:
        return {"ok": False, "reason": "UNKNOWN_TRIGGER", "trigger": trigger, **eff}

    cfg = roles.get(role, {})
    if not cfg.get("enabled", False):
        return {"ok": False, "reason": "ROLE_DISABLED", "trigger": trigger, "role": role, **eff}

    if prog and allow and (trigger not in allow):
        return {"ok": False, "reason": "NOT_ALLOWLISTED", "trigger": trigger, "role": role, **eff}

    return {"ok": True, "trigger": trigger, "role": role, **eff}


def print_status() -> None:
    eff = build_effective()
    roles = eff["roles"]
    table = [
        {"role": k, "enabled": bool(v.get("enabled", False)), "priority": int(v.get("priority", 0))}
        for k, v in roles.items()
    ]
    table.sort(key=lambda r: (not r["enabled"], r["priority"], r["role"]))
    print(json.dumps({"progressive_mode": eff["progressive_mode"], "roles": table}, indent=2))


def main() -> int:
    if len(sys.argv) < 2:
        print("USAGE:\n  router.py route /trigger\n  router.py status", file=sys.stderr)
        return 2
    cmd = sys.argv[1]
    if cmd == "status":
        print_status(); return 0
    if cmd == "route":
        if len(sys.argv) < 3:
            print("ERR: missing trigger, e.g. /plan", file=sys.stderr); return 2
        print(json.dumps(resolve(sys.argv[2]), indent=2)); return 0
    print(f"ERR: unknown cmd {cmd}", file=sys.stderr); return 2


if __name__ == "__main__":
    sys.exit(main())

