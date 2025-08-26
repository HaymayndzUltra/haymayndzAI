import json
import pathlib
import pytest

# Smoke test ensures concurrency config is present and well-formed


def _find_report(base: pathlib.Path) -> pathlib.Path:
    candidates = [
        base / 'concurrency_test_report_20250824_053348.json',
        base / 'concurrency_test_report_20250824_062809.json',
    ]
    for c in candidates:
        if c.exists():
            return c
    # Fallback: pick the latest matching report if available
    matches = sorted(base.glob('concurrency_test_report_*.json'))
    if matches:
        return matches[-1]
    return candidates[0]


def test_concurrency_config_exists_and_is_valid_json():
    base = pathlib.Path(__file__).resolve().parents[2] / 'sync'
    target = _find_report(base)
    assert target.exists(), f'Expected at least one concurrency report JSON present in {base}'
    data = json.loads(target.read_text(encoding='utf-8'))

    # Accept either dict with keys or a list of result entries
    if isinstance(data, dict):
        assert 'results' in data or 'summary' in data
    elif isinstance(data, list):
        assert len(data) > 0
        assert isinstance(data[0], dict)
        # Basic shape checks
        for k in ('result', 'start_time', 'end_time'):
            assert k in data[0]
    else:
        pytest.fail(f'Unexpected report type: {type(data)}')