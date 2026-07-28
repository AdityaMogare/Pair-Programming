"""Simulated card gateway with scripted outcomes (ok / timeout / fail)."""

from __future__ import annotations

from typing import Any


class GatewayTimeout(Exception):
    """Client-side timeout — no capture confirmation."""


class GatewayError(Exception):
    """Hard decline / processor error — charge did not go through."""


class Gateway:
    def __init__(self) -> None:
        self._script: list[str] = []
        self._merchant_charges: list[dict[str, Any]] = []
        self._seq = 0

    def script(self, outcomes: list[str]) -> None:
        """Queue next charge outcomes: 'ok', 'timeout', or 'fail'."""
        self._script = list(outcomes)

    def merchant_charges(self) -> list[dict[str, Any]]:
        return [dict(c) for c in self._merchant_charges]

    def charge(
        self,
        *,
        account_id: str,
        amount_cents: int,
        checkout_id: str,
        idempotency_key: str,
    ) -> dict[str, Any]:
        outcome = self._script.pop(0) if self._script else "ok"
        self._seq += 1
        ref = f"gw_{self._seq:04d}"

        if outcome == "fail":
            raise GatewayError("processor_declined")

        if outcome == "timeout":
            raise GatewayTimeout("gateway_timeout")

        entry = {
            "gateway_ref": ref,
            "account_id": account_id,
            "amount_cents": amount_cents,
            "checkout_id": checkout_id,
            "idempotency_key": idempotency_key,
        }
        self._merchant_charges.append(entry)
        return {"gateway_ref": ref, "status": "captured"}
