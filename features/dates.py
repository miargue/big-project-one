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


def month_bounds(today):
    """Return the (start, end) of the calendar month containing ``today``.

    ``today`` is a date string like ``"2026-09-10"``. The result is a pair
    of date strings, e.g. ``("2026-09-01", "2026-09-30")``.
    """
    current = datetime.strptime(today, "%Y-%m-%d").date()
    start = current.replace(day=1)
    # "start" always has day 1, so replacing only the month gives the first
    # day of the next month even when "today" is, say, the 10th.
    if start.month == 12:
        next_month = start.replace(year=start.year + 1, month=1)
    else:
        next_month = start.replace(month=start.month + 1)
    end = next_month - timedelta(days=1)
    return start.isoformat(), end.isoformat()
