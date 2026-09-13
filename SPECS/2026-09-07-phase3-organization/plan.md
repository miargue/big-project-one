# Phase 3: Organization — Plan

Red/Green TDD: write a failing test first (red), then the minimal code to make
it pass (green), refactor as needed. Run tests after each step.

## Task Group 1: Organization UI on Index Page

- [ ] 1.1 Write failing tests in `tests/test_organization.py`:
      - The index page (`GET /`) includes the organization panel section.
      - The period selector defaults to the current Monday–Sunday week.
      - Users can toggle between "Week" and "Month" views.
      - The purchase list updates when the period changes.
      - The trip dropdown is populated with unique trip labels from the database.
      - The summary statistics (total spent, purchase count) update when the period changes.
- [ ] 1.2 Implement the organization panel in `app.py`:
      - Add `period` parameter (default: week) to the `index()` route.
      - Compute `week_bounds(today)` and `month_bounds(today)` using `features.dates`.
      - Compute filtered purchase lists for week and month.
      - Compute summary statistics for the current period.
      - Pass `period`, `trip_filter`, `purchases`, `stats` to the template.
- [ ] 1.3 Add the organization panel HTML to `templates/index.html`:
      - Period selector (Week/Month toggle).
      - Trip dropdown (populated from database).
      - Purchase list filtered by current period and trip.
      - Summary statistics display.
- [ ] 1.4 Check: run the tests until green.

## Task Group 2: Date Range Filter

- [ ] 2.1 Write failing tests for date range filtering:
      - Users can enter a start date and end date.
      - The purchase list updates to show only purchases within that range.
      - Summary statistics update accordingly.
- [ ] 2.2 Implement date range filter in `app.py`:
      - Add `start_date` and `end_date` parameters to the `index()` route.
      - Parse dates from request args or form POST.
      - Call `purchases.total_spent_between(start, end, db_path)`.
      - Update the template with filtered results.
- [ ] 2.2 Add date range inputs to `templates/index.html`:
      - Start date input field.
      - End date input field.
      - "Apply filter" button.
- [ ] 2.3 Check: run all tests until green.

## Task Group 3: Specification & Cleanup

- [ ] 3.1 Run the full test suite; all green.
- [ ] 3.2 Compare the implementation against these feature specs and the constitution;
      note any differences for the validation step.
- [ ] 3.3 Update SPECS/ROADMAP.md current state to reflect Phase 3 completion.
- [ ] 3.4 On the user's approval, update any constitution or spec files to match
      the implementation before merging.