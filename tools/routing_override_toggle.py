#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, shutil
from pathlib import Path
from datetime import datetime, timezone
import yaml

CHANGES = Path('/workspace/frameworks/fwk-001-cursor-rules/DOCS/changes')
OVERRIDE = CHANGES / 'routing_override.yaml'


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def backup() -> Path:
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H%M%S+0000')
    bak = CHANGES / f'routing_override.yaml.bak.{ts}'
    shutil.copy2(OVERRIDE, bak)
    return bak


def list_backups() -> list[Path]:
    return sorted(CHANGES.glob('routing_override.yaml.bak.*'))


def toggle_on(allowlist: list[str]) -> None:
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
        print(json.dumps({'ok': True, 'backup': str(b), 'progressive_mode': True, 'allowlist': args.allow}))
        return 0

    if args.cmd == 'off':
        restored = restore_latest()
        print(json.dumps({'ok': True, 'restored': str(restored)}))
        return 0

    return 1


if __name__ == '__main__':
    raise SystemExit(main())