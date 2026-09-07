# Phase 1: Walking Skeleton — Feature Specification

## Overview

This is the first feature of Budget Basket, per ROADMAP.md Phase 1. It builds
the thinnest end-to-end slice of the app: a user can record a grocery purchase
and see it appear in a list, along with the total amount spent so far.

## Scope (In)

- A web form to record a purchase: item name, amount, and category.
- A page that lists every recorded purchase.
- A display of the total amount spent across all purchases.
- Purchases persist to a SQLite database (via `sqlite3`).
- Comprehensive logging, kept separate from business logic (decorator style).

## Scope (Out / Non-Goals for this feature)

- No budgets (Phase 2).
- No trips or week/month organization (Phase 3).
- No way to edit or delete a purchase (not required by Phase 1).
- No user accounts/auth (project non-goal).

## Context & Decisions

- **Money is stored as integer cents.** The form accepts dollars (e.g.
  `3.99`); a single shared helper converts dollars→cents on save and
  cents→dollars for display (see SPECS/TECH.md "Money").
- **SQLite is the persistence layer.** Use Python's built-in `sqlite3` module.
  No ORMs, no other file formats (see SPECS/TECH.md "Storage").
- **Schema:** use the `purchases` table exactly as recorded in
  SPECS/TECH.md "Database Schema".
- **Dates:** `date` is stored as `YYYY-MM-DD`. For Phase 1 the date defaults to
  today; "today" is passed into the function as an input so tests are stable
  (see SPECS/TECH.md "Dates").

## Architecture Notes

- Business logic and logging are separated. Logging is applied via a
  decorator so the purchase logic stays clean.
- The feature lives in its own file (`features/purchases.py`) per the project
  structure in SPECS/TECH.md.
- Keep the solution simple, elegant, and general; avoid arbitrary choices.
