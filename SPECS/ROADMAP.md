# Roadmap

## Current State

Phase 1 (walking skeleton) is implemented: a user can record a purchase with
an item name, amount, and category, see all purchases in a list, and see the
total spent. Purchases persist in a SQLite database. See
`SPECS/2026-09-07-phase1-walking-skeleton/` for the feature spec.

## Phase 1: Walking Skeleton (First Feature)

Build the thinnest end-to-end slice — a user can record a purchase and see it in a list.

**Includes:**
- A simple form to enter a purchase (item name, amount, category)
- Display the list of all purchases on the page
- Show the total amount spent

## Phase 2: Budgets

Let users set a spending limit and track how much is left.

**Includes:**
- A form to set a weekly budget (monthly added later if it stays simple)
- Display remaining budget on the page
- Visual feedback when spending approaches (over 80%) or exceeds the budget

## Phase 3: Organization

Help users sort and filter their purchases.

**Includes:**
- Organize purchases by week, month, or trip
- Filter or view purchases by date range
- Clean, easy-to-read display

## Long-Term Vision

Further down the road, we could add:
- Charts or graphs showing spending over time
- Category breakdowns (e.g. how much on produce vs. snacks)
- Multiple budgets for different purposes (e.g. weekly vs. monthly)
