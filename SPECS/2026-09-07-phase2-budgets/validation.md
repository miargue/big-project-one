# Phase 2: Weekly Budgets — Validation

This feature is done and can be merged when **all** of the following are true.

## Functional Checks

- [ ] Setting a weekly budget stores the limit as integer cents in the
      `budgets` table.
- [ ] The index page shows the budget limit, how much is spent in the current
      Monday–Sunday week, and how much is left.
- [ ] Spending over 80% of the limit shows the "approaching budget" warning.
- [ ] Spending over 100% shows how much the user is over budget.
- [ ] With no budget set, the page prompts the user to set one.
- [ ] Setting a new budget replaces the old one (one budget at a time).
- [ ] "Spent" and "left" only count purchases in the current week (reset
      style — the limit persists across weeks).

## Test Checks (Red/Green TDD)

- [ ] A failing test preceded each implementation step.
- [ ] The full test suite passes (`pytest` is green) with no skipped/warning
      workarounds.
- [ ] Week-bound, status, and remaining logic are covered by stable tests
      using a passed-in "today" (no clock dependence).

## Standards & Constitution Checks

- [ ] Logging applied via the `@logged` decorator, separate from business
      logic.
- [ ] Money stored as integer cents; conversions only through the single
      shared helper.
- [ ] The `budgets` table matches SPECS/TECH.md exactly (`id`, `type`,
      `limit`) with `type = "weekly"`.
- [ ] No `start_date` column was added (reset style is derived from today).
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
      `feature/phase2-budgets` branch.