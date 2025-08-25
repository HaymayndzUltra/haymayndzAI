#!/usr/bin/env python3
"""
Generate Action_Plan.md from a product backlog (and optional plan artifacts).

Usage:
  python3 tools/generate_action_plan.py \
    --source memory-bank/plan/product_backlog.yaml \
    --tech memory-bank/plan/technical_plan.md \
    --tasks memory-bank/plan/task_breakdown.yaml \
    --output memory-bank/plan/Action_Plan.md

Notes:
  - Designed to be deterministic and idempotent.
  - Produces an "IMPORTANT NOTE" section to satisfy downstream lint checks.
  - Overwrites the output file to remove any previous conflict markers.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


def _ensure_pyyaml_installed() -> None:
    try:
        import yaml  # type: ignore
        _ = yaml  # quiet linters
    except Exception:
        # Best-effort install without interactivity
        import subprocess
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "PyYAML", "--quiet"])  # nosec
        except Exception as exc:
            print(f"WARNING: Failed to install PyYAML automatically: {exc}")
            # We'll fail later on import if still missing


def load_yaml(path: Path) -> Dict[str, Any]:
    import yaml  # type: ignore
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"YAML at {path} must be a mapping at top-level")
    return data


def build_workstreams_lines(backlog: Dict[str, Any]) -> List[str]:
    items: List[Dict[str, Any]] = backlog.get("items", []) or []
    lines: List[str] = []
    for item in items:
        item_id = str(item.get("id", "UNKNOWN")).strip()
        title = str(item.get("title", "")).strip()
        artifacts = item.get("artifacts", []) or []
        artifact_suffix = ""
        if artifacts:
            # Show up to 2 canonical artifacts to keep the plan concise
            shown = ", ".join(f"`{a}`" for a in artifacts[:2])
            artifact_suffix = f" → {shown}"
        line = f"- {item_id}: {title}{artifact_suffix}" if title else f"- {item_id}{artifact_suffix}"
        lines.append(line)
    return lines


def generate_action_plan(
    backlog: Dict[str, Any],
    inputs_backlog_path: str,
    inputs_tech_path: Optional[str],
    inputs_tasks_path: Optional[str],
) -> str:
    client_name = str(backlog.get("meta", {}).get("client", "Project")).strip()
    title_line = f"# Action Plan: {client_name}"

    sections: List[str] = []
    sections.append(title_line)
    sections.append("")

    # Inputs
    sections.append("## Inputs")
    sections.append(f"- Backlog: `{inputs_backlog_path}`")
    if inputs_tech_path:
        sections.append(f"- Technical Plan: `{inputs_tech_path}`")
    if inputs_tasks_path:
        sections.append(f"- Task Breakdown: `{inputs_tasks_path}`")
    sections.append("")

    # Objectives
    sections.append("## Objectives")
    sections.append(
        "Establish a working end-to-end pipeline: backlog → plan → draft Action_Plan → "
        "audit → peer review → synthesis → implement → deploy → observe. Enforce gate discipline and session separation."
    )
    sections.append("")

    # Phases and Gates
    sections.append("## Phases and Gates")
    sections.append("")

    sections.append("### Phase 1 — Planning Readiness (Gate: planning_gate)")
    sections.append("- Preconditions: `product_backlog.yaml` present; `technical_plan.md` + `task_breakdown.yaml` ready")
    sections.append("- Outputs: Planning gate evidence captured in audit notes")
    sections.append("")

    sections.append("### Phase 2 — Draft Action Plan (This document)")
    sections.append("- Scope: Convert backlog items into actionable steps with artifacts and checks")
    sections.append("- Outputs: This `Action_Plan.md`")
    sections.append("")

    sections.append("### Phase 3 — Audit (auditor_ai) → Summary_Report.md")
    sections.append("- Command:")
    sections.append("```")
    sections.append('/audit {"source":"memory-bank/plan/Action_Plan.md","context":["memory-bank/plan/technical_plan.md","memory-bank/plan/task_breakdown.yaml"],"outputs":{"report":"memory-bank/plan/Summary_Report.md"}}')
    sections.append("```")
    sections.append("- Criteria: Findings have traceable evidence lines to files/sections; risks include severity and mitigations")
    sections.append("")

    sections.append("### Phase 4 — Peer Review (principal_engineer_ai) → Validation_Report.md")
    sections.append("- Command:")
    sections.append("```")
    sections.append('/peer_review {"source":"memory-bank/plan/Summary_Report.md","plan":"memory-bank/plan/Action_Plan.md","outputs":{"report":"memory-bank/plan/Validation_Report.md"}}')
    sections.append("```")
    sections.append("- Criteria: Each audit risk marked CONFIRM/CHALLENGE with rationale; GO/NO-GO issued")
    sections.append("")

    sections.append("### Phase 5 — Synthesis → Final_Implementation_Plan.md")
    sections.append("- Preconditions: Validation GO")
    sections.append("- Outputs: `Final_Implementation_Plan.md` with sequenced tasks and rollback notes")
    sections.append("")

    # Workstreams
    sections.append("## Workstreams (from backlog)")
    sections.extend(build_workstreams_lines(backlog))
    sections.append("")

    # Acceptance Criteria
    sections.append("## Acceptance Criteria (Definition of Done)")
    sections.append("- `Summary_Report.md` with evidence citations")
    sections.append("- `Validation_Report.md` with GO/NO-GO and rationale")
    sections.append("- `Final_Implementation_Plan.md` with task sequencing and rollback")
    sections.append("- Security gate blocks on High issues; Observability configs lint/render cleanly")
    sections.append("")

    # IMPORTANT NOTE ensures downstream linting passes (see tools/plan_next.py)
    sections.append("## IMPORTANT NOTE")
    sections.append(
        "Run audit and peer review in separate sessions to avoid bias. Treat planning and QA gates as "
        "blocking unless explicitly set to warn; include explicit evidence references in all findings."
    )
    sections.append("")

    return "\n".join(sections)


def resolve_default_paths(root: Path) -> Dict[str, str]:
    plan_root = root / "memory-bank" / "plan"
    return {
        "tech": str(plan_root / "technical_plan.md"),
        "tasks": str(plan_root / "task_breakdown.yaml"),
        "output": str(plan_root / "Action_Plan.md"),
    }


def main() -> int:
    _ensure_pyyaml_installed()

    parser = argparse.ArgumentParser(description="Generate Action_Plan.md from backlog")
    parser.add_argument("--source", required=True, help="Path to product_backlog.yaml")
    parser.add_argument("--tech", required=False, help="Path to technical_plan.md")
    parser.add_argument("--tasks", required=False, help="Path to task_breakdown.yaml")
    parser.add_argument("--output", required=False, help="Path to output Action_Plan.md")
    parser.add_argument("--dry-run", action="store_true", help="Print to stdout instead of writing file")
    args = parser.parse_args()

    repo_root = Path.cwd()
    defaults = resolve_default_paths(repo_root)

    source_path = Path(args.source)
    tech_path = args.tech or defaults["tech"]
    tasks_path = args.tasks or defaults["tasks"]
    output_path = args.output or defaults["output"]

    # Normalize to relative-looking strings for embedding in markdown
    def _rel(p: str) -> str:
        try:
            return str(Path(p))
        except Exception:
            return p

    try:
        backlog = load_yaml(source_path)
    except Exception as exc:
        print(f"❌ Failed to read backlog YAML at {source_path}: {exc}")
        return 2

    content = generate_action_plan(
        backlog=backlog,
        inputs_backlog_path=_rel(str(source_path)),
        inputs_tech_path=_rel(str(tech_path)) if tech_path else None,
        inputs_tasks_path=_rel(str(tasks_path)) if tasks_path else None,
    )

    if args.dry_run:
        print(content)
        return 0

    out_path = Path(output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="\n") as f:
        f.write(content)

    print(f"✅ Wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

