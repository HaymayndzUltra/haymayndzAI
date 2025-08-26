#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, shutil, os
from pathlib import Path
from datetime import datetime, timezone
import yaml


def discover_repo_root() -> Path:
    # Prefer REPO_ROOT if it points to a valid repo
    env = os.getenv('REPO_ROOT')
    if env:
        p = Path(env).resolve()
        if (p / 'frameworks' / 'fwk-001-cursor-rules' / 'DOCS' / 'changes' / 'routing_override.yaml').exists():
            return p
    # Ascend from this script's location
    here = Path(__file__).resolve()
    for parent in [here] + list(here.parents):
        candidate = parent / 'frameworks' / 'fwk-001-cursor-rules' / 'DOCS' / 'changes' / 'routing_override.yaml'
        if candidate.exists():
            return parent
    # Fallback to CWD
    return Path.cwd().resolve()


REPO = discover_repo_root()
CHANGES = REPO / 'frameworks' / 'fwk-001-cursor-rules' / 'DOCS' / 'changes'
OVERRIDE = CHANGES / 'routing_override.yaml'


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def backup() -> Path:
    if not OVERRIDE.exists():
        raise SystemExit(f"routing_override.yaml not found at: {OVERRIDE}")
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H%M%S+0000')
    bak = CHANGES / f'routing_override.yaml.bak.{ts}'
    shutil.copy2(OVERRIDE, bak)
    return bak


def list_backups() -> list[Path]:
    return sorted(CHANGES.glob('routing_override.yaml.bak.*'))


def toggle_on(allowlist: list[str]) -> None:
    if not OVERRIDE.exists():
        raise SystemExit(f"routing_override.yaml not found at: {OVERRIDE}")
    data = yaml.safe_load(OVERRIDE.read_text(encoding='utf-8')) or {}
    data.setdefault('overrides', {}).setdefault('allowlist_triggers', [])
    data['progressive_mode'] = True
    data['overrides']['allowlist_triggers'] = sorted(set(allowlist))
    OVERRIDE.write_text(yaml.safe_dump(data, sort_keys=False), encoding='utf-8')


def restore_latest() -> Path:
    backs = list_backups()
    if not backs:
        raise SystemExit('No backups found')
    latest = backs[-1]
    shutil.copy2(latest, OVERRIDE)
    return latest


def main() -> int:
    ap = argparse.ArgumentParser(description='Routing override toggle (BL-012)')
    sub = ap.add_subparsers(dest='cmd', required=True)

    on = sub.add_parser('on', help='Enable progressive mode with allowlist')
    on.add_argument('--allow', nargs='+', default=['/route','/status','/validate_docs'])

    off = sub.add_parser('off', help='Restore from latest .bak')

    args = ap.parse_args()

    if args.cmd == 'on':
        b = backup()
        toggle_on(args.allow)
        print(json.dumps({'ok': True, 'repo_root': str(REPO), 'override': str(OVERRIDE), 'backup': str(b), 'progressive_mode': True, 'allowlist': args.allow}))
        return 0

    if args.cmd == 'off':
        restored = restore_latest()
        print(json.dumps({'ok': True, 'repo_root': str(REPO), 'override': str(OVERRIDE), 'restored': str(restored)}))
        return 0

    return 1


if __name__ == '__main__':
    raise SystemExit(main())