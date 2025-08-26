import json
import subprocess
from pathlib import Path


def repo_root_from_here() -> Path:
    cur = Path(__file__).resolve()
    for p in [cur] + list(cur.parents):
        if (p / ".cursor").exists():
            return p
    return Path(__file__).resolve().parents[5]


def write_file(path: Path, content: str = ""):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def run_detector(tmp_root: Path, script_path: Path) -> dict:
    out = subprocess.run(["python3", str(script_path)], cwd=str(tmp_root), capture_output=True, text=True)
    assert out.returncode == 0, out.stderr
    log_path = tmp_root / "rule_attach_log.json"
    assert log_path.exists()
    return json.loads(log_path.read_text(encoding="utf-8"))


def create_rule_stub(tmp_root: Path, framework_key: str):
    group, name = framework_key.split("/", 1)
    rule_path = tmp_root / ".cursor" / "frameworks" / group / f"{name}.mdc"
    write_file(rule_path, f"---\ndescription: stub for {framework_key}\n---\n")


def assert_only_detected(resp: dict, expected_keys: set[str]):
    detected = {e["framework"] for e in resp["entries"] if e.get("detected")}
    assert detected == expected_keys, f"detected={detected} != expected={expected_keys}"


def test_attach_java(tmp_path: Path):
    repo = repo_root_from_here()
    detector = repo / "tools" / "rule_attach_detector.py"
    create_rule_stub(tmp_path, "backend/java")
    write_file(tmp_path / "pom.xml", "<project></project>\n")
    write_file(tmp_path / "src" / "Main.java", "class Main{}\n")
    resp = run_detector(tmp_path, detector)
    assert_only_detected(resp, {"backend/java"})


def test_attach_rust(tmp_path: Path):
    repo = repo_root_from_here()
    detector = repo / "tools" / "rule_attach_detector.py"
    create_rule_stub(tmp_path, "backend/rust")
    write_file(tmp_path / "Cargo.toml", "[package]\nname=app\n")
    write_file(tmp_path / "src" / "main.rs", "fn main(){}\n")
    resp = run_detector(tmp_path, detector)
    assert_only_detected(resp, {"backend/rust"})


def test_attach_ios(tmp_path: Path):
    repo = repo_root_from_here()
    detector = repo / "tools" / "rule_attach_detector.py"
    create_rule_stub(tmp_path, "mobile/ios")
    write_file(tmp_path / "App.swift", "import Foundation\n")
    resp = run_detector(tmp_path, detector)
    assert_only_detected(resp, {"mobile/ios"})


def test_attach_ecommerce(tmp_path: Path):
    repo = repo_root_from_here()
    detector = repo / "tools" / "rule_attach_detector.py"
    create_rule_stub(tmp_path, "specialized/ecommerce")
    write_file(tmp_path / "theme" / "main.liquid", "{% section 'header' %}\n")
    write_file(tmp_path / "wp-content" / "plugins" / "ecommerce.php", "<?php\n")
    resp = run_detector(tmp_path, detector)
    assert_only_detected(resp, {"specialized/ecommerce"})