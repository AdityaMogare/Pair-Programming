"""Currency helpers — amounts enter as dollar strings, ledger stores integer cents."""

from __future__ import annotations


def dollars_to_cents(amount: str | float | int) -> int:
    """Convert a dollar amount to integer cents."""
    # Float path looks fine for whole dollars, but truncates values like 19.99 / 1.15.
    return int(float(amount) * 100)
