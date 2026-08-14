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

```
python import_statement_v2.py --profile amex --file <path>
python import_statement_v2.py --profile wells_fargo --file <path>
python import_statement_v2.py --profile capital_one --file <path>
python import_statement_v2.py --profile citi --file <path>
```

3. Verify row counts match expected transactions
4. Check `other` category for anything that should be recategorized

## Balance Updates — When You Know a Card Balance

```
python balance.py <last4> <amount>
```

Example: `python balance.py 6194 312.45`

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
