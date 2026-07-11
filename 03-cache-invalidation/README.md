# Cache invalidation

**Level 3** · Redis cache consistency

## Scenario
Users report seeing another account's profile after an update. Support reproduced stale reads for ~60s after profile writes.

## Expected behavior
Reads hit cache when valid; writes invalidate the correct per-user key; TTL and key format stay consistent.

## Broken behavior
Stale or cross-user data is returned after updates. Isolation tests fail.

## Run
```bash
cd 03-cache-invalidation
python3 test_cache.py
```

## Hints
- Inspect cache key construction
- Trace write path invalidation in logs/redis.log
- Check TTL vs test expectations

## Planned bug themes
stale reads, wrong TTL, missing invalidation, key mismatch, cache stampede

## Success criteria
The tests pass and the behavior matches the scenario.

## Stuck?
Open PR `solution/03-cache-invalidation` → **Files changed** (when published). Do not merge that PR.

## Status
Scaffold only — buggy `app.py` and rich fixtures/logs still to be authored.
