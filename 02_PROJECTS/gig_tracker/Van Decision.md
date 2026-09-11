---
tags: [gig_tracker, van, financial_goals]
corrected: 2026-09-10
---

# Van Decision

> ⚠️ **CORRECTED 2026-09-10 — the Funding Path and Debt Kill Order below
> were built on a loan that never existed.** Cristian is visiting dealers
> tomorrow; read the "Real current position" box below before this note,
> not after. Full evidence: "Corrections" section at the bottom and
> `GIG_TRACKER_FLAGS.md` in the repo (2026-09-06/07 entries, where this
> was first found and fixed in README.md and CLAUDE_HANDOFF.md — this
> vault note was missed both times).

## Real current position — read this first

- **The 27% "dealer loan" never had a source, anywhere in this project's
  history.** It was a seeded placeholder (`is_hypothetical=1`), never a
  real quote from any dealer. There is no debt at 27% to kill.
- **Financing is being shopped now, not "already in place."** A real
  written quote exists: **Westlake, 10.49%/60mo.** Others may still come
  in before dealer visits — check `GIG_TRACKER_QUEUE.md` and
  `GIG_TRACKER_SCHEDULE.md` in the repo for the current state of that
  shopping before relying on 10.49% as final.
- **The $16,000 "Upstart personal loan" was also a placeholder** —
  `is_hypothetical=1`, never real. It is not part of any real funding
  path.
- **The real loan already signed is unrelated to van financing**: an
  AmEx personal loan, $15,000 @ 16.99%, 24mo, $741.56/mo (acct ...01006),
  disbursed 2026-09-08. It paid off BofA and funds the down payment — it
  is not the vehicle loan itself.
- **BofA was 22.49% APR, not 0%** (stale promo-era data), and is now
  **paid off ($0)** as of 2026-09-09.

## Target Dates

| Scenario | Date |
|---|---|
| Realistic | September 23, 2026 |
| Optimistic | August 26, 2026 |

Dates are stored in `van_config.json` at the project root — not hardcoded in any script. See [[Decision Log]] for why this was externalized. *(Not re-verified 2026-09-10 — check `GIG_TRACKER_SCHEDULE.md` for the current draft timeline before trusting these.)*

## Why the Van

The van represents a living situation transition. It is not purely a vehicle purchase — it is infrastructure for a different operating model. This context matters for evaluating the financial trade-offs: the cost of *not* having it is higher than it looks on a balance sheet.

*(2026-09-10: the repo's `NAVIGATION.md` now frames this more precisely — the van is the INSTRUMENT, financial freedom is the goal. Worth reading alongside this section.)*

## Funding Path

~~1. **Sell Tacoma** — proceeds go directly against personal loan (Upstart $16,000 @ 9.55%).~~
~~2. **Sell Prius C** — remaining proceeds continue killing the personal loan.~~
~~3. **Dealer financing** — $21,700 at 27% APR already in place. This is the active loan being attacked first.~~

~~The sell sequence matters: Tacoma first because it carries more value and Upstart has the second-highest rate. The dealer loan at 27% APR is the highest-rate debt and gets first dollars from gig income.~~

**CORRECTED 2026-09-10 — steps 1-2 named a loan that isn't real; step 3
described financing that wasn't "already in place," it's actively being
shopped.** Current real funding path:

1. **Sell Tacoma, then Prius C** — proceeds go against the highest-APR
   *real* debt at the time of sale (avalanche order, computed live by
   `runway.py` — not a fixed target, because it shifts as balances move).
2. **Dealer financing for the van itself** — being shopped now. Real
   quote in hand: Westlake 10.49%/60mo. This is a separate loan from the
   AmEx personal loan already signed (which funded the down payment, not
   the van purchase price).

## Debt Kill Order (Post-Van Purchase)

~~1. Dealer loan ($21,700 @ 27% APR)  ← kill first, bleeds fastest~~
~~2. Personal loan (Upstart $16,000 @ 9.55%)~~
~~3. BofA 0% transfer ($5,585)        ← never touch early; use the 0% runway~~

**CORRECTED 2026-09-10 — every line above named a debt that either never
existed or never had the terms stated.** There is no fixed kill order to
follow: the only currently real, non-card debt is the AmEx personal
loan ($15,000 @ 16.99%), and BofA is already paid off. Whatever the real
dealer/van loan's APR turns out to be, it joins the avalanche — repo
`runway.py` computes current priority live; don't hand-maintain a list
here again.

CC debt is separate and managed by due-day payment schedule — see [[Financial Position]] for card due days (also corrected 2026-09-10 — read its header banner first).

## Why 27% APR Gets Priority

~~At 27% APR, the dealer loan costs roughly **$490/month** in interest alone on $21,700. Every dollar directed at principal has an immediate guaranteed 27% return. No gig offer comes close to that rate of return — paying it down is always the best use of surplus.~~

**CORRECTED 2026-09-10 — this section's entire premise was a debt that
never existed; removed rather than re-purposed.** The underlying
principle survives in general form: whatever the real van loan's APR
turns out to be, if it's the highest real rate in the debt stack, it
gets priority — see repo `NAVIGATION.md`'s "THE GOAL" section for the
current reasoning (AmEx at 16.99% currently outranks the van loan's real
10.49% Westlake quote, so AmEx gets attacked first under today's actual
numbers — the opposite of what this section originally argued, because
the numbers it argued from were fictional).

## What the Optimistic Date Requires

Aug 26 requires selling at least one vehicle before that date and no major unexpected costs. It is achievable but depends on variables outside the tracker's control. The realistic date absorbs those unknowns.

*(Not re-verified 2026-09-10.)*

---

## Corrections — append-only, don't rewrite this section

**2026-09-10.** Funding Path, Debt Kill Order, and the "Why 27% APR Gets
Priority" section were built entirely on two seeded placeholder loans
(`is_hypothetical=1` in the repo's `debts` table) and a financing
statement ("already in place") that was never true — financing is being
shopped now, with a real Westlake 10.49%/60mo quote in hand as of
2026-09-10. This is the same false debt narrative already found and
fixed twice in the gig_tracker repo (`README.md`, then
`CLAUDE_HANDOFF.md`, retired to `archive/`) — this vault note was missed
both times, because a repo-only session cannot see the vault. Evidence:
`GIG_TRACKER_FLAGS.md` 2026-09-06/07 entries (original findings),
gig_tracker's `debts` table (2026-09-10, direct verification). Flagged
urgent: this note is named for a decision involving dealer visits
happening the day after this correction.
