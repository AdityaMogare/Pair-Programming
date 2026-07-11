# 01 — Anomaly detector

## Scenario

Security ops opened a ticket: the canary-token anomaly detector is either missing high-risk events or flooding the queue with noise. Overnight review of `tok_prod_api` looked wrong compared to what analysts expected from the raw event feed.

## Expected behavior

Given a batch of cloud events, flag suspicious ones using:

| Rule | Definition |
|------|------------|
| **off_hours** | UTC hour outside **[09:00, 18:00)** — 09:00 in-hours, 18:00 off-hours |
| **unusual_region** | `geo.country` not in `{US, CA, GB}` — **null geo counts as unusual** |
| **sensitive_action** | `action` is `token.exfil` or `secret.read` |
| **new_actor** | First time this `actor.user_id` appears in the batch |
| **high_frequency** | Same `resource.id` appears **more than 3** times → reason + **+1 severity**, severity **capped at 3** |

## Broken behavior

Regression tests against `fixtures/expected.json` fail. Severity and reasons disagree with the analyst playbook for several `event_id`s (see test output).

## Run

```bash
cd 01-anomaly-detector
python3 test_detector.py
# optional:
python3 run.py
```

## Hints

- Check `logs/` for the same `event_id` around the failure window
- Inspect the failing test lines first — one event at a time
- Compare `fixtures/events.json` to `fixtures/expected.json`
- Look for edge cases: boundaries, null geo, first vs later actor, frequency threshold

### Probe events

| Event | Why |
|-------|-----|
| `evt_009` | Exactly `18:00:00Z` |
| `evt_016` | `geo: null` |
| `evt_007` | `token.exfil` + many signals |
| `evt_008` / `evt_002` | Bob second vs first access |
| `evt_019` | `tok_staging` appears 3 times |

## Success criteria

`python3 test_detector.py` exits 0 and matches `fixtures/expected.json`.

## Stuck?

Open PR **`solution/01-anomaly-detector`** → **Files changed**. Do not merge that PR.
