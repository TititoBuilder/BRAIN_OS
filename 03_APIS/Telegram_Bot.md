# API: Telegram Bot

## Purpose
Hybrid deferred approval gate for BDF posts and direct messaging interface for CristianConstruction agents.

## Used by projects
- BDF, CA

## Limits and rules
- Rate limits: Telegram allows ~30 messages/sec per bot; background polling every 2s
- Cost: $0
- Legal constraints: none
- VPN (Surfshark) must be paused before every session — active VPN blocks Telegram API responses

## Credentials
- `TELEGRAM_BOT_TOKEN` (both projects)
- `TELEGRAM_CHAT_ID` (BDF — soccer-content-generator)
- `OWNER_TELEGRAM_ID` (CA — CristianConstruction)

## Connected agents
- [[BDF_Automation_Agent]]
- [[CA_Orchestrator]]

## Inputs

**BDF (python-telegram-bot library):**
- Bot: `@Boticris_1987bot`
- Flow: post generated → status=`pending` → heartbeat pushes to `approver._send_queue` → status=`telegram_pending` → phone tap approve/reject → status=`approved`/`rejected`
- Sends: text + inline keyboard (Approve / Reject buttons) + card image (optional)
- Background polling thread started by `TelegramApprover.start_background_polling()` in bot_service.py

**CA (httpx direct — no library):**
- `POST https://api.telegram.org/bot{TOKEN}/sendMessage`
- `POST https://api.telegram.org/bot{TOKEN}/getUpdates` (polling)
- Used for inbound commands and outbound notifications to construction business owner

## Outputs
- BDF: callback_query triggers `twitter_publisher.publish()` on approval
- CA: plaintext messages delivered to OWNER_TELEGRAM_ID
