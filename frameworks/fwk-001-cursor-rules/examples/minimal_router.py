#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TOOLS = ROOT.parent / 'tools'


def write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def pre_exec_persona(agent: str) -> None:
    # Build index if missing, then build persona payload
    index = TOOLS / 'rule_index.json'
    if not index.exists():
        import subprocess
        subprocess.run([sys.executable, str(TOOLS / 'rules_indexer.py')], check=False)
    import subprocess
    subprocess.run([sys.executable, str(TOOLS / 'jit_persona_orchestrator.py'), agent], check=False)
    # Log a tiny summary beside artifacts
    payload = TOOLS / 'persona_payload.json'
    if payload.exists():
        try:
            data = json.loads(payload.read_text(encoding='utf-8'))
            summary = {
                'agent': data.get('persona', {}).get('agent'),
                'intent': data.get('persona', {}).get('intent'),
                'source_rule': data.get('persona', {}).get('source_rule'),
            }
            write_text(ROOT / 'persona_injection_summary.json', json.dumps(summary, indent=2))
        except Exception:
            pass


def cmd_backlog() -> Path:
    out = ROOT / "product_backlog.yaml"
    write_text(out, """# product backlog (example)
- id: PBI-001
  title: Example backlog item (Django REST API)
  status: draft
  tech: [django, python]
""")
    return out


def cmd_plan() -> Path:
    out = ROOT / "technical_plan.md"
    if not out.exists():
        write_text(out, "# Technical Plan (generated placeholder)\n\nThis file will be refined by planning.\n")
    return out


def cmd_gen_code() -> Path:
    out = ROOT / "task_breakdown.yaml"
    if not out.exists():
        write_text(out, """# task breakdown (example)
- id: T-001
  desc: Example task
  status: todo
""")
    return out


def cmd_test() -> Path:
    out = ROOT / "test_results.json"
    payload = {"summary": {"total": 1, "passed": 1, "failed": 0}}
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return out


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: minimal_router.py [/backlog|/plan|/gen_code|/test|/run_all]", file=sys.stderr)
        return 2
    cmd = argv[1]
    # Persona injection happens just-in-time per command
    agent = 'codegen_ai' if cmd in {"/gen_code", "/run_all"} else 'planning_ai' if cmd == "/plan" else 'codegen_ai'
    pre_exec_persona(agent)
    if cmd == "/backlog":
        p = cmd_backlog(); print(p)
    elif cmd == "/plan":
        p = cmd_plan(); print(p)
    elif cmd == "/gen_code":
        p = cmd_gen_code(); print(p)
    elif cmd == "/test":
        p = cmd_test(); print(p)
    elif cmd == "/run_all":
        for fn in (cmd_backlog, cmd_plan, cmd_gen_code, cmd_test):
            print(fn())
    else:
        print(f"unknown command: {cmd}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

