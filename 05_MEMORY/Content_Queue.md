---
tags: [memory, live]
---

# MEMORY: Content Queue

## Purpose
Single source of truth for all BDF tweet candidates — tracks every generated post from creation through Telegram approval to published or rejected state.

## Type
Append-log JSON file — structured pipeline state store

## Location
**Canonical path:** `C:\Dev\Projects\soccer-content-generator\src\queue\content_queue.json`
**Manager class:** `ContentQueue` in `content_queue.py` (project root)
**Sentinel file:** `src/queue/clip_watcher_active.txt` — written by `bot_service.py` on start, deleted on clean shutdown; dashboard `/clip_status` endpoint reads this to show watcher live/offline

## Post status lifecycle
```
pending → telegram_pending → approved → [published]
                           → rejected
```
- `pending` — generated, not yet sent to Telegram
- `telegram_pending` — sent to Telegram, awaiting phone tap
- `approved` — owner tapped Approve; `twitter_publisher.py` fires
- `rejected` — owner tapped Reject; post archived, not published

## Connected to

### Project
- [[BDF_Operations_Status]]

### Written by
- [[BDF_Automation_Agent]] — writes `pending` entries; updates status through full lifecycle
- [[BDF_Creative_Agent]] — generated captions are packaged into queue entries

### Read by
- [[BDF_Automation_Agent]] — 60s heartbeat scans for `pending` posts, pushes to Telegram
- `dashboard_api.py` — serves queue view at `http://localhost:5173`

### Workflows
- [[BDF_Content_Research_Flow]] — creates new entries with status=`pending`
- [[BDF_Social_Media_Flow]] — reads queue and drives posts through Telegram approval

## Rules
- **NEVER duplicate this file** — it is the single source of truth; copying or syncing it to another location creates split state where the service and dashboard see different queues
- **Never write to it directly** — always use `ContentQueue` class methods; raw JSON edits risk schema corruption
- `bot_service.py` must be running for heartbeat to push `pending` posts to Telegram; posts accumulate silently without it
- Queue path is hardcoded in `bot_service.py` as `PROJECT_ROOT / "src" / "queue" / "content_queue.json"` — do not move the file
- `dashboard_api.py` reads this file to serve the dashboard queue view; both processes share the same path

## Status
Active. Managed by bot_service.py heartbeat loop (60s interval). Dashboard at `http://localhost:5173` reads queue via `dashboard_api.py`.
