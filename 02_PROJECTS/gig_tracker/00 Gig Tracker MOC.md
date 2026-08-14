---
tags: [MOC, gig_tracker]
---

# Gig Tracker — Map of Content

Central index for the gig_tracker knowledge cluster. All files below live in `02_PROJECTS/gig_tracker/`.

## Files in This Folder

| File | Description |
|---|---|
| [[00 Gig Tracker MOC]] | This file — index and navigation hub |
| [[Prop 22 Mechanics]] | Floor formula, HOURS/CASH mode logic, underpayment finding |
| [[Offer Decision Rules]] | When to take or skip an offer depending on mode |
| [[Van Decision]] | Target dates, funding path, sell sequence, debt kill order |
| [[Cost Findings]] | Spending leaks identified from statement imports |
| [[Financial Position]] | Current balances, loans, FICO, monthly run rate |
| [[Wage Claim - Spark Underpayment]] | ~$247 underpayment Jul 6–19, documented not filed |
| [[Codebase Map]] | Every Python file and its purpose |
| [[Decision Log]] | Chronological log of architectural decisions |
| [[Daily Operating Procedure]] | Morning checklist through session close |
| [[Unapplied - Backlog]] | Known items not yet acted on |

## Codebase Entry Points

- [[gig.py]] — 24-command CLI (primary interface)
- [[web.py]] — Flask dashboard
- [[prop22.py]] — Prop 22 floor calculations
- [[import_statement_v2.py]] — 5-profile statement importer
- [[preflight.py]] — morning health check
- [[balance.py]] — quick balance updates (added Aug 13, 2026)

## Project Goal

Fund van purchase by **Sep 23, 2026** (optimistic Aug 26, 2026).
Income sources: Spark (Walmart delivery) + Roadie runs, Southern California.

## Key Numbers

| Item | Value |
|---|---|
| CC debt | $4,009 (7 cards) |
| Dealer loan | $21,700 @ 27% APR |
| Personal loan | $16,000 @ 9.55% |
| Cash on hand | $596 |
| Monthly run rate | ~$2,615 |
| FICO | 716 |


<!-- auto-ingested 2026-08-14 -->
## 2026-08-14 Population
- 11 Obsidian vault docs populated for gig_tracker project during Direction 6
- Includes: Financial Position, Decision Log, Offer Decision Rules, Prop 22 Mechanics, Van Decision, Wage Claim, Cost Findings, Daily Operating Procedure, Unapplied Backlog, Codebase Map, and this MOC
