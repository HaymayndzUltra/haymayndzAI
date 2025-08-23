#!/usr/bin/env python3
"""
Atomic IO utilities with sidecar locks and durable writes.
- Sidecar advisory locks using fcntl.flock on <path>.lock
- Same-directory temp file, fsync file then atomic os.replace, fsync parent dir
- Default file perms 0600
"""
import os
import json
import time
import errno
import random
import tempfile
from contextlib import contextmanager
from typing import Any, Callable

try:
	import fcntl  # type: ignore
except Exception as _e:  # pragma: no cover
	fcntl = None  # type: ignore


_DEF_TIMEOUT_S = 5.0


def _fsync_dir(dirpath: str) -> None:
	try:
		dfd = os.open(dirpath, os.O_DIRECTORY)
		try:
			os.fsync(dfd)
		finally:
			os.close(dfd)
	except Exception:
		pass  # best effort


def atomic_write_bytes(path: str, data: bytes) -> None:
	dirpath = os.path.dirname(os.path.abspath(path)) or "."
	fd, tmppath = tempfile.mkstemp(prefix=".__atomic__", dir=dirpath)
	try:
		with os.fdopen(fd, "wb") as tmp:
			tmp.write(data)
			tmp.flush()
			os.fsync(tmp.fileno())
		os.replace(tmppath, path)
		try:
			os.chmod(path, 0o600)
		except Exception:
			pass
		_fsync_dir(dirpath)
	finally:
		try:
			if os.path.exists(tmppath):
				os.unlink(tmppath)
		except Exception:
			pass


def atomic_write_text(path: str, text: str) -> None:
	atomic_write_bytes(path, text.encode("utf-8"))


def atomic_write_json(path: str, obj: Any, *, indent: int = 2) -> None:
	data = json.dumps(obj, indent=indent, ensure_ascii=False).encode("utf-8")
	atomic_write_bytes(path, data)


@contextmanager
def with_file_lock(lock_path: str, *, exclusive: bool = True, timeout_s: float = _DEF_TIMEOUT_S, retry_min_ms: int = 25, retry_max_ms: int = 100):
	"""Advisory sidecar lock with bounded backoff.
	If fcntl unavailable, acts as a no-op context manager.
	"""
	if fcntl is None:
		yield None
		return
	lock_dir = os.path.dirname(os.path.abspath(lock_path)) or "."
	os.makedirs(lock_dir, exist_ok=True)
	start = time.time()
	f = open(lock_path, "a+")
	locked = False
	try:
		while True:
			try:
				fcntl.flock(f.fileno(), fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH)
				locked = True
				break
			except OSError as e:
				if e.errno not in (errno.EAGAIN, errno.EACCES):
					raise
				if (time.time() - start) > timeout_s:
					raise TimeoutError(f"Timed out acquiring lock: {lock_path}")
				time.sleep(random.uniform(retry_min_ms/1000.0, retry_max_ms/1000.0))
		yield f
	finally:
		try:
			if locked:
				fcntl.flock(f.fileno(), fcntl.LOCK_UN)
		finally:
			f.close()


@contextmanager
def with_json_lock(path: str, *, exclusive: bool = True, timeout_s: float = _DEF_TIMEOUT_S):
	"""Lock helper targeting the JSON file's sidecar lock (<path>.lock)."""
	lock_path = f"{os.path.abspath(path)}.lock"
	with with_file_lock(lock_path, exclusive=exclusive, timeout_s=timeout_s):
		yield


def safe_update_json(path: str, transform: Callable[[Any], Any], *, default_factory: Callable[[], Any] | None = None, timeout_s: float = _DEF_TIMEOUT_S) -> None:
	"""Safely update a JSON file under exclusive lock using transform(current)->new.
	Creates the file if missing; writes atomically.
	"""
	if default_factory is None:
		default_factory = lambda: []  # type: ignore
	with with_json_lock(path, exclusive=True, timeout_s=timeout_s):
		try:
			if os.path.exists(path):
				with open(path, "rb") as f:
					cur = json.load(f)
			else:
				cur = default_factory()
		except Exception:
			cur = default_factory()
		new_obj = transform(cur)
		atomic_write_json(path, new_obj)
