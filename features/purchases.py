"""Store for purchases, backed by SQLite.

The purchases table matches the schema in SPECS/TECH.md exactly.
All money values are stored as integer cents.
"""

import sqlite3

from features.logging import logged

# Where the database file lives. Tests pass their own path instead.
DATABASE_PATH = "budget_basket.db"

# Keeps the table exactly as written in SPECS/TECH.md "Database Schema".
CREATE_PURCHASES_TABLE = """
CREATE TABLE IF NOT EXISTS purchases (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    item     TEXT    NOT NULL,
    amount   INTEGER NOT NULL,
    category TEXT    NOT NULL,
    date     TEXT    NOT NULL,
    trip     TEXT    NOT NULL DEFAULT ''
)
"""


def get_connection(db_path=DATABASE_PATH):
    """Open a connection. Rows come back as dictionaries for easy reading."""
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection


def create_tables(db_path=DATABASE_PATH):
    """Create the purchases table if it does not exist yet."""
    with get_connection(db_path) as connection:
        connection.execute(CREATE_PURCHASES_TABLE)


@logged
def add_purchase(item, amount_cents, category, date, trip="", db_path=DATABASE_PATH):
    """Save one purchase and return its id. Amount must be integer cents."""
    connection = get_connection(db_path)
    try:
        with connection:
            cursor = connection.execute(
                "INSERT INTO purchases (item, amount, category, date, trip) "
                "VALUES (?, ?, ?, ?, ?)",
                (item, amount_cents, category, date, trip),
            )
            return cursor.lastrowid
    finally:
        connection.close()


@logged
def list_purchases(db_path=DATABASE_PATH):
    """Return every purchase as a list of dictionaries, oldest first."""
    connection = get_connection(db_path)
    try:
        rows = connection.execute(
            "SELECT id, item, amount, category, date, trip "
            "FROM purchases ORDER BY id"
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        connection.close()


@logged
def total_spent_cents(db_path=DATABASE_PATH):
    """Return the total amount spent across all purchases, in cents."""
    connection = get_connection(db_path)
    try:
        row = connection.execute(
            "SELECT COALESCE(SUM(amount), 0) AS total FROM purchases"
        ).fetchone()
        return row["total"]
    finally:
        connection.close()


@logged
def total_spent_between(start, end, db_path=DATABASE_PATH):
    """Return the total spent between two dates (both included), in cents."""
    connection = get_connection(db_path)
    try:
        row = connection.execute(
            "SELECT COALESCE(SUM(amount), 0) AS total "
            "FROM purchases WHERE date BETWEEN ? AND ?",
            (start, end),
        ).fetchone()
        return row["total"]
    finally:
        connection.close()
