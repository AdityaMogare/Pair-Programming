#!/usr/bin/env python3
"""Drive the fixture scenario and print allow / 429 decisions (possibly buggy)."""

from __future__ import annotations

import json
from pathlib import Path

from app import run

HERE = Path(__file__).resolve().parent


def main() -> None:
    seed = json.loads((HERE / "fixtures" / "seed_config.json").read_text())
    scenario = json.loads((HERE / "fixtures" / "expected_scenario.json").read_text())
    limit = int(scenario.get("limit", seed.get("limit", 3)))
    window = float(scenario.get("window_seconds", seed.get("window_seconds", 60)))

    run({"action": "reset", "limit": limit, "window_seconds": window})
    print(f"Reset limit={limit} window={window}s\n")

    for step in scenario["steps"]:
        name = step["name"]
        actual = run(step["action"])
        action = step["action"].get("action")

        if action == "advance":
            print(f"{name}: advance now={actual.get('now')}")
            continue

        print(
            f"{name}: allowed={actual.get('allowed')} status={actual.get('status')} "
            f"user={actual.get('user_id')} count={actual.get('count')} "
            f"remaining={actual.get('remaining')} key={actual.get('key')!r}"
        )

    keys = run({"action": "keys"})
    print(f"\nLive store keys: {keys.get('keys')}")


if __name__ == "__main__":
    main()
