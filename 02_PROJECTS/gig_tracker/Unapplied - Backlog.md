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

## 78 Rows Remaining in `other` Category

**What:** 78 `daily_costs` rows are still in the `other` category after import.

**Why deferred:** These are confirmed intentional: rent and storage unit payments that don't map to any gig-operation category. They are correct as `other`.

**If this changes:** If a non-rent/storage row is found in `other`, recategorize via `gig.py` and update the importer profile logic to catch it automatically next import.
