"""Sliding-window rate limiter (per-user request timestamps)."""

from __future__ import annotations

from typing import Any, Callable

from store import TimestampStore


class RateLimiter:
    def __init__(
        self,
        store: TimestampStore,
        *,
        limit: int,
        window_seconds: float,
        clock: Callable[[], float],
    ) -> None:
        self._store = store
        self._limit = limit
        self._window = window_seconds
        self._clock = clock

    def _key(self, user_id: str) -> str:
        return f"rl:{user_id}"

    def allow(self, user_id: str) -> dict[str, Any]:
        now = self._clock()
        key = self._key(user_id)
        timestamps = self._store.get(key)

        # Drop timestamps that have aged out of the sliding window.
        timestamps = [t for t in timestamps if now - t < self._window]

        if len(timestamps) >= self._limit:
            self._store.set(key, timestamps)
            return {
                "allowed": False,
                "status": 429,
                "user_id": user_id,
                "limit": self._limit,
                "remaining": 0,
                "count": len(timestamps),
                "window_seconds": self._window,
                "key": key,
            }

        timestamps.append(now)
        self._store.set(key, timestamps)
        return {
            "allowed": True,
            "status": 200,
            "user_id": user_id,
            "limit": self._limit,
            "remaining": max(self._limit - len(timestamps), 0),
            "count": len(timestamps),
            "window_seconds": self._window,
            "key": key,
        }
