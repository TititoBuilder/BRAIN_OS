---
tags: [bdf, pipeline, master, live]
project: soccer-content-generator
status: live
updated: 2026-05-02
parent: "[[Project_Directory]]"
---

> ⚠️ **CRITICAL DEADLINE — DALL-E 3 deprecation: May 12, 2026.**
> All `dall-e-3` model calls in this codebase must be migrated to `gpt-image-1` (via `images.edit()` for style transfer) before this date. Migration plan and checklist live in [[BDF_Avatar_Pipeline]]. Source: 20260315 style-transfer session compile.

# BDF Soccer Content Generator — Master Pipeline Overview

AI-powered pipeline that ingests football highlight clips from DaVinci Resolve, enriches them with semantic context from a LanceDB vector store, generates platform-specific captions via Claude, and routes finished posts through a Telegram approval flow to Twitter and other social platforms.

Root: `C:\Dev\Projects\soccer-content-generator\`

---

## Business Value

Automated content factory for the BDF soccer animation channel. Takes raw Resolve exports → published Twitter posts with zero manual caption writing. Handles marker tagging, clip export, caption enrichment, Telegram approval, and Twitter publishing end-to-end.

---

## Architecture Overview

Three interlocking components:

```
DaVinci Resolve
    ↓ MCP bridge (resolve-mcp-server, TCP 9000)
export_log.jsonl  (C:\BDF\renders\)
    ↓ mcp_ingest.py
LanceDB mcp_clips + soccer_knowledge tables
    ↓ caption generation (claude-sonnet-4-6)
content_queue.json
    ↓ Telegram approval flow
Twitter (tweepy v2 + v1.1 for media)
```

### Component 1 — DaVinci Resolve MCP Pipeline
- Root: `C:\Users\titit\Projects\resolve-mcp-server\`
- Bridge: `resolve_bridge.py` v16.10 — runs inside Resolve Py3 console
- MCP server: `server_api.py` v10.8 — 31 tools over stdio
- IPC: TCP socket 127.0.0.1:9000

### Component 2 — BDF Content System
- Root: `C:\Dev\Projects\soccer-content-generator\`
- Venv: `venv\`
- Vector store: LanceDB at `C:\lance_db_soccer\` (env: `LANCE_DB_PATH`)
- Queue: `src\queue\content_queue.json`
- Clip drop: `C:\BDF_Share\` (Clip Factory watcher monitors for `.mp4`)

### Component 3 — Integration Adapter
- File: `mcp_ingest.py`
- Reads: `C:\BDF\renders\export_log.jsonl` (append-only)
- State: `mcp_ingest_state.json` (watermark — prevents double-ingest)
- Writes to: LanceDB `mcp_clips` + `content_queue.json`

---

## Stack

| Item | Detail |
|---|---|
| Language | Python 3.12.10 |
| AI / captions | `anthropic` SDK — `claude-sonnet-4-6` |
| Vector store | `lancedb` + `sentence-transformers` |
| Queue / approval | `python-telegram-bot` |
| Web dashboard | `fastapi` + `uvicorn` (port 8000) |
| Social | `tweepy` (Twitter API v2 + v1.1 for media) |
| Media | `pyautogui`, `opencv-python` |
| Venv | `venv\` — always activate before running |

**Model standard:** Always `claude-sonnet-4-6`. Never `claude-opus-*` — Opus drove 87.9% of the prior API bill.

---

## Key Files

| Path | Role |
|---|---|
| `mcp_ingest.py` | Export-log → LanceDB ingestion + caption generation |
| `dashboard_api.py` | FastAPI dashboard backend (port 8000) |
| `telegram_approver.py` | Telegram approval gating layer |
| `src/twitter_publisher.py` | Twitter posting |
| `src/vector_store.py` | LanceDB query patterns |
| `lancedb_integrator.py` | LanceDB write patterns |
| `clip_parser.py` | Clip filename parser |
| `session_close.py` | Session archiver → BRAIN_OS |
| `sync_brain.py` | Weekly health snapshot + Telegram |
| `book_compiler.py` | BDF knowledge book compiler |
| `story_generator.py` | Soccer animation story scripts |
| `tts_local.py` | Kokoro TTS for chapter audio |

---

## Environment Variables

File: `.env` (never commit). Keys only:

```
ANTHROPIC_API_KEY
LANCE_DB_PATH
TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID
TWITTER_BEARER_TOKEN
TWITTER_API_KEY
TWITTER_API_SECRET
TWITTER_ACCESS_TOKEN
TWITTER_ACCESS_TOKEN_SECRET
OPENAI_API_KEY
HF_TOKEN
API_FOOTBALL_KEY
API_FOOTBALL_BASE_URL
FOOTBALL_DATA_API_KEY
FOOTBALL_DATA_BASE_URL
KLING_ACCESS_KEY
KLING_SECRET_KEY
NEWS_API_KEY
OBS_WS_PASSWORD
RAPIDAPI_KEY
YOUTUBE_API_KEY
PIXABAY_API_KEY
UNSPLASH_ACCESS_KEY
GOOGLE_MAPS_API_KEY
```

---

## Running the Pipeline

```powershell
# Activate venv (always first)
cd C:\Dev\Projects\soccer-content-generator
.\venv\Scripts\Activate.ps1

