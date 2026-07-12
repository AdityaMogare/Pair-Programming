"""Parse raw log lines into JSON objects."""

from __future__ import annotations

import json
from typing import Any


def parse_line(line: str) -> dict[str, Any] | None:
    """Return a dict for valid JSON objects; None for blank or unusable lines."""
    text = line.strip()
    if not text:
        return None
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return None

    if not isinstance(payload, dict):
        return None
    return payload
