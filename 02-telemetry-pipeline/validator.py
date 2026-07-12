"""Validate transformed telemetry events before emit."""

from __future__ import annotations

from typing import Any

REQUIRED_FIELDS = ("event_id", "timestamp", "severity", "message", "service", "node_id")
ALLOWED_SEVERITIES = frozenset({"error", "warning", "info", "debug"})


def validate(event: dict[str, Any]) -> list[str]:
    """Return a list of validation problems (empty means OK)."""
    problems: list[str] = []

    for field in REQUIRED_FIELDS:
        if field not in event or event[field] in (None, ""):
            problems.append(f"missing:{field}")

    severity = event.get("severity")
    if severity is not None and severity not in ALLOWED_SEVERITIES:
        problems.append(f"bad_severity:{severity}")

    return problems
