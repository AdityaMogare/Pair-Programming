#!/usr/bin/env python3
"""Drive the fixture scenario and print worker decisions (possibly buggy)."""

from __future__ import annotations

import json
from pathlib import Path

from app import run

HERE = Path(__file__).resolve().parent


def main() -> None:
    seed = json.loads((HERE / "fixtures" / "seed_config.json").read_text())
    scenario = json.loads((HERE / "fixtures" / "expected_scenario.json").read_text())
    max_attempts = int(scenario.get("max_attempts", seed.get("max_attempts", 3)))

    run({"action": "reset", "max_attempts": max_attempts})
    print(f"Reset max_attempts={max_attempts}\n")

    for step in scenario["steps"]:
        name = step["name"]
        actual = run(step["action"])
        action = step["action"].get("action")

        if action == "enqueue":
            print(f"{name}: enqueued {step['action'].get('job_id')} stats={actual.get('stats')}")
            continue

        if action == "sent":
            print(f"{name}: sent_count={actual.get('sent_count')}")
            continue

        print(
            f"{name}: ok={actual.get('ok')} processed={actual.get('processed')} "
            f"job={actual.get('job_id')} action={actual.get('action')!r} "
            f"sent={actual.get('sent_count')} stats={actual.get('stats')}"
        )


if __name__ == "__main__":
    main()
