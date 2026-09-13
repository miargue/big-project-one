"""Helpers that organize and summarize purchases.

These functions work on plain lists of purchase dictionaries that come from
features.purchases. They do no database work themselves — the store stays the
only place that talks to SQLite — which keeps this logic simple to test.
"""


def filter_purchases(purchases, start_date, end_date, trip=""):
    """Return purchases dated between ``start_date`` and ``end_date``.

    Both dates are included. When ``trip`` is a non-empty label, only
    purchases from that trip are kept. ISO dates ("YYYY-MM-DD") compare in
    the right order as plain strings, so no date parsing is needed here.
    """
    result = []
    for purchase in purchases:
        if start_date <= purchase["date"] <= end_date:
            if trip == "" or purchase["trip"] == trip:
                result.append(purchase)
    return result


def unique_trips(purchases):
    """Return the sorted list of distinct, non-empty trip labels."""
    return sorted({purchase["trip"] for purchase in purchases if purchase["trip"]})


def summarize(purchases):
    """Return summary statistics for a list of purchases.

    Money stays in integer cents here (SPECS/TECH.md "Money"); the route
    converts to dollars for display with the single shared money helper.
    """
    count = len(purchases)
    total_cents = sum(purchase["amount"] for purchase in purchases)
    average_cents = int(round(total_cents / count)) if count else 0
    return {
        "count": count,
        "total_cents": total_cents,
        "average_cents": average_cents,
    }