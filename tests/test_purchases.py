"""Tests for the purchases store (SQLite-backed)."""

import pytest

from features import purchases


@pytest.fixture
def db_path(tmp_path):
    """Each test gets its own temporary database file."""
    path = tmp_path / "test_purchases.db"
    purchases.create_tables(str(path))
    return str(path)


def test_add_purchase_and_get_it_back(db_path):
    purchase_id = purchases.add_purchase(
        item="Milk",
        amount_cents=399,
        category="Dairy",
        date="2026-09-07",
        db_path=db_path,
    )
    all_purchases = purchases.list_purchases(db_path=db_path)
    assert len(all_purchases) == 1
    got = all_purchases[0]
    assert got["id"] == purchase_id
    assert got["item"] == "Milk"
    assert got["amount"] == 399
    assert got["category"] == "Dairy"
    assert got["date"] == "2026-09-07"


def test_list_purchases_empty_by_default(db_path):
    assert purchases.list_purchases(db_path=db_path) == []


def test_total_spent_cents_sums_all_amounts(db_path):
    purchases.add_purchase("Milk", 399, "Dairy", "2026-09-07", db_path=db_path)
    purchases.add_purchase("Bread", 125, "Bakery", "2026-09-07", db_path=db_path)
    assert purchases.total_spent_cents(db_path=db_path) == 524


def test_total_spent_cents_is_zero_when_no_purchases(db_path):
    assert purchases.total_spent_cents(db_path=db_path) == 0


def test_purchase_persists_across_connections(db_path):
    purchases.add_purchase("Eggs", 250, "Dairy", "2026-09-07", db_path=db_path)
    # A brand-new connection (simulating a restart) still sees the data.
    assert len(purchases.list_purchases(db_path=db_path)) == 1


def test_add_purchase_logs_via_decorator(db_path, caplog):
    with caplog.at_level("INFO"):
        purchases.add_purchase(
            "Milk", 399, "Dairy", "2026-09-07", db_path=db_path
        )
    assert "add_purchase" in caplog.text
