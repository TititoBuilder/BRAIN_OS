# Vehicle Strategy — Roadie vs Spark

**Established:** 2026-08-21, from live period data
**Status:** Active operating decision

---

## The fact that was missing from every note

**Two vehicles, two platforms, two fuel profiles:**

- **Prius C** → Spark. ~$0.11/mile. Small tank, frequent cheap fills.
- **Tacoma (truck)** → Roadie. Large item delivery, long hauls, heavy fuel burn.

Both share the same cards, so `daily_costs` cannot split gas by vehicle.
**Roadie share of income is the proxy for which vehicle was working.**

This was documented only as a passing line in `SESSION_BRIEF.md` ("the Prius
(personal) and truck (Roadie) share the same cards"). It was never stated as
an operating principle, so every analysis session re-derived gas as a single
trend and reached the wrong conclusion.

---

## The evidence

Per-period, gas tracks Roadie mix almost exactly:

| Period | Roadie mix | Gas | Net |
|---|---|---|---|
| 2026-05-25 .. 06-07 | 16% | $137.96 | $1,499.00 |
| 2026-06-08 .. 06-21 | 30% | $141.56 | $2,474.00 |
| 2026-06-22 .. 07-05 | **64%** | **$377.74** | $2,786.41 |
| 2026-07-06 .. 07-19 | 53% | $413.84 | $2,710.41 |
| 2026-07-20 .. 08-02 | 17% | $274.32 | $2,145.85 |
| 2026-08-03 .. 08-16 | **0%** | **$87.06** | $2,615.62 |

64% Roadie → $377.74 gas. 0% Roadie → $87.06 gas. **A $291 swing driven by
which vehicle was on the road, not by fuel prices.**

Monthly gas from `daily_costs` shows the same story: May $353, June $503,
July $732 — July being the Roadie-heaviest month, not an inflation spike.

---

## The strategy conclusion

**Spark-heavy outperforms Roadie-heavy after fuel.**

2026-08-03..08-16 ran **zero Roadie** and produced **$2,615.62 net** — within
$95 of the best Roadie-heavy period, on **$291 less fuel**. Spark base hit its
highest recorded figure ($1,084.73) and the Prop 22 adjustment hit $832.50.

**Why the mechanism works:**

1. Prop 22 pays **$26.02 of floor per engaged hour** regardless of offer
   quality (`$20.736 wage + 15.1 mi × $0.35`). Hours convert to income at a
   guaranteed rate.
2. **Roadie's MEG adjustment has been $0.00 in all 16 periods.** Roadie trip
   pay clears its guarantee every time, so there is no top-up. What you earn
   is what you get.
3. The Prius burns a fraction of the truck's fuel for the same working hours.

So Spark's lower gross is offset by the adjustment, and the fuel saving is
pure margin.

---

## Caveats — do not overstate this

- The $832.50 for 2026-08-03..08-16 is **estimated**, not yet confirmed by
  Spark. `SPARK_PAID` stops at 2026-07-20. If it posts lower, the comparison
  narrows. All earlier periods use confirmed values.
- Gas is **not split by vehicle in the data**. Roadie mix is a proxy, a good
  one, but personal driving is mixed in and untracked.
- Roadie volume is volatile ($2,034 → $1,656 → $408 → $0). One zero-Roadie
  period is not a trend.
- Roadie remains ~49% of income historically. This is a shift in emphasis,
  not an argument for abandoning the platform.

---

## What this changes

- **Do not read rising gas as cost inflation.** Check Roadie mix first.
- **Do not revise the van timeline on a gas trend alone.** The $280 → $400/mo
  revision that moved the timeline 5.3 → 6.2 months was built on this exact
  error, plus a fuel figure that did not reproduce from raw rows.
- Current position (`income_recompute.py`, 2026-08-21): income $5,060.40,
  costs $3,147.17, **surplus $1,913.22**, van down payment in **2.2 months**.

---

*Related: [[Van Decision]] · [[Cost Findings]] · [[Financial Position]] ·
[[Prop 22 Mechanics]]*