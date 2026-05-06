---
tags: [project, fastapi, react, construction, business-os, ca-book]
project: cristian-construction
status: functional
updated: 2026-05-01
parent: "[[Project_Directory]]"
---

# CristianConstruction — Custom Agent Business OS

> ⚠️ **DISAMBIGUATION**
> This node documents the **9-agent FastAPI business OS** at `C:\Dev\CristianConstruction\`.
> The **TTS audio companion** (`ca_audio.py`) lives at `C:\Dev\Projects\custom-agent\`.
> See [[Custom_Agent]] for that project.

9-agent AI-powered business operating system for Custom Agent Remodel & Skilltrade,
a construction and home services company in South Call, CA (Norwalk area).

---

## Identity

| Property | Value |
|---|---|
| Company | Custom Agent Remodel & Skilltrade |
| Location | South Call, CA (greater Norwalk/Cerritos area) |
| Business phone | (562) 270-3452 (Google Voice → iPhone) |
| Owner Telegram ID | 7813563520 |
| Telegram bot | @CristianConstructionBot |
| GitHub | `TititoBuilder/cristian-construction` (private) |
| Root path | `C:\Dev\CristianConstruction\` |

---

## Architecture

Hub-and-spoke service mesh. Event-driven — each agent waits for specific
event types (SMS keywords, Telegram commands, scheduled triggers).

| Layer | Tech | Port |
|---|---|---|
| Backend | FastAPI | 8000 |
| Frontend | React/Vite dashboard | 3000 |
| Agents | 9 agents in `src/agents/` | — |
| Data | CSV files in `data/` | — |
| Notifications | Telegram Bot API via httpx | — |

**Venv:** Shared with BDF — `C:\Dev\Projects\soccer-content-generator\venv\`
(do NOT create a separate CristianConstruction venv for agent work)

**Launch:**

```powershell
# T1 — backend
cd C:\Dev\CristianConstruction
& .\venv\Scripts\Activate.ps1   # NOTE: activates BDF venv path
uvicorn src.api.main:app --reload

# T2 — dashboard
cd dashboard && npm run dev
```

API docs: `http://localhost:8000/docs`

---

## The 9 Agents

| # | Agent | Trigger | Function |
|---|---|---|---|
| 1 | `lead_agent` | SMS keywords, web form | Classifies leads, auto-reply, saves to CSV, Telegram notification |
| 2 | `quote_agent` | Tier 1/2 requests | Flat-rate estimates + materials list (`max_tokens=4000`) |
| 3 | `review_agent` | Job completion | Review requests + Telegram alerts |
| 4 | `social_agent` | Scheduled / manual | Before/after posts for Nextdoor, Facebook, Instagram |
| 5 | `finance_agent` | Daily/weekly trigger | Job logging, P&L, mileage, weekly tax summary via Telegram |
| 6 | `schedule_agent` | Booking requests | Calendar booking, conflict detection, 24hr reminders |
| 7 | `proposal_agent` | Tier 3 requests | Full project proposals (`max_tokens=4000`) |
| 8 | `reputation_agent` | Review events | Review responses + promotional campaigns |
| 9 | `referral_agent` | Referral events | Referral tracking, $25 credits, thank-you messages |
| + | `sms_handler.py` | Incoming SMS | Routes SMS keywords to correct agent |
| + | `telegram_handler.py` | Telegram webhook | Routes `/commands` to agent endpoints |

**SMS Keywords:** `ESTIMATE` `TILE` `PAINT` `FLOOR` `BATH` `DEAL` `HELP` `STOP`

---

## Utils Layer

```
src/utils/
  claude_client.py    ← Shared Anthropic client (claude-sonnet-4-6) — used by all agents
  pricing.py          ← South Call rate sheet + service catalog
  telegram.py         ← Shared send_telegram() helper — used by all agents
```

---

## Code Conventions

- Type hints on ALL function signatures
- Google-style docstrings on all public functions
- Pydantic v2 models for all schemas
- `.env` for ALL secrets — never hardcode
- `os.getenv()` called at runtime **inside functions**, NOT at module level
- Log with `logging` module, not `print()`

---

## Running Tests

```powershell
pytest tests/ -v
```

