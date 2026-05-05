---
tags: [workflow, live]
---

# WORKFLOW: BDF Video Production Flow

## Project
BDF, Resolve MCP

## Flow
OBS (HP laptop) → SyncThing → mcp_ingest.py → Resolve → C:\BDF_Share

## Steps
1. **OBS on HP laptop** — records match footage to local disk
2. **SyncThing** — syncs recorded files from HP laptop to Resolve workstation over LAN
3. **DaVinci Resolve** — footage appears in media pool; editor (or Claude via MCP) places clips on timeline, sets markers (Cream=in, Cyan=out, content markers per BDF color convention)
4. [[Resolve_Editing_Agent]] — `batch_export_highlights` fires one render job per platform (YouTube 1080p, TikTok 1080p, Instagram Reels, Twitter 720p, Facebook 1080p); sequential one-job-at-a-time due to Resolve Free constraint
5. [[Resolve_Editing_Agent]] — `post_export_cleanup` verifies files, clears markers, flags clips Orange, detects competition, writes entry to `C:\BDF\renders\export_log.jsonl`
6. [[BDF_Memory_Agent]] — `mcp_ingest.py` detects new `export_log.jsonl` entries (watermarked by `mcp_ingest_state.json`), enriches with TF-IDF knowledge facts, generates captions via Claude Haiku, writes document to LanceDB (`C:\BDF\lancedb`)
7. Exported render files routed to `C:\BDF\library\{category}\{Subject}\{content_type}\`

## Trigger
New entry appended to `C:\BDF\renders\export_log.jsonl` by `post_export_cleanup`.

`mcp_ingest.py` must be run manually or on a schedule:
```bash
venv/Scripts/python mcp_ingest.py         # all new entries
venv/Scripts/python mcp_ingest.py --dry-run  # most recent only
```

## Output
- 5 platform-specific MP4 files per highlight clip in `C:\BDF\library\`
- Named: `{subject}_{content_type}[_{description}]_{YYYY-MM-DD}_{Platform-Slug}.mp4`
- LanceDB document in `mcp_clips` table with enriched caption and metadata
- `export_log.jsonl` entry with: subject, competition, content_type, clip_name, platform paths, timestamps

## Rules and constraints
- Resolve Free: one render job at a time — queuing multiple jobs causes I/O collapse to 1 frame
- `LoadRenderPreset()` resets I/O — must re-set in/out after every preset load (bridge v16.10 handles this)
- `MarkIn`/`MarkOut` in `SetRenderSettings` are timeline offsets, not absolute frames
- `SetCurrentTimecode` requires absolute TC including start hour (01:00:00:00 base)
- SyncThing must be running on both machines; Resolve window must not be minimized during export
- Bridge runs inside Resolve Py3 console on TCP 127.0.0.1:9000

## Kling AI Integration Notes

<!-- Source: 20260315_session_compile_story_kling (ingested 2026-05-05) -->

`kling_agent.py` connects to the Kling AI API for image-to-video animation of player avatars. Status as of 2026-03-15:

- **Web interface:** working — first successful test was a Haaland head-turn clip via the Kling web UI (50 free flames are available on a fresh account).
- **API:** blocked at HTTP 429 on the test account — no credits remaining. Production use requires a credit top-up before the API path is viable.
- **Image upload constraint:** Kling enforces a specific aspect ratio on image-to-video uploads. A Pillow resize script is included in the Kling agent codebase to coerce input PNGs to the accepted aspect ratio before upload — without it, uploads are silently rejected.
- **Avatar path discipline:** be aware of folder-name drift — Haaland avatars were saved under `haaland_concepts/` rather than the expected `haaland/`, and the agent looked in the wrong directory. Standardise the directory before running the agent.

For Kling cost economics ($0.14 image-to-video, $0.28 text-to-video, 5-second clips, model `kling-v1`, HS256 JWT auth) see [[BDF_Avatar_Pipeline]].

---

## Connected to
- [[DaVinci_Resolve_MCP]]
- [[Resolve_Export_Log]]
- [[BDF_Memory_Agent]]
