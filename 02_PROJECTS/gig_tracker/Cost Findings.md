---
tags: [gig_tracker, spending, analysis]
---

# Cost Findings

Analysis sourced from 929 rows of `daily_costs` imported via [[import_statement_v2.py]].

## Major Spending Leaks

### food_fast — $5,251 across 460 rows (18% of all spending)

The single largest spending category. Fast food and convenience purchases average $11.41 per transaction over 460 rows. This is not a rounding error — it is structural behavior worth addressing directly.

The figure is a **floor**: ATM cash withdrawals (see below) almost certainly contain additional food spending that cannot be categorized.

### Entertainment — $1,580 (stopped)

Three recurring charges identified and cancelled:

| Merchant | Status |
|---|---|
| Mike Topanga | Stopped |
| Level8 | Stopped |
| PP*OGK | Stopped |

No new entertainment charges should appear going forward.

## ATM Withdrawals — The Invisible Leak

ATM withdrawals dominate **checking account outflow** but cannot be categorized. Every spending figure derived from statement imports is a floor. The actual number for any category is likely higher.

Implication: the $5,251 food_fast figure probably understates the real food spending.

## Vehicle Spending — $3,316

Includes **SP PAINT N SHIP $448** — an accident repair, not routine vehicle maintenance. This inflates the vehicle category relative to a normal period. The recurring vehicle baseline without that repair is closer to $2,868.

## Subscriptions — $760 across 55 rows

Subscriptions are now visible after import cleanup. $760 is the identified total; the per-subscription breakdown is in the database. No action flagged yet — visibility is the first step.

## Database Reference

| Table | Rows |
|---|---|
| daily_costs | 929 |
| delivery_runs | 67 |

Categories are assigned at import time by [[import_statement_v2.py]] profile logic. Uncategorized rows land in `other` — 78 rows remain there (rent + storage, intentional).
