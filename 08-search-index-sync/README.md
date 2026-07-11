# Search index sync

**Level 3** · Search indexing and eventual consistency

## Scenario
Deleted products still appear in search. Newly updated titles show the old string for a long time.

## Expected behavior
Creates/updates/deletes are reflected in the search index in order; partial failures don't leave stale docs.

## Broken behavior
Stale and deleted docs remain searchable. Sync tests fail.

## Run
```bash
cd 08-search-index-sync
python3 test_search_sync.py
```

## Hints
- Order of apply operations matters
- Check logs/indexer.log for skipped deletes
- Inspect partial index update path

## Planned bug themes
missing reindex, stale index entry, deleted still searchable, out-of-order updates, bad partial indexing

## Success criteria
The tests pass and the behavior matches the scenario.

## Stuck?
Open PR `solution/08-search-index-sync` → **Files changed** (when published). Do not merge that PR.

## Status
Scaffold only — buggy `app.py` and rich fixtures/logs still to be authored.
