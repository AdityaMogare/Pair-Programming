# Canary-flavored anomaly detection (pair programming)

25–35 minute exercise: flag suspicious cloud events from a small JSON dataset using rules you define **together during the session**.

## Quick start (interviewer)

```bash
# Python (default)
python3 run.py

# Node (optional — same exercise)
node run.js
```

Open `events.json` on screen. Hand the candidate `detector.py` (or `detector.js`) and say:

> "Given these events, write something that surfaces the ones that look suspicious. We'll define what 'suspicious' means as we go."

## Suggested live rule rollout

Introduce criteria in phases so you can watch them adapt to a changing spec.

### Phase 1 — Baseline (5–8 min)

Define together:

| Rule | Definition |
|------|------------|
| **Off-hours** | Event timestamp outside **09:00–18:00 UTC** (inclusive start, exclusive end of window — clarify this!) |
| **Unusual region** | `geo.country` not in **`US`, `CA`, `GB`** |

Expected output shape (negotiate with candidate):

```json
{
  "event_id": "evt_007",
  "suspicious": true,
  "reasons": ["off_hours", "unusual_region"],
  "severity": 2
}
```

**Watch for:** Do they ask whether 09:00 is in or out? Empty/missing `geo`? Missing timestamp?

### Phase 2 — Extend (8–12 min)

Add one or two rules:

| Rule | Definition |
|------|------------|
| **Sensitive action** | `action` is `token.exfil` or `secret.read` |
| **New actor** | First time this `actor.user_id` appears in the dataset (requires seeing all events) |

**Watch for:** Do they refactor into pluggable rules instead of one giant `if` chain?

### Phase 3 — Frequency weight (5–8 min)

> "Now also weight by frequency: if the same `resource.id` is accessed **more than 3 times** in the dataset, bump severity by 1 (cap at 3)."

**Watch for:** Two-pass design (count first, then score)? Reuse of existing severity logic?

### Optional stretch

- Sort results by severity descending
- Return only `suspicious: true` events
- Treat `geo.country: null` as suspicious (unknown location)

## Evaluation rubric

| Signal | Strong | Weak |
|--------|--------|------|
| **Clarification** | Asks about timezone, inclusive bounds, missing fields, output format | Assumes silently, codes wrong edge behavior |
| **Structure** | Rules as functions/modules; easy to add Phase 2/3 | Monolithic nested ifs; hard to extend |
| **Testing** | Runs on 2–3 events verbally or with prints before "done" | Never validates edge cases |
| **Adaptability** | Minimal refactor when spec changes | Rewrites from scratch |
| **Communication** | Talks through tradeoffs (single vs two pass) | Goes quiet for long stretches |

## Files

| File | Purpose |
|------|---------|
| `events.json` | 20 raw cloud events (mix of normal + suspicious) |
| `detector.py` / `detector.js` | Candidate starter (stub + types/comments) |
| `run.py` / `run.js` | Runs detector and prints results |
| `reference/detector.py` | Interviewer-only reference solution |
| `reference/expected_phase3.json` | Expected flags after all three phases |

## Sample debrief questions

1. How would you deploy this if events arrived as a stream instead of a batch?
2. What would you log when a rule fires in production?
3. How would you unit-test the off-hours rule across DST?
