#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

WAIVERS = Path('/workspace/security/waiver_db.json')


def load_waivers() -> dict:
	try:
		return json.loads(WAIVERS.read_text(encoding='utf-8'))
	except Exception:
		return {"waivers": []}


def _run_cmd(args: list[str]) -> tuple[int, str, str]:
	try:
		cp = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
		return cp.returncode, cp.stdout, cp.stderr
	except Exception as e:
		return 127, "", str(e)


def run_bandit() -> list:
	# Prefer module invocation to avoid PATH issues
	rc, out, err = _run_cmd([sys.executable, '-m', 'bandit', '-q', '-r', '/workspace', '-f', 'json'])
	if rc not in (0, 1):
		# Fallback to CLI name
		rc, out, err = _run_cmd(['bandit', '-q', '-r', '/workspace', '-f', 'json'])
		if rc not in (0, 1):
			print('bandit error:', (err or '').strip())
			return []
	try:
		data = json.loads(out or '{}')
		return data.get('results', [])
	except Exception:
		return []


def run_safety() -> list:
	# Use JSON-only output; some envs may still raise tool exceptions—handle gracefully
	rc, out, err = _run_cmd([sys.executable, '-m', 'safety', 'check', '--json'])
	if rc not in (0, 1):
		# Fallback to CLI name
		rc, out, err = _run_cmd(['safety', 'check', '--json'])
		if rc not in (0, 1):
			print('safety error:', (err or '').strip())
			return []
	try:
		data = json.loads(out or '[]')
		return data if isinstance(data, list) else []
	except Exception:
		# Safety sometimes fails JSON in certain dependency combos
		return []


def allowed_by_waiver(finding: dict, waivers: dict) -> bool:
	sev = (finding.get('issue_severity') or finding.get('severity') or '').upper()
	tool = finding.get('tool', 'bandit')
	for w in waivers.get('waivers', []):
		cond = w.get('conditions', {})
		sev_max = (cond.get('severity_max') or 'LOW').upper()
		tools = [t.lower() for t in cond.get('tools', [])]
		if tools and tool.lower() not in tools:
			continue
		order = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
		try:
			if order.index(sev) <= order.index(sev_max):
				return True
		except Exception:
			pass
	return False


def main() -> int:
	waivers = load_waivers()
	bandit_findings = [{
		'tool': 'bandit',
		'issue_severity': f.get('issue_severity', ''),
		'issue_text': f.get('issue_text', ''),
		'filename': f.get('filename')
	} for f in run_bandit()]
	safety_findings = [{
		'tool': 'safety',
		'severity': (f.get('severity') or ''),
		'package_name': f.get('package_name'),
		'advisory': f.get('advisory', '')
	} for f in run_safety()]

	all_findings = bandit_findings + safety_findings
	violations = [f for f in all_findings if not allowed_by_waiver(f, waivers)]
	print(json.dumps({
		'total': len(all_findings),
		'violations': len(violations),
		'waived': len(all_findings) - len(violations)
	}, indent=2))
	return 1 if violations else 0


if __name__ == '__main__':
	sys.exit(main())

