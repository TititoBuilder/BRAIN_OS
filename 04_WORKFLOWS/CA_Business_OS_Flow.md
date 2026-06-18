---
tags: [workflow, live]
---

# WORKFLOW: CA Business OS Flow

## Project
CA (CristianConstruction)

## Flow
Inquiry (SMS / web form / Thumbtack) → [[CA_Lead_Agent]] → [[CA_Quote_Agent]] → [[CA_Schedule_Agent]] → [[CA_Finance_Agent]] → [[CA_Review_Agent]] → [[CA_Reputation_Agent]]

## Steps
1. **Inbound trigger** — SMS arrives via Google Voice/Twilio webhook (`POST /sms/incoming`); SMS Handler routes by keyword (`ESTIMATE` → [[CA_Lead_Agent]]; `TILE/PAINT/BATH` → [[CA_Lead_Agent]] pre-filled; `DEAL` → [[CA_Reputation_Agent]])
2. [[CA_Orchestrator]] / [[CA_Lead_Agent]] (`POST /leads/incoming`) — classifies job tier (1/2/3) via `pricing.py`, generates auto-reply via Claude, saves lead to `data/clients.csv`, fires Telegram alert to owner via Review Agent
3. **Owner (dashboard gate)** — reviews lead at `localhost:3000`, clicks "Generate Quote"; triggers [[CA_Quote_Agent]]
4. [[CA_Quote_Agent]] (`POST /quotes/estimate`) — Claude analyzes job, computes labor range + materials list with 15% markup + 25% emergency surcharge if flagged; returns flat-rate SMS text; Tier 3 jobs → [[CA_Proposal_Agent]] instead
5. [[CA_Proposal_Agent]] (`POST /proposals/generate`) *(Tier 3 only)* — Claude writes full professional proposal (scope, materials, payment schedule, warranty); sends to owner via Telegram
6. [[CA_Schedule_Agent]] (`POST /schedule/book`) — books job, checks conflicts (Tier 1=3h, Tier 2=8h, Tier 3=16h blocks), saves to `data/schedule.csv`, sends Telegram confirmation; sends reminders 24h before
7. [[CA_Finance_Agent]] (`POST /finance/log-job`) — owner logs completion; records to `data/jobs.csv` (IRS format); computes mileage deduction ($0.70/mi), weekly P&L, monthly tax estimate; sends Sunday Telegram report
8. [[CA_Review_Agent]] (`POST /reviews/job-complete`) — sends client review request 24h after completion via Telegram (Claude-generated personalized message)
9. [[CA_Social_Agent]] (`POST /social/send-to-me`) — generates Nextdoor, Facebook, Instagram posts from before/after job description; delivers copy-paste text to owner via Telegram
10. [[CA_Reputation_Agent]] (`POST /reputation/alert`) — monitors incoming Google/Yelp/Thumbtack reviews; Claude drafts personalized response; logs to `data/reviews.csv`; tracks star rating trends
11. [[CA_Referral_Agent]] (`POST /referrals/register`) — registers referrer; on booking confirmation issues $25 credit automatically; maintains leaderboard in `data/referrals.csv`

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

## Connected to

### Project
- [[CristianConstruction]]

### Trigger
- [[Trigger_Telegram_Message]]

### Agents
- [[CA_Orchestrator]]
- [[CA_Lead_Agent]]
- [[CA_Quote_Agent]]
- [[CA_Proposal_Agent]]
- [[CA_Schedule_Agent]]
- [[CA_Finance_Agent]]
- [[CA_Review_Agent]]
- [[CA_Social_Agent]]
- [[CA_Reputation_Agent]]
- [[CA_Referral_Agent]]

### APIs / Memory
- [[CA_Knowledge_Book]]
- [[GoogleDrive_API]]
- [[Telegram_Bot]]
