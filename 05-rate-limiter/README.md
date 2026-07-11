# Rate limiter

**Level 2** · Request throttling

## Scenario
API clients are getting 429s too early, or one noisy user is starving others. Edge gateway metrics look wrong for the sliding window.

## Expected behavior
Per-user limits enforce N requests per window; windows don't collide across users; counters behave at boundaries.

## Broken behavior
Off-by-one window behavior and key collisions. Boundary tests fail.

## Run
```bash
cd 05-rate-limiter
python3 test_rate_limiter.py
```

## Hints
- Draw the window on paper for the failing fixture
- Check key namespacing per user
- Read logs/gateway.log around 429s

## Planned bug themes
off-by-one window, per-user key collision, global limit misapplied, clock drift, counter reset bug

## Success criteria
The tests pass and the behavior matches the scenario.

## Stuck?
Open PR `solution/05-rate-limiter` → **Files changed** (when published). Do not merge that PR.

## Status
Scaffold only — buggy `app.py` and rich fixtures/logs still to be authored.
