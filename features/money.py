"""Shared helper for converting between dollars and cents.

Money is always stored as integer cents (never float dollars) to avoid
rounding errors like 0.1 + 0.2 != 0.3. This module is the ONLY place
where dollars <-> cents conversion happens (DRY).
"""


def dollars_to_cents(dollars):
    """Convert a dollar amount (string or number) to integer cents.

    >>> dollars_to_cents("3.99")
    399
    """
    return round(float(dollars) * 100)


def cents_to_dollars(cents):
    """Convert integer cents to a dollar string with two decimals.

    >>> cents_to_dollars(399)
    '3.99'
    """
    return f"{cents / 100:.2f}"