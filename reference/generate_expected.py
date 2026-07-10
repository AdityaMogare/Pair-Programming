#!/usr/bin/env python3
"""Generate reference/expected_phase3.json for interviewer validation."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from detector import flag_suspicious_events  # noqa: E402


def main() -> None:
    root = Path(__file__).parent.parent
    events = json.loads((root / "events.json").read_text())
    results = flag_suspicious_events(events)
    out = root / "reference" / "expected_phase3.json"
    out.write_text(json.dumps(results, indent=2) + "\n")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
