---
tags: [gig_tracker, financial, snapshot]
updated: 2026-08-13
corrected: 2026-09-10
---

# Financial Position

> ⚠️ **CORRECTED 2026-09-10 — this note's Loans and Kill Order sections
> were wrong.** They carried a debt narrative already found false and
> fixed twice in the gig_tracker repo (README.md, then CLAUDE_HANDOFF.md,
> retired) — this vault copy was missed both times, because a repo-only
> session cannot see the vault. See "Corrections" at the bottom for what
> changed and the evidence.
>
> **This note is a dated snapshot (August 13, 2026), not a live source.**
> For current numbers, don't trust anything below that touches a dollar
> figure — go to:
> - `NAVIGATION.md` (repo root) — current debt, surplus, settled facts
> - `_generated/Financial Position.md` (this folder) — auto-refreshed by
>   `export_vault.py`, current as of its own header date
>
> What's still safe to read below as-is: the due-day payment schedule
> concept, the monthly-run-rate ballpark, and the general shape of the
> funding path — none of that was wrong, only the specific debt figures.

Snapshot as of **August 13, 2026**.

## Credit Cards — $4,009 total across 7 cards (Aug 13 snapshot — see repo `cards` table for current balances)

| Card | Due Day | Notes |
|---|---|---|
| Citi 6194 | Day 3 | |
| **US Bank Amazon Business ...7863** | **Day 19** | Corrected 2026-09-10 — was listed "AMEX 01007" (retired identity; AMEX/Amazon co-brand ended, transferred to U.S. Bank) |
| **Wells Fargo Active Cash ...5552** | Day 9 | Corrected 2026-09-10 — was listed "WF 6017" (card reissued, same account/terms) |
| Cap One 4987 | Day 10 | |
| AMEX 91009 | Day 16 | |
| Costco 5812 | Day 22 | |
| Citi 8315 | Day 27 | |

Cards are managed by due-day payment schedule. Minimum payments cleared on time to protect FICO. Citi 6936 is a **closed card** — its CSV is archived, no active balance.

## Loans

~~| Loan | Balance | Rate | Priority |~~
~~|---|---|---|---|~~
~~| Dealer loan (van) | $21,700 | 27% APR | Kill first |~~
~~| Personal loan (Upstart) | $16,000 | 9.55% APR | Kill second |~~
~~| BofA 0% transfer | $5,585 | 0% | Never touch early |~~

~~**Total loan debt: $43,285**~~

~~The BofA 0% balance should run to term. Paying it early wastes free financing. Dealer loan bleeds $490+/month in interest — every surplus dollar goes there.~~

**CORRECTED 2026-09-10 — every row above was wrong, not just stale.**
Struck through rather than deleted, per this project's rule that
corrections get recorded, not silently erased. The real picture, as of
2026-09-10:

| Loan | Balance | Rate | Real? |
|---|---|---|---|
| "Dealer loan (van)" | $21,700 | 27% | **NO — a seeded placeholder, `is_hypothetical=1`. Never a real quote, never real debt owed.** |
| "Personal loan (Upstart)" | $16,000 | 9.55% | **NO — same: seeded placeholder, never real.** |
| BofA CC (balance transfer) | $5,522.10 (now $0) | **22.49%**, not 0% — stale promo-era data | Was real; **paid in full 2026-09-09** from AmEx loan proceeds. Row kept for history. |
| AmEx Personal Loan (acct ...01006) | $15,000 | 16.99% | **The actual real loan.** Signed 2026-09-07, disbursed 2026-09-08. 24mo, $741.56/mo. Retired BofA; funds the van down payment. |

Current total debt (loan + cards) lives in the repo's `NAVIGATION.md`, not
here — it changes too often for a hand-written note to track safely.

## Cash

~~| Account | Balance |~~
~~|---|---|~~
~~| WF Checking ...0669 | $12.79 |~~
~~| WF Savings ...4700 | $28.03 |~~
~~| AMEX Rewards ...5562 | $13.35 |~~
~~| Capital One 360 ...0974 | $13.81 |~~
~~| **Total** | **$67.98** |~~

*Updated Aug 14, 2026 — an Aug 13/14 snapshot, not live.* Capital One
360 ...0974 belongs to Cristian's son, not Cristian — excluded from real
cash totals in the repo (`cash_accounts.is_external=1`), which the
snapshot above didn't yet know. Current cash: repo `NAVIGATION.md` or
`_generated/Financial Position.md` in this folder.

## Monthly Run Rate

~$2,615/month in expenses. This is the baseline that gig income must clear before any debt paydown is possible.

*(Ballpark, not contradicted by anything found 2026-09-10 — left as-is.)*

## Credit Score

~~**FICO 716 — Good**~~

**CORRECTED 2026-09-10 — FICO 732 (Experian, FICO Score 9), confirmed
2026-08-12.** 716 was a different bureau/model (Equifax VantageScore) at
a different point — not directly comparable, not a decline. A 695
Equifax VantageScore 3.0 figure also exists elsewhere in this project's
history; same caveat applies to it. Don't present either as "the score
changed" without naming which bureau/model.

## Kill Order

~~1. Dealer loan ($21,700 @ 27%) ← immediate priority~~
~~2. Personal loan ($16,000 @ 9.55%)~~
~~3. BofA 0% ($5,585) ← let it run to term~~

**CORRECTED 2026-09-10 — this kill order was built entirely on
placeholder debt that never existed.** There is no multi-loan kill order
to run today: the only real loan is the AmEx personal loan above (BofA is
paid off). Card payoff priority is avalanche (highest real APR first),
computed live by `runway.py` in the repo — not a fixed list, because it
shifts as balances move. Don't hand-maintain one here again.

Vehicle sell sequence: Tacoma first → Prius C → proceeds attack the
highest-APR real debt at the time of sale. See [[Van Decision]] for the
full funding path and timeline — corrected the same session as this note.

---

## Corrections — append-only, don't rewrite this section

**2026-09-10.** Loans, Kill Order, Cash, and Credit Score sections
carried figures found false, not just stale, during a gig_tracker vault
audit. Evidence: gig_tracker's `debts`/`cards` tables (repo,
2026-09-10), cross-checked against `GIG_TRACKER_FLAGS.md`'s
2026-09-06/07 entries (where the placeholder-loan and BofA-rate findings
were first made in the repo — this vault note was never updated to
match, twice, because a repo-only session cannot see the vault). Card
identities also corrected: "AMEX 01007" → US Bank Amazon Business
...7863 (co-brand transfer, 2026-08-14); "WF 6017" → Wells Fargo Active
Cash ...5552 (card reissue, same account/terms, 2026-09-05). Live dollar
figures were deliberately NOT re-copied into this note — they change
weekly and a hand-written snapshot goes stale silently. See the header
banner for where current numbers actually live.

<!-- auto-ingested 2026-08-16 -->
2026-08-16: Expanded cash breakdown detail (fix applied this session).
