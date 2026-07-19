"""In-memory stand-in for Redis — dict-backed cache with TTL."""

from __future__ import annotations

import time
from typing import Any, Callable


class InMemoryCache:
    """Tiny Redis-like cache used by the profile service."""

    def __init__(self, clock: Callable[[], float] | None = None) -> None:
        self._store: dict[str, tuple[Any, float]] = {}
        self._clock: Callable[[], float] = clock or time.time

    def get(self, key: str) -> Any | None:
        if key not in self._store:
            return None

        value, expires_at = self._store[key]
        if self._clock() >= expires_at:
            del self._store[key]
            return None
        return value

    def set(self, key: str, value: Any, ttl_seconds: int) -> None:
        expires_at = self._clock() + ttl_seconds
        self._store[key] = (value, expires_at)

    def delete(self, key: str) -> bool:
        if key in self._store:
            del self._store[key]
            return True
        return False

    def keys(self) -> list[str]:
        return list(self._store.keys())

    def clear(self) -> None:
        self._store.clear()
