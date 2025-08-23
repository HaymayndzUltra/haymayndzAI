#!/usr/bin/env python3
import os
import re
import sys
import json
import time
from pathlib import Path
from typing import Dict, Any, List, Tuple

try:
	import yaml  # type: ignore
except Exception as e:
	print("PyYAML is required. Install with: pip install pyyaml", file=sys.stderr)
	raise


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


def read_text(path: Path) -> str:
	return path.read_text(encoding="utf-8", errors="ignore")


def extract_yaml_blocks(text: str) -> List[str]:
	blocks: List[str] = []
	code_fence = re.compile(r"```yaml\n([\s\S]*?)```", re.MULTILINE)
	for m in code_fence.finditer(text):
		blocks.append(m.group(1))
	return blocks


def load_yaml_doc(doc: str) -> Any:
	return yaml.safe_load(doc)


def parse_routing_baseline(toggle_text: str) -> Tuple[Dict[str, Any], Dict[str, str]]:
	roles: Dict[str, Any] = {}
	routing: Dict[str, str] = {}
	blocks = extract_yaml_blocks(toggle_text)
	for b in blocks:
		loaded = load_yaml_doc(b) or {}
		if isinstance(loaded, dict) and "roles" in loaded:
			roles = loaded.get("roles", {}) or {}
		if isinstance(loaded, dict) and "command_routing" in loaded:
			routing = loaded.get("command_routing", {}) or {}
	if not roles:
		raise RuntimeError("Could not find roles YAML in rules_master_toggle.mdc")
	if not routing:
		raise RuntimeError("Could not find command_routing YAML in rules_master_toggle.mdc")
	return roles, routing


def parse_gates_baseline(orchestrator_text: str) -> Dict[str, Any]:
	blocks = extract_yaml_blocks(orchestrator_text)
	for b in blocks:
		loaded = load_yaml_doc(b) or {}
		if isinstance(loaded, dict) and "pipeline_gates" in loaded:
			return loaded["pipeline_gates"] or {}
	raise RuntimeError("Could not find pipeline_gates YAML in execution_orchestrator.mdc")


def write_json(path: Path, obj: Any) -> None:
	path.parent.mkdir(parents=True, exist_ok=True)
	path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
	path.parent.mkdir(parents=True, exist_ok=True)
	path.write_text(text, encoding="utf-8")


def build_override(roles: Dict[str, Any]) -> Dict[str, Any]:
	# Minimal safe slice: orchestrator + master toggle + planning + product owner + memory
	keep_enabled = {
		"execution_orchestrator",
		"rules_master_toggle",
		"product_owner_ai",
		"planning_ai",
		"memory_ai",
	}
	ovr_roles: Dict[str, Any] = {}
	for role_name in roles.keys():
		ovr_roles[role_name] = {"enabled": (role_name in keep_enabled)}
	# Ensure dependency: planning_ai depends on product_owner_ai (kept above)
	return {
		"version": 0,
		"scope": "routing_slice_dry_run",
		"timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
		"overrides": {"roles": ovr_roles},
		"notes": "Dry-run: minimal activation slice; mapping unchanged; dependencies respected.",
	}


def apply_override(roles: Dict[str, Any], routing: Dict[str, str], override: Dict[str, Any]) -> Dict[str, Any]:
	roles_eff = json.loads(json.dumps(roles))  # deep copy
	ovr_roles = ((override or {}).get("overrides", {}) or {}).get("roles", {})
	changed_on: List[str] = []
	changed_off: List[str] = []
	for name, cfg in ovr_roles.items():
		if name in roles_eff and isinstance(cfg, dict) and "enabled" in cfg:
			prev = bool(roles_eff[name].get("enabled", False))
			now = bool(cfg["enabled"])
			roles_eff[name]["enabled"] = now
			if prev != now:
				(changed_on if now else changed_off).append(name)
	# Validate routing targets exist
	invalid_targets = [t for t in set(routing.values()) if t not in roles_eff]
	integrity = {
		"invalid_targets": invalid_targets,
		"triggers_changed": [],  # mapping unchanged in this slice
	}
	return {
		"roles": roles_eff,
		"command_routing": routing,
		"diff_summary": {
			"toggled_on": sorted(changed_on),
			"toggled_off": sorted(changed_off),
		},
		"integrity": integrity,
	}


def main() -> int:
	repo = discover_repo_root()
	fwk = "frameworks/fwk-001-cursor-rules"
	toggle_path = repo / fwk / "system-prompt/rules_master_toggle.mdc"
	orch_path = repo / fwk / "system-prompt/execution_orchestrator.mdc"
	changes_dir = repo / fwk / "DOCS/changes"
	reports_dir = repo / fwk / "DOCS/reports"

	try:
		toggle_text = read_text(toggle_path)
		orch_text = read_text(orch_path)
		roles, routing = parse_routing_baseline(toggle_text)
		gates = parse_gates_baseline(orch_text)
		write_json(changes_dir / "routing_baseline.json", {"roles": roles, "command_routing": routing})
		write_json(changes_dir / "gates_baseline.json", {"pipeline_gates": gates, "observability": {"status": "N/A", "reason": "Routing slice dry-run"}})

		override = build_override(roles)
		write_text(changes_dir / "routing_override.yaml", yaml.safe_dump(override, sort_keys=False))

		effective = apply_override(roles, routing, override)
		write_json(changes_dir / "routing_effective.shadow.json", effective)

		# Write a concise labnotes entry in changes area
		entry_lines = [
			f"### {time.strftime('%Y-%m-%d %H:%M:%S')} — DRY-RUN — Routing Slice",
			"",
			"- Scope: Routing matrix and role toggles only",
			"- Diff: mapping unchanged; roles toggled OFF except minimal slice",
			f"- Toggled ON: {', '.join(effective['diff_summary']['toggled_on']) or '(none)'}",
			f"- Toggled OFF: {', '.join(effective['diff_summary']['toggled_off']) or '(none)'}",
			f"- Invalid routing targets: {', '.join(effective['integrity']['invalid_targets']) or '(none)'}",
			"- Gates: parsed from execution_orchestrator.mdc",
			"- Observability: N/A for this slice",
			"- Rollback: restore from routing_baseline.json",
			"- Next: expand slice after gate validation",
		]
		write_text(changes_dir / "labnotes_entry.routing_slice.md", "\n".join(entry_lines) + "\n")

		print("Wrote baselines and dry-run artifacts:")
		print(f"- {changes_dir / 'routing_baseline.json'}")
		print(f"- {changes_dir / 'gates_baseline.json'}")
		print(f"- {changes_dir / 'routing_override.yaml'}")
		print(f"- {changes_dir / 'routing_effective.shadow.json'}")
		print(f"- {changes_dir / 'labnotes_entry.routing_slice.md'}")
		return 0
	except Exception as e:
		print(f"ERROR: {e}", file=sys.stderr)
		return 1


if __name__ == "__main__":
	sys.exit(main())