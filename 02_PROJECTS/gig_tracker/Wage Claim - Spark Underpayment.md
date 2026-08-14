---
tags: [gig_tracker, prop22, wage_claim]
---

# Wage Claim — Spark Underpayment

## Summary

**Period:** July 6–19, 2026
**Documented underpayment:** ~$247
**Status:** Documented. Not yet filed.

## How the Underpayment Was Detected

The [[Prop 22 Mechanics]] floor formula was applied to each completed period in the database. A reference period with a known correct payment was used to validate the model — the formula reproduced the reference period's result to under $1.00, confirming accuracy.

The same formula applied to the Jul 6–19 period produced a floor that exceeded what Spark actually paid by approximately $247.

## Why This Period Is Excluded from Calibration

The mileage baseline (`calibrate_miles.py`) requires periods where pay was correct to accurately derive the engaged mi/hr rate. Since Jul 6–19 was not paid in full, its run data cannot be used to establish a reliable baseline.

Current mileage baseline (15.1 mi/hr) is derived from 1 paid period only and is marked **provisional**. See [[Unapplied - Backlog]] for the planned update after a second paid period is available.

## Evidence Chain

1. Floor formula reproduced reference period to < $1 error
2. Formula applied to Jul 6–19 → result: floor exceeds paid amount by ~$247
3. Run data stored in `delivery_runs` table (67 rows total)
4. Period data isolated and flagged in database

## Filing Status

**Not yet filed.** The ~$247 is documented and the math is reproducible, but no claim has been submitted to Spark or to the California Labor Commissioner.

## Next Steps (When Ready to File)

1. Export run-level data for the Jul 6–19 period from the DB
2. Compute floor formula line-by-line for each run
3. Compare sum to actual pay received
4. Prepare claim with itemized breakdown
5. File through Spark support first; escalate to California Labor Commissioner if unresolved

## Amount in Context

$247 at the dealer loan rate (27% APR) represents real money. It is worth pursuing through the support channel at minimum cost before deciding whether to escalate.
