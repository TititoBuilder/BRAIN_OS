---
tags: [project, live]
---

# PROJECT: Custom Agent (CristianConstruction)

## Status
Active

## Brain Architecture coverage
- Input Layer: yes
- AI Agents: yes
- Workflows: yes
- Knowledge Graph: no
- Output Layer: yes
- Infrastructure: yes

## Root path
C:\Dev\CristianConstruction\

## GitHub
TititoBuilder/CristianConstruction

## Inputs
- Inbound SMS via Google Voice webhook or Twilio (keywords: ESTIMATE, TILE, PAINT, FLOOR, BATH, DEAL, STOP)
- Thumbtack webhook (new job inquiries)
- Web form submissions (name, phone, message, city, source)
- Nextdoor / Facebook / Instagram direct messages
- Telegram webhook — client messages routed to owner
- Before/after job descriptions (for social post generation)
- Book chapters at `C:\Knowledge\CA\CA_Book\chapters\*.md` (for audio synthesis)

## Active agents
- [[LeadAgent]] — classifies tier 1/2/3, generates Claude auto-reply, saves to `data/clients.csv`, fires owner Telegram alert
- [[QuoteAgent]] — job description → Claude flat-rate estimate + materials list + SMS-ready quote text + formal PDF document
- [[ReviewAgent]] — Telegram notification hub: owner lead alerts, client review requests 24hr after job, daily summaries, Telegram webhook handler
- [[SocialAgent]] — before/after job → Claude-generated Nextdoor, Facebook, Instagram posts delivered to owner via Telegram
- [[FinanceAgent]] — job logging, weekly/monthly/annual P&L, IRS mileage tracking ($0.70/mi), tax summary, Sunday Telegram report
- [[ScheduleAgent]] — calendar booking, conflict detection, 24hr reminders to owner + client, job status lifecycle (booked → in_progress → complete)
- [[ProposalAgent]] — Tier 3 project proposals with scope, timeline, payment schedule, materials breakdown — PDF-ready text via Telegram
- [[ReputationAgent]] — review response drafting, Google/Yelp/Thumbtack/Nextdoor/Facebook review logging, promotional campaigns
- [[ReferralAgent]] — referral tracking, $25 credit per converted referral, automated Telegram thank-you messages, leaderboard

## Connected APIs
- [[Anthropic_Claude]] — claude-sonnet-4-6 used by all 9 agents for: tier classification, auto-replies, estimates, social posts, P&L insights, reminder text, proposal drafting, review responses
- [[Telegram_Bot]] — httpx direct (no library); owner notifications, client reminders, daily/weekly reports, Telegram webhook for inbound messages
- [[Twilio]] — optional SMS receive/send (not active — Telegram preferred)
- [[Google_Voice]] — SMS webhook source for keyword-based lead capture (ESTIMATE, TILE, PAINT etc.)
- [[Kokoro_TTS]] — local Kokoro KPipeline (voice: af_heart) for book chapter audio synthesis (`ca_audio.py`)

## Outputs
- Telegram messages to owner: lead alerts, booking confirmations, job logged confirmations, daily job lists, weekly P&L reports, proposal text
- Telegram messages to clients: 24hr job reminders, Claude-generated friendly confirmations
- Google review request links sent to clients via Telegram after job completion
- Social media post copy (Nextdoor, Facebook, Instagram) delivered to owner via Telegram for copy-paste publish
- Formal proposal documents (plain text, PDF-ready) for Tier 3 projects
- Weekly P&L + annual IRS Schedule C tax summary (console + Telegram)
- WAV audio files at `C:\Knowledge\CA\CA_Book\audio\` from Kokoro TTS
- React dashboard at `http://localhost:3000` — all 9 agent tabs, health polling every 30s

## Workflows
- [[LeadIntake]] — SMS/web form → `POST /leads/incoming` → classify tier → Claude auto-reply → `data/clients.csv` → owner Telegram alert
- [[QuoteFlow]] — `POST /quotes/estimate` → Claude JSON estimate → SMS flat-rate text → `POST /quotes/formal` → proposal document
- [[JobComplete]] — `POST /reviews/job-complete` → mark done → schedule review request 24hr → send Google review link to client via Telegram
- [[ScheduleFlow]] — `POST /schedule/book` → conflict check → save `data/schedule.csv` → owner Telegram confirm → `POST /schedule/remind` daily at 8am → 24hr owner + client reminder
- [[FinanceReporting]] — `POST /finance/log-job` → compute markup + mileage deduction → `data/jobs.csv` → `POST /finance/report/send` Sunday 8am → weekly Telegram P&L
- [[SocialGeneration]] — before/after description → `POST /social/send-to-me` → Claude 3-platform posts → owner Telegram for instant copy-paste
- [[SMSRouter]] — `POST /sms/incoming` → keyword match → route to `lead_agent` or `reputation_agent` with pre-filled service context
- [[CABookAudio]] — `python ca_audio.py ch01_origin [...]` → strip markdown → Kokoro af_heart synthesis → `C:\Knowledge\CA\CA_Book\audio\chXX.wav`

## Key data files
- `data/jobs.csv` — finance ledger (NEVER DELETE)
- `data/clients.csv` — lead/client records (NEVER DELETE)
- `data/schedule.csv` — job calendar (NEVER DELETE)
- `data/reviews.csv` — review log (NEVER DELETE)
- `data/referrals.csv` — referral tracking (NEVER DELETE)
- `C:\Knowledge\CA\CA_Book\chapters\` — book chapter source markdown
- `C:\Knowledge\CA\CA_Book\audio\` — synthesized WAV audio output
- `C:\Dev\Projects\custom-agent\ca_audio.py` — Kokoro TTS chapter synthesizer
