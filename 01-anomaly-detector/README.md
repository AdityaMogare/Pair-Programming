# 01 — Anomaly detector

Someone "finished" this cloud-event anomaly detector. It runs. Output looks plausible. Tests fail.

## Goal

```bash
cd 01-anomaly-detector
python3 test_detector.py
```

Optional: `python3 run.py` to print currently flagged events.

## Spec

| Rule | Definition |
|------|------------|
| **off_hours** | UTC hour outside **[09:00, 18:00)** — 09:00 in-hours, 18:00 off-hours |
| **unusual_region** | `geo.country` not in `{US, CA, GB}` — **null geo counts as unusual** |
| **sensitive_action** | `action` is `token.exfil` or `secret.read` |
| **new_actor** | First time this `actor.user_id` appears in the batch |
| **high_frequency** | Same `resource.id` appears **more than 3** times → append reason and **+1 severity**, severity **capped at 3** |

Expected results: `expected.json`.

## Debug loop

1. **Reproduce** — run the test; read failures.
2. **Isolate** — pick one `event_id` in `events.json`.
3. **Predict** — which reasons should fire? What severity?
4. **Observe** — temporary prints in `detector.py`.
5. **Fix one bug** — re-run; watch the failure count drop.

## Probe events

| Event | Why |
|-------|-----|
| `evt_009` | Exactly `18:00:00Z` — off-hours boundary |
| `evt_016` | `geo: null` |
| `evt_007` | `token.exfil` + many signals |
| `evt_008` | Bob's *second* access — should **not** be `new_actor` |
| `evt_002` | Bob's *first* access — **should** be `new_actor` |
| `evt_019` | `tok_staging` appears 3 times — frequency threshold |

## Stuck?

Open the Pull Request **`solution/01-anomaly-detector`** on GitHub and inspect **Files changed**. Do not merge that PR.

Time box: 20–30 minutes.
