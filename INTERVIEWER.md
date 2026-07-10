# Interviewer cheat sheet

## Opening script

> "You're looking at cloud security events — token accesses, secret reads, that kind of thing. Implement `flag_suspicious_events` so we can see which ones look off. I'll give you criteria as we go; ask me anything ambiguous before you lock it in."

## Edge-case events (good prompts if they're quiet)

| Event | Why it matters |
|-------|----------------|
| **evt_008** | Bob's *second* access — should be clean after Phase 2 if rules are correct |
| **evt_009** | Exactly 18:00 UTC — off-hours if window is `[09:00, 18:00)` |
| **evt_016** | `geo: null` — do they flag it? (stretch: yes) |
| **evt_019** | 08:59 UTC — one minute before business hours |
| **evt_007** | Kitchen sink: off-hours + RU + exfil + new actor + hot token |

## Expected suspicious counts (reference solution)

| Phase | Rules added | Suspicious count |
|-------|-------------|------------------|
| 1 | off_hours, unusual_region | **10** |
| 2 | + sensitive_action, new_actor | **19** (only evt_008 clean) |
| 3 | + high_frequency bump | same 19, severities shift |

### Phase 1 event IDs

`evt_003`, `evt_004`, `evt_007`, `evt_009`, `evt_011`, `evt_012`, `evt_015`, `evt_016`, `evt_018`, `evt_019`

## Validate reference output

```bash
python3 -c "
import json, sys
sys.path.insert(0, 'reference')
from detector import flag_suspicious_events
exp = json.load(open('reference/expected_phase3.json'))
act = flag_suspicious_events(json.load(open('events.json')))
assert act == exp, 'mismatch'
print('reference OK')
"
```

## If they finish early

- "How would you make rules configurable without redeploying?"
- "What if `timestamp` is missing?"
- "Return a single `risk_score` float instead of integer severity"

## Red flags vs green flags

**Green:** Separates rule functions; builds context in a first pass when frequency/new_actor appear; asks about UTC vs local time.

**Red:** Hardcodes event IDs; ignores null geo silently; can't add a third rule without copy-paste.
