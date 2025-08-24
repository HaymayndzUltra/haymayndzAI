import json
import pathlib


def main() -> None:
    root = pathlib.Path("VERIFICATION")
    out = {"summaries": [], "duplicates": [], "conflicts": []}
    seen = {}

    for j in root.glob("*/findings.json"):
        try:
            data = json.loads(j.read_text(encoding="utf-8"))
        except Exception:
            continue
        vertical = data.get("vertical") or j.parent.name
        status = data.get("status")
        issues = data.get("issues", [])
        out["summaries"].append({
            "vertical": vertical,
            "status": status,
            "issues": issues,
            "file": str(j)
        })
        for issue in issues:
            tag = (issue.get("concern") or issue.get("tag") or "").strip()
            if not tag:
                continue
            seen.setdefault(tag, set()).add(vertical)

    for tag, verts in seen.items():
        if len(verts) > 1:
            out["duplicates"].append({"concern": tag, "verticals": sorted(verts)})

    out_path = root / "summary.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()


