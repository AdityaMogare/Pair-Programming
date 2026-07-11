# Payment transaction

**Level 3** · Money movement and idempotency

## Scenario
Finance flagged duplicate charges for the same checkout_id after a gateway timeout retry.

## Expected behavior
Charges are idempotent per idempotency key; failures roll back cleanly; amounts use exact decimal money math.

## Broken behavior
Retries double-charge; some failures leave partial state; money tests fail on precision.

## Run
```bash
cd 04-payment-transaction
python3 test_payments.py
```

## Hints
- Follow the retry path in logs/worker.log
- Check idempotency key handling
- Avoid float for currency

## Planned bug themes
partial rollback, duplicate charge, floating-point precision, missing idempotency key, retry double processing

## Success criteria
The tests pass and the behavior matches the scenario.

## Stuck?
Open PR `solution/04-payment-transaction` → **Files changed** (when published). Do not merge that PR.

## Status
Scaffold only — buggy `app.py` and rich fixtures/logs still to be authored.
