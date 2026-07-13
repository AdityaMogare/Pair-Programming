"""In-memory database for user profiles."""

from __future__ import annotations

import copy
from typing import Any


class Database:
    """Mutable row store keyed by user_id."""

    def __init__(self, rows: list[dict[str, Any]] | None = None) -> None:
        self._rows: dict[str, dict[str, Any]] = {}
        for row in rows or []:
            self._rows[row["user_id"]] = copy.deepcopy(row)

    def get_user(self, user_id: str) -> dict[str, Any] | None:
        row = self._rows.get(user_id)
        return copy.deepcopy(row) if row is not None else None

    def update_user(self, user_id: str, fields: dict[str, Any]) -> dict[str, Any] | None:
        if user_id not in self._rows:
            return None
        self._rows[user_id].update(fields)
        return copy.deepcopy(self._rows[user_id])

    def all_users(self) -> list[dict[str, Any]]:
        return [copy.deepcopy(r) for r in self._rows.values()]