# Dashboard API (T1)
python dashboard_api.py

# Ingest new exports (T2)
python mcp_ingest.py

# Telegram approval bot (T3)
python bot_service.py
```

Dashboard docs: `http://localhost:8000/docs`

---

## Do Not Run

| Script | Reason |
|---|---|
| `bot_service.py` outside venv | Opens ports + starts Telegram poller; orphaned processes |
| `mcp_ingest.py` concurrently | No file lock — double-ingests export log |
| `mcp_ingest.py --rebuild` | Drops and rebuilds `mcp_clips` — confirm row count first |
| `nuclear_clear_all` MCP tool | Irreversibly clears all timeline markers |

---

## Marker Color Convention

| Color | Meaning |
|---|---|
| Cream / White | Export In |
| Cyan | Export Out |
| Blue | Skill |
| Green | Goal |
| Red | Shot |
| Pink | Magic |
| Purple | Legendary |
| Yellow | Review |
| Orange | Buildup |
| Rose | Reaction |
| Sand | Title |
| Lemon | Slowmo |

---

## BDF Queue Entry Schema

```json
{
  "id": "post_{12 hex chars}",
  "topic": "subject content_type description",
  "content_type": "hot_take",
  "platform": "twitter",
  "content": "Twitter caption max 270 chars",
  "title": "...",
  "hashtags": ["tag1", "tag2"],
  "status": "pending",
  "created_at": "YYYY-MM-DD HH:MM:SS",
  "cost": 0,
  "image_path": "C:\\BDF_Share\\filename.mp4",
  "source": "mcp_adapter"
}
```

---

## Library Structure

```
C:\BDF\library\
  players\{Subject}\{content_type}\
  teams\{Team}\{content_type}\
  international\{Competition}\{content_type}\
  themes\{theme}\
```

Filename: `{subject}_{content_type}_{description}_{YYYY-MM-DD}_{Platform-Slug}.mp4`

---

## Agent Evolution Roadmap (Option 4)

The current `mcp_ingest.py` is a stateless adapter. Target: stateful agent loop that:
1. **Remembers** everything via LanceDB (`mcp_clips` table)
2. **Notices patterns** — export frequency, caption style performance
3. **Searches `soccer_knowledge`** semantically before generating captions
4. **Suggests content angles** based on export history + knowledge trends
5. **Maintains session memory** across runs

---

## Milestones

<!-- Sources: 20260401_session_compile (ingested 2026-05-05) -->

| Date | Milestone |
|---|---|
| 2026-04-01 | Pipeline confirmed live end-to-end: Telegram tap → background thread (within 5s) → Twitter publish. @tititoluli1987 went 6 → 10 posts in-session after the asyncio fix in `telegram_approver.py`. |

---

## Known Fixes

<!-- Source: 20260318_session_compile (ingested 2026-05-05) -->

### GPT-4o quality/format 400 errors (2026-03-18)
The `images.generate()` call returned HTTP 400 when `quality="standard"` and `output_format="b64_json"` were used. Correct values are `quality="medium"` and `output_format="png"`.

```python
# WRONG (HTTP 400)
quality="standard", output_format="b64_json"

# CORRECT
quality="medium", output_format="png"
```

Confirmed working post-fix: `gpt4o_doue_1772141923.png` generated at $0.042 (Status 200).

### CostTracker.track_generation missing args (2026-03-18)
`CostTracker.track_generation()` signature added required `content_type` and `input_tokens` parameters. `soccer_bot.py` line 507 was patched to pass `content_type="generation"`. An error-detail logger was added in `media_agent.py` immediately before `raise_for_status()` so future API errors surface their response body.

---

## Connected to

- [[Resolve_MCP_Server]]
- [[OBS_MCP_Server]]
- [[BDF_Agent_Pipeline]]
- [[BDF_Twitter_Publisher]]
- [[LanceDB_Vector_Store]]
- [[Tools_Registry]]
- [[BRAIN_OS]]
