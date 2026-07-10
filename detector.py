"""
Pair programming starter — implement flag_suspicious_events().

Each event looks like:
{
  "id": "evt_001",
  "timestamp": "2025-07-09T14:30:00Z",   # ISO-8601 UTC
  "actor": { "user_id": "alice", "ip": "..." },
  "action": "token.access",
  "resource": { "type": "canary_token", "id": "tok_prod_api" },
  "geo": { "country": "US", "region": "..." }   # may be null
}

Return a list of result objects, one per input event:
{
  "event_id": str,
  "suspicious": bool,
  "reasons": list[str],
  "severity": int   # optional until interviewer asks for scoring
}
"""

from __future__ import annotations

from typing import Any


def flag_suspicious_events(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Flag events that match suspicious criteria (define rules with interviewer)."""
    results: list[dict[str, Any]] = []

    for event in events:
        # TODO: implement with interviewer
        results.append(
            {
                "event_id": event["id"],
                "suspicious": False,
                "reasons": [],
                "severity": 0,
            }
        )

    return results
