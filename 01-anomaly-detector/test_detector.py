"""
Regression tests for 01-anomaly-detector.

Run from this directory:
  python3 test_detector.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from app import flag_suspicious_events  # noqa: E402


def _load() -> tuple[list, list]:
    events = json.loads((HERE / "fixtures" / "events.json").read_text())
    expected = json.loads((HERE / "fixtures" / "expected.json").read_text())
    return events, expected


def _reason_set(item: dict) -> set[str]:
    return set(item.get("reasons", []))


def compare(actual: list, expected: list) -> list[str]:
    failures: list[str] = []

    if len(actual) != len(expected):
        failures.append(
            f"length mismatch: got {len(actual)} results, expected {len(expected)}"
        )
        return failures

    for got, want in zip(actual, expected):
        eid = want["event_id"]
        if got.get("event_id") != eid:
            failures.append(f"{eid}: event_id mismatch ({got.get('event_id')!r})")
            continue

        if got.get("suspicious") != want["suspicious"]:
            failures.append(
                f"{eid}: suspicious={got.get('suspicious')} "
                f"(expected {want['suspicious']})"
            )

        if _reason_set(got) != _reason_set(want):
            missing = _reason_set(want) - _reason_set(got)
            extra = _reason_set(got) - _reason_set(want)
            parts = []
            if missing:
                parts.append(f"missing {sorted(missing)}")
            if extra:
                parts.append(f"extra {sorted(extra)}")
            failures.append(f"{eid}: reasons {'; '.join(parts)}")

        if got.get("severity") != want["severity"]:
            failures.append(
                f"{eid}: severity={got.get('severity')} "
                f"(expected {want['severity']})"
            )

    return failures


def main() -> int:
    events, expected = _load()
    actual = flag_suspicious_events(events)
    failures = compare(actual, expected)

    print(f"Checked {len(expected)} events against fixtures/expected.json\n")

    if not failures:
        print("All checks passed. Nice debugging.")
        return 0

    print(f"{len(failures)} failure(s):\n")
    for line in failures:
        print(f"  • {line}")

    print("\nHints (no spoilers):")
    print("  1. Pick ONE failing event_id and open it in fixtures/events.json.")
    print("  2. Check logs/ for the same event_id around the failure window.")
    print("  3. Manually apply the rules from README.md — what should fire?")
    print("  4. Fix one bug in app.py, re-run. Don't boil the ocean.")
    print("\nStuck? Open PR solution/01-anomaly-detector → Files changed.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
