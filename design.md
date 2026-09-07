# Project Brainstorming

## Idea 1: Grocery budget tracker
- **Problem:** People often lose track of how much they spend on groceries.
- **Who experiences this:** Students, families, and people living on a budget.
- **Why it matters:** Tracking spending can help people avoid overspending and plan their weekly budget.

## Idea 2: Pet medication tracker
- **Problem:** Pet owners can forget when they last gave their pet medication or when the next dose is due.
- **Who experiences this:** People who own pets that need regular medication.
- **Why it matters:** Keeping a clear record helps prevent missed or double doses.

## Idea 3: Homework deadline tracker
- **Problem:** Students can forget assignment deadlines when they have multiple subjects and tasks.
- **Who experiences this:** School and university students.
- **Why it matters:** A simple tracker can help students stay organized, prioritize tasks, and submit work on time.

---

## Selected Project
- **App Name:** Budget Basket
- **Target User:** Students, families, and anyone trying to manage their grocery spending.
- **Core Problem:** People often lose track of how much they spend on groceries and may go over their budget.
- **Purpose:** To help users record grocery purchases, track their total spending, and stay within their weekly or monthly budget.

---

## Core Requirements
- Users can record a grocery purchase with an item name, amount, and category
- Users can see all their purchases displayed in a list
- Users can set a weekly or monthly budget
- Users can see how much of their budget is left
- Users can organize purchases by week, month, or trip

---

## Non-Goals
- User Authentication / Multi-user support: No login screens, user accounts, password hashing, or user roles. Assume a single user is using the app locally.
- External Notifications: No email alerts, push notifications, or SMS reminders.
- Mobile Applications: No native iOS or Android apps.
- Complex Frontends & ORMs: No React, Vue, SQLAlchemy, or third-party cloud databases.
- Export / Third-Party Integrations: No PDF exports, Google Calendar syncs, or payment gateways.
- No receipt scanning, barcodes, or price comparisons.

---

## Database Questions

For each core requirement, write the specific question your database must be able to answer to make it work.

- Requirement 1 → What is every purchase (item, amount, category)?
- Requirement 2 → What is the total amount spent across all purchases?
- Requirement 3 → What is the user's budget limit and how much is left?
- Requirement 4 → Which purchases fall within a given week, month, or trip?

---

## Schema

```
Table: purchases
- id:       INTEGER PRIMARY KEY AUTOINCREMENT
- item:     TEXT      # the name of the item bought (e.g. Milk)
- amount:   INTEGER   # cost in CENTS, not dollars (e.g. 399 = $3.99)
- category: TEXT      # the kind of item (e.g. Dairy, Produce)
- date:     TEXT      # when it was bought (YYYY-MM-DD)
- trip:     TEXT      # which shopping trip it belongs to (e.g. Weekly Shop)

Table: budgets
- id:    INTEGER PRIMARY KEY AUTOINCREMENT
- type:  TEXT     # "weekly" or "monthly" (one budget at a time)
- limit: INTEGER  # the spending limit in CENTS (e.g. 10000 = $100.00)
```

