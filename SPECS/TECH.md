# Tech Stack & Standards

## Languages & Frameworks

- **Backend:** Python with Flask
- **Frontend:** Vanilla HTML, CSS, and JavaScript (no frameworks or libraries)
- **Storage:** SQLite database (via Python's built-in `sqlite3` module)

## Project Structure

Separate files for separate features. Each feature gets its own file so the code stays organized and easy to find.

```
app.py                  # main Flask server (routes)
features/
    purchases.py        # recording and listing purchases (SQLite store)
    budget.py           # setting and tracking budgets
    money.py            # shared dollars <-> cents helper (the only conversion point)
    logging.py          # @logged decorator, keeps logging out of business logic
static/
    style.css           # all styles
templates/
    index.html          # main page
tests/                  # pytest tests (one file per feature)
requirements.txt        # Flask, pytest
```

## Engineering Standards

These are the rules we follow to keep the code clean and simple:

### Spec-Driven Development
Every feature starts with a written plan (requirements, how to build it, how to test it). Code always ties back to an approved plan.

### Test-Driven Development (TDD)
Write a small test first, watch it fail, then write just enough code to make it pass. Repeat.

### DRY (Don't Repeat Yourself)
If you find yourself writing the same thing twice, pull it into a shared function or variable instead.

### Simple and Clear Names
Use straightforward, consistent names for variables, functions, and files. Avoid abbreviations unless they're obvious.

### Simplicity Over Complexity
Pick the simplest solution that works. Avoid clever tricks — clear code beats fancy code every time.

## Locked-in Design Decisions

These decisions are fixed and all code must follow them:

### Money
- Store all money as **integer cents**, never dollars as floats (floats cause
  rounding errors like `0.1 + 0.2 != 0.3`).
- Money crosses the app boundary in cents only. The web form accepts dollars
  (e.g. `3.99`), and a **single shared helper** converts dollars↔cents (DRY —
  the conversion happens in exactly one place).

### Dates
- A **"week" runs Monday through Sunday** so grouping is consistent.
- **"Today's date" is passed into functions as an input**, not read from the
  clock inside them. This lets tests control what "today" is, so date-based
  tests are stable.

### Trips
- A **"trip" is a label the user types in** (e.g. "Weekly Shop"), not something
  the app computes. It's just text on a purchase.

### Budgets
- **"Approaching budget" means spending over 80% of the limit.**
- Build **weekly** budgets first; add **monthly** only if it stays simple.
- **One budget at a time** — `type` is weekly or monthly; `limit` stays set
  until the user changes it.
- **Reset style:** the budget period is derived from today's date, not stored.
  For weekly, the period is the Mon–Sun week containing today; for monthly,
  the calendar month. "How much is left" =
  `limit` − `SUM(amount)` of purchases in the current period, computed fresh
  each time. The limit persists across periods; only "spent so far" resets.
  Because the period is derived from the clock, the `budgets` table needs no
  start date column.

## Database Schema

This is the single source of truth for the database schema. The
feature-specification skill reads this when producing requirements.

```
Table: purchases
- id:       INTEGER PRIMARY KEY AUTOINCREMENT
- item:     TEXT      # the name of the item bought (e.g. Milk)
- amount:   INTEGER   # cost in CENTS, not dollars (e.g. 399 = $3.99)
- category: TEXT      # the kind of item (e.g. Dairy, Produce)
- date:     TEXT      # when it was bought (YYYY-MM-DD)
- trip:     TEXT      # which shopping trip it belongs to (e.g. Weekly Shop)

Table: budgets
- id:    INTEGER PRIMARY KEY AUTOINCREMENT
- type:  TEXT     # "weekly" or "monthly" (one budget at a time)
- limit: INTEGER  # the spending limit in CENTS (e.g. 10000 = $100.00)
```

## Roadmap Priority

Built in this order: Phase 1 (record + list purchases), then Phase 2 (budgets,
weekly first), then Phase 3 (organization).
