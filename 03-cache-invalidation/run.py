#!/usr/bin/env python3
"""Drive the fixture scenario and print responses (possibly buggy)."""

from __future__ import annotations

import json
from pathlib import Path

from app import run

HERE = Path(__file__).resolve().parent


def main() -> None:
    seed = json.loads((HERE / "fixtures" / "seed_users.json").read_text())
    scenario = json.loads((HERE / "fixtures" / "expected_scenario.json").read_text())
    ttl = int(scenario.get("ttl_seconds", 60))

    run({"action": "reset", "users": seed["users"], "ttl_seconds": ttl})
    print(f"Reset with {len(seed['users'])} users, ttl={ttl}s\n")

    for step in scenario["steps"]:
        name = step["name"]
        actual = run(step["action"])
        if step["action"].get("action") == "advance":
            print(f"{name}: advance ok now={actual.get('now')}")
            continue

        profile = actual.get("profile") or {}
        print(
            f"{name}: status={actual.get('status')} source={actual.get('source')} "
            f"user={profile.get('user_id')} name={profile.get('display_name')!r}"
        )

    keys = run({"action": "cache_keys"})
    print(f"\nLive cache keys: {keys.get('keys')}")


if __name__ == "__main__":
    main()
