#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Dict, Any, List, Tuple


def discover_repo_root() -> Path:
    env = os.getenv("REPO_ROOT")
    if env:
        try:
            return Path(env).resolve()
        except Exception:
            pass
    ws = Path("/workspace")
    if ws.exists():
        return ws.resolve()
    return Path.cwd().resolve()


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_yaml(path: Path) -> Dict[str, Any]:
    import yaml  # lazy import
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def compute_metrics(repo: Path) -> Tuple[Dict[str, Any], List[str]]:
    fwk = repo / "frameworks" / "fwk-001-cursor-rules"
    changes = fwk / "DOCS" / "changes"

    routing_baseline = load_json(changes / "routing_baseline.json")
    override = load_yaml(changes / "routing_override.yaml")
    shadow = json.loads((changes / "routing_effective.shadow.json").read_text(encoding="utf-8"))

    roles: Dict[str, Any] = routing_baseline.get("roles", {})
    routing: Dict[str, str] = routing_baseline.get("command_routing", {})

    alerts: List[str] = []
    progressive_on: bool = bool(override.get("progressive_mode"))
    allowlist: List[str] = list(override.get("overrides", {}).get("allowlist_triggers", []))

    # Expectations under limited Progressive ON (/route only)
    expected_trigger = "/route"
    expected_role = "rules_master_toggle"
    route_target_ok = routing.get(expected_trigger) == expected_role
    role_enabled_ok = roles.get(expected_role, {}).get("enabled", False) is True
    scope_ok = progressive_on and allowlist == [expected_trigger]

    # Drift detection: effective shadow should not alter routing targets
    shadow_routing = shadow.get("command_routing", {})
    no_routing_drift = shadow_routing == routing

    if not progressive_on:
        alerts.append("Progressive mode expected True but found False")
    if allowlist != [expected_trigger]:
        alerts.append(f"Allowlist triggers must be ['{expected_trigger}'] but found {allowlist}")
    if not route_target_ok:
        alerts.append(f"Baseline routing for {expected_trigger} must be {expected_role}")
    if not role_enabled_ok:
        alerts.append(f"Role {expected_role} must be enabled in roles matrix")
    if not no_routing_drift:
        alerts.append("routing_effective.shadow.json differs from baseline routing targets")

    metrics: Dict[str, Any] = {
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime()),
        "progressive_mode": progressive_on,
        "allowlist_triggers": allowlist,
        "route_target_ok": route_target_ok,
        "role_enabled_ok": role_enabled_ok,
        "no_routing_drift": no_routing_drift,
    }
    return metrics, alerts


def write_observability(repo: Path, metrics: Dict[str, Any], alerts: List[str]) -> None:
    fwk = repo / "frameworks" / "fwk-001-cursor-rules"
    obs_dir = fwk / "DOCS" / "reports" / "progressive_observability"
    obs_dir.mkdir(parents=True, exist_ok=True)

    # Dashboard (JSON)
    dash = {
        "component": "routing_progressive_monitor",
        "scope": "limited:/route",
        "metrics": metrics,
        "alerts": alerts,
        "status": "PASS" if not alerts else "WARN" if alerts else "PASS",
    }
    (obs_dir / "monitoring_dashboard.json").write_text(json.dumps(dash, indent=2), encoding="utf-8")

    # Health report (Markdown)
    health_lines = [
        "# Progressive ON Health Report (limited: /route)",
        "",
        f"- Timestamp (UTC): {metrics['timestamp_utc']}",
        f"- Progressive mode: {metrics['progressive_mode']}",
        f"- Allowlist triggers: {metrics['allowlist_triggers']}",
        f"- Route target OK: {metrics['route_target_ok']}",
        f"- Role enabled OK: {metrics['role_enabled_ok']}",
        f"- No routing drift: {metrics['no_routing_drift']}",
        "",
        "## Alerts",
    ]
    if alerts:
        health_lines += [f"- {a}" for a in alerts]
    else:
        health_lines.append("- (none)")
    write_text(obs_dir / "health_report.md", "\n".join(health_lines) + "\n")

    # Alerts log (append)
    if alerts:
        with open(obs_dir / "alert_history.log", "a", encoding="utf-8") as f:
            for a in alerts:
                f.write(f"{metrics['timestamp_utc']} ALERT {a}\n")
    else:
        with open(obs_dir / "alert_history.log", "a", encoding="utf-8") as f:
            f.write(f"{metrics['timestamp_utc']} OK no-alerts\n")


def append_consolidated(repo: Path, metrics: Dict[str, Any], alerts: List[str]) -> None:
    fwk = repo / "frameworks" / "fwk-001-cursor-rules"
    latest = fwk / "DOCS" / "reports" / "Latest_Current.md"
    status = "PASS" if not alerts else "WARN"
    lines = [
        "\n## Progressive Monitoring Snapshot (/route)",
        f"- Timestamp (UTC): {metrics['timestamp_utc']}",
        f"- Status: {status}",
        f"- Progressive mode: {metrics['progressive_mode']}",
        f"- Allowlist: {metrics['allowlist_triggers']}",
        f"- Route target OK: {metrics['route_target_ok']}",
        f"- No routing drift: {metrics['no_routing_drift']}",
    ]
    latest.write_text(latest.read_text() + "\n" + "\n".join(lines) + "\n", encoding="utf-8")


def run_once() -> int:
    repo = discover_repo_root()
    metrics, alerts = compute_metrics(repo)
    write_observability(repo, metrics, alerts)
    append_consolidated(repo, metrics, alerts)
    # Exit non-zero if alerts (to integrate with CI if desired)
    return 1 if alerts else 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Monitor limited Progressive ON (/route) health and produce observability artifacts")
    ap.add_argument("--interval", type=int, default=0, help="Seconds between checks (0 for single run)")
    ap.add_argument("--repeat", type=int, default=1, help="Number of runs (ignored if interval=0)")
    args = ap.parse_args()

    if args.interval <= 0:
        return run_once()

    code = 0
    for i in range(max(args.repeat, 1)):
        rc = run_once()
        code = rc or code
        if i < args.repeat - 1:
            time.sleep(args.interval)
    return code


if __name__ == "__main__":
    sys.exit(main())

