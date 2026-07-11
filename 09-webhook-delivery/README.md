# Webhook delivery

**Level 3** · Outbound integrations

## Scenario
Partner says signatures fail verification and they sometimes receive the same event twice after our retries.

## Expected behavior
Signed payloads verify with the shared secret; retries are idempotent; permanent failures land in DLQ.

## Broken behavior
Signature mismatch and duplicate deliveries. Partner contract tests fail.

## Run
```bash
cd 09-webhook-delivery
python3 test_webhooks.py
```

## Hints
- Recompute signature against fixtures/payload.json
- Trace retry + timeout in logs/dispatcher.log
- Confirm DLQ on permanent failure

## Planned bug themes
signature generation bug, retry duplication, bad timeout handling, wrong payload format, DLQ not used

## Success criteria
The tests pass and the behavior matches the scenario.

## Stuck?
Open PR `solution/09-webhook-delivery` → **Files changed** (when published). Do not merge that PR.

## Status
Scaffold only — buggy `app.py` and rich fixtures/logs still to be authored.
