"""Tests for the week-bound and month-bound date helpers."""

from features.dates import month_bounds, week_bounds


def test_monday_starts_its_own_week():
    assert week_bounds("2026-09-07") == ("2026-09-07", "2026-09-13")


def test_midweek_returns_previous_monday_as_start():
    # Thursday 2026-09-10 belongs to the week starting Mon 2026-09-07.
    assert week_bounds("2026-09-10") == ("2026-09-07", "2026-09-13")


def test_sunday_is_the_end_of_its_week():
    assert week_bounds("2026-09-13") == ("2026-09-07", "2026-09-13")


def test_week_rolls_over_after_sunday():
    # Sunday 2026-09-06 ends the previous week (starting Mon 2026-08-31).
    assert week_bounds("2026-09-06") == ("2026-08-31", "2026-09-06")


def test_month_bounds_start_and_end():
    assert month_bounds("2026-09-10") == ("2026-09-01", "2026-09-30")


def test_month_bounds_first_day():
    assert month_bounds("2026-09-01") == ("2026-09-01", "2026-09-30")


def test_month_bounds_december_rolls_over_year():
    assert month_bounds("2026-12-15") == ("2026-12-01", "2026-12-31")


def test_month_bounds_leap_year_february():
    assert month_bounds("2028-02-10") == ("2028-02-01", "2028-02-29")
