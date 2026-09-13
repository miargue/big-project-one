"""Tests for the Phase 3 organization feature (period, trip, date range).

"Today" is passed into the app as a fixed date so every test is stable and
never depends on the real clock (SPECS/TECH.md "Dates").
"""

import pytest

from app import create_app
from features import purchases

# A fixed "today" (a Thursday) so the current week and current month differ.
FIXED_TODAY = "2026-09-10"


@pytest.fixture
def db_path(tmp_path):
    """A temporary database path shared by the app and the store."""
    return str(tmp_path / "org_web_test.db")


@pytest.fixture
def client(db_path):
    """A test client backed by a temporary database and a fixed today."""
    app = create_app(db_path, today=FIXED_TODAY)
    app.config["TESTING"] = True
    return app.test_client()


def seed_purchases(db_path):
    """Four purchases with different dates and trips for list/stat tests.

    - Milk and Bread are in the current week (2026-09-10/11), both "Weekly Shop".
    - Soda is in the same month but a different (earlier) week — it shows in
      the month view but not the week view.
    - Chips is in October, outside both the current week and month.
    """
    purchases.add_purchase(
        "Milk", 399, "Dairy", "2026-09-10", trip="Weekly Shop", db_path=db_path
    )
    purchases.add_purchase(
        "Bread", 125, "Bakery", "2026-09-11", trip="Weekly Shop", db_path=db_path
    )
    purchases.add_purchase(
        "Soda", 250, "Drinks", "2026-09-05", trip="Corner Store", db_path=db_path
    )
    purchases.add_purchase(
        "Chips", 150, "Snacks", "2026-10-02", trip="Corner Store", db_path=db_path
    )


# --- Task Group 1: organization panel on the index page --------------------

def test_index_has_organization_panel(client):
    page = client.get("/")
    assert b"Organize purchases" in page.data


def test_period_defaults_to_current_week(client):
    page = client.get("/")
    # FIXED_TODAY is a Thursday; its Mon-Sun week is 2026-09-07..2026-09-13.
    assert b"This week: 2026-09-07 to 2026-09-13" in page.data
    # The "week" radio button is selected by default.
    assert b'value="week" checked' in page.data


def test_period_toggles_to_current_month(client):
    page = client.get("/?period=month")
    assert b"This month: 2026-09-01 to 2026-09-30" in page.data
    assert b'value="month" checked' in page.data


def test_purchase_list_updates_with_period(client, db_path):
    seed_purchases(db_path)

    week_page = client.get("/")
    assert b"Milk" in week_page.data
    assert b"Bread" in week_page.data
    assert b"Soda" not in week_page.data
    assert b"Chips" not in week_page.data

    month_page = client.get("/?period=month")
    assert b"Milk" in month_page.data
    assert b"Bread" in month_page.data
    assert b"Soda" in month_page.data
    assert b"Chips" not in month_page.data


def test_trip_dropdown_lists_each_unique_trip_once(client, db_path):
    seed_purchases(db_path)
    html = client.get("/").data.decode()

    # Each distinct trip label appears once, as a dropdown option.
    assert html.count('value="Weekly Shop"') == 1
    assert html.count('value="Corner Store"') == 1
    # "All trips" plus the two unique trips.
    assert html.count("<option") == 3


def test_trip_filter_shows_only_that_trip(client, db_path):
    seed_purchases(db_path)

    weekly_page = client.get("/?trip=Weekly+Shop")
    assert b"Milk" in weekly_page.data
    assert b"Bread" in weekly_page.data
    assert b"Soda" not in weekly_page.data

    # Soda is the only "Corner Store" purchase inside the current month;
    # Chips is also "Corner Store" but in October, outside the month.
    corner_page = client.get("/?period=month&trip=Corner+Store")
    assert b"Soda" in corner_page.data
    assert b"Chips" not in corner_page.data
    assert b"Milk" not in corner_page.data


def test_summary_stats_update_with_period(client, db_path):
    seed_purchases(db_path)

    week_page = client.get("/")
    assert b"2 purchases" in week_page.data
    assert b"Spent: $5.24" in week_page.data

    month_page = client.get("/?period=month")
    assert b"3 purchases" in month_page.data
    assert b"Spent: $7.74" in month_page.data


def test_average_is_total_divided_by_count(client, db_path):
    seed_purchases(db_path)
    # $7.74 total across 3 purchases = $2.58 each.
    page = client.get("/?period=month")
    assert b"Average: $2.58" in page.data


def test_add_purchase_can_save_a_trip(client):
    response = client.post(
        "/add",
        data={"item": "Eggs", "amount": "2.50", "category": "Dairy",
              "trip": "Corner Store"},
    )
    assert response.status_code == 302

    page = client.get("/")
    # Eggs has today's date, so it shows in the current week.
    assert b"Eggs" in page.data
    # And its trip label appears in the dropdown.
    assert b"Corner Store" in page.data


# --- Task Group 2: date range filter ---------------------------------------

def test_date_range_filters_purchase_list(client, db_path):
    seed_purchases(db_path)
    page = client.get(
        "/?period=custom&start_date=2026-09-01&end_date=2026-09-30"
    )
    assert b"Milk" in page.data
    assert b"Bread" in page.data
    assert b"Soda" in page.data
    assert b"Chips" not in page.data
    assert b"Custom range: 2026-09-01 to 2026-09-30" in page.data


def test_date_range_echoes_input_values(client, db_path):
    seed_purchases(db_path)
    page = client.get(
        "/?period=custom&start_date=2026-09-10&end_date=2026-09-10"
    )
    assert b'value="2026-09-10"' in page.data


def test_date_range_updates_stats(client, db_path):
    seed_purchases(db_path)
    # Only Milk falls on 2026-09-10: 1 purchase, $3.99.
    page = client.get(
        "/?period=custom&start_date=2026-09-10&end_date=2026-09-10"
    )
    assert b"1 purchase" in page.data
    assert b"Spent: $3.99" in page.data


def test_date_range_can_combine_with_trip(client, db_path):
    seed_purchases(db_path)
    page = client.get(
        "/?period=custom&start_date=2026-09-01&end_date=2026-10-31"
        "&trip=Weekly+Shop"
    )
    assert b"Milk" in page.data
    assert b"Bread" in page.data
    assert b"Soda" not in page.data
    assert b"2 purchases" in page.data
    assert b"Spent: $5.24" in page.data


def test_date_range_without_end_date_uses_period(client, db_path):
    # A lone start date is ignored; the week period still applies.
    seed_purchases(db_path)
    page = client.get("/?period=custom&start_date=2026-09-01")
    assert b"This week: 2026-09-07 to 2026-09-13" in page.data
    assert b"Milk" in page.data
    assert b"Soda" not in page.data


def test_period_radio_beats_stale_dates(client, db_path):
    # Leftover dates in the form must NOT silently override the period radio:
    # choosing "This week" (or "This month") always wins (PR review B1).
    seed_purchases(db_path)
    page = client.get(
        "/?period=week&start_date=2026-09-01&end_date=2026-09-30"
    )
    assert b"This week: 2026-09-07 to 2026-09-13" in page.data
    assert b'Soda' not in page.data  # outside the week, despite the old dates

    month_page = client.get(
        "/?period=month&start_date=2026-09-01&end_date=2026-09-30"
    )
    assert b"This month: 2026-09-01 to 2026-09-30" in month_page.data
    assert b"Soda" in month_page.data


def test_custom_radio_is_selected_in_custom_mode(client):
    page = client.get("/?period=custom&start_date=2026-09-01&end_date=2026-09-30")
    assert b'value="custom" checked' in page.data