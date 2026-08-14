---
tags: [gig_tracker, codebase]
---

# Codebase Map

Root: `C:\Dev\Projects\gig_tracker\gig_tracker\`

## CLI Tools

| File | Purpose |
|---|---|
| `gig.py` | Primary CLI — 24 commands covering runs, costs, Prop 22, reports, and balance |
| `preflight.py` | Morning health check — verifies DB integrity, flags missing data, confirms the day is ready |
| `balance.py` | Quick card balance update: `python balance.py <last4> <amount>` (added Aug 13, 2026) |

## Web

| File | Purpose |
|---|---|
| `web.py` | Flask dashboard — visual summary of runs, costs, Prop 22 progress, card balances |

## Tracker Module

| File | Purpose |
|---|---|
| `prop22.py` | Prop 22 floor formula, mode detection (HOURS/CASH), adjustment calculation |
| `db.py` | Database layer — SQLite connection, schema, CRUD operations |

## Importers

| File | Purpose |
|---|---|
| `import_statement_v2.py` | Statement importer with 5 card profiles: `amex`, `wells_fargo`, `capital_one`, `capital_one_en`, `citi` |

Replaced three separate importers with one multi-profile script. See [[Decision Log]] for context.

## Auditors

| File | Purpose |
|---|---|
| `calibrate_miles.py` | Derives engaged mi/hr baseline from paid periods; current baseline 15.1 mi/hr (provisional) |

## Configuration

| File | Purpose |
|---|---|
| `van_config.json` | Van purchase target dates (realistic: 2026-09-23, optimistic: 2026-08-26) |

Dates externalized from hardcoded script values — see [[Decision Log]].

## Archive / One-Time Scripts

Legacy importers and exploratory scripts that were superseded or run once. Do not reference for active use.

## Database

| Table | Rows (Aug 13, 2026) | Contents |
|---|---|---|
| `daily_costs` | 929 | All card statement transactions |
| `delivery_runs` | 67 | Individual gig runs with engaged time and miles |
| `cards` | 7 | Card metadata including `due_day` column |
