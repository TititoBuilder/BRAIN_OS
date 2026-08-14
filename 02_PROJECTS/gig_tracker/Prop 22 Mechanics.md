---
tags: [prop22, gig_tracker, income]
---

# Prop 22 Mechanics

## The Floor Formula

Spark (and other app-based gig platforms in California) must pay at least:

```
floor = (engaged_hours × $20.736) + (engaged_miles × $0.35)
```

**Engaged time** = only the time between accepting an order and completing delivery.
Waiting at the app, driving to the zone, idle time — none of that counts.

**Engaged miles** = only miles driven during an active order.

If actual pay (base_pay + tips) falls below the floor, Spark must make up the difference with an **adjustment**.

## What Tips Do and Don't Affect

- Tips are **invisible to the floor calculation**. Spark does not include tips when computing whether they owe an adjustment.
- If base_pay alone exceeds the floor, no adjustment is owed — but tips are still yours on top.
- This means a high-tip, low-base order can *look* great but still trigger an adjustment, or a low-tip, high-base order might not.

## 14-Day Period Structure

Prop 22 operates on rolling **14-day periods**. Spark audits your pay against the floor at the end of each period. If the sum of base_pay across all runs falls short of the floor (calculated from total engaged hours + engaged miles), they issue an adjustment lump sum in the following pay period.

## HOURS Mode vs CASH Mode

The tracker uses two operating modes that flip based on where you are in the 14-day period.

### CASH Mode (Days 1–10)
- Optimize for **offer quality**.
- Target: $25+ fast runs; skip orders under $20.
- You have time to be selective — a rejected order now doesn't cost you floor credit.

### HOURS Mode (Days 11–14, or 45h target hit)
- Switch when you've crossed ~day 11 OR when you've banked enough hours that any extra hour maximizes floor credit.
- **Take every shopping order** — walking the store aisles is engaged time and counts toward the floor.
- Skip nothing based on low base_pay; the floor formula rewards time-heavy orders that CASH mode would reject.
- A $12 base-pay order that takes 45 minutes at Walmart is worth $15.55 in floor credit (`0.75 hr × $20.736`). A $20 fast run in 20 min is worth $6.91. HOURS mode flips the math.

## Best Adjustment Amounts

From verified periods:
- **$781.52** — largest confirmed adjustment
- **$546.90** — second confirmed adjustment

These amounts give a rough upper bound on what a well-optimized HOURS-mode period can recover.

## Underpayment Finding

**Jul 6–19, 2026** period: documented ~$247 underpayment.

The floor formula was reproduced against the correctly-paid reference period to under $1.00, confirming the model is accurate. The Jul 6–19 period was then applied and came up short.

This period is **excluded from the mileage baseline calibration** — it cannot be used to estimate mi/hr because the pay data is unreliable.

See [[Wage Claim - Spark Underpayment]] for full documentation and filing status.

## Constants

| Constant | Value |
|---|---|
| Engaged hour rate | $20.736/hr |
| Engaged mile rate | $0.35/mi |
| Period length | 14 days |
| HOURS mode trigger | Day 11 OR 45h target reached |
