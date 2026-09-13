# Phase 3: Organization — Feature Specification

## Overview

This is the third feature of Budget Basket, per ROADMAP.md Phase 3. It helps users
sort, filter, and view their purchases by week, month, or trip, with a clean,
easy-to-read interface.

## Scope (In)

- A filter controls the current time period: **Monday–Sunday week** (constitution default)
  or **calendar month**, determining which purchases are "in the current period."
- **Organize by trip**: The `trip` label on each purchase (user-typed, e.g. "Weekly Shop")
  can be used to group/filter purchases.
- **Filter purchases** by date range: users can enter a start date and end date to
  view purchases within that window.
- A **clean, easy-to-read display** shows purchases matching the current criteria,
  with summary statistics (total spent, purchase count).
- **No automatic "reset"** — the current period is derived from today's date
  (reset style), never stored.
- **One budget at a time** continues from Phase 2; organization is separate from
  budget tracking but uses the same SQLite database.

## Scope (Out / Non-Goals)

- No CSV/PDF export or print-friendly views (out of scope per constitution non-goals).
- No user-defined week start; weeks always start on Monday per constitution.
- No calendar months that are 30-day rolling periods; months are calendar months Jan–Dec.
- No new database tables or columns beyond what's already in SPECS/TECH.md.
- No user authentication or multi-user features (constitution non-goal).

## Context & Decisions

- **Money is always stored as integer cents** — conversions via the single shared helper
  in `features/money.py` (DRY; see SPECS/TECH.md "Money").
- **Week definition**: the current period is the Mon–Sun week containing today (SPECS/TECH.md "Dates").
  The week's start and end dates should be computed by a shared, testable helper
  in `features/dates.py` (already existing from Phase 2; Phase 3 reuses it).
- **"Today" is passed in**: the current period is always computed from a date passed
  into functions as an input, never read from the clock inside them. This lets tests
  control what "today" is, so organization tests are stable.
- **Trip is user-typed text** — from Phase 1, each purchase has a `trip` column
  (e.g. "Weekly Shop"). Phase 3 adds filtering and grouping by this field.
- **Organization reuses existing store**: Phase 2's `purchases.total_spent_between()`
  remains the single shared store function for date-range totals (used by the
  budget panel). The organization filters instead work on the in-memory list
  returned by `purchases.list_purchases()` via `organization.filter_purchases()`;
  this is simpler and lets the summary statistics (which must also respect the
  trip filter and include an average) always match the exact rows being shown.
  No new store is needed.
- **Pure status/helpers** from Phase 2 (`budget_status`, `remaining_cents`) are not
  reused here — organization is display/filtering, not budget tracking.
- **Backward compatibility**: the index page evolves in place to add organization
  filters; the existing `/` and `/add` routes keep their behavior. No legacy URLs
  are preserved intentionally — no old code is kept for compatibility's sake.
- The app's "Add a purchase" form includes a **Trip** text input so users can
  type a trip label (SPECS/TECH.md "Trips") — without it the trip dropdown and
  filter would always be empty (the `trip` column existed since Phase 1, but
  the earlier forms never captured it). This is a small, documented extension,
  not a legacy-compatibility shim.

## Architecture Notes

- Organization feature lives in `features/organization.py` per SPECS/TECH.md structure.
- Week/reusable helpers live in `features/dates.py` (already existing from Phase 2).
- **Filter by date range** is a filter over the in-memory purchase list
  (`organization.filter_purchases()`); it combines with the trip filter so the
  list and stats always agree.
- Filter UI lives on the index page alongside the budget panel and purchase form.
- Keep it simple, elegant, and general; no clever tricks.

## Display Components

- **Period selector**: a control (dropdown or date pickers) that sets the current
  period (week or month). When changed, the purchase list and statistics update.
- **Purchase list**: only purchases whose `date` falls within the current period
  (or match the filtered trip) are shown.
- **Summary statistics**: total spent, purchase count, average per purchase.
- **Trip filter**: a dropdown of all unique trip labels from the purchase table,
  allowing users to show only purchases from a specific trip.