# Telemetry pipeline

**Level 2** · Structured logging and pipeline transforms

## Scenario
On-call got paged: dashboards show gaps after the log shipper upgrade. Downstream analytics is missing fields and double-counting some events.

## Expected behavior
Ingest raw log lines, parse JSON payloads, normalize timestamps to UTC, map severity, and emit one clean event per input without duplicates.

## Broken behavior
Tests fail on dropped fields, bad timestamp parsing, severity mapping, and duplicate ingestion.

## Run
```bash
cd 02-telemetry-pipeline
python3 test_pipeline.py
```

## Hints
- Compare fixtures/raw_lines.jsonl to fixtures/expected_events.json
- Check logs/shipper.log for parse errors
- Inspect timestamp and severity transforms in app.py

## Planned bug themes
dropped fields, wrong timestamp parsing, malformed JSON handling, duplicate event ingestion, incorrect severity mapping

## Success criteria
The tests pass and the behavior matches the scenario.

## Stuck?
Open PR `solution/02-telemetry-pipeline` → **Files changed** (when published). Do not merge that PR.

## Status
Scaffold only — buggy `app.py` and rich fixtures/logs still to be authored.
