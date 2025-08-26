import json
import pathlib
import pytest

# Smoke test ensures concurrency config is present and well-formed

def test_concurrency_config_exists_and_is_valid_json():
    base = pathlib.Path(__file__).resolve().parents[2] / 'sync'
    report = base / 'concurrency_test_report_20250824_053348.json'
    alt = base / 'concurrency_test_report_20250824_062809.json'
    target = report if report.exists() else alt
    assert target.exists(), 'Expected at least one concurrency report JSON present'
    data = json.loads(target.read_text(encoding='utf-8'))
    assert isinstance(data, dict)
    assert 'results' in data or 'summary' in data