import json
import os
import subprocess
from pathlib import Path


def repo_root_from_here() -> Path:
    cur = Path(__file__).resolve()
    for p in [cur] + list(cur.parents):
        if (p / ".cursor").exists():
            # repo root is parent of '.cursor' if this test resides deeper under frameworks/
            return p
    # Fallback: four levels up (frameworks/.../tests/unit)
    return Path(__file__).resolve().parents[5]


def write_file(path: Path, content: str = ""):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def run_detector(tmp_root: Path, script_path: Path) -> dict:
    # Run detector with CWD at tmp_root so it scans that root
    out = subprocess.run(
        ["python3", str(script_path)], cwd=str(tmp_root), capture_output=True, text=True
    )
    assert out.returncode == 0, out.stderr
    log_path = tmp_root / "rule_attach_log.json"
    assert log_path.exists(), "rule_attach_log.json not created"
    return json.loads(log_path.read_text(encoding="utf-8"))


def create_rule_stub(tmp_root: Path, framework_key: str):
    group, name = framework_key.split("/", 1)
    rule_path = tmp_root / ".cursor" / "frameworks" / group / f"{name}.mdc"
    write_file(rule_path, f"---\ndescription: stub for {framework_key}\n---\n")


def assert_only_detected(resp: dict, expected_keys: set[str]):
    detected = {e["framework"] for e in resp["entries"] if e.get("detected")}
    assert detected == expected_keys, f"detected={detected} != expected={expected_keys}"


def test_attach_react(tmp_path: Path):
    repo = repo_root_from_here()
    detector = repo / "tools" / "rule_attach_detector.py"

    # Create rule stub and markers
    create_rule_stub(tmp_path, "frontend/react")
    write_file(tmp_path / "package.json", '{"dependencies":{"react":"^18.2.0"}}')
    write_file(tmp_path / "src" / "App.tsx", "export const App = () => null;\n")

    resp = run_detector(tmp_path, detector)
    assert_only_detected(resp, {"frontend/react"})


def test_attach_python(tmp_path: Path):
    repo = repo_root_from_here()
    detector = repo / "tools" / "rule_attach_detector.py"

    create_rule_stub(tmp_path, "backend/python")
    write_file(tmp_path / "service" / "main.py", "print('ok')\n")

    resp = run_detector(tmp_path, detector)
    assert_only_detected(resp, {"backend/python"})


def test_attach_flutter(tmp_path: Path):
    repo = repo_root_from_here()
    detector = repo / "tools" / "rule_attach_detector.py"

    create_rule_stub(tmp_path, "mobile/flutter")
    write_file(tmp_path / "pubspec.yaml", "name: app\ndependencies:\n  flutter: any\n")
    write_file(tmp_path / "lib" / "main.dart", "void main(){}\n")

    resp = run_detector(tmp_path, detector)
    assert_only_detected(resp, {"mobile/flutter"})


def test_attach_node(tmp_path: Path):
    repo = repo_root_from_here()
    detector = repo / "tools" / "rule_attach_detector.py"

    create_rule_stub(tmp_path, "backend/node")
    write_file(tmp_path / "package.json", '{"dependencies":{"express":"^4.19.0"}}')
    write_file(tmp_path / "server.js", "const express=require('express');\n")

    resp = run_detector(tmp_path, detector)
    assert_only_detected(resp, {"backend/node"})

