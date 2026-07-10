#!/usr/bin/env python3
"""Load events.json and print anomaly flags."""

import json
from pathlib import Path

from detector import flag_suspicious_events


def main() -> None:
    events_path = Path(__file__).parent / "events.json"
    events = json.loads(events_path.read_text())

    results = flag_suspicious_events(events)
    suspicious = [r for r in results if r.get("suspicious")]

    print(f"Scanned {len(events)} events — {len(suspicious)} suspicious\n")
    for r in sorted(suspicious, key=lambda x: (-x.get("severity", 0), x["event_id"])):
        reasons = ", ".join(r.get("reasons", []))
        print(f"  {r['event_id']}  severity={r.get('severity', '?')}  [{reasons}]")


if __name__ == "__main__":
    main()
