"""
Cache invalidation — profile service with Redis-style cache-aside.

Stack:
  API → cache (Redis stand-in) → repository → database

Run: python3 test_cache.py
Stuck? Open PR solution/03-cache-invalidation → Files changed.
"""

from __future__ import annotations

from typing import Any, Callable

from api import ProfileAPI
from cache import InMemoryCache
from db import Database
from repository import UserRepository
from service import DEFAULT_TTL_SECONDS, ProfileService

# Controllable clock so tests can advance past TTL without sleeping.
_clock_now: float = 1_000_000.0


def _clock() -> float:
    return _clock_now


def advance_time(seconds: float) -> float:
    global _clock_now
    _clock_now += seconds
    return _clock_now


def reset_clock(at: float = 1_000_000.0) -> None:
    global _clock_now
    _clock_now = at


def build_app(
    seed_users: list[dict[str, Any]],
    ttl_seconds: int = DEFAULT_TTL_SECONDS,
    clock: Callable[[], float] | None = None,
) -> tuple[ProfileAPI, InMemoryCache, Database]:
    database = Database(seed_users)
    cache = InMemoryCache(clock=clock or _clock)
    repo = UserRepository(database)
    service = ProfileService(repo, cache, ttl_seconds=ttl_seconds)
    return ProfileAPI(service), cache, database


_api: ProfileAPI | None = None
_cache: InMemoryCache | None = None
_db: Database | None = None


def reset(seed_users: list[dict[str, Any]], ttl_seconds: int = DEFAULT_TTL_SECONDS) -> None:
    global _api, _cache, _db
    reset_clock()
    _api, _cache, _db = build_app(seed_users, ttl_seconds=ttl_seconds, clock=_clock)


def run(payload: dict[str, Any]) -> dict[str, Any]:
    """
    Scripted action runner used by tests.

    Actions:
      reset          — seed DB + empty cache
      get            — GET /profiles/{user_id}
      update         — PATCH /profiles/{user_id}
      advance        — move the fake clock forward
      cache_keys     — inspect live cache keys (debug aid)
    """
    global _api, _cache

    action = payload.get("action")

    if action == "reset":
        reset(payload.get("users", []), ttl_seconds=int(payload.get("ttl_seconds", DEFAULT_TTL_SECONDS)))
        return {"ok": True, "action": "reset"}

    if _api is None or _cache is None:
        return {"ok": False, "error": "app_not_initialized — call reset first"}

    if action == "get":
        return _api.get(payload["user_id"])

    if action == "update":
        fields = payload.get("fields", {})
        return _api.patch(payload["user_id"], fields)

    if action == "advance":
        now = advance_time(float(payload.get("seconds", 0)))
        return {"ok": True, "action": "advance", "now": now}

    if action == "cache_keys":
        return {"ok": True, "keys": _cache.keys()}

    return {"ok": False, "error": f"unknown_action:{action}"}
