---
tags: [workflow, live]
---

# WORKFLOW: BDF Social Media Flow

## Project
BDF

## Flow
content_queue.json → Telegram approval → twitter_publisher.py → Twitter

## Steps
1. [[BDF_Automation_Agent]] — heartbeat loop (every 60s) scans `content_queue.json` for posts with status=`pending`; pushes each to `approver._send_queue` and flips status to `telegram_pending`
2. [[BDF_Automation_Agent]] — `TelegramApprover` sends post to `@Boticris_1987bot` via python-telegram-bot: text preview + inline keyboard (Approve / Reject) + card image if available
3. **Phone (human gate)** — owner taps Approve or Reject on Telegram
4. [[BDF_Automation_Agent]] — callback_query handler receives decision; on Approve: calls `twitter_publisher.publish()` and flips status to `approved`; on Reject: flips to `rejected`
5. [[BDF_Creative_Agent]] — `twitter_publisher.py` uploads card image via tweepy API v1.1 `media_upload()`, then posts text + media_id via tweepy v2 `create_tweet()`

## Trigger
Post enters `content_queue.json` with status=`pending` (written by BDF_Content_Research_Flow or manually via dashboard).

## Output
Published tweet on @BreakingDownFutbol Twitter account with card image attached.

## Rules and constraints
- **200-char hard cap**: enforced in three places — at prompt construction, at `create_tweet_text()` truncation, and shown in dashboard UI character counter; stricter than Twitter's 280-char limit
- **No broadcast footage**: only composed card images (1200×675 PNG) may be attached — no raw video clips; DMCA risk from broadcast rights holders
- **Max 3 hashtags** per post — enforced in caption generator
- **VPN**: Surfshark must be paused before every session — active VPN blocks Telegram API responses
- **Approval required**: no post may reach Twitter without explicit phone tap; no auto-publish path exists
- `bot_service.py` must be running for the background polling thread to be active

## Image Pipeline — 5-Source Strategy

<!-- Source: 20260401_session_compile (ingested 2026-05-05) -->

Card images attached to BDF posts are sourced via a waterfall of five providers, evaluated in priority order. The pipeline picks the first source that yields a relevant, rights-clear image; later sources are fallbacks.

| Order | Source | Type | Notes |
|---|---|---|---|
| 1 | Pixabay | stock | Free tier, soccer search terms |
| 2 | Unsplash | stock | Free tier, broader sport imagery |
| 3 | NewsImageAgent | news scrape | Pulls `og:image` from ESPN, Sky Sports, BBC Sport, Goal.com |
| 4 | DALL-E 3 (→ gpt-image-1 by 2026-05-12) | generative | Style-transfer card art; see [[BDF_Avatar_Pipeline]] |
| 5 | Kling AI | generative video | Animated clips for hero posts only |

### Experiment scripts (image-source evaluation)

| Script | Purpose | Output |
|---|---|---|
| `experiment1_pixabay.py` | Probe Pixabay for 5 soccer search terms; download top 3 images per term | `test_results/experiment1/` |
| `experiment2_news_images.py` | Scrape `og:image` from ESPN/Sky Sports/BBC Sport/Goal.com for Mbappe / Haaland / Yamal / Real Madrid vs Man City | `test_results/experiment2/` |

Run-time install required for the news scraper: `pip install beautifulsoup4 pillow --break-system-packages`.

### Visual Review Workflow

Two-stage review before publish: (1) terminal preview prints chosen image path so the operator can sanity-check the file before sending; (2) Telegram approval message attaches the composed card so the final visual is what gets approved, not a placeholder.

---

## Connected to
- [[Telegram_Bot]]
- [[Twitter_API_v2]]
- [[Content_Queue]]
