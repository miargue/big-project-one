# Phase 2: Weekly Budgets — Plan

Red/Green TDD: write a failing test first (red), then the minimal code to make
it pass (green), refactor as needed. Run tests after each step.

## Task Group 1: Week-bound Date Helper

- [ ] 1.1 Write failing tests for `week_bounds(today)` in
      `features/dates.py`:
      - a Monday input returns that Monday as the start,
      - a mid-week input returns the previous Monday as the start,
      - the end is the Sunday after the start (6 days later).
      Uses dates like `"2026-09-07"` (a Monday).
- [ ] 1.2 Implement `week_bounds`.
- [ ] 1.3 Check: run the tests until green.

## Task Group 2: Budget Store (SQLite)

- [ ] 2.1 Write failing tests in `tests/test_budget.py`:
      - `set_budget` saves a budget and `get_budget` returns it,
      - setting a new budget overwrites the old one (one row, one budget),
      - `get_budget` returns `None` when no budget has been set,
      - the stored row uses the `budgets` table per SPECS/TECH.md.
- [ ] 2.2 Implement `set_budget(limit_cents, db_path)` and
      `get_budget(db_path)` in `features/budget.py`, using `sqlite3` and the
      `@logged` decorator.
- [ ] 2.3 Check: run the tests until green.

## Task Group 3: Spending + Status Logic

- [ ] 3.1 Write a failing test for `total_spent_between(start, end, db_path)`
      on the purchases store: sums amounts with `date` in `[start, end]` only.
- [ ] 3.2 Implement `total_spent_between` in `features/purchases.py`.
- [ ] 3.3 Write failing tests for the pure status helper, e.g.
      `budget_status(limit_cents, spent_cents)` returning
      `"ok"`, `"approaching"` (over 80%), or `"over"` (over 100%).
      Also test a `remaining_cents(limit, spent)` helper that can go negative.
- [ ] 3.4 Run the tests — they fail because the helpers do not exist yet.
- [ ] 3.5 Implement both helpers in `features/budget.py`.
- [ ] 3.6 Check: run all tests until green.

## Task Group 4: Web Layer

- [ ] 4.1 Write failing Flask-route tests:
      - filling the budget form for the first time stores the budget,
      - the index page shows the budget limit and remaining,
      - the panel shows "approaching budget" when spent is over 80%,
      - the panel shows "over budget by $X" when spent is over 100%,
      - with no budget set, the page shows a prompt to set one.
      Tests pass a fixed "today" into the app/route so the current week is
      deterministic.
- [ ] 4.2 Add a `POST /budget` route to `app.py` that reads `limit` (dollars),
      converts via `dollars_to_cents`, and saves via `set_budget`.
- [ ] 4.3 Update the `GET /` route to pass the budget, week-spent, remaining,
      and status into the template.
- [ ] 4.4 Add the budget panel + form to `templates/index.html`.
- [ ] 4.5 Add needed styles to `static/style.css` for the panel states.
- [ ] 4.6 Check: run all tests until green.

## Task Group 5: Sanity & Cleanup

- [ ] 5.1 Run the full test suite; all green.
- [ ] 5.2 Resolve any linting/compile issues.
- [ ] 5.3 Start the server (bound to `0.0.0.0`, port 3000) and confirm the
      page loads through the Codio public URL (see AGENTS.md). Manually set a
      budget and add a purchase.
- [ ] 5.4 Compare the implementation against these specs and the constitution;
      note any differences for the validation step.