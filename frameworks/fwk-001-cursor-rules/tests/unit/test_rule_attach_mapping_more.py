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


def test_attach_vue(tmp_path: Path):
    repo = repo_root_from_here()
    detector = repo / "tools" / "rule_attach_detector.py"
    create_rule_stub(tmp_path, "frontend/vue")
    write_file(tmp_path / "package.json", '{"dependencies":{"vue":"^3.4.0"}}')
    write_file(tmp_path / "src" / "App.vue", "<template><div/></template>\n")
    resp = run_detector(tmp_path, detector)
    assert_only_detected(resp, {"frontend/vue"})


def test_attach_angular(tmp_path: Path):
    repo = repo_root_from_here()
    detector = repo / "tools" / "rule_attach_detector.py"
    create_rule_stub(tmp_path, "frontend/angular")
    write_file(tmp_path / "angular.json", "{\n}")
    write_file(tmp_path / "src" / "app" / "main.ts", "console.log('ok');\n")
    # json-dep is optional for angular spec; our detector uses angular.json + ts glob
    resp = run_detector(tmp_path, detector)
    assert_only_detected(resp, {"frontend/angular"})


def test_attach_svelte(tmp_path: Path):
    repo = repo_root_from_here()
    detector = repo / "tools" / "rule_attach_detector.py"
    create_rule_stub(tmp_path, "frontend/svelte")
    write_file(tmp_path / "package.json", '{"dependencies":{"svelte":"^4.0.0"}}')
    write_file(tmp_path / "src" / "App.svelte", "<script>let x=1;</script>\n")
    resp = run_detector(tmp_path, detector)
    assert_only_detected(resp, {"frontend/svelte"})


def test_attach_php(tmp_path: Path):
    repo = repo_root_from_here()
    detector = repo / "tools" / "rule_attach_detector.py"
    create_rule_stub(tmp_path, "backend/php")
    write_file(tmp_path / "composer.json", "{\n}")
    write_file(tmp_path / "index.php", "<?php echo 'ok'; ?>\n")
    resp = run_detector(tmp_path, detector)
    assert_only_detected(resp, {"backend/php"})


def test_attach_go(tmp_path: Path):
    repo = repo_root_from_here()
    detector = repo / "tools" / "rule_attach_detector.py"
    create_rule_stub(tmp_path, "backend/go")
    write_file(tmp_path / "go.mod", "module example.com/app\n")
    write_file(tmp_path / "main.go", "package main\nfunc main(){}\n")
    resp = run_detector(tmp_path, detector)
    assert_only_detected(resp, {"backend/go"})


def test_attach_dotnet(tmp_path: Path):
    repo = repo_root_from_here()
    detector = repo / "tools" / "rule_attach_detector.py"
    create_rule_stub(tmp_path, "backend/dotnet")
    write_file(tmp_path / "app.sln", "\n")
    write_file(tmp_root := tmp_path / "src" / "app" / "Program.cs", "class Program{}\n")
    resp = run_detector(tmp_path, detector)
    assert_only_detected(resp, {"backend/dotnet"})

