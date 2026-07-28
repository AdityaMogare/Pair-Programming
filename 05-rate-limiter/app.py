"""
Rate limiter — sliding-window throttle at the edge gateway.

Stack:
  API harness (app.py)
    ↓
  RateLimiter (limiter.py)
    ↓
  TimestampStore (store.py)

Run: python3 test_rate_limiter.py
Stuck? Open PR solution/05-rate-limiter → Files changed.
"""

from __future__ import annotations

from typing import Any, Callable

from limiter import RateLimiter
from store import TimestampStore

# Controllable clock so tests can walk the sliding window without sleeping.
_clock_now: float = 1_000_000.0

_store: TimestampStore | None = None
_limiter: RateLimiter | None = None
_limit: int = 3
_window_seconds: float = 60.0


def _clock() -> float:
    return _clock_now


def advance_time(seconds: float) -> float:
    global _clock_now
    _clock_now += seconds
    return _clock_now


def reset_clock(at: float = 1_000_000.0) -> None:
    global _clock_now
    _clock_now = at


def reset(
    *,
    limit: int = 3,
    window_seconds: float = 60.0,
    clock: Callable[[], float] | None = None,
) -> None:
    global _store, _limiter, _limit, _window_seconds
    reset_clock()
    _limit = limit
    _window_seconds = window_seconds
    _store = TimestampStore()
    _limiter = RateLimiter(
        _store,
        limit=limit,
        window_seconds=window_seconds,
        clock=clock or _clock,
    )


def run(payload: dict[str, Any]) -> dict[str, Any]:
    """
    Scripted action runner used by tests.

    Actions:
      reset       — configure limit / window and clear counters
      request     — attempt one request for a user_id
      advance     — move the fake clock forward
      keys        — inspect live store keys (debug aid)
      snapshot    — dump timestamps for a user key
    """
    global _limiter, _store

    action = payload.get("action")

    if action == "reset":
        reset(
            limit=int(payload.get("limit", 3)),
            window_seconds=float(payload.get("window_seconds", 60)),
        )
        return {
            "ok": True,
            "action": "reset",
            "limit": _limit,
            "window_seconds": _window_seconds,
        }

    if _limiter is None or _store is None:
        return {"ok": False, "error": "app_not_initialized — call reset first"}

    if action == "request":
        result = _limiter.allow(payload["user_id"])
        return {"ok": True, **result}

    if action == "advance":
        now = advance_time(float(payload.get("seconds", 0)))
        return {"ok": True, "action": "advance", "now": now}

    if action == "keys":
        return {"ok": True, "keys": _store.keys()}

    if action == "snapshot":
        # Debug aid — shows whatever key the limiter actually used.
        user_id = payload["user_id"]
        key = _limiter._key(user_id)
        return {
            "ok": True,
            "user_id": user_id,
            "key": key,
            "timestamps": _store.get(key),
        }

    return {"ok": False, "error": f"unknown_action:{action}"}
