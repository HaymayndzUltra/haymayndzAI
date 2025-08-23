#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import List, Dict, Any
from atomic_io import with_file_lock

ACTIVE = Path("memory-bank/queue-system/tasks_active.json")
DONEL = Path("memory-bank/queue-system/tasks_done.jsonl")


def append_jsonl_line(path: Path, obj: dict) -> None:
	path.parent.mkdir(parents=True, exist_ok=True)
	with open(path, "ab") as f:
		f.write((json.dumps(obj, ensure_ascii=False) + "\n").encode("utf-8"))


def archive_completed() -> Dict[str, Any]:
	"""Append completed tasks to tasks_done.jsonl and keep only non-completed in active."""
	if not ACTIVE.exists():
		return {"status": "noop", "reason": "no active file"}
	# lock on active file sidecar
	with with_file_lock(str(ACTIVE) + ".lock", exclusive=True):
		try:
			data: List[Dict[str, Any]] = json.loads(ACTIVE.read_text("utf-8"))
		except Exception:
			return {"status": "error", "error": "cannot read active"}
		keep: List[Dict[str, Any]] = []
		archived = 0
		for t in data:
			if t.get("status") == "completed":
				append_jsonl_line(DONEL, t)
				archived += 1
			else:
				keep.append(t)
		ACTIVE.write_text(json.dumps(keep, indent=2, ensure_ascii=False))
		return {"status": "ok", "archived": archived, "remaining": len(keep)}

if __name__ == "__main__":
	print(json.dumps(archive_completed(), indent=2))