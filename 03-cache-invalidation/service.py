"""Profile service — cache-aside reads, write-through DB + invalidation."""

from __future__ import annotations

from typing import Any

from cache import InMemoryCache
from repository import UserRepository

DEFAULT_TTL_SECONDS = 60


def cache_key_for_read(user_id: str) -> str:
    return f"profile:{user_id}"


def cache_key_for_invalidate(user_id: str) -> str:
    return cache_key_for_read(user_id)


class ProfileService:
    def __init__(
        self,
        repo: UserRepository,
        cache: InMemoryCache,
        ttl_seconds: int = DEFAULT_TTL_SECONDS,
    ) -> None:
        self._repo = repo
        self._cache = cache
        self._ttl = ttl_seconds

    def get_profile(self, user_id: str) -> dict[str, Any] | None:
        key = cache_key_for_read(user_id)
        cached = self._cache.get(key)
        if cached is not None:
            return {**cached, "_source": "cache"}

        row = self._repo.find_by_id(user_id)
        if row is None:
            return None

        self._cache.set(key, row, ttl_seconds=self._ttl)
        return {**row, "_source": "db"}

    def update_profile(self, user_id: str, fields: dict[str, Any]) -> dict[str, Any] | None:
        updated = self._repo.save_profile(user_id, fields)
        if updated is None:
            return None

        # Cache-aside: drop the cached profile so the next read reloads from DB.
        self._cache.delete(cache_key_for_invalidate(user_id))
        return {**updated, "_source": "db"}
