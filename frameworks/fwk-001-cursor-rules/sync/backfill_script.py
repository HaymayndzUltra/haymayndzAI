#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
import sys
import time
from typing import Dict, List, Tuple

# Local imports
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", ".."))
FRAMEWORK = "fwk-001-cursor-rules"
EXAMPLES_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "examples"))
LEGACY_DIR = os.path.join(REPO_ROOT, "legacy", ".cursor-rules-archived")
SCHEMA_PATH = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "schemas", "artifact.schema.json"))
INDEX_PATH = os.path.abspath(os.path.join(SCRIPT_DIR, "artifacts_index.json"))

# Index helpers
sys.path.insert(0, SCRIPT_DIR)
from index_writer import upsert_entry, load_index  # noqa: E402

DEFAULT_VERSION = "1.0.0"
DEFAULT_STATUS = "review"

KIND_MAP = {
	"Action_Plan.md": "action_plan",
	"Summary_Report.md": "summary_report",
	"Validation_Report.md": "validation_report",
	"Final_Implementation_Plan.md": "final_implementation_plan",
	"migration_plan.md": "migration_plan",
}


def rfc3339_utc(ts: float) -> str:
	return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(ts))


def file_sha256(path: str) -> str:
	with open(path, "rb") as f:
		sha = hashlib.sha256()
		for chunk in iter(lambda: f.read(8192), b""):
			sha.update(chunk)
	return sha.hexdigest()


def discover_example_artifacts() -> List[Tuple[str, str]]:
	"""Return list of (artifact_path, sidecar_path)."""
	pairs: List[Tuple[str, str]] = []
	for name in os.listdir(EXAMPLES_DIR):
		if not name.endswith(".md"):
			continue
		artifact = os.path.join(EXAMPLES_DIR, name)
		sidecar = artifact + ".sidecar.json"
		pairs.append((artifact, sidecar))
	return pairs


def maybe_legacy_candidates(include_legacy: bool) -> List[str]:
	if not include_legacy or not os.path.isdir(LEGACY_DIR):
		return []
	return [os.path.join(LEGACY_DIR, n) for n in os.listdir(LEGACY_DIR) if n.endswith(".mdc")]


def infer_id_and_kind(artifact_path: str) -> Tuple[str, str]:
	name = os.path.basename(artifact_path)
	if name in KIND_MAP:
		id_ = os.path.splitext(name)[0]
		return id_, KIND_MAP[name]
	# Fallbacks
	stem, ext = os.path.splitext(name)
	kind = stem.lower().replace("-", "_")
	return stem, kind


def build_sidecar(artifact_path: str) -> Dict[str, str]:
	stat = os.stat(artifact_path)
	created = rfc3339_utc(stat.st_mtime)
	updated = created
	artifact_id, kind = infer_id_and_kind(artifact_path)
	return {
		"id": artifact_id,
		"version": DEFAULT_VERSION,
		"status": DEFAULT_STATUS,
		"framework": FRAMEWORK,
		"kind": kind,
		"checksumSha256": file_sha256(artifact_path),
		"createdAt": created,
		"updatedAt": updated,
	}


def ensure_sidecar(artifact_path: str, sidecar_path: str, dry_run: bool) -> Dict[str, str]:
	if os.path.exists(sidecar_path):
		return json.load(open(sidecar_path))
	obj = build_sidecar(artifact_path)
	if dry_run:
		return obj
	# First-time create with .bak guard
	bak = sidecar_path + ".bak"
	if not os.path.exists(bak):
		open(bak, "w", encoding="utf-8").write("")
	with open(sidecar_path, "w", encoding="utf-8") as f:
		json.dump(obj, f, indent=2)
	return obj


def backfill(dry_run: bool, write_index: bool, include_legacy: bool, apply_legacy: bool) -> int:
	pairs = discover_example_artifacts()
	legacy = maybe_legacy_candidates(include_legacy)
	summary: Dict[str, any] = {"examples": [], "legacy": []}

	# Process examples
	for art, sc in pairs:
		entry = ensure_sidecar(art, sc, dry_run)
		summary["examples"].append({"artifact": art, "sidecar": sc, "entry": entry})
		if write_index and not dry_run:
			upsert_entry(entry, INDEX_PATH)

	# Legacy preview/migration (no writes unless apply_legacy)
	for path in legacy:
		art_id = os.path.splitext(os.path.basename(path))[0]
		entry = {
			"id": art_id,
			"version": DEFAULT_VERSION,
			"status": DEFAULT_STATUS,
			"framework": FRAMEWORK,
			"kind": "legacy_mdc",
			"createdAt": rfc3339_utc(os.stat(path).st_mtime),
			"updatedAt": rfc3339_utc(os.stat(path).st_mtime),
		}
		summary["legacy"].append({"artifact": path, "entry": entry})
		if apply_legacy and write_index and not dry_run:
			upsert_entry(entry, INDEX_PATH)

	# Report
	print(json.dumps({
		"dryRun": dry_run,
		"writeIndex": write_index,
		"includeLegacy": include_legacy,
		"applyLegacy": apply_legacy,
		"counts": {"examples": len(summary["examples"]), "legacy": len(summary["legacy"])}
	}, indent=2))
	return 0


def main():
	ap = argparse.ArgumentParser(description="Backfill sidecars and artifacts index")
	ap.add_argument("--dry-run", action="store_true", help="Plan only; do not write")
	ap.add_argument("--write-index", action="store_true", help="Write artifacts_index.json entries")
	ap.add_argument("--include-legacy", action="store_true", help="Scan legacy .mdc for preview")
	ap.add_argument("--apply-legacy", action="store_true", help="Also index legacy preview entries (use with --write-index)")
	args = ap.parse_args()

	# Default to dry-run if neither write nor dry-run specified
	dry_run = args.dry_run or (not args.write_index)
	return sys.exit(backfill(dry_run, args.write_index, args.include_legacy, args.apply_legacy))


if __name__ == "__main__":
	main()