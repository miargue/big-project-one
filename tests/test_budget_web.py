"""Tests for the budget web layer (form + panel)."""

import pytest

from app import create_app

# A fixed "today" (a Monday) so the current week is deterministic in tests.
FIXED_TODAY = "2026-09-07"


@pytest.fixture
def client(tmp_path):
    """A test client backed by a temporary database and a fixed today."""
    db_path = tmp_path / "budget_web_test.db"
    app = create_app(str(db_path), today=FIXED_TODAY)
    app.config["TESTING"] = True
    return app.test_client()


def test_set_budget_stores_it(client):
    response = client.post("/budget", data={"limit": "100.00"})
    assert response.status_code == 302

    page = client.get("/")
    assert b"Weekly budget" in page.data
    assert b"$100.00" in page.data


def test_index_shows_limit_spent_and_remaining(client):
    client.post("/budget", data={"limit": "100.00"})
    # One purchase in the current week: $10.00
    client.post("/add", data={"item": "Milk", "amount": "10.00", "category": "Dairy"})

    page = client.get("/")
    assert b"$100.00" in page.data  # limit
    assert b"$10.00" in page.data   # spent this week
    assert b"$90.00" in page.data   # remaining


def test_panel_warns_when_approaching_budget(client):
    # 80% of $100.00 is $80.00 — $81.00 is over 80%.
    client.post("/budget", data={"limit": "100.00"})
    client.post("/add", data={"item": "Milk", "amount": "81.00", "category": "Dairy"})

    page = client.get("/")
    assert b"Approaching budget" in page.data


def test_panel_shows_over_budget_amount(client):
    client.post("/budget", data={"limit": "100.00"})
    client.post("/add", data={"item": "Milk", "amount": "120.00", "category": "Dairy"})

    page = client.get("/")
    assert b"Over budget by $20.00" in page.data


def test_panel_prompts_when_no_budget_set(client):
    page = client.get("/")
    assert b"No budget set yet" in page.data


def test_spent_counts_only_current_week(client, tmp_path):
    """A purchase from a previous week must not count toward this week."""
    client.post("/budget", data={"limit": "100.00"})
    client.post("/add", data={"item": "Milk", "amount": "10.00", "category": "Dairy"})
    client.post("/add", data={"item": "Old", "amount": "50.00", "category": "Old"})

    # Fix the "Old" purchase's date to the previous Sunday directly in the app.
    from datetime import datetime, timedelta

    previous_sunday = (
        datetime.strptime(FIXED_TODAY, "%Y-%m-%d") - timedelta(days=1)
    ).date().isoformat()

    # Update the newest purchase to the previous week via the store.
    import sqlite3

    connection = sqlite3.connect(tmp_path / "budget_web_test.db")
    connection.execute(
        "UPDATE purchases SET date = ? WHERE item = 'Old'",
        (previous_sunday,),
    )
    connection.commit()
    connection.close()

    page = client.get("/")
    assert b"$10.00" in page.data  # spent, not $60.00
    assert b"$90.00" in page.data  # remaining, not $40.00
