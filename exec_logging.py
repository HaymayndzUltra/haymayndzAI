#!/usr/bin/env python3
from __future__ import annotations

import os
import json
import time
import stat
from subprocess import run, CompletedProcess
from typing import Tuple, Dict, Any
from tz_utils import now_ph

LOGS_DIR = os.path.join("memory-bank", "logs")


def _ensure_logs_dir() -> None:
	os.makedirs(LOGS_DIR, exist_ok=True)


def _set_private_perms(path: str) -> None:
	try:
		os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)  # 0o600
	except Exception:
		pass


def run_logged(cmd: str) -> Tuple[int, Dict[str, Any]]:
	"""Run a shell command, capture stdout/stderr, write metadata json.
	Returns (exit_code, meta_dict). Files are written under memory-bank/logs.
	"""
	_ensure_logs_dir()
	ts = now_ph().strftime("%Y%m%dT%H%M%S%z")
	base = os.path.join(LOGS_DIR, f"run_{ts}")
	outp, errp, metap = base + ".out", base + ".err", base + ".json"

	start = time.time()
	cp: CompletedProcess = run(cmd, shell=True, text=True, capture_output=True)
	end = time.time()

	# Write outputs
	with open(outp, "w", encoding="utf-8") as f:
		f.write(cp.stdout or "")
	_set_private_perms(outp)
	with open(errp, "w", encoding="utf-8") as f:
		f.write(cp.stderr or "")
	_set_private_perms(errp)

	meta = {
		"cmd": cmd,
		"exit_code": cp.returncode,
		"started_at": now_ph().fromtimestamp(start, tz=now_ph().tzinfo).isoformat() if hasattr(now_ph(), 'fromtimestamp') else now_ph().isoformat(),
		"ended_at": now_ph().fromtimestamp(end, tz=now_ph().tzinfo).isoformat() if hasattr(now_ph(), 'fromtimestamp') else now_ph().isoformat(),
		"duration_s": round(end - start, 3),
		"stdout": outp,
		"stderr": errp,
		"status": "success" if cp.returncode == 0 else "failed",
	}
	with open(metap, "w", encoding="utf-8") as f:
		json.dump(meta, f, indent=2, ensure_ascii=False)
	_set_private_perms(metap)
	return cp.returncode, meta