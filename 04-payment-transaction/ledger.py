"""In-process ledger: account balances + charge records."""

from __future__ import annotations

from typing import Any


class Ledger:
    def __init__(self, accounts: list[dict[str, Any]]) -> None:
        self._balances: dict[str, int] = {
            a["account_id"]: int(a["balance_cents"]) for a in accounts
        }
        self._charges: list[dict[str, Any]] = []
        self._by_idempotency: dict[str, dict[str, Any]] = {}

    def balance(self, account_id: str) -> int | None:
        if account_id not in self._balances:
            return None
        return self._balances[account_id]

    def balances(self) -> dict[str, int]:
        return dict(self._balances)

    def charges(self) -> list[dict[str, Any]]:
        return [dict(c) for c in self._charges]

    def find_by_idempotency(self, idempotency_key: str) -> dict[str, Any] | None:
        found = self._by_idempotency.get(idempotency_key)
        return dict(found) if found is not None else None

    def debit(self, account_id: str, cents: int) -> bool:
        if account_id not in self._balances:
            return False
        if self._balances[account_id] < cents:
            return False
        self._balances[account_id] -= cents
        return True

    def credit(self, account_id: str, cents: int) -> bool:
        if account_id not in self._balances:
            return False
        self._balances[account_id] += cents
        return True

    def record_charge(self, charge: dict[str, Any]) -> dict[str, Any]:
        row = dict(charge)
        self._charges.append(row)
        self._by_idempotency[row["idempotency_key"]] = row
        return dict(row)
