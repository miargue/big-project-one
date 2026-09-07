"""Tests for spending-between-dates and the pure budget status helpers."""

import pytest

from features import budget, purchases


@pytest.fixture
def db_path(tmp_path):
    """Each test gets its own temporary database file."""
    path = tmp_path / "test_status.db"
    purchases.create_tables(str(path))
    return str(path)


def test_total_spent_between_only_counts_dates_in_range(db_path):
    purchases.add_purchase("Milk", 399, "Dairy", "2026-09-07", db_path=db_path)
    purchases.add_purchase("Bread", 125, "Bakery", "2026-09-10", db_path=db_path)
    # Outside the week Mon 2026-09-07 .. Sun 2026-09-13:
    purchases.add_purchase("Water", 50, "Drinks", "2026-09-06", db_path=db_path)
    purchases.add_purchase("Juice", 200, "Drinks", "2026-09-14", db_path=db_path)

    assert (
        purchases.total_spent_between("2026-09-07", "2026-09-13", db_path=db_path)
        == 524
    )


def test_total_spent_between_returns_zero_for_empty_range(db_path):
    assert (
        purchases.total_spent_between("2026-09-07", "2026-09-13", db_path=db_path)
        == 0
    )


def test_remaining_cents_can_go_negative():
    assert budget.remaining_cents(10000, 4000) == 6000
    assert budget.remaining_cents(10000, 10000) == 0
    assert budget.remaining_cents(10000, 12000) == -2000


def test_budget_status_ok_under_80_percent():
    # 80% of $100.00 is $80.00 (8000 cents). $70.00 is under it.
    assert budget.budget_status(10000, 7000) == "ok"
    # Exactly 80% is still okay (not "over 80%").
    assert budget.budget_status(10000, 8000) == "ok"


def test_budget_status_approaching_over_80_percent():
    # $81.00 is over 80% of $100.00 but not over $100.00.
    assert budget.budget_status(10000, 8100) == "approaching"
    # Exactly at the limit is not "over", so still approaching.
    assert budget.budget_status(10000, 10000) == "approaching"


def test_budget_status_over_100_percent():
    assert budget.budget_status(10000, 12000) == "over"
