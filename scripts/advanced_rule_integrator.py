#!/usr/bin/env python3
"""
Advanced Rule Integrator

Purpose
- Selects best-fit rules from harvested catalogs for a new client project using a
  hybrid similarity + risk-aware selection (ILP if OR-Tools available, otherwise
  a robust greedy fallback).
- Synthesizes a composite rule pack by borrowing the best-matching sections
  across the selected rule documents.
- Optionally integrates with the framework by:
  - Backing up and updating routing_override.yaml (allowlist_triggers,
    progressive_mode), preserving existing content where possible
  - Running per-trigger monitors (progressive_monitor.py) and collecting status
  - Appending a concise summary to DOCS/reports/Latest_Current.md

Safety
- Defaults to dry-run; requires --apply to modify files
- Progressive is OFF by default when applying; override via --progressive on|off

Dependencies
- Standard library only. If OR-Tools is installed, it will be used; otherwise,
  automatic greedy fallback is applied.

Usage
  python3 scripts/advanced_rule_integrator.py \
    --text "Brief text here..." \
    --max-select 12 --risk-budget 6.0 \
    --apply --progressive off --run-monitors --repeat 1 --interval 1

Outputs
- selection_<timestamp>/selection.json
- selection_<timestamp>/composite_rule.mdc
- Optional edits to: DOCS/changes/routing_override.yaml (with backups)
- Optional appends to: DOCS/reports/Latest_Current.md
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import math
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Dict, List, Tuple, Iterable


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


# --------------------------- Text and Similarity --------------------------- #

STOPWORDS = set(
    """
