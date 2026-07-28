#!/usr/bin/env python3
"""Drive the fixture scenario and print responses (possibly buggy)."""

from __future__ import annotations

import json
from pathlib import Path

from app import run

HERE = Path(__file__).resolve().parent


def main() -> None:
    seed = json.loads((HERE / "fixtures" / "seed_accounts.json").read_text())
    scenario = json.loads((HERE / "fixtures" / "expected_scenario.json").read_text())

    run({"action": "reset", "accounts": seed["accounts"]})
    print(f"Reset with {len(seed['accounts'])} account(s)\n")

    for step in scenario["steps"]:
        name = step["name"]
        actual = run(step["action"])
        action = step["action"].get("action")

        if action == "script_gateway":
            print(f"{name}: scripted {step['action'].get('outcomes')}")
            continue

        if action == "charges":
            charges = actual.get("charges") or []
            print(f"{name}: charge_count={len(charges)}")
            continue

        charge = actual.get("charge") or {}
        print(
            f"{name}: ok={actual.get('ok')} duplicate={actual.get('duplicate')} "
            f"error={actual.get('error')!r} balance={actual.get('balance_cents')} "
            f"amount_cents={charge.get('amount_cents')}"
        )

    balances = run({"action": "balances"})
    print(f"\nBalances: {balances.get('balances')}")
    merchant = run({"action": "merchant_charges"})
    print(f"Merchant captures: {len(merchant.get('merchant_charges') or [])}")


if __name__ == "__main__":
    main()
