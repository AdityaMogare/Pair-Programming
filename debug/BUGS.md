# Spoilers — planted bugs in `debug/detector.py`

Only open after you've hunted, or when time-boxed.

There are **5** intentional bugs.

---

### Bug 1 — Off-hours boundary (`evt_009`)

**Symptom:** `evt_009` missing `off_hours` (timestamp `18:00:00Z`).

**Cause:** Condition uses `hour > OFF_HOURS_END` instead of `hour >= OFF_HOURS_END`.
Hour 18 is treated as in-hours.

**Fix:** `if hour < OFF_HOURS_START or hour >= OFF_HOURS_END:`

---

### Bug 2 — Null geo ignored (`evt_016`)

**Symptom:** `evt_016` missing `unusual_region` (`geo` is `null`).

**Cause:** Region check is wrapped in `if geo is not None`, so unknown location is skipped.

**Fix:** Treat missing geo as unusual, e.g. flag when `geo is None` or country not allowed.

---

### Bug 3 — Typo in sensitive action (`evt_007`, `…`)

**Symptom:** Events with `token.exfil` missing `sensitive_action`.

**Cause:** `SENSITIVE_ACTIONS` contains `"token.exfill"` (extra `l`).

**Fix:** `"token.exfil"`.

---

### Bug 4 — Inverted new-actor check (`evt_001` vs `evt_008`, etc.)

**Symptom:** First appearance of a user is *not* flagged; later appearances *are*.
E.g. `evt_002` missing `new_actor`, `evt_008` has extra `new_actor`.

**Cause:**
```python
if user_id and first_seen_user.get(user_id) != event["id"]:
```
Should be `==` (flag the first-seen event id).

**Fix:** `if user_id and first_seen_user.get(user_id) == event["id"]:`

---

### Bug 5 — Frequency threshold + uncapped severity

**Symptoms:**
- Extra `high_frequency` on resources with **exactly 3** hits (e.g. `tok_staging` → `evt_002`, `evt_008`, `evt_019`).
- Severity can exceed 3 (e.g. kitchen-sink events).

**Cause:**
- Uses `>= FREQ_THRESHOLD` instead of `>`.
- Sets `severity = len(reasons)` / `severity + 1` without `min(..., MAX_SEVERITY)`.

**Fix:**
```python
severity = min(len(reasons), MAX_SEVERITY)
if resource_id and resource_counts.get(resource_id, 0) > FREQ_THRESHOLD:
    reasons.append("high_frequency")
    severity = min(severity + 1, MAX_SEVERITY)
```

---

## Suggested fix order (matches natural test failures)

1. Typo / null geo / boundary — local, easy to see from one event  
2. New-actor inversion — needs comparing two events for the same user  
3. Frequency + severity cap — needs counting across the batch  

## Verify

```bash
python3 -m debug.test_detector
# → All checks passed.
```
