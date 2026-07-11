# Config & deployment

**Level 4** · Environment and release problems

## Scenario
Prod behaves like staging after a release. A migration ran in the wrong order and a feature flag doesn't match the binary.

## Expected behavior
Env-specific config loads correctly; migrations are ordered; feature flags match the deployed version.

## Broken behavior
Wrong env vars / flag mismatch / migration order. Deploy verification tests fail.

## Run
```bash
cd 12-config-deployment
python3 test_config.py
```

## Hints
- Diff fixtures/config.staging.json vs config.prod.json
- Read logs/deploy.log for migration order
- Check feature flag vs app version

## Planned bug themes
wrong env var, feature flag mismatch, stale container image, migration order issue, dev/prod config drift

## Success criteria
The tests pass and the behavior matches the scenario.

## Stuck?
Open PR `solution/12-config-deployment` → **Files changed** (when published). Do not merge that PR.

## Status
Scaffold only — buggy `app.py` and rich fixtures/logs still to be authored.
