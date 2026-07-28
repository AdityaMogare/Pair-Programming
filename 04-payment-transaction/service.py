"""Payment service — charge orchestration with ledger + gateway."""

from __future__ import annotations

from typing import Any

from gateway import Gateway, GatewayError, GatewayTimeout
from ledger import Ledger
from money import dollars_to_cents


class PaymentService:
    def __init__(self, ledger: Ledger, gateway: Gateway) -> None:
        self._ledger = ledger
        self._gateway = gateway
        self._charge_seq = 0

    def charge(
        self,
        *,
        account_id: str,
        amount: str,
        checkout_id: str,
        idempotency_key: str,
    ) -> dict[str, Any]:
        existing = self._ledger.find_by_idempotency(idempotency_key)
        if existing is not None:
            return {
                "ok": True,
                "duplicate": True,
                "charge": existing,
                "balance_cents": self._ledger.balance(account_id),
            }

        cents = dollars_to_cents(amount)

        # Debit first so the hold is visible — roll back on gateway failure.
        if not self._ledger.debit(account_id, cents):
            return {
                "ok": False,
                "error": "insufficient_funds",
                "balance_cents": self._ledger.balance(account_id),
            }

        try:
            gw = self._gateway.charge(
                account_id=account_id,
                amount_cents=cents,
                checkout_id=checkout_id,
                idempotency_key=idempotency_key,
            )
        except GatewayTimeout:
            self._ledger.credit(account_id, cents)
            return {
                "ok": False,
                "error": "gateway_timeout",
                "balance_cents": self._ledger.balance(account_id),
            }
        except GatewayError as exc:
            self._ledger.credit(account_id, cents)
            return {
                "ok": False,
                "error": str(exc),
                "balance_cents": self._ledger.balance(account_id),
            }

        self._charge_seq += 1
        charge = self._ledger.record_charge(
            {
                "charge_id": f"ch_{self._charge_seq:04d}",
                "account_id": account_id,
                "checkout_id": checkout_id,
                "idempotency_key": idempotency_key,
                "amount_cents": cents,
                "gateway_ref": gw["gateway_ref"],
                "status": "captured",
            }
        )
        return {
            "ok": True,
            "duplicate": False,
            "charge": charge,
            "balance_cents": self._ledger.balance(account_id),
        }
