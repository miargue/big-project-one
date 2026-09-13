# Budget Basket

*Track your grocery spending, stay on budget, and know where your money goes.*

Budget Basket is a simple web app that records your grocery purchases, shows you exactly how much you've spent, and warns you before you blow past your weekly limit.

## The Problem

Groceries are dozens of small purchases that quietly add up. By the end of the month it's hard to remember where the money went — the receipts pile up, the bank app only shows a lump sum, and "I'll check my budget later" turns into never. Most people skip budgeting because it feels like too much paperwork for a few items of food.

## The Solution

Budget Basket turns budgeting into a two-second habit: type the item, hit save. The app keeps a running list of everything you've bought, tells you what you've spent this week, and gives you a clear heads-up when you're getting close to your limit — all in one page, no spreadsheet required.

## Main Features

- **Record a purchase** — enter the item, amount (in dollars), category, an optional trip label (e.g. "Weekly Shop"), and it's saved instantly.
- **Track a weekly budget** — set a spending limit and see how much is spent and how much is left.
- **Get budget warnings** — the app flags you at 80% ("approaching budget") and tells you exactly how much you're over when you exceed the limit.
- **Filter purchases** — view spending by the current Monday–Sunday week, calendar month, a custom date range, or a specific trip.
- **See summary statistics** — the total spent, purchase count, and average per purchase for whatever you're looking at.

## Tech Stack & Architecture

- **Frontend:** Vanilla HTML, CSS, and a tiny bit of server-rendered templating — no frameworks, no build steps.
- **Backend:** Python with Flask, split into small single-purpose modules under `features/` (purchases, budgets, money, dates, organization).
- **Database:** SQLite via Python's built-in `sqlite3` module — one local file, no server to install.

## Database Design

The app runs on two tables:

```
purchases   (id, item, amount, category, date, trip)
budgets     (id, type, limit)
```

Money is stored as **integer cents** (e.g. `399` for $3.99) to avoid floating-point rounding errors, and converted to dollars in exactly one shared helper.

The database answers questions like:
- How much have I spent in total, this week, or this month?
- What did I buy on this shopping trip?
- What's my budget limit, and how much is left?
- How much did I spend between any two dates?

## What I Learned

Building this taught me how much a little structure pays off. The early temptation was to just spin up the app and start coding, but writing the plan down first (mission, tech standards, a roadmap) made every later step calmer — when a decision came up, the answer was already written somewhere.

The two habits that made the biggest difference were **testing first** and **keeping money off floats**. Writing a failing test before the code sounds backwards, but it forces you to think about what "done" means, and it saved me more than once when a change broke something old. And storing everything as integer cents felt fussy on day one, but it meant I never chased a weird `0.1 + 0.2` bug that so many money apps hit.

I also worked alongside AI assistants a lot on this project. The lesson there was that they're great at execution but you still have to be the one making decisions - the AI would happily build something clever, and my job was keeping things simple, readable, and true to the plan. A spec is only useful if you treat it as a contract, not a suggestion.
