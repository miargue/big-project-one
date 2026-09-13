"""Budget Basket — main Flask application.

Run with:  python app.py
Current feature set: record a purchase, list purchases, show the total,
track a weekly budget, and organize purchases by week, month, or trip.
"""

import os
from datetime import date

from flask import Flask, redirect, render_template, request, url_for

from features import budget, organization, purchases
from features.dates import month_bounds, week_bounds
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
        # Organization filter inputs (all optional).
        period = request.args.get("period", "week")
        trip_filter = request.args.get("trip", "")
        start_date = request.args.get("start_date", "").strip()
        end_date = request.args.get("end_date", "").strip()

        # The current window for purchases. A custom date range applies only
        # when the user chose "Custom range" AND filled in both dates. The
        # Mon-Sun week or the calendar month (SPECS/TECH.md "Dates") is used
        # otherwise. The period is never stored — it is derived from today.
        if period == "custom" and start_date and end_date:
            period_start, period_end = start_date, end_date
        elif period == "month":
            period = "month"
            start_date = end_date = ""  # don't echo stale dates into the form
            period_start, period_end = month_bounds(today)
        else:
            period = "week"
            start_date = end_date = ""  # don't echo stale dates into the form
            period_start, period_end = week_bounds(today)

        all_purchases = purchases.list_purchases(db_path=db_path)
        visible = organization.filter_purchases(
            all_purchases, period_start, period_end, trip_filter
        )

        # Convert cents to dollar strings once, here, for display (DRY).
        for entry in visible:
            entry["amount_dollars"] = cents_to_dollars(entry["amount"])

        raw_stats = organization.summarize(visible)
        stats = {
            "count": raw_stats["count"],
            "total_dollars": cents_to_dollars(raw_stats["total_cents"]),
            "average_dollars": cents_to_dollars(raw_stats["average_cents"]),
        }
        trips = organization.unique_trips(all_purchases)

        total_cents = purchases.total_spent_cents(db_path=db_path)

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
            purchases=visible,
            total_dollars=cents_to_dollars(total_cents),
            panel=panel,
            period=period,
            period_start=period_start,
            period_end=period_end,
            trip_filter=trip_filter,
            start_date=start_date,
            end_date=end_date,
            trips=trips,
            stats=stats,
        )

    @app.route("/add", methods=["POST"])
    def add():
        item = request.form.get("item", "").strip()
        category = request.form.get("category", "").strip()
        amount_cents = dollars_to_cents(request.form.get("amount", "0"))
        trip = request.form.get("trip", "").strip()
        # "Today" is passed into the store function as a plain input
        # (SPECS/TECH.md "Dates").
        purchases.add_purchase(
            item=item,
            amount_cents=amount_cents,
            category=category,
            date=today,
            trip=trip,
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
