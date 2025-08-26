#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, os, sys
from datetime import datetime, timezone
from pathlib import Path

BASE = Path('/workspace/frameworks/fwk-001-cursor-rules/DOCS/reports/planner_mode')
STATE_PATH = BASE / 'planner_state.json'
LOG_PATH = BASE / 'planner_decision_log.md'


def ensure_dirs() -> None:
    BASE.mkdir(parents=True, exist_ok=True)


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_state(enabled: bool, actor: str) -> None:
    ensure_dirs()
    payload = {
        'planner_mode': {
            'enabled': enabled,
            'answer_first': True,
            'confirm_before_action': 'always',
            'code_default': 'blocked',
        },
        'updated_at': iso_now(),
        'actor': actor,
    }
    STATE_PATH.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


def append_log(entry: str) -> None:
    ensure_dirs()
    header = '' if LOG_PATH.exists() else '# Planner Decision Log\n\n'
    with LOG_PATH.open('a', encoding='utf-8') as f:
        if header:
            f.write(header)
        f.write(entry.rstrip() + '\n')


def log_toggle(enabled: bool, actor: str) -> None:
    write_state(enabled, actor)
    append_log(f"- {iso_now()} — TOGGLE — planner_mode={'on' if enabled else 'off'} — actor={actor}")


def log_confirmation(action: str, decision: str, actor: str, notes: str) -> None:
    status = 'CONFIRMED' if decision.strip().lower() in {'yes', 'y', 'sige', 'go'} else 'DENIED'
    append_log(f"- {iso_now()} — CONFIRM — action={action} — decision={status} — actor={actor} — notes={notes}")


def main() -> int:
    ap = argparse.ArgumentParser(description='Planner Mode CLI (BL-010)')
    sub = ap.add_subparsers(dest='cmd', required=True)

    t = sub.add_parser('toggle', help='Toggle planner mode on/off')
    t.add_argument('--on', action='store_true', help='Enable planner mode')
    t.add_argument('--off', action='store_true', help='Disable planner mode')
    t.add_argument('--actor', default='system')

    c = sub.add_parser('confirm', help='Log a restricted action confirmation')
    c.add_argument('--action', required=True)
    c.add_argument('--decision', required=True, help='yes/no')
    c.add_argument('--actor', default='user')
    c.add_argument('--notes', default='')

    args = ap.parse_args()

    if args.cmd == 'toggle':
        if args.on == args.off:
            ap.error('Specify exactly one of --on or --off')
        log_toggle(args.on, args.actor)
        print(json.dumps({'ok': True, 'mode': 'on' if args.on else 'off'}))
        return 0

    if args.cmd == 'confirm':
        log_confirmation(args.action, args.decision, args.actor, args.notes)
        print(json.dumps({'ok': True, 'logged': True}))
        return 0

    return 1


if __name__ == '__main__':
    raise SystemExit(main())