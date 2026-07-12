"""
Regression tests for 02-telemetry-pipeline.

Run from this directory:
  python3 test_pipeline.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from app import run  # noqa: E402


def _load() -> tuple[dict, dict]:
    payload = json.loads((HERE / "fixtures" / "ingest_payload.json").read_text())
    expected = json.loads((HERE / "fixtures" / "expected_events.json").read_text())
    return payload, expected


def _by_id(events: list[dict]) -> dict[str, dict]:
    return {e["event_id"]: e for e in events}


def compare(actual: dict, expected: dict) -> list[str]:
    failures: list[str] = []

    got_events = actual.get("events", [])
    want_events = expected["events"]
    got_errors = actual.get("errors", [])
    want_errors = expected["errors"]

    if len(got_events) != len(want_events):
        failures.append(
            f"event count: got {len(got_events)}, expected {len(want_events)} "
            f"(duplicates or cross-node bleed?)"
        )

    want_ids = [e["event_id"] for e in want_events]
    got_ids = [e.get("event_id") for e in got_events]
    for eid in want_ids:
        if got_ids.count(eid) > 1:
            failures.append(f"{eid}: duplicated in output ({got_ids.count(eid)} times)")
        if eid not in got_ids:
            failures.append(f"{eid}: missing from output")

    got_map = _by_id(got_events)
    for want in want_events:
        eid = want["event_id"]
        got = got_map.get(eid)
        if got is None:
            continue

        for field in ("timestamp", "severity", "message", "service", "node_id"):
            if got.get(field) != want[field]:
                failures.append(
                    f"{eid}: {field}={got.get(field)!r} (expected {want[field]!r})"
                )

    # West-node events must not carry east node_id (bleed symptom).
    for got in got_events:
        eid = got.get("event_id", "")
        if eid.startswith("evt_w") and got.get("node_id") != "agent-west-2":
            failures.append(
                f"{eid}: node_id={got.get('node_id')!r} "
                f"(west event contaminated by another node)"
            )
        if eid.startswith("evt_e") and got.get("node_id") != "agent-east-1":
            failures.append(
                f"{eid}: node_id={got.get('node_id')!r} "
                f"(east event contaminated by another node)"
            )

    if len(got_errors) != len(want_errors):
        failures.append(
            f"parse errors: got {len(got_errors)}, expected {len(want_errors)} "
            f"(malformed JSON silently dropped?)"
        )
    else:
        for got_err, want_err in zip(got_errors, want_errors):
            for field in ("node_id", "line", "reason"):
                if got_err.get(field) != want_err[field]:
                    failures.append(
                        f"error.{field}={got_err.get(field)!r} "
                        f"(expected {want_err[field]!r})"
                    )

    return failures


def main() -> int:
    payload, expected = _load()
    actual = run(payload)
    failures = compare(actual, expected)

    print(
        f"Checked {len(expected['events'])} events and "
        f"{len(expected['errors'])} parse error(s) "
        f"against fixtures/expected_events.json\n"
    )

    if not failures:
        print("All checks passed. Nice debugging.")
        return 0

    print(f"{len(failures)} failure(s):\n")
    for line in failures:
        print(f"  • {line}")

    print("\nHints (no spoilers):")
    print("  1. Event count / duplicates → how are per-node batches accumulated?")
    print("  2. timestamp skew → Pacific offsets must become UTC Z.")
    print("  3. severity mismatch on WARN vs WARNING.")
    print("  4. missing parse errors → malformed lines should not vanish silently.")
    print("  5. Compare fixtures/raw_lines.jsonl to logs/shipper.log.")
    print("\nStuck? Open PR solution/02-telemetry-pipeline → Files changed.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
