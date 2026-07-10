"""
Reference solution (interviewer eyes only) — all three phases.

Phase 1: off_hours, unusual_region
Phase 2: sensitive_action, new_actor
Phase 3: high_frequency bump (+1 severity if resource accessed >3 times, cap 3)
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Callable

ALLOWED_COUNTRIES = frozenset({"US", "CA", "GB"})
SENSITIVE_ACTIONS = frozenset({"token.exfil", "secret.read"})
OFF_HOURS_START = 9   # inclusive
OFF_HOURS_END = 18    # exclusive
FREQ_THRESHOLD = 3
MAX_SEVERITY = 3


def _parse_hour(ts: str) -> int:
    dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    return dt.astimezone(timezone.utc).hour


def _rule_off_hours(event: dict[str, Any], _ctx: dict[str, Any]) -> str | None:
    hour = _parse_hour(event["timestamp"])
    if hour < OFF_HOURS_START or hour >= OFF_HOURS_END:
        return "off_hours"
    return None


def _rule_unusual_region(event: dict[str, Any], _ctx: dict[str, Any]) -> str | None:
    geo = event.get("geo")
    if geo is None:
        return "unusual_region"  # stretch: unknown geo is suspicious
    country = geo.get("country")
    if country not in ALLOWED_COUNTRIES:
        return "unusual_region"
    return None


def _rule_sensitive_action(event: dict[str, Any], _ctx: dict[str, Any]) -> str | None:
    if event.get("action") in SENSITIVE_ACTIONS:
        return "sensitive_action"
    return None


def _rule_new_actor(event: dict[str, Any], ctx: dict[str, Any]) -> str | None:
    user_id = event.get("actor", {}).get("user_id")
    first_seen = ctx["first_seen_user"].get(user_id)
    if first_seen == event["id"]:
        return "new_actor"
    return None


RULES: list[tuple[str, Callable[[dict[str, Any], dict[str, Any]], str | None]]] = [
    ("off_hours", _rule_off_hours),
    ("unusual_region", _rule_unusual_region),
    ("sensitive_action", _rule_sensitive_action),
    ("new_actor", _rule_new_actor),
]


def _build_context(events: list[dict[str, Any]]) -> dict[str, Any]:
    first_seen_user: dict[str, str] = {}
    resource_counts: dict[str, int] = {}

    for event in events:
        user_id = event.get("actor", {}).get("user_id")
        if user_id and user_id not in first_seen_user:
            first_seen_user[user_id] = event["id"]

        resource_id = event.get("resource", {}).get("id")
        if resource_id:
            resource_counts[resource_id] = resource_counts.get(resource_id, 0) + 1

    return {
        "first_seen_user": first_seen_user,
        "resource_counts": resource_counts,
    }


def flag_suspicious_events(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    ctx = _build_context(events)
    results: list[dict[str, Any]] = []

    for event in events:
        reasons: list[str] = []
        for _name, rule_fn in RULES:
            reason = rule_fn(event, ctx)
            if reason:
                reasons.append(reason)

        severity = min(len(reasons), MAX_SEVERITY)

        resource_id = event.get("resource", {}).get("id")
        if resource_id and ctx["resource_counts"].get(resource_id, 0) > FREQ_THRESHOLD:
            if "high_frequency" not in reasons:
                reasons.append("high_frequency")
            severity = min(severity + 1, MAX_SEVERITY)

        results.append(
            {
                "event_id": event["id"],
                "suspicious": len(reasons) > 0,
                "reasons": reasons,
                "severity": severity,
            }
        )

    return results
