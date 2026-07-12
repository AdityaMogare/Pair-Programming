# Fixtures for 02-telemetry-pipeline

| File | Role |
|------|------|
| `ingest_payload.json` | Multi-agent shipper POST body (`nodes[].lines`) |
| `raw_lines.jsonl` | Same lines flattened for eyeballing |
| `expected_events.json` | Clean events + parse errors after a correct run |
