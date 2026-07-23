"""Normalize parsed payloads into clean telemetry events."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

# Canonical severity labels expected by downstream analytics.
SEVERITY_MAP = {
    "ERROR": "error",
    "ERR": "error",
    "WARN": "warning",
    "WARNING": "warning",
    "INFO": "info",
    "DEBUG": "debug",
}


def normalize_timestamp(raw: str) -> str:
    """Parse an ISO-8601 timestamp and emit UTC with a trailing Z."""
    dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def transform(raw: dict[str, Any], node_id: str) -> dict[str, Any]:
    """Map shipper fields → analytics event schema."""
    level = str(raw.get("level", "INFO")).upper()
    severity = SEVERITY_MAP.get(level, "info")

    return {
        "event_id": raw["id"],
        "timestamp": normalize_timestamp(str(raw["ts"])),
        "severity": severity,
        "message": raw.get("msg", ""),
        "service": raw.get("service", "unknown"),
        "node_id": node_id,
    }
