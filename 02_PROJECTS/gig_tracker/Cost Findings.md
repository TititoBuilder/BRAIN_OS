---
tags: [gig_tracker, spending, analysis]
---

# Cost Findings

Analysis sourced from 929 rows of `daily_costs` imported via [[import_statement_v2.py]]
*(as of Aug 13, 2026 — 938 rows as of 2026-09-11; the category totals below
were not re-run against current data, see Corrections at the bottom)*.

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

~~| Table | Rows |~~
~~|---|---|~~
~~| daily_costs | 929 |~~
~~| delivery_runs | 67 |~~

**CORRECTED 2026-09-11 — `delivery_runs` was off by 10x, not just
stale.** Verified against the live DB:

| Table | Rows (2026-09-11, verified) |
|---|---|
| daily_costs | 938 |
| delivery_runs | **688** (was listed 67) |

Categories are assigned at import time by [[import_statement_v2.py]] profile logic.

~~Uncategorized rows land in `other` — 78 rows remain there (rent + storage, intentional).~~

**CORRECTED 2026-09-11 — this was already wrong once and the correction
never reached this note.** [[Unapplied - Backlog]] found on 2026-08-21
that the real count was 39 rows ($6,748.27), not 78 — rent and storage
accounted for only 13 of them, the other 26 were real miscategorized
spend (Walmart grocery runs, a driving-school charge, USPS/UPS/Staples,
two fee rows). That correction was made in Backlog but never propagated
here. **Verified again 2026-09-11: the `other` category has moved a
second time, to 16 rows, $7,263.95** — a prior gig_tracker session's
categorizer fix (boundary-aware merchant matching, 2026-09-09)
recategorized most of the 26 real-spend rows out of `other` on its own.
What's left today is 7 Rent rows, 8 Storage unit rows, and one
unidentified merchant (SFC CERRITOS, $3.95, no rule matches it — flagged,
not miscategorized). **Not written as a new fixed number** — this figure
has proven itself unstable twice now (78 → 39 → 16) as import and
categorizer work landed; a hand-written count will be wrong again the
next time either changes. Query `SELECT COUNT(*) FROM daily_costs WHERE
category='other'` directly instead of trusting a note.

## Corrections — append-only, don't rewrite this section

**2026-09-11.** `delivery_runs` row count corrected (67 -> 688, a 10x
gap). The `other`-category claim ("78 rows, rent+storage, intentional")
was already superseded once by [[Unapplied - Backlog]] on 2026-08-21 (39
rows, 26 of them real spend) and that correction never reached this
note — found because the two notes stated different numbers for the
same fact. Re-verified against the live DB rather than just copying
Backlog's 2026-08-21 figure forward: the real count has moved again, to
16 rows, mostly rent/storage, because a categorizer fix since then
recategorized most of the real-spend rows on its own. The category
totals in "Major Spending Leaks" above (food_fast, entertainment,
vehicle, subscriptions) were NOT re-verified this pass — they are Aug 13
figures, likely stale, out of scope for this correction.
