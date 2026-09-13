# Phase 3: Organization — Validation

This feature is done and can be merged when **all** of the following are true.

## Functional Checks

- [ ] The index page lets the user choose a period: the current Monday–Sunday
      week or the current calendar month.
- [ ] The purchase list and summary statistics update when the period changes.
- [ ] A trip dropdown lists each distinct trip label from the purchases table,
      and selecting one shows only purchases from that trip.
- [ ] The user can enter a start date and an end date, and the purchase list
      and statistics reflect only purchases in that range.
- [ ] Summary statistics (total spent, purchase count) match the filtered set
      of purchases.
- [ ] The organization feature adds no new database tables or columns; the
      existing `purchases` table (with its `trip` column) is reused.

## Test Checks (Red/Green TDD)

- [ ] A failing test preceded each implementation step.
- [ ] The full test suite passes (`pytest` is green) with no skipped/warning
      workarounds.
- [ ] Period bounds and filtering logic are covered by stable tests using a
      passed-in "today" (no clock dependence).

## Standards & Constitution Checks

- [ ] Logging applied via the `@logged` decorator, separate from business
      logic.
- [ ] Money stored as integer cents; conversions only through the single
      shared helper.
- [ ] Week = Monday–Sunday and month = calendar month, per SPECS/TECH.md.
- [ ] No legacy URLs/code are kept for backward compatibility's sake; the
      index page evolved in place.
- [ ] Only `sqlite3` is used; no ORMs or other storage formats.
- [ ] The server runs bound to `0.0.0.0` on a valid port and the page loads
      through the Codio public URL (AGENTS.md).

## Spec Reconciliation

- [ ] The implementation is compared against these feature specs and the
      constitution. Any differences found are surfaced to the user.
- [ ] On the user's approval, the specs (feature specs and/or constitution)
      are updated to match the implementation before merging.

## Merge

- [ ] All of the above are satisfied and the user has approved merging the
      `feature/phase3-organization` branch.