"""
Telemetry pipeline — log shipper ingest API.

Accepts batched raw lines from multi-agent nodes, runs:
  API → Parser → Transformer → Validator → Output

Run: python3 test_pipeline.py
Stuck? Open PR solution/02-telemetry-pipeline → Files changed.
"""

from __future__ import annotations

from typing import Any

from pipeline import run_pipeline


def run(payload: dict[str, Any]) -> dict[str, Any]:
    """Entry point under test — shipper upgrade ingest handler."""
    return run_pipeline(payload)
