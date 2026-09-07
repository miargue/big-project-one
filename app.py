"""Budget Basket — main Flask application.

Run with:  python app.py
Current feature set: record a purchase, list purchases, show the total,
and track a weekly budget.
"""

import os
from datetime import date

from flask import Flask, redirect, render_template, request, url_for

from features import budget, purchases
from features.dates import week_bounds
from features.money import cents_to_dollars, dollars_to_cents

PORT = int(os.environ.get("PORT", 3000))


def create_app(db_path=None, today=None):
    """Build the Flask app. Tests pass a temporary db_path and a fixed today."""
    if db_path is None:
        db_path = purchases.DATABASE_PATH
    if today is None:
        today = date.today().isoformat()

    app = Flask(__name__)
    purchases.create_tables(db_path)
    budget.create_tables(db_path)

    def week_spent_cents():
        """Total spent in the Monday-Sunday week containing 'today'."""
        week_start, week_end = week_bounds(today)
        return purchases.total_spent_between(week_start, week_end, db_path=db_path)

    @app.route("/", methods=["GET"])
    def index():
        all_purchases = purchases.list_purchases(db_path=db_path)
        total_cents = purchases.total_spent_cents(db_path=db_path)

        # Convert cents to dollar strings once, here, for display (DRY).
        for entry in all_purchases:
            entry["amount_dollars"] = cents_to_dollars(entry["amount"])

        # Budget panel data (None if no budget is set).
        current_budget = budget.get_budget(db_path=db_path)
        panel = None
        if current_budget is not None:
            spent = week_spent_cents()
            remaining = budget.remaining_cents(current_budget["limit"], spent)
            panel = {
                "limit_dollars": cents_to_dollars(current_budget["limit"]),
                "spent_dollars": cents_to_dollars(spent),
                "remaining_dollars": cents_to_dollars(remaining),
                "status": budget.budget_status(current_budget["limit"], spent),
                "over_dollars": cents_to_dollars(spent - current_budget["limit"])
                if spent > current_budget["limit"]
                else None,
            }

        return render_template(
            "index.html",
            purchases=all_purchases,
            total_dollars=cents_to_dollars(total_cents),
            panel=panel,
        )

    @app.route("/add", methods=["POST"])
    def add():
        item = request.form.get("item", "").strip()
        category = request.form.get("category", "").strip()
        amount_cents = dollars_to_cents(request.form.get("amount", "0"))
        # "Today" is passed into the store function as a plain input
        # (SPECS/TECH.md "Dates").
        purchases.add_purchase(
            item=item,
            amount_cents=amount_cents,
            category=category,
            date=today,
            db_path=db_path,
        )
        return redirect(url_for("index"))

    @app.route("/budget", methods=["POST"])
    def set_budget():
        limit_cents = dollars_to_cents(request.form.get("limit", "0"))
        budget.set_budget(limit_cents, db_path=db_path)
        return redirect(url_for("index"))

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
