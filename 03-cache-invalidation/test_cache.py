"""
Regression tests for 03-cache-invalidation.

Run from this directory:
  python3 test_cache.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from app import run  # noqa: E402


def _load() -> tuple[dict, dict]:
    seed = json.loads((HERE / "fixtures" / "seed_users.json").read_text())
    scenario = json.loads((HERE / "fixtures" / "expected_scenario.json").read_text())
    return seed, scenario


def _compare_profile(got: dict | None, want: dict, step: str) -> list[str]:
    failures: list[str] = []
    if got is None:
        failures.append(f"{step}: missing profile object")
        return failures
    for field, expected in want.items():
        if got.get(field) != expected:
            failures.append(
                f"{step}: profile.{field}={got.get(field)!r} (expected {expected!r})"
            )
    return failures


def compare_step(name: str, actual: dict, expect: dict) -> list[str]:
    failures: list[str] = []

    if "ok" in expect and actual.get("ok") != expect["ok"]:
        failures.append(f"{name}: ok={actual.get('ok')!r} (expected {expect['ok']!r})")

    if "source" in expect and actual.get("source") != expect["source"]:
        failures.append(
            f"{name}: source={actual.get('source')!r} (expected {expect['source']!r})"
        )

    if "profile" in expect:
        failures.extend(_compare_profile(actual.get("profile"), expect["profile"], name))

    return failures


def main() -> int:
    seed, scenario = _load()
    ttl = int(scenario.get("ttl_seconds", seed.get("ttl_seconds", 60)))

    run({"action": "reset", "users": seed["users"], "ttl_seconds": ttl})

    failures: list[str] = []
    print(f"Running {len(scenario['steps'])} scenario steps (ttl={ttl}s)\n")

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
    print("  1. After PATCH, does the next GET still say source=cache?")
    print("  2. Compare the DEL key in logs/redis.log to the GET cache key.")
    print("  3. On TTL expiry: is the entry gone before the value is returned?")
    print("  4. Trace API → service → cache → repository → db.")
    print("\nStuck? Open PR solution/03-cache-invalidation → Files changed.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
