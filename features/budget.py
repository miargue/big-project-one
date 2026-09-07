"""Weekly budget store and logic, backed by SQLite.

The budgets table matches the schema in SPECS/TECH.md exactly. There is one
budget at a time — setting a new one overwrites the previous row.
"""

import sqlite3

from features.logging import logged

# Where the database file lives. Tests pass their own path instead.
DATABASE_PATH = "budget_basket.db"

# Keeps the table exactly as written in SPECS/TECH.md "Database Schema".
CREATE_BUDGETS_TABLE = """
CREATE TABLE IF NOT EXISTS budgets (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    type  TEXT    NOT NULL,
    "limit" INTEGER NOT NULL
)
"""


def get_connection(db_path=DATABASE_PATH):
    """Open a connection. Rows come back as dictionaries for easy reading."""
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection


def create_tables(db_path=DATABASE_PATH):
    """Create the budgets table if it does not exist yet."""
    with get_connection(db_path) as connection:
        connection.execute(CREATE_BUDGETS_TABLE)


@logged
def set_budget(limit_cents, db_path=DATABASE_PATH):
    """Save the weekly budget. Overwrites any previous budget (one at a time)."""
    connection = get_connection(db_path)
    try:
        with connection:
            existing = connection.execute(
                "SELECT id FROM budgets LIMIT 1"
            ).fetchone()
            if existing is None:
                cursor = connection.execute(
                    "INSERT INTO budgets (type, \"limit\") VALUES ('weekly', ?)",
                    (limit_cents,),
                )
                return cursor.lastrowid
            connection.execute(
                "UPDATE budgets SET type = 'weekly', \"limit\" = ? WHERE id = ?",
                (limit_cents, existing["id"]),
            )
            return existing["id"]
    finally:
        connection.close()


@logged
def get_budget(db_path=DATABASE_PATH):
    """Return the current budget as a dictionary, or None if none is set."""
    connection = get_connection(db_path)
    try:
        row = connection.execute(
            "SELECT id, type, \"limit\" FROM budgets LIMIT 1"
        ).fetchone()
        return dict(row) if row else None
    finally:
        connection.close()


def remaining_cents(limit_cents, spent_cents):
    """Return how much is left. May be negative when over budget."""
    return limit_cents - spent_cents


def budget_status(limit_cents, spent_cents):
    """Return "ok", "approaching", or "over".

    - "ok": spent at or under 80% of the limit
    - "approaching": spent over 80% but not over 100%
    - "over": spent over 100% of the limit
    """
    if spent_cents > limit_cents:
        return "over"
    if spent_cents > int(limit_cents * 0.8):
        return "approaching"
    return "ok"
