"""
Regression tests for 06-background-jobs.

Run from this directory:
  python3 test_jobs.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from app import run  # noqa: E402


def _load() -> tuple[dict, dict]:
    seed = json.loads((HERE / "fixtures" / "seed_config.json").read_text())
    scenario = json.loads((HERE / "fixtures" / "expected_scenario.json").read_text())
    return seed, scenario


def _compare_value(name: str, field: str, actual: object, expected: object) -> list[str]:
    failures: list[str] = []
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            failures.append(f"{name}: {field}={actual!r} (expected object {expected!r})")
            return failures
        for sub, want in expected.items():
            failures.extend(_compare_value(name, f"{field}.{sub}", actual.get(sub), want))
        return failures
    if actual != expected:
        failures.append(f"{name}: {field}={actual!r} (expected {expected!r})")
    return failures


def compare_step(name: str, actual: dict, expect: dict) -> list[str]:
    failures: list[str] = []
    for field, expected in expect.items():
        failures.extend(_compare_value(name, field, actual.get(field), expected))
    return failures


def main() -> int:
    seed, scenario = _load()
    max_attempts = int(scenario.get("max_attempts", seed.get("max_attempts", 3)))

    run({"action": "reset", "max_attempts": max_attempts})

    failures: list[str] = []
    print(f"Running {len(scenario['steps'])} scenario steps "
          f"(max_attempts={max_attempts})\n")

    for step in scenario["steps"]:
        name = step["name"]
        actual = run(step["action"])
        step_failures = compare_step(name, actual, step.get("expect", {}))
        if step_failures:
            failures.extend(step_failures)
            print(f"  ✗ {name}")
            for line in step_failures:
                print(f"      {line}")
        else:
            print(f"  ✓ {name}")

    print()
    if not failures:
        print("All checks passed. Nice debugging.")
        return 0

    print(f"{len(failures)} failure(s).\n")
    print("Hints (no spoilers):")
    print("  1. After a successful handle, is the job acked (done) or still inflight?")
    print("  2. A second tick must not resend the same digest.")
    print("  3. After max_attempts transient failures, does the job land in the DLQ?")
    print("  4. Unexpected worker crashes must not leave the job stuck inflight.")
    print("\nStuck? Open PR solution/06-background-jobs → Files changed.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
