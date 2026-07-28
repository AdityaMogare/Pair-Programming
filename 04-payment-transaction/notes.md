# Notes (learner scratchpad)

## Ticket
- Symptom: duplicate charges for same checkout_id after gateway timeout retry; some declines leave balance lower
- When: client retries with the same idempotency key

## Hypotheses
1.
2.
3.

## Evidence
- logs/worker.log IDEMPOTENCY_LOOKUP / DEBIT
- fixtures/expected_scenario.json vs run.py output
- test output:
