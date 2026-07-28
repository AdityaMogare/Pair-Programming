"""
Payment transaction — checkout charges with idempotency + ledger.

Stack:
  API harness → PaymentService → Ledger / Gateway
  Money helpers convert dollar amounts → integer cents

Run: python3 test_payments.py
Stuck? Open PR solution/04-payment-transaction → Files changed.
"""

from __future__ import annotations

from typing import Any

from gateway import Gateway
from ledger import Ledger
from service import PaymentService

_ledger: Ledger | None = None
_gateway: Gateway | None = None
_service: PaymentService | None = None


def reset(accounts: list[dict[str, Any]]) -> None:
    global _ledger, _gateway, _service
    _ledger = Ledger(accounts)
    _gateway = Gateway()
    _service = PaymentService(_ledger, _gateway)


def run(payload: dict[str, Any]) -> dict[str, Any]:
    """
    Scripted action runner used by tests.

    Actions:
      reset              — seed account balances
      script_gateway     — queue next gateway outcomes
      charge             — capture a checkout charge
      balance            — read one account balance
      balances           — dump all balances
      charges            — list local ledger charges
      merchant_charges   — list gateway captures (debug aid)
    """
    global _ledger, _gateway, _service

    action = payload.get("action")

    if action == "reset":
        reset(payload.get("accounts", []))
        return {"ok": True, "action": "reset"}

    if _ledger is None or _gateway is None or _service is None:
        return {"ok": False, "error": "app_not_initialized — call reset first"}

    if action == "script_gateway":
        _gateway.script(payload.get("outcomes", []))
        return {"ok": True, "action": "script_gateway"}

    if action == "charge":
        return _service.charge(
            account_id=payload["account_id"],
            amount=str(payload["amount"]),
            checkout_id=payload["checkout_id"],
            idempotency_key=payload["idempotency_key"],
        )

    if action == "balance":
        account_id = payload["account_id"]
        return {
            "ok": True,
            "account_id": account_id,
            "balance_cents": _ledger.balance(account_id),
        }

    if action == "balances":
        return {"ok": True, "balances": _ledger.balances()}

    if action == "charges":
        return {"ok": True, "charges": _ledger.charges()}

    if action == "merchant_charges":
        return {"ok": True, "merchant_charges": _gateway.merchant_charges()}

    return {"ok": False, "error": f"unknown_action:{action}"}
