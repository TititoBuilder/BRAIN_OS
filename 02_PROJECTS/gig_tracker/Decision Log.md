---
tags: [gig_tracker, decisions, architecture]
---

# Decision Log

Chronological record of architectural and operational decisions. Newest entries at top.

---

## 2026-08-13 — Template variable `d` renamed to `dash`

**Decision:** Renamed template variable `d` to `dash` in web.py dashboard templates.

**Reason:** `d` collided with an outer-scope variable, causing silent rendering bugs. `dash` is unambiguous within Jinja2 template context.

---

## 2026-08-13 — Mileage baseline 15.1 mi/hr marked provisional

**Decision:** Mileage baseline set to 15.1 mi/hr but flagged as provisional in `calibrate_miles.py`.

**Reason:** Only one paid period available for calibration. One data point is not enough to set a stable baseline — it could be an outlier. Baseline will be updated once a second paid period is available.

**Rule:** Do not update the baseline before 2+ paid periods are confirmed. See [[Unapplied - Backlog]].

---

## 2026-08-13 — Van dates moved to `van_config.json`

**Decision:** Van purchase target dates (realistic Sep 23, optimistic Aug 26) moved from hardcoded script values to `van_config.json`.

**Reason:** Hardcoded dates in scripts violate the DRY principle and require code edits to update. A config file makes the dates a data concern, not a code concern. Any script that needs them reads the file.

---

## 2026-08 — `_DUE_DAYS` moved from hardcoded dict to `cards.due_day` column

**Decision:** Card due days moved from a hardcoded Python dictionary to a `due_day` column in the `cards` table.

**Reason:** Hardcoded dicts are fragile — adding a card or changing a due day required a code edit. Storing due days in the DB makes them data: queryable, updatable via `gig.py` commands, and visible in the dashboard without touching source.

---

## 2026-08 — `import_statement_v2.py` replaced three separate importers

**Decision:** Consolidated `import_amex.py`, `import_wf.py`, and `import_citi.py` (and variants) into a single `import_statement_v2.py` with 5 named profiles.

**Profiles:** `amex`, `wells_fargo`, `capital_one`, `capital_one_en`, `citi`

**Reason:** Separate importers had duplicated logic and diverged over time. A single importer with a profile flag is easier to maintain, easier to extend for new cards, and produces consistent category assignment.

---

## 2026-07 — Chrome extension approach abandoned

**Decision:** Dropped the Chrome extension plan for automated statement scraping.

**Reason:** Card issuers (Citi, AMEX, WF, Capital One) actively resist scraping — they detect and block browser automation. The extension would require constant maintenance against anti-bot updates. CSV download + `import_statement_v2.py` is slower but reliable and does not depend on any issuer's DOM staying stable.


<!-- auto-ingested 2026-08-13 -->
## 2026-08-13
- van_build field renamed; is_onetime confirmed
- 11 vault docs populated for gig_tracker project
- gig_tracker imports completed (Direction 6)


<!-- auto-ingested 2026-08-15 -->
2026-08-15: Committed gig_tracker ingestion flags from 2026-08-14 session. Flags deduplicated and sorted.
