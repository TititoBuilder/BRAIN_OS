---
tags: [agent, live]
---

# AGENT: BDF Automation Agent

## Project
BDF Soccer Bot

## Function
Silent background service orchestrator — starts SoccerBot (vector store + Claude), ClipWatcher (OneDrive → auto-caption → Telegram), ContentQueue, and TelegramApprover, then runs a 60s heartbeat that surfaces pending posts to Telegram for human approval.

## Input
- OneDrive folder watch — new clip files trigger ClipWatcher
- `src/queue/content_queue.json` — pending posts polled every 60s
- Telegram incoming messages (approval decisions from owner)
- SIGINT / SIGTERM — triggers clean shutdown + sentinel deletion

## Output
- Sentinel file `src/queue/clip_watcher_active.txt` — written on start, deleted on shutdown (dashboard `/clip_status` reads this)
- Telegram messages pushed to owner for each pending post
- `logs/bot_service.log` — rotating log of all service activity
- Twitter posts published after Telegram approval (via TelegramApprover)

## Trigger
Manual: `python bot_service.py`; runs continuously until Ctrl+C. Designed as a match-day background process alongside `python dashboard_api.py`.

## Tools and APIs
- [[SoccerBot]] — internal (vector store + Claude API connection); loaded at step 1
- [[ClipWatcher]] — internal (OneDrive folder monitor, auto-caption pipeline)
- [[TelegramApprover]] — internal; background polling; sends pending posts to owner, publishes on approval
- [[ContentQueue]] — internal; `content_queue.json`; tracks pending/telegram_pending/published states
- [[Twitter_X]] — publish target after Telegram approval
- [[LanceDB]] — `LANCE_DB_PATH` env var (default: `./lance_db_soccer`); doc count logged at startup

## Canonical file
C:\Dev\Projects\soccer-content-generator\bot_service.py

## Connected to
- [[BDF_Research_Agent]] — ScheduleManager queried for active content windows
- [[BDF_Analysis_Agent]] — SoccerBot wraps RagPipeline for retrieval
- [[BDF_Creative_Agent]] — ClipWatcher triggers image + caption pipeline
- [[BDF_Soccer_Bot]] project

## Status
Live

## Startup sequence
1. Load SoccerBot (VectorStore + Claude connection) — logs doc count
2. Load Twitter publisher (optional — warnings only if unavailable)
3. Load ContentQueue from `src/queue/content_queue.json`
4. Connect TelegramApprover + start background polling
5. Start ClipWatcher on OneDrive folder — write sentinel
6. Enter 60s heartbeat loop: log status, surface pending posts to Telegram
