"""Persistence helpers over the in-memory database."""

from __future__ import annotations

from typing import Any

from db import Database


class UserRepository:
    def __init__(self, database: Database) -> None:
        self._db = database

    def find_by_id(self, user_id: str) -> dict[str, Any] | None:
        return self._db.get_user(user_id)

    def save_profile(self, user_id: str, fields: dict[str, Any]) -> dict[str, Any] | None:
        allowed = {k: v for k, v in fields.items() if k in {"display_name", "email", "plan"}}
        if not allowed:
            return self._db.get_user(user_id)
        return self._db.update_user(user_id, allowed)
