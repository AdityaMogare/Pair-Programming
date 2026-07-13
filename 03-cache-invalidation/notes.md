# Notes (learner scratchpad)

## Ticket
- Symptom: stale profile after save; sometimes one more stale read ~60s later
- When: after PATCH /profiles/{id}

## Hypotheses
1.
2.
3.

## Evidence
- logs/redis.log DEL result / live_keys
- cache keys from run.py
- test output:
