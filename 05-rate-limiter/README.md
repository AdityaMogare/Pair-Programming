# 05 — Rate limiter

**Level 2** · Request throttling

## Scenario

API clients are getting 429s too early under a limit of N, and one noisy user appears to starve everyone else. Edge gateway metrics for the sliding window also look wrong exactly when the window should roll forward.

## Stack

```text
API harness (app.py)
  ↓
RateLimiter (limiter.py) — sliding window of request timestamps
  ↓
TimestampStore (store.py)
```

## Expected behavior

| Path | Behavior |
|------|----------|
| **Allow** | Each user may send up to **N** requests inside the window |
| **Block** | Request **N+1** in the same window returns **429** |
| **Isolation** | Counters are **per user** — Alice’s traffic must not 429 Bob |
| **Window edge** | A hit exactly `window_seconds` old is aged out (`now - t < window`) |

## Broken behavior

Regression tests against `fixtures/expected_scenario.json` fail: the Nth request is rejected early, Bob shares Alice’s counter, and the exact window boundary still counts the oldest hit.

## Run

```bash
cd 05-rate-limiter
python3 test_rate_limiter.py
# optional:
python3 run.py
```

## Hints

- Draw the window on paper for the failing fixture steps
- Check key namespacing per user in `logs/gateway.log`
- Inspect the allow / deny comparison against `limit`
- At exactly `window_seconds` later — is the oldest timestamp pruned?

### Probe steps

| Step | Why |
|------|-----|
| `alice_3_allowed_nth_must_pass` | Off-by-one / 429 too early |
| `bob_not_starved_by_alice` | Shared / colliding counter key |
| `alice_after_window_edge_must_allow` | Inclusive vs exclusive window edge |

## Success criteria

`python3 test_rate_limiter.py` exits 0 and matches `fixtures/expected_scenario.json`.

## Stuck?

Open PR **`solution/05-rate-limiter`** → **Files changed**. Do not merge that PR.
