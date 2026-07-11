"""
Tests for 06-background-jobs.

Run from this directory:
  python3 test_jobs.py
"""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from app import run  # noqa: E402


def main() -> int:
    try:
        run({})
    except NotImplementedError as exc:
        print(f"FAIL (expected until exercise is authored): {exc}")
        print("See README.md for the incident scenario and success criteria.")
        return 1
    except Exception as exc:  # noqa: BLE001
        print(f"FAIL: {type(exc).__name__}: {exc}")
        return 1

    print("Unexpected success — scaffold should fail until implemented.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
