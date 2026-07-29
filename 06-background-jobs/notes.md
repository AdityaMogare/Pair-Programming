# Notes (learner scratchpad)

## Ticket
- Symptom: digests sometimes never send; other times customers get two; worker goes quiet while queue depth looks fine
- When: after worker deploy; crashes and SMTP blips

## Hypotheses
1.
2.
3.

## Evidence
- logs/worker.log missing_ack / swallowed / past_max_no_dlq
- fixtures/expected_scenario.json vs run.py output
- test output:
