# Phase 1: Walking Skeleton — Plan

Red/Green TDD: write a failing test first (red), then the minimal code to make
it pass (green), refactor as needed. Run tests after each step.

## Task Group 1: Project Setup

- [ ] 1.1 Create a virtual environment and a `requirements.txt` with Flask.
- [ ] 1.2 Create the minimal Flask app structure per SPECS/TECH.md:
      `app.py`, `features/`, `templates/`, `static/`, and a `tests/` folder.
- [ ] 1.3 Set up a test runner (pytest) so `tests/` can run.
- [ ] 1.4 Check: run an empty/placeholder test to confirm the runner works.

## Task Group 2: Money Helper (DRY)

- [ ] 2.1 Write a failing test for a `dollars_to_cents` helper
      (`3.99` → `399`), and for `cents_to_dollars` (`399` → `"3.99"`).
- [ ] 2.2 Implement the helpers in a single shared module.
- [ ] 2.3 Check: run the tests until green. Keep the helper in one place.

## Task Group 3: Database / Purchases Store + Logging

- [ ] 3.1 Write a failing test that adds a purchase (item, amount-cents,
      category, date) and retrieves it back.
- [ ] 3.2 Implement the `purchases` table creation and an insert/list store in
      `features/purchases.py`, using `sqlite3`.
- [ ] 3.3 Add a logging decorator and apply it to the purchase functions,
      keeping logging out of the business logic.
- [ ] 3.4 Write a failing test that asks for the **total amount spent** across
      all purchases.
- [ ] 3.5 Implement the total calculation.
- [ ] 3.6 Check: run all tests until green.

## Task Group 4: Web Layer (Flask routes + template)

- [ ] 4.1 Write a failing test for a route that displays the list of purchases
      with the total.
- [ ] 4.2 Write a failing test for a route that accepts a submitted purchase
      (item, amount, category) and saves it.
- [ ] 4.3 Implement the routes in `app.py`, wiring them to the store.
- [ ] 4.4 Create `templates/index.html` with a form (item, amount, category)
      and a list showing all purchases plus the total.
- [ ] 4.5 Check: run all tests until green.

## Task Group 5: Sanity & Cleanup

- [ ] 5.1 Run the full test suite once more; all green.
- [ ] 5.2 Confirm no linting/test issues; resolve anything that fails.
- [ ] 5.3 Start the server (bound to `0.0.0.0`, port 3000) and confirm the
      page loads through the Codio public URL (see AGENTS.md).
- [ ] 5.4 Review the implementation against these specs and the constitution;
      note any differences for the validation step.