the a an and or of in to for with on at from into during including until against
among throughout despite toward upon concerning as about above below under over
again further then once here there when where why how all any both each few more
most other some such no nor not only own same so than too very can will just don
t should now is are was were be been being by this that these those you your yours
""".split()
)


def _read_text(path: str, max_bytes: int = 300_000) -> str:
    try:
        size = os.path.getsize(path)
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read(max_bytes if size > max_bytes else size)
    except Exception:
        return ""


def _tokenize(text: str) -> List[str]:
    words = re.findall(r"[a-zA-Z0-9_]+", text.lower())
    return [w for w in words if w not in STOPWORDS and len(w) > 2]


def _tf(tokens: Iterable[str]) -> Dict[str, float]:
    c = Counter(tokens)
    total = float(sum(c.values()) or 1.0)
    return {k: v / total for k, v in c.items()}


def _cos(a: Dict[str, float], b: Dict[str, float]) -> float:
    if not a or not b:
        return 0.0
    keys = a.keys() & b.keys()
    num = sum(a[k] * b[k] for k in keys)
    den = math.sqrt(sum(v * v for v in a.values())) * math.sqrt(
        sum(v * v for v in b.values())
    )
    return (num / den) if den else 0.0


# --------------------------- Document Extraction -------------------------- #

TRIGGER_RX = re.compile(r"/[a-z][a-z0-9_/-]+")
SECTION_RX = re.compile(r"^##\s+([^\n]+)\n", re.M)
CONFLICTS_RX = re.compile(r"conflicts?_with\s*:\s*\[([^\]]*)\]", re.I)


def _infer_read_only(text: str) -> bool:
    tl = text.lower()
    ro = any(k in tl for k in ("read-only", "read only", "validate", "review", "audit", "observe"))
    rw = any(k in tl for k in ("deploy", "write ", "writes ", "mutation", "create ", "update "))
    return (1 if ro else 0) - (1 if rw else 0) >= 0


def _infer_risk(text: str) -> float:
    tl = text.lower()
    risk = 1.0
    if any(k in tl for k in ("deploy", "write", "create", "delete", "mutation", "production")):
        risk += 1.0
    if any(k in tl for k in ("read-only", "validate", "review", "observe", "audit", "test")):
        risk -= 0.5
    return max(0.25, min(risk, 3.0))


def _extract_triggers(text: str) -> List[str]:
    return sorted(set(TRIGGER_RX.findall(text)))


def _extract_conflicts(text: str) -> List[str]:
    m = CONFLICTS_RX.search(text)
    if not m:
        return []
    return [x.strip().strip("'\"") for x in m.group(1).split(",") if x.strip()]


def _split_sections(text: str) -> Dict[str, str]:
    sections: Dict[str, str] = {}
    positions = [(m.start(), m.group(1).strip()) for m in SECTION_RX.finditer(text)]
    if not positions:
        return {"FULL": text}
    positions.append((len(text), "END"))
    for i in range(len(positions) - 1):
        start, title = positions[i]
        next_start, _ = positions[i + 1]
        head_end = text.find("\n", start) + 1
        sections[title] = text[head_end:next_start].strip()
    return sections


@dataclass
class RuleDoc:
    id: str
    path: str
    text: str
    read_only: bool
    risk: float
    triggers: List[str]
    conflicts_with: List[str]


def _hash_id(path: str) -> str:
    return hashlib.sha1(path.encode()).hexdigest()[:8]


def load_harvested_docs(paths: List[str]) -> List[RuleDoc]:
    docs: List[RuleDoc] = []
    for base in paths:
        if not os.path.isdir(base):
            continue
        for name in os.listdir(base):
            if not name.endswith(".mdc"):
                continue
            p = os.path.join(base, name)
            text = _read_text(p)
            if not text.strip():
                continue
            doc_id = os.path.splitext(name)[0]
            docs.append(
                RuleDoc(
                    id=doc_id,
                    path=p,
                    text=text,
                    read_only=_infer_read_only(text),
                    risk=_infer_risk(text),
                    triggers=_extract_triggers(text),
                    conflicts_with=_extract_conflicts(text),
                )
            )
    return docs


# --------------------------- Selection (ILP or Greedy) -------------------- #

def _try_ilp_selection(
    docs: List[RuleDoc],
    brief_vec: Dict[str, float],
    max_select: int,
    risk_budget: float,
    require_ids: List[str],
    deny_ids: List[str],
):
    try:
        from ortools.linear_solver import pywraplp  # type: ignore
    except Exception:
        return None  # fallback to greedy

    solver = pywraplp.Solver.CreateSolver("SCIP")
    x = [solver.BoolVar(d.id) for d in docs]

    # similarities
    sims = []
    for d in docs:
        sims.append(_cos(brief_vec, _tf(_tokenize(d.text))) + (0.05 if d.read_only else 0.0))

    # objective: maximize sim - 0.05*risk
    solver.Maximize(
        solver.Sum(x[i] * (float(sims[i]) - 0.05 * float(docs[i].risk)) for i in range(len(docs)))
    )

    # cardinality
    solver.Add(solver.Sum(x) <= max_select)

    # deny / require
    id_to_idx = {d.id: i for i, d in enumerate(docs)}
    for rid in require_ids:
        if rid in id_to_idx:
            solver.Add(x[id_to_idx[rid]] == 1)
    for did in deny_ids:
        if did in id_to_idx:
            solver.Add(x[id_to_idx[did]] == 0)

    # conflicts
    for i, d in enumerate(docs):
        for c in d.conflicts_with:
            if c in id_to_idx:
                solver.Add(x[i] + x[id_to_idx[c]] <= 1)

    # risk budget
    solver.Add(solver.Sum(x[i] * float(docs[i].risk) for i in range(len(docs))) <= risk_budget)

    status = solver.Solve()
    if status != pywraplp.Solver.OPTIMAL:
        return None

    selected = [docs[i] for i in range(len(docs)) if x[i].solution_value() > 0.5]
    return selected


def _greedy_selection(
    docs: List[RuleDoc],
    brief_vec: Dict[str, float],
    max_select: int,
    risk_budget: float,
    require_ids: List[str],
    deny_ids: List[str],
) -> List[RuleDoc]:
    # base score: similarity + read-only bonus
    scored: List[Tuple[float, RuleDoc]] = []
    for d in docs:
        if d.id in deny_ids:
            continue
        vec = _tf(_tokenize(d.text))
        sim = _cos(brief_vec, vec) + (0.05 if d.read_only else 0.0)
        scored.append((sim, d))
    scored.sort(key=lambda x: x[0], reverse=True)

    selected: List[RuleDoc] = []
    used_ids: set[str] = set()
    used_triggers: set[str] = set()
    total_risk = 0.0

    # ensure require first
    required_set = [d for d in docs if d.id in set(require_ids)]
    for d in required_set:
        if total_risk + float(d.risk) <= risk_budget:
            selected.append(d)
            used_ids.add(d.id)
            used_triggers.update(d.triggers)
            total_risk += float(d.risk)

    for _, d in scored:
        if len(selected) >= max_select:
            break
        if d.id in used_ids:
            continue
        if any(c in used_ids for c in d.conflicts_with):
            continue
        if total_risk + float(d.risk) > risk_budget:
            continue
        # prefer those adding new triggers
        new_trigs = [t for t in d.triggers if t not in used_triggers]
        # light preference: if no triggers at all, still allow if highly relevant
        selected.append(d)
        used_ids.add(d.id)
        used_triggers.update(new_trigs)
        total_risk += float(d.risk)
    return selected


def select_rules(
    docs: List[RuleDoc], brief_text: str, max_select: int, risk_budget: float, require_ids: List[str], deny_ids: List[str]
) -> Tuple[List[RuleDoc], List[str], float]:
    brief_vec = _tf(_tokenize(brief_text))
    selected = _try_ilp_selection(docs, brief_vec, max_select, risk_budget, require_ids, deny_ids)
    if selected is None:
        selected = _greedy_selection(docs, brief_vec, max_select, risk_budget, require_ids, deny_ids)
    used_triggers = sorted({t for d in selected for t in d.triggers})
    total_risk = sum(float(d.risk) for d in selected)
    return selected, used_triggers, total_risk


# --------------------------- Composite Synthesis --------------------------- #

def synthesize_composite(selected: List[RuleDoc], brief_text: str, max_chars: int = 16000) -> str:
    brief_vec = _tf(_tokenize(brief_text))
    parts: List[Tuple[float, str, str, str]] = []  # (score, doc_id, title, body)
    for d in selected:
        sections = _split_sections(d.text)
        local: List[Tuple[float, str, str]] = []
        for title, body in sections.items():
            vec = _tf(_tokenize(body))
            local.append((_cos(brief_vec, vec), title, body.strip()))
        local.sort(key=lambda x: x[0], reverse=True)
        take = local[:2] if len(local) > 1 else local[:1]
        for s, title, body in take:
            parts.append((s, d.id, title, body))
    parts.sort(key=lambda x: x[0], reverse=True)

    header = [
        "# Composite Rule Pack — Auto-synthesized", "",
        "## Sourcing", "- Composed from best-matching sections across selected rules.",
        "- Preference: read-only and validation-first; minimize mutating guidance.", "",
        "## Project Brief", brief_text.strip()[:4000], ""
    ]
    out = "\n".join(header)
    for score, doc_id, title, body in parts:
        label = title if title != "FULL" else "Extract"
        out += f"## From {doc_id} — {label}\n\n{body}\n\n"
        if len(out) >= max_chars:
            out += "\n## Note\nFurther excerpts truncated for size.\n"
            break
    return out.strip()


# --------------------------- Integration Helpers -------------------------- #

ROUTING_OVERRIDE = os.path.join(
    REPO_ROOT, "frameworks", "fwk-001-cursor-rules", "DOCS", "changes", "routing_override.yaml"
)
LATEST_REPORT = os.path.join(
    REPO_ROOT, "frameworks", "fwk-001-cursor-rules", "DOCS", "reports", "Latest_Current.md"
)
MONITOR_SCRIPT = os.path.join(REPO_ROOT, "scripts", "progressive_monitor.py")


def _timestamp() -> str:
    return _dt.datetime.utcnow().strftime("%Y-%m-%dT%H%M%S+0000")


def _backup_file(path: str) -> str:
    if not os.path.isfile(path):
        return ""
    backup = f"{path}.bak.{_timestamp()}"
    with open(path, "rb") as src, open(backup, "wb") as dst:
        dst.write(src.read())
    return backup


def _update_routing_override(allowlist: List[str], progressive_mode: bool) -> Tuple[str, List[str]]:
    """Best-effort YAML update for allowlist_triggers and progressive_mode.
    Preserves unknown content; appends keys if not present.
    Returns: (backup_path, final_allowlist)
    """
    existing = ""
    if os.path.isfile(ROUTING_OVERRIDE):
        existing = _read_text(ROUTING_OVERRIDE, max_bytes=200_000)

    # Attempt to parse existing allowlist (simple YAML: either flow [..] or block - ..)
    current: List[str] = []
    flow_m = re.search(r"allowlist_triggers\s*:\s*\[([^\]]*)\]", existing)
    if flow_m:
        items = [x.strip().strip("'\"") for x in flow_m.group(1).split(",") if x.strip()]
        current = items
    else:
        block_m = re.search(r"allowlist_triggers\s*:\s*\n((?:\s*-\s*.+\n)+)", existing)
        if block_m:
            lines = [ln.strip() for ln in block_m.group(1).splitlines() if ln.strip().startswith("-")]
            current = [ln.split("-", 1)[1].strip().strip("'\"") for ln in lines]

    final = sorted({*current, *allowlist})

    # Build replacement/append content
    prog_line = f"progressive_mode: {'true' if progressive_mode else 'false'}\n"
    allow_block = "allowlist_triggers:\n" + "\n".join(f"  - {t}" for t in final) + "\n"

    content = existing
    changed = False

    if re.search(r"^\s*progressive_mode\s*:\s*", content, re.M):
        content = re.sub(r"^\s*progressive_mode\s*:\s*.*$", prog_line.strip(), content, flags=re.M)
        changed = True
    else:
        content += ("\n" if content and not content.endswith("\n") else "") + prog_line
        changed = True

    if re.search(r"^\s*allowlist_triggers\s*:\s*\[", content, re.M) or re.search(
        r"^\s*allowlist_triggers\s*:\s*$", content, re.M
    ):
        # Replace any existing block (flow or block)
        # Normalize by replacing entire section; simple approach
        content = re.sub(
            r"^\s*allowlist_triggers\s*:\s*\[[^\]]*\]\s*$",
            allow_block.strip(),
            content,
            flags=re.M,
        )
        content = re.sub(
            r"^\s*allowlist_triggers\s*:\s*\n(?:\s*-.*\n)+",
            allow_block,
            content,
            flags=re.M,
        )
        changed = True
    else:
        content += ("\n" if content and not content.endswith("\n") else "") + allow_block
        changed = True

    backup = _backup_file(ROUTING_OVERRIDE) if os.path.isfile(ROUTING_OVERRIDE) else ""
    with open(ROUTING_OVERRIDE, "w", encoding="utf-8") as f:
        f.write(content)
    return backup, final


def _run_monitor(trigger: str, repeat: int, interval: int) -> Dict[str, str]:
    if not os.path.isfile(MONITOR_SCRIPT):
        return {"trigger": trigger, "status": "ERROR", "error": "monitor_script_missing"}
    try:
        cp = subprocess.run(
            [sys.executable, MONITOR_SCRIPT, "--trigger", trigger, "--repeat", str(repeat), "--interval", str(interval)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            cwd=REPO_ROOT,
            timeout=60,
        )
        return {"trigger": trigger, "status": "OK", "exit": str(cp.returncode), "out": cp.stdout[-500:]}
    except Exception as e:
        return {"trigger": trigger, "status": "ERROR", "error": str(e)}


def _append_latest_report(header: str, body_lines: List[str]) -> None:
    ts = _dt.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    lines = ["\n\n", f"## {header} — {ts}", ""] + body_lines + [""]
    os.makedirs(os.path.dirname(LATEST_REPORT), exist_ok=True)
    with open(LATEST_REPORT, "a", encoding="utf-8") as f:
        f.write("\n".join(lines))


# --------------------------- CLI Orchestration ---------------------------- #


def main() -> int:
    ap = argparse.ArgumentParser(description="Advanced rule selector and integrator")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--brief", help="Path to project brief (text/markdown)")
    g.add_argument("--text", help="Inline project brief text")
    ap.add_argument("--harvest-dirs", nargs="*", default=[
        os.path.join(REPO_ROOT, "frameworks", "fwk-001-cursor-rules", "DOCS", "harvested"),
        os.path.join(REPO_ROOT, ".cursor", "rules"),
    ], help="Directories to scan for rule docs (.mdc)")
    ap.add_argument("--max-select", type=int, default=12)
    ap.add_argument("--risk-budget", type=float, default=6.0)
    ap.add_argument("--require-ids", nargs="*", default=[])
    ap.add_argument("--deny-ids", nargs="*", default=[])
    ap.add_argument("--outdir", default=None)
    ap.add_argument("--apply", action="store_true", help="Apply integration edits safely (backups created)")
    ap.add_argument("--progressive", choices=["on", "off"], default="off")
    ap.add_argument("--run-monitors", action="store_true")
    ap.add_argument("--repeat", type=int, default=1)
    ap.add_argument("--interval", type=int, default=1)
    ap.add_argument("--append-report", action="store_true")

    args = ap.parse_args()

    brief = args.text or ""
    if args.brief:
        brief = _read_text(args.brief, max_bytes=500_000) or brief
    if not brief.strip():
        print(json.dumps({"error": "no_brief"}, indent=2))
        return 2

    docs = load_harvested_docs(args.harvest_dirs)
    if not docs:
        print(json.dumps({"error": "no_documents_found", "dirs": args.harvest_dirs}, indent=2))
        return 3

    selected, allowlist, total_risk = select_rules(
        docs=docs,
        brief_text=brief,
        max_select=args.max_select,
        risk_budget=args.risk_budget,
        require_ids=args.require_ids,
        deny_ids=args.deny_ids,
    )

    ts = _dt.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    outdir = args.outdir or os.path.join(
        REPO_ROOT,
        "frameworks",
        "fwk-001-cursor-rules",
        "DOCS",
        "harvested",
        f"selection_{ts}",
    )
    os.makedirs(outdir, exist_ok=True)

    composite = synthesize_composite(selected, brief_text=brief)
    comp_path = os.path.join(outdir, "composite_rule.mdc")
    with open(comp_path, "w", encoding="utf-8") as f:
        f.write(composite)

    summary = {
        "selected_rule_ids": [d.id for d in selected],
        "selected_paths": [d.path for d in selected],
        "num_selected": len(selected),
        "allowlist_triggers": allowlist,
        "total_risk": total_risk,
        "risk_budget": args.risk_budget,
        "read_only_fraction": round(sum(1 for d in selected if d.read_only) / max(1, len(selected)), 3),
        "output_dir": outdir,
        "applied": False,
        "routing_override_backup": None,
        "monitors": [],
    }

    # Optional integration apply
    if args.apply:
        prog = (args.progressive == "on")
        backup, final_allowlist = _update_routing_override(allowlist=allowlist, progressive_mode=prog)
        summary["applied"] = True
        summary["routing_override_backup"] = backup
        summary["allowlist_triggers"] = final_allowlist

        # Optional monitors
        if args.run_monitors and final_allowlist:
            for trig in final_allowlist:
                mon = _run_monitor(trig, repeat=args.repeat, interval=args.interval)
                summary["monitors"].append(mon)

        # Optional report
        if args.append_report:
            lines: List[str] = []
            lines.append(f"- Selected {len(summary['selected_rule_ids'])} rules; total_risk={summary['total_risk']:.2f} / budget={args.risk_budget}")
            lines.append(f"- Allowlist triggers: {summary['allowlist_triggers']}")
            lines.append(f"- Progressive mode: {args.progressive.upper()}")
            if summary["monitors"]:
                lines.append("- Monitors:")
                for m in summary["monitors"]:
                    lines.append(f"  - {m.get('trigger')}: status={m.get('status')} exit={m.get('exit', '?')}")
            _append_latest_report("Advanced Rule Integration", lines)

    # Persist selection summary
    sel_path = os.path.join(outdir, "selection.json")
    with open(sel_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

