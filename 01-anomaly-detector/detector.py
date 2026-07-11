"""
Fixed anomaly detector — answer key for solution/01-anomaly-detector.

Spec:
  - off_hours: timestamp hour outside [09:00, 18:00) UTC
  - unusual_region: geo.country not in {US, CA, GB}; null geo is unusual
  - sensitive_action: action in {token.exfil, secret.read}
  - new_actor: first appearance of actor.user_id in the batch
  - high_frequency: resource.id appears more than 3 times → +1 severity (cap 3)
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

ALLOWED_COUNTRIES = frozenset({"US", "CA", "GB"})
SENSITIVE_ACTIONS = frozenset({"token.exfil", "secret.read"})
OFF_HOURS_START = 9
OFF_HOURS_END = 18
FREQ_THRESHOLD = 3
MAX_SEVERITY = 3


def _parse_hour(ts: str) -> int:
    dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    return dt.astimezone(timezone.utc).hour


def flag_suspicious_events(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    first_seen_user: dict[str, str] = {}
    resource_counts: dict[str, int] = {}

    for event in events:
        user_id = event.get("actor", {}).get("user_id")
        if user_id and user_id not in first_seen_user:
            first_seen_user[user_id] = event["id"]

        resource_id = event.get("resource", {}).get("id")
        if resource_id:
            resource_counts[resource_id] = resource_counts.get(resource_id, 0) + 1

    results: list[dict[str, Any]] = []

    for event in events:
        reasons: list[str] = []

        hour = _parse_hour(event["timestamp"])
        if hour < OFF_HOURS_START or hour >= OFF_HOURS_END:
            reasons.append("off_hours")

        geo = event.get("geo")
        if geo is None or geo.get("country") not in ALLOWED_COUNTRIES:
            reasons.append("unusual_region")

        if event.get("action") in SENSITIVE_ACTIONS:
            reasons.append("sensitive_action")

        user_id = event.get("actor", {}).get("user_id")
        if user_id and first_seen_user.get(user_id) == event["id"]:
            reasons.append("new_actor")

        severity = min(len(reasons), MAX_SEVERITY)

        resource_id = event.get("resource", {}).get("id")
        if resource_id and resource_counts.get(resource_id, 0) > FREQ_THRESHOLD:
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
