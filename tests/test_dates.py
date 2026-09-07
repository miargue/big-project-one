"""Tests for the week-bound date helper."""

from features.dates import week_bounds


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
