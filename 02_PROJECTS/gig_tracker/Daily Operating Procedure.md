---
tags: [gig_tracker, procedure, daily]
---

# Daily Operating Procedure

## Morning — Before Going Out

```
python preflight.py
```

Check for green on all items. If anything is red, resolve before starting runs. Preflight verifies:
- DB accessible and not corrupted
- No missing engaged_miles on recent runs
- Card due days coming up in next 3 days

Do not skip preflight — missing engaged_miles silently breaks Prop 22 calculations.

## After Runs — Log the Session

```
python gig.py log-run ...
```

Log every run before the end of the day. Runs logged late are harder to reconstruct and may miss engaged time precision.

Key fields to capture:
- Platform (spark / roadie)
- Start/end time (for engaged hours)
- Engaged miles
- Base pay
- Tip (separate from base_pay — needed to distinguish floor coverage)

## Weekly — Statement Import

1. Download CSV from each card issuer's website
2. Run importer for each card:

~~python import_statement_v2.py --profile amex --file <path>~~
~~python import_statement_v2.py --profile wells_fargo --file <path>~~
~~python import_statement_v2.py --profile capital_one --file <path>~~
~~python import_statement_v2.py --profile citi --file <path>~~

**CORRECTED 2026-09-11 — this command would fail if run as written.**
There is no `--profile` or `--file` flag; verified directly against
`import_statement_v2.py`'s own argument parser. The bank format IS
auto-detected from the CSV's own headers — nothing to pass for it. The
real interface is a **positional CSV path** plus **`--card <TAG>`**
(the label stored in `daily_costs.card` — not the issuer name, the
tracker's own per-card tag), dry-run by default:

```
python import_statement_v2.py <path-to.csv> --card WF_5552
python import_statement_v2.py <path-to.csv> --card capone_4987
python import_statement_v2.py <path-to.csv> --card CITI_6194
python import_statement_v2.py <path-to.csv> --card CITI_8315
python import_statement_v2.py <path-to.csv> --card AMEX_91009
python import_statement_v2.py <path-to.csv> --card citi_5812
python import_statement_v2.py <path-to.csv> --card AMEX_7863
python import_statement_v2.py <path-to.csv> --card WF_5552 --commit
```

Nothing writes without `--commit` — run without it first, check the
dry-run output, then re-run with `--commit` to actually import.

3. Verify row counts match expected transactions
4. Check `other` category for anything that should be recategorized

## Balance Updates — When You Know a Card Balance

~~python balance.py <last4> <amount>~~

~~Example: `python balance.py 6194 312.45`~~

**DEAD 2026-09-11 — `balance.py` does not exist in the repo.** Verified
absent at `C:\Dev\Projects\gig_tracker\gig_tracker\balance.py`. Same file
referenced in [[00 Gig Tracker MOC]] and [[Codebase Map]], also marked
there. The real current tool for this: `python update.py` — interactive
menu (option 1 = card, per `README.md`'s "Most Used Commands").

Run this any time you check a card balance — keeps the dashboard accurate without waiting for the next statement.

## Prop 22 Period Check — During Active Period

```
python gig.py prop22-status
```

Shows:
- Current mode (HOURS or CASH)
- Engaged hours to date
- Floor earned vs base_pay to date
- Projected adjustment

Run this before deciding whether to work a particular day.

## Session Close — End of Work Session

```
python C:\BRAIN_OS\09_TOOLS\session_close.py
```

Run from Win+X Terminal (PowerShell), not VS Code or Claude Code terminal. Writes session summary to Obsidian vault and sends Telegram confirmation.

Confirm:
- [ ] Telegram confirmation received
- [ ] BRAIN_OS git commit visible in `git log`

## Corrections — append-only, don't rewrite this section

**2026-09-11.** "Weekly — Statement Import" command corrected: it used a
`--profile`/`--file` interface that never existed in
`import_statement_v2.py` — verified directly against the script's own
argument parser, not guessed. The real interface is a positional CSV
path plus `--card <TAG>`; bank format is auto-detected from the CSV
itself. "Balance Updates" marked dead: `balance.py` does not exist in
the repo, checked directly. Not confirmed or touched: `gig.py
prop22-status` (Prop 22 Period Check section) — not part of this
correction, unverified either way.
