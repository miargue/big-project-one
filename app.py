"""Budget Basket — main Flask application.

Run with:  python app.py
Serves the walking skeleton: record a purchase, see the list, see the total.
"""

import os
from datetime import date

from flask import Flask, redirect, render_template, request, url_for

from features import purchases
from features.money import cents_to_dollars, dollars_to_cents

PORT = int(os.environ.get("PORT", 3000))


def create_app(db_path=None):
    """Build the Flask app. Tests pass a temporary db_path."""
    if db_path is None:
        db_path = purchases.DATABASE_PATH

    app = Flask(__name__)
    purchases.create_tables(db_path)

    @app.route("/", methods=["GET"])
    def index():
        all_purchases = purchases.list_purchases(db_path=db_path)
        total_cents = purchases.total_spent_cents(db_path=db_path)

        # Convert cents to dollar strings once, here, for display (DRY).
        for entry in all_purchases:
            entry["amount_dollars"] = cents_to_dollars(entry["amount"])

        return render_template(
            "index.html",
            purchases=all_purchases,
            total_dollars=cents_to_dollars(total_cents),
        )

    @app.route("/add", methods=["POST"])
    def add():
        item = request.form.get("item", "").strip()
        category = request.form.get("category", "").strip()
        amount_cents = dollars_to_cents(request.form.get("amount", "0"))
        # "Today" comes from the clock here, and is passed into the store
        # function as a plain input (SPECS/TECH.md "Dates").
        today = date.today().isoformat()
        purchases.add_purchase(
            item=item,
            amount_cents=amount_cents,
            category=category,
            date=today,
            db_path=db_path,
        )
        return redirect(url_for("index"))

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)