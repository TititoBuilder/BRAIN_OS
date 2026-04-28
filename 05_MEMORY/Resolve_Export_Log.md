---
tags: [memory, live]
---

# MEMORY: Resolve Export Log

## Purpose
Append-only audit trail of every clip exported from DaVinci Resolve — the handoff point between the Resolve video production pipeline and the mcp_ingest enrichment pipeline.

## Type
Append-only JSONL file — one JSON object per line, never overwritten

## Location
**Export log:** `C:\BDF\renders\export_log.jsonl`
**Watermark file:** `C:\Users\titit\Projects\resolve-mcp-server\mcp_ingest_state.json` — stores timestamp of last processed entry; mcp_ingest.py skips entries at or before this timestamp
**Sidecar files:** `{clip_name}.meta.json` written alongside each `.mp4` in the render staging area at `C:\BDF\renders\staging\`
**Render staging:** `C:\BDF\renders\staging\`
**Library destination:** `C:\BDF\library\{category}\{Subject}\{content_type}\`

## Written by
`post_export_cleanup` tool in `server_api.py` (v10.8) — fires automatically after each successful render batch. Each entry contains:
- `subject` — player or team name
- `competition` — detected via 3-tier cascade: explicit arg → `_detect_competition(clip_name)` → `get_project_info` from bridge
- `content_type` — goal / skill / assist / save / defensive / extended / compilation / reaction
- `clip_name` — base filename without platform suffix
- `platform_paths` — dict of `{platform_slug: absolute_path}` for all 5 render variants
- `exported_at` — ISO timestamp

## Read by
`mcp_ingest.py` — reads all entries with `exported_at` > watermark in `mcp_ingest_state.json`; runs 8-step enrichment pipeline per entry; advances watermark on completion.

```bash
venv/Scripts/python mcp_ingest.py          # process all new entries
venv/Scripts/python mcp_ingest.py --dry-run  # most recent entry only, no writes
```

## Connected agents
- [[Resolve_Editing_Agent]]
- [[BDF_Memory_Agent]]

## Rules
- **Append-only** — never edit or delete lines; the watermark in `mcp_ingest_state.json` is the only mechanism for tracking what has been ingested; editing past entries will cause re-ingestion or skipping
- **Never reset `mcp_ingest_state.json`** unless you intend to re-ingest all entries from the beginning (creates duplicate LanceDB documents)
- Sidecar `.meta.json` is written per render alongside the MP4 — both files travel together when moving to library
- Competition field populated by 3-tier cascade — if detected incorrectly, pass explicit `competition` arg to `post_export_cleanup`
- `COMPETITION_MAP` in `server_api.py` lists all supported competition keywords for detection

## Status
Active. Written after every `batch_export_highlights` + `post_export_cleanup` cycle. mcp_ingest.py must be run manually to advance the watermark.
