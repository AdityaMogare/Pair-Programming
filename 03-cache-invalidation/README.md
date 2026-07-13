# 03 — Cache invalidation

**Level 3** · Redis cache consistency (first “real backend” issue)

## Scenario

Users report seeing another account’s profile — or their own **old** profile — after saving changes. Support reproduced stale reads for about a minute after profile writes, and one extra stale read right when the TTL should have expired.

## Stack

```text
API (api.py)
  ↓
Service (service.py)
  ↓
Cache / Redis stand-in (cache.py)
  ↓
Repository (repository.py)
  ↓
Database (db.py)
```

`app.py` wires the stack and exposes a scripted `run({action: ...})` harness for tests.

## Expected behavior

| Path | Behavior |
|------|----------|
| **Read** | Cache hit when entry is still within TTL; otherwise load DB and populate cache |
| **Write** | Persist to DB, then invalidate the **same** per-user key the read path uses |
| **TTL** | Expired entries are treated as misses — never returned, then evicted |

Cache key format must be consistent on get / set / delete (e.g. `profile:{user_id}`).

## Broken behavior

Isolation and freshness checks in `fixtures/expected_scenario.json` fail: post-write stale reads, wrong or ineffective invalidation, and a TTL path that still serves expired data once.

## Run

```bash
cd 03-cache-invalidation
python3 test_cache.py
# optional:
python3 run.py
```

## Hints

- Inspect cache key construction for reads vs invalidation
- Trace the write path in `logs/redis.log` (`DEL` result / live keys)
- Check TTL handling in `cache.py` — when is expiry decided relative to the return?
- Confirm the write path actually updates or drops the cached row

### Probe steps

| Step | Why |
|------|-----|
| `read_after_write_must_be_fresh` | Invalidation / key mismatch |
| `first_read_after_ttl_must_not_be_stale` | TTL ordered wrong vs return |
| `alice_still_alice_not_bob` | Cross-user isolation |

## Success criteria

`python3 test_cache.py` exits 0 and matches `fixtures/expected_scenario.json`.

## Stuck?

Open PR **`solution/03-cache-invalidation`** → **Files changed**. Do not merge that PR.
