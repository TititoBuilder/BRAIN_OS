# AGENT: CA Orchestrator

## Project
Custom Agent (CristianConstruction)

## Function
FastAPI backend that mounts all 9 business agents as independent routers and exposes a unified API for the React dashboard — routing inbound leads, quotes, job scheduling, social posts, finance logging, proposals, reputation management, referrals, and SMS keyword handling for a South Call, CA remodel & skilltrade business.

## Input
- HTTP requests from React dashboard (localhost:3000 → localhost:8000)
- SMS webhook payloads (Google Voice or Twilio) via `POST /sms/incoming`
- Telegram webhook for inbound client messages via `POST /reviews/webhook/telegram`
- Web form submissions and Thumbtack webhook payloads via `POST /leads/incoming`

## Output
- JSON API responses to dashboard for all 9 agent tabs
- Telegram messages to owner (lead alerts, booking confirmations, job completions, weekly P&L)
- Telegram messages to clients (24hr job reminders via ScheduleAgent)
- Google review request links sent to clients via ReviewAgent
- Social media post copy (Nextdoor, Facebook, Instagram) via SocialAgent → Telegram
- Formal proposal documents and flat-rate SMS quote texts via QuoteAgent/ProposalAgent
- CSV records appended to `data/jobs.csv`, `data/clients.csv`, `data/schedule.csv`, `data/reviews.csv`, `data/referrals.csv`

## Trigger
`uvicorn src.api.main:app --reload` — always-on during business hours; React dashboard is the primary interface.

## Tools and APIs
- [[Anthropic_Claude]] — `claude-sonnet-4-6` shared across all 9 agents via `src/utils/claude_client.py`; used for: tier classification, auto-replies, estimates, social posts, P&L insights, reminders, proposals, review responses
- [[Telegram_Bot]] — httpx direct (no library); all agents fire-and-forget to `TELEGRAM_BOT_TOKEN` + `OWNER_TELEGRAM_ID`; webhook at `POST /reviews/webhook/telegram`
- [[Twilio]] — optional SMS receive/send (TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN); not active — Telegram preferred
- [[Google_Voice]] — SMS webhook source for keyword-based lead capture

## Canonical file
C:\Dev\CristianConstruction\src\api\main.py

## Connected to
- [[LeadIntake]] workflow — SMSHandler → LeadAgent → ReviewAgent (Telegram alert)
- [[QuoteFlow]] workflow — QuoteAgent → ProposalAgent
- [[ScheduleFlow]] workflow — ScheduleAgent → ReviewAgent (reminders)
- [[FinanceReporting]] workflow — FinanceAgent → Telegram Sunday report
- [[SocialGeneration]] workflow — SocialAgent → Telegram for copy-paste publish
- [[Custom_Agent]] project

## Status
Live

## Mounted routers (9 agents + SMS handler)
| Route prefix | Agent | Key function |
|---|---|---|
| /leads | LeadAgent | Classify tier 1/2/3, Claude auto-reply, save clients.csv |
| /quotes | QuoteAgent | Claude flat-rate estimate + formal PDF-ready document |
| /reviews | ReviewAgent | Telegram notification hub, webhook handler, daily summary |
| /social | SocialAgent | Claude-generated Nextdoor/Facebook/Instagram posts via Telegram |
| /finance | FinanceAgent | Job logging, P&L, IRS mileage ($0.70/mi), tax summary |
| /schedule | ScheduleAgent | Booking, conflict detection, 24hr reminders, status lifecycle |
| /proposals | ProposalAgent | Tier 3 scope/timeline/payment proposals |
| /reputation | ReputationAgent | Review response drafting, review logging, promotions |
| /referrals | ReferralAgent | $25/referral credit, thank-you messages, leaderboard |
| /sms | SMSHandler | Keyword router: ESTIMATE/TILE/PAINT/FLOOR/BATH/DEAL/STOP |
