#!/usr/bin/env python3
"""Run the buggy detector the same way as the main exercise."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from debug.detector import flag_suspicious_events  # noqa: E402


def main() -> None:
    events = json.loads((ROOT / "events.json").read_text())
    results = flag_suspicious_events(events)
    suspicious = [r for r in results if r.get("suspicious")]

    print(f"Scanned {len(events)} events — {len(suspicious)} suspicious\n")
    for r in sorted(suspicious, key=lambda x: (-x.get("severity", 0), x["event_id"])):
        reasons = ", ".join(r.get("reasons", []))
        print(f"  {r['event_id']}  severity={r.get('severity', '?')}  [{reasons}]")


if __name__ == "__main__":
    main()
