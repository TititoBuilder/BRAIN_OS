---
tags: [workflow, live]
---

# WORKFLOW: CA Business OS Flow

## Project
CA (CristianConstruction)

## Flow
Inquiry (SMS / web form / Thumbtack) → Lead Agent → Quote Agent → Schedule Agent → Finance Agent → Review Agent → Reputation Agent

## Steps
1. **Inbound trigger** — SMS arrives via Google Voice/Twilio webhook (`POST /sms/incoming`); SMS Handler routes by keyword (`ESTIMATE` → Lead Agent; `TILE/PAINT/BATH` → Lead Agent pre-filled; `DEAL` → Reputation Agent)
2. [[CA_Orchestrator]] / **Lead Agent** (`POST /leads/incoming`) — classifies job tier (1/2/3) via `pricing.py`, generates auto-reply via Claude, saves lead to `data/clients.csv`, fires Telegram alert to owner via Review Agent
3. **Owner (dashboard gate)** — reviews lead at `localhost:3000`, clicks "Generate Quote"; triggers Quote Agent
4. **Quote Agent** (`POST /quotes/estimate`) — Claude analyzes job, computes labor range + materials list with 15% markup + 25% emergency surcharge if flagged; returns flat-rate SMS text; Tier 3 jobs → Proposal Agent instead
5. **Proposal Agent** (`POST /proposals/generate`) *(Tier 3 only)* — Claude writes full professional proposal (scope, materials, payment schedule, warranty); sends to owner via Telegram
6. **Schedule Agent** (`POST /schedule/book`) — books job, checks conflicts (Tier 1=3h, Tier 2=8h, Tier 3=16h blocks), saves to `data/schedule.csv`, sends Telegram confirmation; sends reminders 24h before
7. **Finance Agent** (`POST /finance/log-job`) — owner logs completion; records to `data/jobs.csv` (IRS format); computes mileage deduction ($0.70/mi), weekly P&L, monthly tax estimate; sends Sunday Telegram report
8. **Review Agent** (`POST /reviews/job-complete`) — sends client review request 24h after completion via Telegram (Claude-generated personalized message)
9. **Social Agent** (`POST /social/send-to-me`) — generates Nextdoor, Facebook, Instagram posts from before/after job description; delivers copy-paste text to owner via Telegram
10. **Reputation Agent** (`POST /reputation/alert`) — monitors incoming Google/Yelp/Thumbtack reviews; Claude drafts personalized response; logs to `data/reviews.csv`; tracks star rating trends
11. **Referral Agent** (`POST /referrals/register`) — registers referrer; on booking confirmation issues $25 credit automatically; maintains leaderboard in `data/referrals.csv`

## Trigger
Any of:
- SMS to Google Voice / Twilio webhook → `POST /sms/incoming`
- Owner submits lead form on dashboard at `localhost:3000`
- Thumbtack webhook (incoming inquiry)
- Owner manually triggers any agent via dashboard tab

## Output
- Telegram notifications to owner at each step
- CSV ledger entries: `data/clients.csv`, `data/jobs.csv`, `data/schedule.csv`, `data/reviews.csv`, `data/referrals.csv`
- Platform-specific social posts (Nextdoor / Facebook / Instagram) delivered to owner via Telegram
- Weekly P&L and monthly tax summaries sent to owner on schedule

## Rules and constraints
- **No agent-to-agent direct HTTP calls** — agents communicate via Telegram notifications and dashboard-triggered HTTP; owner is always in the loop
- **CSV flat-file persistence** — no database; `data/` directory files must never be deleted
- All 9 agents use shared `src/utils/claude_client.py` (claude-sonnet-4-6); one Anthropic client instance
- Telegram via httpx direct (no python-telegram-bot library); `TELEGRAM_BOT_TOKEN` + `OWNER_TELEGRAM_ID`
- Dashboard polls `GET /health` every 30s — must show "LIVE — 9 AGENTS" for all agents loaded
- FastAPI backend: `uvicorn src.api.main:app --reload` on port 8000; React+Vite dashboard on port 3000
- 15% materials markup and 25% emergency surcharge are hardcoded in `pricing.py` — change there, not in agent prompts
