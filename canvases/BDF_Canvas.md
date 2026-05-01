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

## Image pipeline

The image pipeline produces branded 1200×675 PNG cards that are attached to Twitter posts. DALL-E was deprecated as of 2026-04-30; the current approach uses DaVinci Resolve exports and a custom card compositor.

`src/card_composer.py` is the compositing engine. Its public entry point is `compose_bdf_card(content_type, variant, headline, body, ...)`, which renders a finished card and saves it to `src/images/cards/`. The function supports five layout variants:

- **v1 (Bold Headline)** — Canvas split vertically: source image fills the left half, a dark panel fills the right half with a large headline and optional body text.
- **v2 (DaVinci Reference)** — Dark top panel (~33% height) holds BDF logo and headline; source image fills the lower two-thirds, separated by a 4-pixel accent bar. Default variant in the dashboard approval flow.
- **v3 (Stat Card)** — Fully dark background with up to three large stat boxes (number + label) across the top and a headline below. Used for player milestones.
- **v3b (Comparison Stat)** — Player photo fills the left 40% with a fade gradient. Right zone shows a giant number, arrow + comparison label, two subject rows with coloured bars, and a caption. Used for head-to-head comparisons.
- **v4 (Dual Team)** — Two team images split at the horizontal midpoint with a darkening overlay and a centre badge containing a score or "VS".

Accent colour is determined by `content_type`: hot_take = red, match_recap = orange, match_preview = cyan, tactical_analysis = purple, transfer_news = green. BDF logo watermark is sourced from `src/images/gallery/bdf_logo.png`. During dashboard generation, the `/generate` endpoint runs a waterfall: gallery matcher → ImageAgent → `compose_bdf_card` wrap → copies to `src/images/export/` for the `/media/` static route. The compositor has no external API dependencies — it uses Pillow, Windows system fonts (Arial Bold fallback chain), and the local logo file.

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
