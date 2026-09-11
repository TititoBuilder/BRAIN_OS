---
tags: [gig_tracker, codebase]
---

# Codebase Map

Root: `C:\Dev\Projects\gig_tracker\gig_tracker\`

## CLI Tools

| File | Purpose |
|---|---|
| `gig.py` | Primary CLI — ~~24 commands~~ **42 commands (verified 2026-09-11, `grep -c "^@cli.command" gig.py`)** covering runs, costs, Prop 22, reports, and balance |
| `preflight.py` | Morning health check — verifies DB integrity, flags missing data, confirms the day is ready |
| ~~`balance.py`~~ | ~~Quick card balance update: `python balance.py <last4> <amount>` (added Aug 13, 2026)~~ **DEAD 2026-09-11 — does not exist in the repo. Verified absent, not just unreferenced. Not deleted here, only marked; see Corrections at the bottom.** |

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

## Corrections — append-only, don't rewrite this section

**2026-09-11.** `gig.py`'s command count (24 -> 42) and `delivery_runs`'
row count (67 -> 688, a 10x gap) were both verified wrong, not just
stale, during a gig_tracker vault audit. `balance.py` was checked
against the live repo and does not exist — marked dead rather than
silently removed, since two other notes ([[00 Gig Tracker MOC]],
[[Daily Operating Procedure]]) reference it too and this file isn't the
only record. Evidence: direct verification against
`C:\Dev\Projects\gig_tracker\gig_tracker` on 2026-09-11 (`grep -c`,
`sqlite3` row counts, filesystem check).

## Database

~~| Table | Rows (Aug 13, 2026) | Contents |~~
~~|---|---|---|~~
~~| `daily_costs` | 929 | All card statement transactions |~~
~~| `delivery_runs` | 67 | Individual gig runs with engaged time and miles |~~
~~| `cards` | 7 | Card metadata including `due_day` column |~~

**CORRECTED 2026-09-11 — `delivery_runs` was off by 10x, not just
stale.** Verified directly against the live DB:

| Table | Rows (2026-09-11, verified) | Contents |
|---|---|---|
| `daily_costs` | 938 | All card statement transactions |
| `delivery_runs` | **688** (was listed 67 — a 10x gap, not normal drift) | Individual gig runs with engaged time and miles |
| `cards` | 7 (count unchanged; 2 of the 7 have new identities — see [[Financial Position]]) | Card metadata including `due_day` column |

Row counts will drift again immediately — this table is not being kept
live here. For current counts: `python preflight.py` in the repo prints
both, or query the DB directly.
