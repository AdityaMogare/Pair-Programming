# 06 — Background jobs

**Level 3** · Queue workers

## Scenario

Email digests sometimes never send; other times customers get two. The ready-queue depth looks healthy, but worker logs go quiet while a job sits inflight after a crash. Poison SMTP failures also never leave the ready lane.

## Stack

```text
API harness (app.py)
  ↓
Worker (worker.py) — reserve → handle → ack / nack / DLQ
  ↓
JobQueue (queue.py)          Handler (handler.py)
```

## Expected behavior

| Path | Behavior |
|------|----------|
| **Success** | Handler sends once, worker **acks** → job moves to `done` |
| **Retry** | Transient failure **nacks** (attempts++) and requeues |
| **Poison** | After `max_attempts` failures, job goes to the **DLQ** (no infinite loop) |
| **Crash** | Unexpected errors must not leave the job stuck **inflight** — dead-letter it |

Unacked inflight jobs are redelivered on the next tick (visibility timeout). Missing acks therefore cause duplicate sends.

## Broken behavior

Regression tests against `fixtures/expected_scenario.json` fail: successful jobs are redelivered and sent twice, poison jobs never reach the DLQ, and crashes leave work stuck inflight while ready depth looks fine.

## Run

```bash
cd 06-background-jobs
python3 test_jobs.py
# optional:
python3 run.py
```

## Hints

- Compare ack vs retry paths in `worker.py`
- Check `logs/worker.log` for `missing_ack` / `swallowed` / `past_max_no_dlq`
- Inspect poison-message handling against `max_attempts`
- After a crash, is the job still in `inflight`?

### Probe steps

| Step | Why |
|------|-----|
| `tick_alice_success_acks` / `tick_idle_must_not_resend_alice` | Missing ack → duplicate send |
| `tick_carol_poison_to_dlq` | No DLQ past max attempts |
| `tick_crash_must_not_stick_inflight` | Swallowed exception / stuck inflight |

## Success criteria

`python3 test_jobs.py` exits 0 and matches `fixtures/expected_scenario.json`.

## Stuck?

Open PR **`solution/06-background-jobs`** → **Files changed**. Do not merge that PR.
