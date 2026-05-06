---
tags: [project, construction, business]
project: CristianConstruction
status: active
created: 2026-05-05
updated: 2026-05-05
domain: CristianConstruction
---

# CristianConstruction Canvas

## Identity
- **Brand:** Custom Agent Remodel & Skilltrade
- **Structure:** Sole proprietor, South Call CA
- **Service radius:** South Call, Cerritos, Downey, Santa Fe Springs, Bellflower
- **Root:** `C:\Dev\CristianConstruction\`
- **Venv:** `C:\Dev\CristianConstruction\venv\` (independent)
- **Workspace:** `custom-agent.code-workspace`

---

## Architecture
FastAPI (port 8000) + 9 agents + React/Vite dashboard (port 3000) + Telegram bot

**Run:**
```powershell
# Backend
cd C:\Dev\CristianConstruction
.\venv\Scripts\Activate.ps1
uvicorn src.api.main:app --reload

# Dashboard
cd dashboard && npm run dev
```

---

## The 9 Agents

| File | Function |
|---|---|
| `lead_agent.py` | Inbound lead → classify, auto-reply, save CSV, Telegram notify |
| `quote_agent.py` | Job description → flat-rate estimate + materials list |
| `review_agent.py` | Job complete → review request + Telegram alerts |
| `social_agent.py` | Before/after → Nextdoor, Facebook, Instagram posts |
| `finance_agent.py` | Job logging, P&L, mileage, weekly tax summary |
| `schedule_agent.py` | Calendar booking, conflict detection, reminders |
| `proposal_agent.py` | Tier 3 project proposals (PDF-ready) |
| `reputation_agent.py` | Review responses + promotional campaigns |
| `referral_agent.py` | Referral tracking, credits, thank-you messages |

Routing: `sms_handler.py` (SMS keywords) + `telegram_handler.py` (/commands)
Shared: `claude_client.py` (claude-sonnet-4-6), `pricing.py`, `telegram.py`

---

## Data Layer — NEVER DELETE
```
data/jobs.csv       ← finance ledger
data/clients.csv    ← lead/client records
data/schedule.csv   ← job calendar
data/reviews.csv    ← review log
data/referrals.csv  ← referral tracking
```

---

## Pricing
| Service | Rate |
|---|---|
| Labor | $85–95/hr |
| Materials | Cost + 15% |
| Emergency/weekend | +25% |
| Referral credit | $25 |
| Tier 1 (solo) | $75–300 |
| Tier 2 (with helper) | $300–1,200 |
| Tier 3 | Quote-based |

---

## Brand Assets
| File | Purpose |
|---|---|
| `cc_landing.html` | Mobile landing page (QR code target) |
| `cc_door_hanger.html` | Print-ready door hanger |
| `cc_business_card.html` | Print-ready business card |
| `CA_logo_production.svg` | Main logo |
| `CA_logo_transparent.svg` | Transparent version |
| `CA_logo_white_truck.svg` | White truck variant |
| `vercel.json` | Vercel deploy config |

---

## Marketing Channels
| Channel | Status |
|---|---|
| Nextdoor | Profile exists — verify brand name is updated |
| Thumbtack | Setup status unconfirmed |
| Angi | Setup status unconfirmed |
| Facebook | Setup status unconfirmed |
| Instagram | Setup status unconfirmed |

---

## Legal & Insurance
| Item | Status |
|---|---|
| Business license | Week 1 task — **unconfirmed** |
| Public liability insurance | $30–45/mo estimated — **not confirmed purchased** |
| C-33 painting license | Researched — **not filed** |

---

## Wooden House Numbers
- **Status:** Ideation only — nothing built, priced, or listed
- Channels: Etsy, Shopify, real estate agent partnerships

---

## Open Tasks
1. Confirm business license filed
2. Purchase insurance or drop decision
3. Verify all marketing channels active
4. Build + price first wooden house number product
5. QR code → print 500 door hangers (~$40 Vistaprint)
6. Post first $75 off promo to Nextdoor
7. Lock first client booking

---

## Environment Variables
```
ANTHROPIC_API_KEY
TELEGRAM_BOT_TOKEN     # @CristianConstructionBot
OWNER_TELEGRAM_ID      # 7813563520
OWNER_PHONE            # +15622703452
BUSINESS_NAME
BUSINESS_CITY
GOOGLE_REVIEW_URL
```

---

## Connected Nodes
- [[CristianConstruction]] — domain root
- [[Navigation_Shortcuts]] — all project paths
