"""
Regression tests for the debug exercise.

Run from repo root:
  python3 -m debug.test_detector

Compares debug.detector output to reference/expected_phase3.json and prints
a focused diff so you can hunt bugs one symptom at a time.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from debug.detector import flag_suspicious_events  # noqa: E402


def _load() -> tuple[list, list]:
    events = json.loads((ROOT / "events.json").read_text())
    expected = json.loads((ROOT / "reference" / "expected_phase3.json").read_text())
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

    print(f"Checked {len(expected)} events against reference/expected_phase3.json\n")

    if not failures:
        print("All checks passed. Nice debugging.")
        return 0

    # Group by symptom family for a friendlier hunt
    print(f"{len(failures)} failure(s):\n")
    for line in failures:
        print(f"  • {line}")

    print("\nHints (no spoilers):")
    print("  1. Pick ONE failing event_id and open it in events.json.")
    print("  2. Manually apply the rules from DEBUG.md — what should fire?")
    print("  3. Add a temporary print for that event inside the detector.")
    print("  4. Fix one bug, re-run. Don't boil the ocean.")
    print("\nWhen stuck, see debug/BUGS.md (spoilers).")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
