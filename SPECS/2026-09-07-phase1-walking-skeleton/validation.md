# Phase 1: Walking Skeleton — Validation

This feature is done and can be merged when **all** of the following are true.

## Functional Checks

- [ ] A user can submit a purchase with an item name, amount (in dollars), and
      category, and it is saved to the SQLite `purchases` table.
- [ ] The saved purchase appears in the list of all purchases on the page.
- [ ] The page shows the correct total amount spent across all purchases
      (e.g. $3.99 + $1.25 = $5.24).
- [ ] Money is stored as integer cents in the database (verified by checking a
      stored row's `amount` is `399`, not `3.99`).
- [ ] Purchases persist across a server restart (data comes from SQLite, not
      in-memory lists).

## Test Checks (Red/Green TDD)

- [ ] A failing test preceded each implementation step (the repo followed
      spec-driven, Red/Green TDD).
- [ ] The full test suite passes (`pytest` is green) with no skipped/warning
      workarounds.

## Standards & Constitution Checks

- [ ] Logging is applied via a decorator and is kept separate from the
      purchase business logic (SPECS/TECH.md "Logging").
- [ ] A single shared money helper handles dollars↔cents (DRY, SPECS/TECH.md).
- [ ] The `purchases` table matches the schema in SPECS/TECH.md exactly.
- [ ] No ORMs, no other storage formats; only `sqlite3` (constitution rule).
- [ ] The server runs bound to `0.0.0.0` on a valid port and the page loads
      through the Codio public URL (AGENTS.md).

## Spec Reconciliation

- [ ] The implementation is compared against these feature specs and the
      constitution. Any differences found are surfaced to the user.
- [ ] On the user's approval, the specs (feature specs and/or constitution)
      are updated to match the implementation before merging.

## Merge

- [ ] All of the above are satisfied and the user has approved merging the
      `feature/phase1-walking-skeleton` branch.