---

## Pricing Model

| Tier | Range | Jobs |
|---|---|---|
| Tier 1 | $75–300 | Door repair, drywall patch, faucet, ceiling fan (solo) |
| Tier 2 | $300–1200 | Painting, tile, flooring, bathroom refresh (helper needed) |
| Tier 3 | $1200+ | Full remodel, ADU — formal proposal required |

Labor rate: $85–95/hr · Materials: cost + 15% · Emergency/weekend: +25%

---

## Brand Identity

| Property | Value |
|---|---|
| Logo letters | CA |
| Font | Bebas Neue |
| Gradient | amber `#F59E0B` → orange `#F97316` → red `#EF4444` |
| Background | `#0A0A0A` |
| Headline | GET IT FIXED NOW |
| "Cristian" | ONLY in client-facing auto-replies (personal trust signal) |
| All other contexts | Use brand name: "Custom Agent Remodel & Skilltrade" |

**Brand files in repo:**

| File | Purpose |
|---|---|
| `cc_landing.html` | Mobile landing page (single source of truth) |
| `cc_door_hanger.html` | Print-ready door hanger |
| `cc_business_card.html` | Print-ready business card |
| `CA_logo_production.svg` | Dark background version |
| `CA_logo_transparent.svg` | Transparent (Canva/shirts) |
| `CA_logo_white_truck.svg` | Dark panel for white Tacoma |

---

## CC-Landing (Project 4)

Live URL: `https://cc-landing-v2-eta.vercel.app`

> ⚠️ CC-Landing lives in its **own separate GitHub repo**: `TititoBuilder/cc-landing`
> It is NOT inside the `cristian-construction` repo.

| Item | Path |
|---|---|
| Source file | `C:\Dev\CristianConstruction\cc_landing.html` (edit here) |
| Deploy script | `C:\Dev\deploy-landing.ps1` |
| Dev watcher | `dev` alias in PowerShell profile |
| Vercel account | cristian's projects (TititoBuilder scope) |

Deploy workflow: edit `cc_landing.html` → run `C:\Dev\deploy-landing.ps1` → live in 30 seconds.

---

## Data Layer

```
C:\Dev\CristianConstruction\data\
  jobs.csv
  clients.csv
  schedule.csv
  reviews.csv
  referrals.csv
```

All gitignored.

---

## Environment Variables

File: `C:\Dev\CristianConstruction\.env` (gitignored)

| Variable | Notes |
|---|---|
| `ANTHROPIC_API_KEY` | Agent model calls |
| `TELEGRAM_BOT_TOKEN` | @CristianConstructionBot |
| `OWNER_TELEGRAM_ID` | `7813563520` |
| `OWNER_PHONE` | `+15622703452` |
| `BUSINESS_NAME` | Custom Agent Remodel & Skilltrade |
| `BUSINESS_CITY` | South Call, CA |
| `GOOGLE_REVIEW_URL` | — |
| `TWILIO_*` | Unused — Telegram used instead |

`env.example` tracked in git (placeholder values only).

---

## Critical Bug Fix History

| Bug | Fix |
|---|---|
| `lead_agent`: `notify_owner_of_lead()` defined but never called | Added call before return statement |
| `quote_agent` + `proposal_agent`: `max_tokens=1000` causing JSON truncation | Raised to 4000 with fallback |
| All agents: `os.getenv()` called at module level before dotenv loaded | Moved all `os.getenv()` inside functions |
| Telegram: entities parse error from special characters | Removed markdown from all Telegram payloads |

---

## Workspace

```
custom-agent.code-workspace
Path: C:\Dev\CristianConstruction\custom-agent.code-workspace
Multi-root: includes CristianConstruction AND custom-agent (TTS companion)
Each folder uses its own venv via .vscode\settings.json
```

---

## Pending

- [ ] Generate QR code → `cc-landing-v2-eta.vercel.app`
- [ ] Print 500 door hangers (~$40 Vistaprint)
- [ ] Post first $75 off promotion to Nextdoor
- [ ] Lock first client booking

---

## Connected to

- [[Custom_Agent]]
- [[Project_Directory]]
- [[Tools_Registry]]
- [[Session_Protocol]]
