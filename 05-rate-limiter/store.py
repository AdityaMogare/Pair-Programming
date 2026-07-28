"""In-memory timestamp store for the sliding-window rate limiter."""

from __future__ import annotations


class TimestampStore:
    def __init__(self) -> None:
        self._windows: dict[str, list[float]] = {}

    def get(self, key: str) -> list[float]:
        return list(self._windows.get(key, []))

    def set(self, key: str, timestamps: list[float]) -> None:
        self._windows[key] = list(timestamps)

    def keys(self) -> list[str]:
        return list(self._windows.keys())

    def clear(self) -> None:
        self._windows.clear()
