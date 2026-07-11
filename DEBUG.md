# Debug exercise — learn by fixing a broken detector

Someone "finished" the anomaly detector. It runs. The output looks plausible.
The tests say otherwise.

## Goal

Make this pass:

```bash
python3 -m debug.test_detector
```

Optional: eyeball live output with `python3 debug/run.py`.

## Spec (ground truth)

| Rule | Definition |
|------|------------|
| **off_hours** | UTC hour outside **[09:00, 18:00)** — 09:00 in-hours, 18:00 off-hours |
| **unusual_region** | `geo.country` not in `{US, CA, GB}` — **null geo counts as unusual** |
| **sensitive_action** | `action` is `token.exfil` or `secret.read` |
| **new_actor** | First time this `actor.user_id` appears in the batch |
| **high_frequency** | Same `resource.id` appears **more than 3** times → append reason and **+1 severity**, severity **capped at 3** |

Expected results live in `reference/expected_phase3.json`.

## How to debug (practice this loop)

1. **Reproduce** — run the test; read the failure list.
2. **Isolate** — pick one `event_id`. Open that object in `events.json`.
3. **Predict** — on paper, which reasons should fire? What severity?
4. **Observe** — print that event's `reasons` / intermediate values in `debug/detector.py`.
5. **Hypothesize** — one concrete wrong assumption (boundary? typo? inverted check?).
6. **Fix & re-run** — change one thing; confirm that failure shrinks.

Resist rewriting the whole file. The point is the hunt.

## Good starter events

| Event | Why it's a useful probe |
|-------|-------------------------|
| `evt_009` | Exactly `18:00:00Z` — boundary for off-hours |
| `evt_016` | `geo: null` — missing-data path |
| `evt_007` | `token.exfil` + many other signals |
| `evt_008` | Bob's *second* access — should **not** be `new_actor` |
| `evt_002` | Bob's *first* access — **should** be `new_actor` |
| `evt_019` | `tok_staging` appears 3 times total — frequency threshold |

## When you're done

- Re-run tests until green.
- Skim `debug/BUGS.md` and check whether you found every planted bug.
- Note which bug took longest — that pattern is worth remembering.

## Time box

20–30 minutes solo. If you're stuck >10 minutes on one failure, peek at **one** spoiler in `debug/BUGS.md`, then close it and keep going.
