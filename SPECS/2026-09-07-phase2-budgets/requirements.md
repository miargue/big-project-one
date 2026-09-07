# Phase 2: Weekly Budgets — Feature Specification

## Overview

Per ROADMAP.md Phase 2, this feature lets users set a weekly spending limit
and see how much of it is left. The budget panel lives on the main index page
alongside the existing purchase form and list. Weekly only — monthly budgets
are deferred per SPECS/TECH.md ("Build weekly first").

## Scope (In)

- A form to set a weekly budget (dollars input, stored as integer cents).
- A budget panel on the index page showing:
  - the weekly limit,
  - how much has been spent in the current week (Mon–Sun),
  - how much is left.
- **Visual feedback in text:** when spending goes over 80% of the limit, show
  an "approaching budget" warning; when it goes over 100%, show how much the
  user is over budget.
- Setting a new budget **overwrites** the previous one (one budget at a time,
  per SPECS/TECH.md "Budgets").
- Budget persists in SQLite via the `budgets` table (SPECS/TECH.md "Schema").
- Comprehensive logging via the existing `@logged` decorator
  (`features/logging.py`), separate from business logic.

## Scope (Out / Non-Goals)

- No monthly budgets (deferred).
- No trips, or week/month organization of the list (Phase 3).
- No way to clear the budget besides setting a new one.
- No multiple budgets.
- No automatic "reset" write — the period is derived from today's date
  (reset style), never stored.

## Context & Decisions

- **Money:** all values are integer cents, converted to dollars only for
  display via the single shared helper (`features/money.py`, DRY).
- **Week definition:** the current period is the Monday–Sunday week containing
  "today" (SPECS/TECH.md "Dates"). The week's start and end dates should be
  computed by a shared, testable helper.
- **"Today" is passed in:** the week bounds are computed from a date passed
  into functions as an input, never read from the clock inside the store logic,
  so tests are stable. The Flask route reads the clock and passes `today` in.
- **Reset style:** "how much is left" = `limit` − `SUM(amount)` of purchases
  whose `date` is in the current week. Computed fresh on every page load.
- **No `start_date`:** the `budgets` table is exactly as in SPECS/TECH.md —
  `id`, `type`, `limit`. The `type` column is stored as `"weekly"` (monthly
  uses `"monthly"` later). With one budget at a time, the app manages a single
  row.
- **Backward compatibility:** the index page evolves in place to add the
  budget panel; the existing `/` and `/add` routes keep their behavior. No
  legacy URLs are preserved intentionally — no old code is kept for
  compatibility's sake.

## Architecture Notes

- Budget feature lives in `features/budget.py` per SPECS/TECH.md structure.
- Week-bound helpers live in `features/dates.py` (general — Phase 3 will also
  group by week).
- "Spent in the current week" is a purchases question; add it as a
  `total_spent_between` function on the purchases store so features stay
  separated and DRY.
- Status rules are pure, testable functions: over 80% → approaching; over
  100% → over budget.
- Keep it simple, elegant, and general; no clever tricks.