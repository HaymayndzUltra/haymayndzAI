#!/usr/bin/env python3
from __future__ import annotations

import os
import json
import time
import stat
import re
from subprocess import run, CompletedProcess
from typing import Tuple, Dict, Any
from tz_utils import now_ph, PH_TZ

LOGS_DIR = os.path.join("memory-bank", "logs")

# Basic redaction patterns (extendable)
_SECRET_PATTERNS = [
	re.compile(r"(AWS_(ACCESS|SECRET)_KEY|SECRET|TOKEN|PASSWORD|API_KEY)\s*[:=]\s*[^\s]+", re.IGNORECASE),
	re.compile(r"Bearer\s+[A-Za-z0-9\-_.]+", re.IGNORECASE),
]


def _redact(text: str) -> str:
	redacted = text or ""
	for pat in _SECRET_PATTERNS:
		redacted = pat.sub("***REDACTED***", redacted)
	return redacted


def _ensure_logs_dir() -> None:
	os.makedirs(LOGS_DIR, exist_ok=True)


def _set_private_perms(path: str) -> None:
	try:
		os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)  # 0o600
	except Exception:
		pass


def run_logged(cmd: str) -> Tuple[int, Dict[str, Any]]:
	"""Run a shell command, capture stdout/stderr (with redaction), write metadata json.
	Returns (exit_code, meta_dict). Files are written under memory-bank/logs.
	"""
	_ensure_logs_dir()
	ts = now_ph().strftime("%Y%m%dT%H%M%S%z")
	base = os.path.join(LOGS_DIR, f"run_{ts}")
	outp, errp, metap = base + ".out", base + ".err", base + ".json"

	start = time.time()
	cp: CompletedProcess = run(cmd, shell=True, text=True, capture_output=True)
	end = time.time()

	# Redact and write outputs
	stdout_red = _redact(cp.stdout or "")
	stderr_red = _redact(cp.stderr or "")
	with open(outp, "w", encoding="utf-8") as f:
		f.write(stdout_red)
	_set_private_perms(outp)
	with open(errp, "w", encoding="utf-8") as f:
		f.write(stderr_red)
	_set_private_perms(errp)

	meta = {
		"cmd": cmd,
		"exit_code": cp.returncode,
		"started_at": time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime(start)),
		"ended_at": time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime(end)),
		"duration_s": round(end - start, 3),
		"stdout": outp,
		"stderr": errp,
		"status": "success" if cp.returncode == 0 else "failed",
	}
	with open(metap, "w", encoding="utf-8") as f:
		json.dump(meta, f, indent=2, ensure_ascii=False)
	_set_private_perms(metap)
	return cp.returncode, meta