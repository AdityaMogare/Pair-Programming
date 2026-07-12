#!/usr/bin/env python3
"""Print pipeline output for the fixture ingest payload (possibly buggy)."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from app import run

HERE = Path(__file__).resolve().parent


def main() -> None:
    payload = json.loads((HERE / "fixtures" / "ingest_payload.json").read_text())
    result = run(payload)
    events = result.get("events", [])
    errors = result.get("errors", [])

    print(f"Emitted {len(events)} events, {len(errors)} parse error(s)\n")

    counts = Counter(e.get("event_id") for e in events)
    dupes = {k: v for k, v in counts.items() if v > 1}
    if dupes:
        print("Duplicates:")
        for eid, n in sorted(dupes.items()):
            print(f"  {eid} x{n}")
        print()

    print("Events:")
    for e in events:
        print(
            f"  {e.get('event_id')}  node={e.get('node_id')}  "
            f"sev={e.get('severity')}  ts={e.get('timestamp')}"
        )

    if errors:
        print("\nErrors:")
        for err in errors:
            print(f"  {err.get('node_id')}: {err.get('reason')} — {err.get('line')!r}")


if __name__ == "__main__":
    main()
