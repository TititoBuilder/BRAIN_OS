---
tags: [prop22, gig_tracker, strategy]
---

# Offer Decision Rules

Two modes, two completely different filters. Switching between them is the core skill of working Prop 22 correctly.

See [[Prop 22 Mechanics]] for why the modes exist.

## CASH Mode (Days 1–10)

**Goal:** maximize real dollars per hour.

| Rule | Threshold |
|---|---|
| Take | $25+ fast deliveries |
| Consider | $20–$24 if distance is short |
| Skip | Under $20 regardless of tip |
| Skip | Long-distance hauls with low base_pay |

In CASH mode, tips matter and a fast run always beats a slow one. You're not accumulating floor credit yet — you're just earning.

## HOURS Mode (Day 11+ or 45h target reached)

**Goal:** maximize engaged hours, because every hour is worth $20.736 toward the floor.

| Rule | Action |
|---|---|
| Shopping orders | **Always take** — in-store walk time is engaged time |
| Any order, any tip | Take it |
| Fast high-tip runs | Still fine, just not preferred over slow store orders |
| Idle waiting | Does not count — keep moving |

### Why Time-Heavy Low-Base Orders Win in HOURS Mode

Example comparison:

**Order A (CASH mode winner):**
- Base pay: $20, tip: $8 → total $28
- Duration: 20 min, 8 miles
- Floor credit: `(0.33 hr × $20.736) + (8 mi × $0.35)` = $6.84 + $2.80 = **$9.64**

**Order B (HOURS mode winner):**
- Base pay: $12, tip: $2 → total $14
- Duration: 45 min (Walmart shop), 3 miles
- Floor credit: `(0.75 hr × $20.736) + (3 mi × $0.35)` = $15.55 + $1.05 = **$16.60**

Order B pays less in tips but earns nearly **twice the floor credit**. In HOURS mode, Order B is the correct choice every time.

## The Mode Switch Trigger

Track both:
1. **Day in period** — switch at day 11 if you haven't hit 45h
2. **Cumulative engaged hours** — if you hit 45h before day 11, switch immediately

The `prop22.py` module tracks these and surfaces the current mode.

## What Never Changes Between Modes

- A run that pays well *and* takes time is always good.
- Never take a run that puts you in physical danger regardless of mode.
- Roadie runs operate outside Prop 22 — evaluate them purely on CASH mode logic.
