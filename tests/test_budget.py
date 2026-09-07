"""Tests for the budget store and helpers."""

import sqlite3

import pytest

from features import budget, purchases


@pytest.fixture
def db_path(tmp_path):
    """Each test gets its own temporary database file."""
    path = tmp_path / "test_budget.db"
    purchases.create_tables(str(path))
    budget.create_tables(str(path))
    return str(path)


def test_set_and_get_budget(db_path):
    budget.set_budget(10000, db_path=db_path)  # $100.00
    saved = budget.get_budget(db_path=db_path)

    assert saved is not None
    assert saved["type"] == "weekly"
    assert saved["limit"] == 10000


def test_setting_new_budget_overwrites_old_one(db_path):
    budget.set_budget(10000, db_path=db_path)
    budget.set_budget(20000, db_path=db_path)

    saved = budget.get_budget(db_path=db_path)
    assert saved["limit"] == 20000

    # Still exactly one row — one budget at a time.
    connection = sqlite3.connect(db_path)
    count = connection.execute("SELECT COUNT(*) FROM budgets").fetchone()[0]
    connection.close()
    assert count == 1


def test_get_budget_returns_none_when_unset(db_path):
    assert budget.get_budget(db_path=db_path) is None


def test_budgets_table_matches_schema(db_path):
    budget.set_budget(10000, db_path=db_path)
    connection = sqlite3.connect(db_path)
    row = connection.execute(
        "SELECT id, type, \"limit\" FROM budgets LIMIT 1"
    ).fetchone()
    connection.close()
    assert tuple(row) == (1, "weekly", 10000)
