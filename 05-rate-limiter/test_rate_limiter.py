"""
Regression tests for 05-rate-limiter.

Run from this directory:
  python3 test_rate_limiter.py
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


def compare_step(name: str, actual: dict, expect: dict) -> list[str]:
    failures: list[str] = []
    for field, expected in expect.items():
        if actual.get(field) != expected:
            failures.append(
                f"{name}: {field}={actual.get(field)!r} (expected {expected!r})"
            )
    return failures


def main() -> int:
    seed, scenario = _load()
    limit = int(scenario.get("limit", seed.get("limit", 3)))
    window = float(scenario.get("window_seconds", seed.get("window_seconds", 60)))

    run({"action": "reset", "limit": limit, "window_seconds": window})

    failures: list[str] = []
    print(f"Running {len(scenario['steps'])} scenario steps "
          f"(limit={limit}, window={window}s)\n")

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
    print("  1. Does the Nth request under the limit get 200 or 429?")
    print("  2. After Alice is saturated, can Bob still get through?")
    print("  3. At exactly window_seconds later, has the oldest hit aged out?")
    print("  4. Compare store keys in logs/gateway.log — per-user or shared?")
    print("\nStuck? Open PR solution/05-rate-limiter → Files changed.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
