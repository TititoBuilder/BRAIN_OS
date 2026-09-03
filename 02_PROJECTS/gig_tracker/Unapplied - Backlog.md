---
tags: [gig_tracker, backlog]
---

# Unapplied — Backlog

Items that are known, documented, and intentionally deferred. Each entry explains why it is not being acted on now.

---

## Runs 56–59: Missing `engaged_miles` (Aug 5 Spark)

**What:** Four delivery runs (IDs 56–59) logged without `engaged_miles` data.

**Why deferred:** The mileage baseline (`calibrate_miles.py`) currently has only one paid period of data (15.1 mi/hr, provisional). Patching these runs with an estimate derived from a single-period baseline would propagate that uncertainty into the Prop 22 floor calculation for those runs.

**When to act:** After `calibrate_miles.py` has 2+ paid periods of data and a stable baseline is confirmed. Then back-fill engaged_miles using the stabilized rate.

**Risk if ignored:** These 4 runs' floor credit is undercounted. Low risk since the period they belong to is likely already settled, but the runs remain in the DB with a gap.

---

## 11 Obsidian Vault `.md` Files

**What:** This session (Aug 13, 2026) created 11 vault documents for the gig_tracker project cluster.

**Status:** Creating now — this file is the last of the 11. Will be committed to BRAIN_OS in this session.

---

## Van Config Created — Dates in `van_config.json`

**What:** Van purchase target dates moved from hardcoded values to `van_config.json`.

**Status:** Done as of Aug 13, 2026. Logged here as a record that the config file now exists and is the canonical source. See [[Decision Log]].

---

## Citi 6936 — Closed Card CSV Archived

**What:** Citi 6936 is a closed card. Its statement CSV has been archived.

**Status:** No active balance, no future imports. Archived location confirmed. No further action needed unless a dispute arises.

---

## Rows in `other` Category — CORRECTED 2026-08-21

**Previous claim (wrong):** ~~78 rows, confirmed intentional: rent and storage
unit payments that don't map to any gig-operation category.~~

**Verified against the live DB:** **39 rows, $6,748.27.** Rent ($5,490.00,
6 rows) and Storage unit 277 ($755.00, 7 rows) account for $6,245.00 across
13 rows. **The other 26 rows — $503.27 — are neither rent nor storage.**

The entry's own escape clause said "if a non-rent/storage row is found in
`other`, recategorize." 26 were found.

**What's actually sitting there:**

| Rows | Merchant pattern | Belongs in |
|---|---|---|
| 11 | Walmart / WM SUPERCENTER | `food_grocery` |
| 1 | A P DRIVING SCHOOL $271.00 | `vehicle` or one-time |
| 3 | USPS, UPS Store, Staples | `supplies` |
| 2 | FREETAXUSACOM, FAST CARD FEE | `fees` — **leak category** |
| 1 | CRUNCH NORWALK (gym) | `entertainment` |
| ~8 | liquor, pizza, Stater Bros, Speedway | `food_fast` / `food_grocery` |

**Why this matters beyond $503:** `fees` and `food_fast` are the two leak
categories, flagged everywhere as the most-fixable spend. Rows parked in
`other` never appear in leak analysis. The Walmart rows are the clearest
case — the same merchants appear correctly categorised elsewhere in
`daily_costs`.

**Why still deferred:** This is a recategorisation pass that writes to the
DB. Needs a dry-run and a per-row judgement on the mapping, not a blanket
rule. Roughly a 30-minute focused task.

**When to act:** Before the next leak analysis or cost comparison. The
dollar impact is small; the analytical distortion is not.

**Also fix:** whichever importer profile assigned Walmart grocery runs to
`other` in the first place, or the next import repeats it.

---

## `auto_categorize()` files card payments as gas

**What:** `tracker/importer.py`'s `auto_categorize()` assigns
`CAPITAL ONE MOBILE PYMT` to **"Gas / mileage"**. Three rows in `expenses`:
$562.68 + $200.00 + $565.19 = **$1,327.87** of debt payments counted as fuel.

**Why deferred:** Contained. Nothing reads `expenses` — `cost.py` and
`compare.py` both read `daily_costs`, which is verified clean (zero payment
rows under `category='gas'`).

**When to act:** Before `tracker/importer.py` is ever repointed at
`daily_costs`. That repoint would import the bug into the table the runway
depends on.

**Risk if ignored:** Zero today. High the moment the two-table situation is
consolidated without checking this first.

---

## Trip ID recycling breaks the UNIQUE constraint

**What:** `delivery_runs` has `UNIQUE(platform, trip_id)` on the assumption
that Spark trip IDs never repeat. **They do.** Trip #2386 appeared on
2026-04-13 (id=88) and again in a later export; the second had to be inserted
with `trip_id` NULL.

**Why deferred:** Needs a schema decision, and schema changes here are
in-place `ALTER` + backfill only. Not a quick fix.

**When to act:** Before the next full-history re-import. The constraint will
silently reject legitimate new trips whose 4-digit ID collides with an old
one — data loss with no error surfaced to the user.

**Candidate fix:** make the uniqueness `(platform, trip_id, run_date)`.

---

## `import_wf_raw.py` — supersession unverified

**What:** Claimed absorbed into `import_statement_v2.py`'s Wells Fargo
profile. Held back from the 2026-08-21 archive pass because that claim was
never verified.

**Why deferred:** Archiving the only handler of a format on an unverified
supersession claim is not worth the speed.

**When to act:** Read v2's WF profile, confirm it handles the raw export
format (sign-flip, payment/reversal exclusion), then archive.

---

## Aug 3–16 Prop 22 adjustment still estimated

**What:** `SPARK_PAID` in `tracker/prop22.py` stops at `2026-07-20`. The
2026-08-03..08-16 period shows **$832.50 estimated**.

**Why deferred:** Spark posts a period's adjustment the Wednesday three days
after it closes — around Aug 19. The Aug 19 export showed everything still
Processing through Aug 18.

**When to act:** Next export with the adjustment Posted. Add the confirmed
figure to `SPARK_PAID`.

**Note:** The full-history export Summary reports **$4,407.78** of earnings
adjustments Jan 1 – Aug 11 across 16 payments. `SPARK_PAID` holds five
totalling $1,555.20. The other **$2,852.58** is confirmed paid money the
tracker does not know about. Reference only — not operationally needed
unless doing taxes.