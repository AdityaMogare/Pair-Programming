"""
Regression tests for 04-payment-transaction.

Run from this directory:
  python3 test_payments.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from app import run  # noqa: E402


def _load() -> tuple[dict, dict]:
    seed = json.loads((HERE / "fixtures" / "seed_accounts.json").read_text())
    scenario = json.loads((HERE / "fixtures" / "expected_scenario.json").read_text())
    return seed, scenario


def _compare_charge(got: dict | None, want: dict, step: str) -> list[str]:
    failures: list[str] = []
    if got is None:
        failures.append(f"{step}: missing charge object")
        return failures
    for field, expected in want.items():
        if got.get(field) != expected:
            failures.append(
                f"{step}: charge.{field}={got.get(field)!r} (expected {expected!r})"
            )
    return failures


def compare_step(name: str, actual: dict, expect: dict) -> list[str]:
    failures: list[str] = []

    if "ok" in expect and actual.get("ok") != expect["ok"]:
        failures.append(f"{name}: ok={actual.get('ok')!r} (expected {expect['ok']!r})")

    if "duplicate" in expect and actual.get("duplicate") != expect["duplicate"]:
        failures.append(
            f"{name}: duplicate={actual.get('duplicate')!r} "
            f"(expected {expect['duplicate']!r})"
        )

    if "error" in expect and actual.get("error") != expect["error"]:
        failures.append(
            f"{name}: error={actual.get('error')!r} (expected {expect['error']!r})"
        )

    if "balance_cents" in expect and actual.get("balance_cents") != expect["balance_cents"]:
        failures.append(
            f"{name}: balance_cents={actual.get('balance_cents')!r} "
            f"(expected {expect['balance_cents']!r})"
        )

    if "charge" in expect:
        failures.extend(_compare_charge(actual.get("charge"), expect["charge"], name))

    if "charge_count" in expect:
        charges = actual.get("charges") or []
        if len(charges) != expect["charge_count"]:
            failures.append(
                f"{name}: charge_count={len(charges)} "
                f"(expected {expect['charge_count']})"
            )

    return failures


def main() -> int:
    seed, scenario = _load()
    run({"action": "reset", "accounts": seed["accounts"]})

    failures: list[str] = []
    print(f"Running {len(scenario['steps'])} scenario steps\n")

    for step in scenario["steps"]:
        name = step["name"]
        actual = run(step["action"])
        step_failures = compare_step(name, actual, step.get("expect", {}))
        if step_failures:
            failures.extend(step_failures)
            print(f"  ✗ {name}")
            for line in step_failures:
                print(f"      {line}")
        else:
            print(f"  ✓ {name}")

    print()
    if not failures:
        print("All checks passed. Nice debugging.")
        return 0

    print(f"{len(failures)} failure(s).\n")
    print("Hints (no spoilers):")
    print("  1. Retry with the same idempotency key — does the ledger index match the lookup?")
    print("  2. amount_cents for 19.99 / 1.15 — float or exact decimal math?")
    print("  3. After processor_declined / timeout, is the debit rolled back?")
    print("  4. Compare logs/worker.log retry path to fixtures/expected_scenario.json.")
    print("\nStuck? Open PR solution/04-payment-transaction → Files changed.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
