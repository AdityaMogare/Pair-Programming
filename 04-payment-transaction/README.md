# 04 — Payment transaction

**Level 3** · Money movement and idempotency

## Scenario

Finance flagged duplicate charges for the same `checkout_id` after a gateway timeout retry. Some declines also left customer balances lower even though no capture was recorded. Amounts like `19.99` and `1.15` disagree with the ledger’s cent totals.

## Stack

```text
API harness (app.py)
  ↓
PaymentService (service.py)
  ↓
Ledger (ledger.py)     Gateway (gateway.py)
  ↓
Money helpers (money.py) — dollars → integer cents
```

## Expected behavior

| Path | Behavior |
|------|----------|
| **Charge** | Convert amount to **exact** integer cents, capture via gateway, debit once, record one ledger row |
| **Retry** | Same `idempotency_key` returns the original charge (`duplicate=true`) — no second debit / capture |
| **Decline / timeout** | Balance unchanged; no ledger charge row |

## Broken behavior

Regression tests against `fixtures/expected_scenario.json` fail: retries create a second capture, cent math is short by a penny, and failed / timed-out charges leave a debit hold.

## Run

```bash
cd 04-payment-transaction
python3 test_payments.py
# optional:
python3 run.py
```

## Hints

- Follow the retry path in `logs/worker.log` (`IDEMPOTENCY_LOOKUP`)
- Check how `find_by_idempotency` is called vs how charges are indexed
- Avoid `float` for currency — probe `19.99` and `1.15`
- On `processor_declined` / `gateway_timeout`, is the debit rolled back?

### Probe steps

| Step | Why |
|------|-----|
| `timeout_retry_same_key_must_not_double_charge` | Idempotency key mismatch / missed lookup |
| `charge_19_99_exact_cents` / `charge_1_15_float_trap` | Float truncation to cents |
| `declined_charge_must_not_keep_debit` | Partial rollback |
| `timeout_must_not_leave_partial_hold` | Hold left after timeout |

## Success criteria

`python3 test_payments.py` exits 0 and matches `fixtures/expected_scenario.json`.

## Stuck?

Open PR **`solution/04-payment-transaction`** → **Files changed**. Do not merge that PR.
