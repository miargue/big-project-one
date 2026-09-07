"""Small date helpers shared across features.

A "week" runs Monday through Sunday (SPECS/TECH.md "Dates"). All helpers
receive the date string they need as an input — they never read the clock —
so tests can control what "today" is.
"""

from datetime import datetime, timedelta


def week_bounds(today):
    """Return the (start, end) of the Mon-Sun week containing ``today``.

    ``today`` is a date string like ``"2026-09-07"``. The result is also a
    pair of date strings, e.g. ``("2026-09-07", "2026-09-13")``.
    """
    current = datetime.strptime(today, "%Y-%m-%d").date()
    start = current - timedelta(days=current.weekday())  # Monday = 0
    end = start + timedelta(days=6)  # Sunday
    return start.isoformat(), end.isoformat()
