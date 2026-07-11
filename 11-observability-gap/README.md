# Observability gap

**Level 4** · Debugging with incomplete signals

## Scenario
An incident took 90 minutes because traces were broken and logs couldn't be correlated across services.

## Expected behavior
Every request carries a request_id; spans parent correctly; important paths emit metrics; alerts use the right threshold.

## Broken behavior
Correlation IDs missing, traces incomplete, alert tests fail.

## Run
```bash
cd 11-observability-gap
python3 test_observability.py
```

## Hints
- Grep logs for missing request_id
- Compare fixtures/trace.json to expected parent/child spans
- Check metric names and alert thresholds

## Planned bug themes
missing request IDs, broken tracing, logs at wrong level, metrics not emitted, alert threshold wrong

## Success criteria
The tests pass and the behavior matches the scenario.

## Stuck?
Open PR `solution/11-observability-gap` → **Files changed** (when published). Do not merge that PR.

## Status
Scaffold only — buggy `app.py` and rich fixtures/logs still to be authored.
