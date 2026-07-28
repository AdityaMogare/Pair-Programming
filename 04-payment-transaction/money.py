"""Currency helpers — amounts enter as dollar strings, ledger stores integer cents."""

from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP


def dollars_to_cents(amount: str | float | int) -> int:
    """Convert a dollar amount to integer cents using exact decimal math."""
    return int(
        (Decimal(str(amount)) * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    )
