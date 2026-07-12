# 02 — Telemetry pipeline

**Level 2** · Structured logging and pipeline transforms

## Scenario

On-call got paged after the log shipper upgrade: dashboards show gaps, analytics is double-counting events, and severity / timestamps look wrong. Two multi-agent nodes (`agent-east-1`, `agent-west-2`) ship into the same process.

## Pipeline

```text
API (app.py)
  ↓
Parser (parser.py)
  ↓
Transformer (transform.py)
  ↓
Validator (validator.py)
  ↓
Batched output (pipeline.py + logger.py)
```

## Expected behavior

Ingest raw log lines from each node, parse JSON payloads, normalize timestamps to **UTC** (`…Z`), map severity labels, record malformed lines as parse errors, and emit **one clean event per valid input** with the correct `node_id` — no cross-node contamination.

| Input `level` | Output `severity` |
|---------------|-------------------|
| `ERROR` / `ERR` | `error` |
| `WARN` / `WARNING` | `warning` |
| `INFO` | `info` |
| `DEBUG` | `debug` |

Timestamps with offsets (e.g. `-07:00`) must be converted to UTC, not relabeled with a `Z`.

## Broken behavior

Regression tests against `fixtures/expected_events.json` fail: wrong event counts / duplicates across nodes, timestamp skew, severity mismatches, and missing parse errors for malformed JSON.

## Run

```bash
cd 02-telemetry-pipeline
python3 test_pipeline.py
# optional:
python3 run.py
```

## Hints

- Compare `fixtures/raw_lines.jsonl` to `fixtures/expected_events.json`
- Check `logs/shipper.log` for parse errors and the west-node flush count spike
- Inspect timestamp and severity transforms in `transform.py`
- Trace how per-node batches are accumulated in `pipeline.py`

### Probe events

| Event | Why |
|-------|-----|
| `evt_e1` | `WARN` + Pacific offset `-07:00` |
| `evt_w1` / `evt_e3` | Appear on the “wrong” node when batches bleed |
| malformed line in east payload | Should show up under `errors`, not vanish |
| `evt_w2` | `WARNING` (long form) vs `WARN` |

## Success criteria

`python3 test_pipeline.py` exits 0 and matches `fixtures/expected_events.json`.

## Stuck?

Open PR **`solution/02-telemetry-pipeline`** → **Files changed**. Do not merge that PR.
