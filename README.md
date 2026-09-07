# Budget Basket

A grocery spending tracker for students, families, and anyone trying to manage their grocery budget.

Record your purchases, set a spending limit, and see exactly how much you've spent and how much you have left — organized by week, month, or trip.

## Tech Stack

- **Backend:** Python with Flask
- **Frontend:** Vanilla HTML, CSS, and JavaScript
- **Storage:** SQLite database

## Getting Started

_(Setup steps to be added once the project has code.)_

## Project Documentation

- **[SPECS/MISSION.md](SPECS/MISSION.md)** — the project's purpose, values, and non-negotiables
- **[SPECS/TECH.md](SPECS/TECH.md)** — the technology stack and engineering standards
- **[SPECS/ROADMAP.md](SPECS/ROADMAP.md)** — where the project is now and where it's headed
- **[design.md](design.md)** — the original brainstorm and design notes

## Roadmap Overview

- **Phase 1:** Record a purchase and see it in a list
- **Phase 2:** Set a budget and track how much is left (weekly first)
- **Phase 3:** Organize purchases by week, month, or trip

## Key Design Decisions

- Money is stored as **integer cents** (never float dollars) — see [SPECS/TECH.md](SPECS/TECH.md)
- A "week" runs **Monday to Sunday**
- "Trip" is **user-typed text**, not auto-computed
- "Approaching budget" means **over 80%** of the limit
