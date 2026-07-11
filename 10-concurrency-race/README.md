# Concurrency race

**Level 4** · Multi-request race conditions

## Scenario
Flash sale oversold inventory when two checkouts hit the same SKU. Load test reproduces negative stock.

## Expected behavior
Inventory decrements atomically; concurrent checkouts cannot oversell; locks are always released.

## Broken behavior
Under parallel requests, stock goes negative or duplicates appear. Race tests fail.

## Run
```bash
cd 10-concurrency-race
python3 test_concurrency.py
```

## Hints
- Run the parallel fixture more than once
- Look for check-then-act without a lock/transaction
- Check logs/app.log for interleaved updates

## Planned bug themes
last-write-wins, inventory oversell, duplicate insert, lock not released, inconsistent state under load

## Success criteria
The tests pass and the behavior matches the scenario.

## Stuck?
Open PR `solution/10-concurrency-race` → **Files changed** (when published). Do not merge that PR.

## Status
Scaffold only — buggy `app.py` and rich fixtures/logs still to be authored.
