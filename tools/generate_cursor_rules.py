#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, subprocess, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TEST_RULES = REPO / '.cursor' / 'test-rules'
DEST_RULES = REPO / '.cursor' / 'rules'
ATTACH_LOG = REPO / 'rule_attach_log.json'


def run(cmd: list[str], cwd: Path | None = None) -> None:
    proc = subprocess.run(cmd, cwd=str(cwd or REPO), text=True)
    if proc.returncode != 0:
        raise SystemExit(proc.returncode)


def main() -> int:
    ap = argparse.ArgumentParser(description='Generate Cursor Rules from curated .cursor/test-rules')
    ap.add_argument('--attach-log', default=str(ATTACH_LOG))
    ap.add_argument('--source', default=str(TEST_RULES))
    ap.add_argument('--dest', default=str(DEST_RULES))
    ap.add_argument('--lint', action='store_true', help='Run MDC linter after selection')
    args = ap.parse_args()

    # 1) Detector
    run([sys.executable, str(REPO / 'tools' / 'rule_attach_detector.py'), '--output', args.attach_log])

    # 2) Curated selector (promote curated test-rules)
    run([sys.executable, str(REPO / 'tools' / 'curated_selector.py'), '--attach-log', args.attach_log, '--source', args.source, '--dest', args.dest])

    # 3) Linter (optional)
    if args.lint:
        run([sys.executable, str(REPO / 'tools' / 'mdc_linter.py'), '--paths', args.dest, args.source, '--write'])

    # Print summary
    payload = {
        'repo': str(REPO),
        'attach_log': str(args.attach_log),
        'source': str(args.source),
        'dest': str(args.dest),
        'linted': bool(args.lint),
    }
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())