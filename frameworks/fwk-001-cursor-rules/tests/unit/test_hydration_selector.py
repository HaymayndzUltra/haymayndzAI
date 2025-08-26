import pytest

from hydration.hydration_selector import select_candidate


def test_prefer_approved_over_newer_review():
    candidates = [
        {"id": "A", "status": "review", "updatedAt": "2025-08-23T10:00:00Z", "path": "a.yaml"},
        {"id": "B", "status": "approved", "updatedAt": "2025-08-23T09:00:00Z", "path": "b.yaml"},
    ]
    got = select_candidate(candidates)
    assert got.get("path") == "b.yaml"


def test_tiebreak_by_updatedAt_then_path():
    candidates = [
        {"id": "A", "status": "approved", "updatedAt": "2025-08-23T10:00:00Z", "path": "a.yaml"},
        {"id": "C", "status": "approved", "updatedAt": "2025-08-23T10:00:00Z", "path": "c.yaml"},
    ]
    got = select_candidate(candidates)
    assert got.get("path") == "c.yaml"