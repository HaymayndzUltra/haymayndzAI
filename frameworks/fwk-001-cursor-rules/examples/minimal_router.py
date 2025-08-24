#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")

def cmd_backlog() -> Path:
    out = ROOT / "product_backlog.yaml"
    write_text(out, """# product backlog (example)\n- id: PBI-001\n  title: Example backlog item\n  status: draft\n""")
    return out

def cmd_plan() -> Path:
    out = ROOT / "technical_plan.md"
    if not out.exists():
        write_text(out, "# Technical Plan (generated placeholder)\n\nThis file will be refined by planning.\n")
    return out

def cmd_gen_code() -> Path:
    out = ROOT / "task_breakdown.yaml"
    if not out.exists():
        write_text(out, """# task breakdown (example)\n- id: T-001\n  desc: Example task\n  status: todo\n""")
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

