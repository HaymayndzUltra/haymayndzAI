#!/usr/bin/env python3
import json, os, sys
from typing import List

SCHEMA_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "frameworks", "fwk-001-cursor-rules", "schemas", "artifact.schema.json")
)

def load_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def simple_validate(obj: dict, schema: dict) -> List[str]:
    errors: List[str] = []
    required = schema.get("required", [])
    props = schema.get("properties", {})
    for key in required:
        if key not in obj:
            errors.append(f"missing required: {key}")
    # simple pattern checks for createdAt/updatedAt
    for k in ("createdAt", "updatedAt"):
        if k in obj and not isinstance(obj[k], str):
            errors.append(f"{k} must be string RFC3339-Z")
    # enum check for status
    if "status" in obj:
        enum = props.get("status", {}).get("enum")
        if enum and obj["status"] not in enum:
            errors.append(f"status not in {enum}")
    return errors

def main() -> int:
    schema = load_json(SCHEMA_PATH)
    examples_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "frameworks", "fwk-001-cursor-rules", "examples")
    )
    sidecars = [
        "Action_Plan.md.sidecar.json",
        "Summary_Report.md.sidecar.json",
        "Validation_Report.md.sidecar.json",
        "Final_Implementation_Plan.md.sidecar.json",
    ]
    failed = 0
    for name in sidecars:
        path = os.path.join(examples_dir, name)
        if not os.path.exists(path):
            print(f"MISSING: {name}")
            failed += 1
            continue
        obj = load_json(path)
        errs = simple_validate(obj, schema)
        if errs:
            print(f"INVALID: {name} -> {errs}")
            failed += 1
        else:
            print(f"OK: {name}")
    return 1 if failed else 0

if __name__ == "__main__":
    sys.exit(main())


