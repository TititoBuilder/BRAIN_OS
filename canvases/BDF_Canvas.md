---
tags: [canvas, bdf, pipeline, status]
project: BDF Soccer Bot
parent: "[[BDF_Soccer_Bot]]"
---

# BDF Canvas

Per-project canvas for the BreakingDown Futbol soccer content pipeline.

---

## Pipeline Status 2026-04-29

- OBS → `C:\Media\Recordings` (MKV, CQP 18, NVENC, 20sec replay buffer)
- `obs_relay.py` → `C:\BDF_Share` (direct on Predator, SyncThing on HP)
- `clip_watcher.py` → `src/queue/content_queue.json` (status=pending, no Telegram)
- DaVinci Resolve → `master_edit\ready\` → clip_watcher → queue
- Dashboard `localhost:5173` → Approve → Twitter
- Image pipeline: DALL-E DEPRECATED → DaVinci exports + card_composer.py
- LanceDB: `D:/lance_db_soccer` (WD Elements, always mounts as D: on Predator)
- WD Elements always mounts as `D:` on Predator (not `F:` — recovery partition blocks `F:`)

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
