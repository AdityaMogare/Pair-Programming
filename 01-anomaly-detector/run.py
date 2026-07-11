#!/usr/bin/env python3
"""Print currently flagged events from the (possibly buggy) detector."""

import json
from pathlib import Path

from app import flag_suspicious_events

HERE = Path(__file__).resolve().parent


def main() -> None:
    events = json.loads((HERE / "fixtures" / "events.json").read_text())
    results = flag_suspicious_events(events)
    suspicious = [r for r in results if r.get("suspicious")]

    print(f"Scanned {len(events)} events — {len(suspicious)} suspicious\n")
    for r in sorted(suspicious, key=lambda x: (-x.get("severity", 0), x["event_id"])):
        reasons = ", ".join(r.get("reasons", []))
        print(f"  {r['event_id']}  severity={r.get('severity', '?')}  [{reasons}]")


if __name__ == "__main__":
    main()
