"""Tests for the Flask web layer."""
import pytest

from app import create_app


@pytest.fixture
def client(tmp_path):
    """A test client backed by a temporary database."""
    db_path = tmp_path / "web_test.db"
    app = create_app(str(db_path))
    app.config["TESTING"] = True
    return app.test_client()


def test_index_shows_empty_state_and_zero_total(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"No purchases yet" in response.data
    assert b"$0.00" in response.data


def test_add_purchase_saves_and_shows_in_list(client):
    response = client.post(
        "/add",
        data={"item": "Milk", "amount": "3.99", "category": "Dairy"},
    )
    assert response.status_code == 302

    page = client.get("/")
    assert b"Milk" in page.data
    assert b"Dairy" in page.data
    assert b"3.99" in page.data


def test_total_spent_is_sum_of_all_purchases(client):
    client.post("/add", data={"item": "Milk", "amount": "3.99", "category": "Dairy"})
    client.post("/add", data={"item": "Bread", "amount": "1.25", "category": "Bakery"})

    page = client.get("/")
    assert b"$5.24" in page.data


def test_amounts_are_stored_as_integer_cents(client, tmp_path):
    client.post("/add", data={"item": "Milk", "amount": "3.99", "category": "Dairy"})

    import sqlite3

    connection = sqlite3.connect(tmp_path / "web_test.db")
    amount = connection.execute("SELECT amount FROM purchases").fetchone()[0]
    connection.close()
    assert amount == 399
