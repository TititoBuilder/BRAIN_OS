# Van Financial Case

**Built:** 2026-08-21, from 462 logged transactions and 12 months of cost data
**Status:** The argument for the purchase, in numbers

---

## The one-line case

**You are already buying the food. You just have nowhere to cook it.**

May 2026: $666.73 fast food **and** $643.20 groceries. $1,309.93 on food in a
single month. That is not someone who cannot cook — that is someone paying
twice because the kitchen is missing.

---

## Fast food, measured

`daily_costs`, category `food_fast`, all 462 rows:

| Month | Visits | Spend |
|---|---|---|
| 2025-12 | 28 | $405.17 |
| 2026-01 | 60 | $682.80 |
| 2026-02 | 82 | $778.71 |
| 2026-03 | 57 | $643.74 |
| 2026-04 | 52 | $713.06 |
| 2026-05 | 59 | $666.73 |
| 2026-06 | 47 | $594.06 |
| 2026-07 | 57 | $563.73 |

**462 visits over 12 months = $438.17/mo, 38 visits/mo, $11.38 average.**

The 12-month figure is dragged down by four near-zero months at the start
(Sep–Nov 2025, before full logging). **Every complete month since December has
run $563–$779.** Use ~$560/mo as the working number, not $438.

**Largest single line: Starbucks, $437.60 across 32 visits** (two merchant
strings), ~$13.67 a visit. Coffee bought on route — the thing a van kitchen
most directly replaces.

---

## The arithmetic

| | Monthly |
|---|---|
| Rent eliminated | $915.00 |
| Fast food (working figure) | $560.00 |
| **Gross saving** | **$1,475.00** |
| Van payment (dealer loan, ~27% APR) | −$693.00 |
| **Net** | **+$782.00** |

At a conservative 50% reduction in fast food instead of elimination:

| | Monthly |
|---|---|
| Rent eliminated | $915.00 |
| Fast food halved | $280.00 |
| Gross saving | $1,195.00 |
| Van payment | −$693.00 |
| **Net** | **+$502.00** |

**Even the conservative case clears $500/month.**

---

## What this does not count

**Costs van life adds that rent covers:** propane, water fills, ice,
laundromat, gym membership for showers, occasional paid parking. Estimate
$100–150/mo. Subtract it — the conservative case still nets ~$370.

**Fuel is not in this calculation.** It moves with Roadie mix, not with
housing. See [[Vehicle Strategy - Roadie vs Spark]].

**Fast food will not go to zero.** Coffee on a route, a meal when the day
runs long. Halving it is the realistic target, not eliminating it.

**The dealer loan is 27% APR.** The $693/mo assumes that rate. Killing it
first is already the stated plan — see [[Van Decision]].

---

## Why the tracker never said this

`van-date` projects against the $4,301 down payment. `runway.py` computes debt
payoff order. Neither one asks what the van *saves*.

The saving was sitting in `daily_costs` the whole time — 462 rows in a
category CLAUDE.md already flags as the most-fixable spend — but no command
put it next to the rent line.

---

## Current position

`income_recompute.py`, 2026-08-21:

| | |
|---|---|
| Income | $5,060.40/mo |
| Costs | $3,147.17/mo |
| **Surplus** | **$1,913.22/mo** |
| Van down payment $4,301 | **2.2 months** |

---

*Related: [[Van Decision]] · [[Vehicle Strategy - Roadie vs Spark]] ·
[[Cost Findings]] · [[Financial Position]]*