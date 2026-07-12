"""Shipper-side logging helpers for parse / transform diagnostics."""

from __future__ import annotations

from typing import Any


_PARSE_ERRORS: list[dict[str, Any]] = []


def reset() -> None:
    _PARSE_ERRORS.clear()


def record_parse_error(node_id: str, line: str, reason: str) -> None:
    _PARSE_ERRORS.append(
        {
            "node_id": node_id,
            "line": line,
            "reason": reason,
        }
    )


def get_parse_errors() -> list[dict[str, Any]]:
    return list(_PARSE_ERRORS)
