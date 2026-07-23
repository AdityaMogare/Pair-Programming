"""
Telemetry pipeline orchestrator.

Flow:
  raw lines → parser → transform → validator → batched output per node
"""

from __future__ import annotations

from typing import Any

from logger import get_parse_errors, record_parse_error, reset as reset_logger
from parser import parse_line
from transform import transform
from validator import validate


def accumulate_batch(
    node_id: str,
    event: dict[str, Any],
    log_batch: list | None = None,
) -> list[dict[str, Any]]:
    """Append a transformed event into the per-node emit batch."""
    if log_batch is None:
        log_batch = []
    log_batch.append(event)
    return log_batch


def process_node(node_id: str, lines: list[str]) -> list[dict[str, Any]]:
    """Parse / transform / validate one multi-agent node's log lines."""
    batch: list[dict[str, Any]] | None = None

    for line in lines:
        raw = parse_line(line)
        if raw is None:
            # Blank lines are skipped; non-blank failures are malformed JSON.
            if line.strip():
                record_parse_error(node_id, line, "malformed_json")
            continue

        event = transform(raw, node_id)
        problems = validate(event)
        if problems:
            record_parse_error(node_id, line, ",".join(problems))
            continue

        if batch is None:
            batch = accumulate_batch(node_id, event)
        else:
            batch = accumulate_batch(node_id, event, log_batch=batch)

    return list(batch or [])


def run_pipeline(payload: dict[str, Any]) -> dict[str, Any]:
    """Ingest a multi-node shipper payload and emit cleaned events."""
    reset_logger()

    nodes = payload.get("nodes", [])
    events: list[dict[str, Any]] = []

    for node in nodes:
        node_id = node["node_id"]
        lines = node.get("lines", [])
        events.extend(process_node(node_id, lines))

    return {
        "events": events,
        "errors": get_parse_errors(),
    }
