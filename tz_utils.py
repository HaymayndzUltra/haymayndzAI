#!/usr/bin/env python3
"""Timezone helpers for PH (Asia/Manila) with aware datetimes."""
from __future__ import annotations

from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from typing import Optional

PH_TZ = ZoneInfo("Asia/Manila")


def now_ph() -> datetime:
    """Current time in Asia/Manila as aware datetime."""
    return datetime.now(PH_TZ)


def now_ph_iso() -> str:
    """Current time in Asia/Manila, ISO-8601 with offset."""
    return now_ph().isoformat()


def parse_iso_aware(value: str) -> datetime:
    """Parse ISO string; if naive, assume UTC and convert to PH timezone."""
    dt = datetime.fromisoformat(value)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(PH_TZ)


def days_since(then_iso: str, *, now: Optional[datetime] = None) -> int:
    """Whole days between PH-now and an ISO timestamp (normalized to PH)."""
    now_dt = (now or now_ph())
    then_dt = parse_iso_aware(then_iso)
    return (now_dt - then_dt).days