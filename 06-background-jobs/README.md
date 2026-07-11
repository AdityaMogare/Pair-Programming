# Background jobs

**Level 3** · Queue workers

## Scenario
Email digests sometimes never send; other times customers get two. The queue depth looks healthy but worker logs go quiet.

## Expected behavior
Jobs are acknowledged after success, retried with backoff on failure, and poison messages go to a DLQ without infinite loops.

## Broken behavior
Jobs stick unacked, crash silently, or run twice. Worker tests fail.

## Run
```bash
cd 06-background-jobs
python3 test_jobs.py
```

## Hints
- Compare ack vs retry paths
- Check logs/worker.log for crashes without ack
- Inspect poison-message handling

## Planned bug themes
job never acknowledged, silent worker crash, retry loop, duplicate execution, poison message handling

## Success criteria
The tests pass and the behavior matches the scenario.

## Stuck?
Open PR `solution/06-background-jobs` → **Files changed** (when published). Do not merge that PR.

## Status
Scaffold only — buggy `app.py` and rich fixtures/logs still to be authored.
