---
tags: [canvas, bdf, pipeline, status]
project: BDF Soccer Bot
parent: "[[BDF_Soccer_Bot]]"
---

# BDF Canvas

Per-project canvas for the BreakingDown Futbol soccer content pipeline.

---

## Pipeline Status 2026-04-30

- OBS → `C:\Media\Recordings` (MKV, CQP 18, NVENC, 20sec replay buffer)
- `obs_relay.py` → `C:\BDF_Share` (direct on Predator, SyncThing on HP)
- `clip_watcher.py` → `src/queue/content_queue.json` (status=pending, no Telegram)
- DaVinci Resolve → `master_edit\ready\` → clip_watcher → queue
- Dashboard `localhost:5173` → Approve → Twitter
- Image pipeline: DALL-E DEPRECATED → DaVinci exports + card_composer.py
- LanceDB: `D:/lance_db_soccer` (WD Elements, always mounts as D: on Predator)
- WD Elements always mounts as `D:` on Predator (not `F:` — recovery partition blocks `F:`)

---

## Model standard — updated 2026-04-30
- All API calls: `claude-sonnet-4-6` (switched from claude-opus-4-5)
- Opus was 87.9% of April API bill ($17.79 of $20.25)
- Files updated: book_compiler.py, mcp_book_compiler.py, story_generator.py
- Projected saving: ~$17/month

---

## Active Scripts

| Script | Role | Status |
|---|---|---|
| `obs_relay.py` | Watches `C:\Media\Recordings`, renames + copies to BDF_Share | ✅ Active |
| `clip_watcher.py` | Watches BDF_Share + master_edit\ready\, injects to queue | ✅ Active |
| `trigger_watcher.py` | Watches `triggers\`, auto-generates content to queue | ✅ Active |
| `sync_brain.py` | Weekly health snapshot + git commit | ✅ Active |
| `dashboard_api.py` | REST API for dashboard | ✅ Active |
| `bot_service.py` | Background service runner | ✅ Active |

---

## Queue Flow

```
pending  →  [dashboard review]  →  approved  →  TwitterPublisher
                                 →  rejected
```

All clips enter queue as `status="pending"`. No auto-post.
Human approves in dashboard at `localhost:5173`.

---

## Resolved Issues

- `IsRenderingInProgress()` NoneType crash — guarded with `bool()` check (v10.8)
- One-job-at-a-time render queue enforced (Resolve Free constraint)
- Timeline start offset `01:00:00:00` handled by `_frame_to_tc()` in bridge
- `SetRenderSettings` uses offsets not absolute frames (`_to_offset()`)
- Opus cost spike April 2026 — all model calls switched to Sonnet (2026-04-30)

---

## Image Pipeline

**Current architecture (as of 2026-04-30): DaVinci Resolve exports + card_[composer.py](http://composer.py)**

| Stage | Tool |
|---|---|
| Video/clip editing | DaVinci Resolve (Free license) |
| Still frame export | DaVinci render bridge via `resolve-mcp-server` (TCP 9000) |
| Card compositing | `card_[composer.py](http://composer.py)` + Pillow |
| Output | Branded image cards saved to `src/images/cards/` (gitignored) |

> ⚠️ **DEPRECATED:** `gpt-image-1` (OpenAI image generation) was the previous
> image source. It was replaced by DaVinci exports. Any reference to `gpt-image-1`
> in old documentation or the cheat sheet is stale — do not restore.

The `card_[composer.py](http://composer.py)` takes DaVinci-exported stills and applies branding
overlays, text, and layout. Pillow handles all compositing. No external image
API calls in the current pipeline.

---

## Google Drive Sync

Both the BDF and CA book compilers share a **single Google OAuth credential**
living inside the BDF project root.

| File | Path |
|---|---|
| OAuth client | `C:\Dev\Projects\soccer-content-generator\gdrive_credentials.json` |
| OAuth token | `C:\Dev\Projects\soccer-content-generator\gdrive_token.json` |

Both files are gitignored. **Never duplicate them** — one Google account,
one token, both compilers reference the BDF path directly.

**BDF sync target (Google Drive):**

| Content | Drive path |
|---|---|
| Chapter audio (.mp3) | `BDF_Book_Audio\chapters\` |
| Session audio | `BDF_Book_Audio\` |

**CA sync target (Google Drive):**

| Content | Drive path |
|---|---|
| Chapter audio (.wav) | `CA_Book_Audio\chapters\` |
| Master book (.txt) | `CA_Book_Audio\CA_Master_Book.txt` |

CA sync fires automatically on every `ca-book` run.
For bulk CA re-sync (after major expansion): run `ca_bulk_[upload.py](http://upload.py)` from
`C:\Users\titit\Downloads\` using the BDF venv.

**Token refresh (applies to both compilers):**

```powershell
cd C:\Dev\Projects\soccer-content-generator
Remove-Item gdrive_token.json
python -c "import book_compiler; book_compiler.get_drive_service()"
# Browser opens → approve → token refreshed
```

---

## Dashboard

The BDF Command Center dashboard is a React SPA at `localhost:5173` (Vite dev server). In production, `npm run build` outputs to `dashboard/dist/` and FastAPI serves it via `StaticFiles`.

`dashboard_api.py` is the FastAPI backend on port 8000 with CORS open to ports 5173, 5174, and 3000. The dashboard has five tabs: Overview (KPI cards + health panel), Fixtures (upcoming matches with hype scores), Review Queue (approve/reject/edit), Players (cast statistics), and Analytics (competition breakdown).

The queue is a unified view of two sources: `content_schedule` in `src/soccer_bot.db` (SQLite, calendar-scheduled posts linked to fixture IDs) and `src/queue/content_queue.json` (posts from the terminal bot, `clip_watcher.py`, or `mcp_ingest.py`). Both are merged and sorted newest-first by `created_at`.

Approval workflow from the dashboard:

1. Post arrives as `status="pending"` from any source.
2. User opens Review Queue — sees content, title, hashtags, and character count.
3. **Approve** → `POST /queue/{post_id}/approve` → saves approval → card composition attempt → `TwitterPublisher.publish_tweet` → returns `tweet_url`.
4. **Reject** → `POST /queue/{post_id}/reject` → records `rejected_at`.
5. **Send to Telegram** → `POST /queue/{post_id}/send_telegram` → fires Telegram approval message → sets `status="telegram_pending"`.
6. **Sync Telegram** → `POST /telegram/sync` → polls for phone button taps → processes approvals and rejections in batch.

Content can be generated directly from the dashboard via `POST /generate` (SoccerBot engine) or `POST /api/generate` (fixture-linked). Both paths run the full image waterfall and return the new post immediately.

---

## Connected to
