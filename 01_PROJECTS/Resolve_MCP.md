---
tags: [project, live]
---

# PROJECT: Resolve MCP Server (BDF)

## Status
Active

## Brain Architecture coverage
- Input Layer: yes
- AI Agents: yes
- Workflows: yes
- Knowledge Graph: yes
- Output Layer: yes
- Infrastructure: yes

## Root path
C:\Users\titit\Projects\resolve-mcp-server\

## GitHub
TititoBuilder/resolve-mcp-server

## Inputs
- MCP client (Claude Desktop / Claude Code) over stdio — tool calls drive all operations
- DaVinci Resolve internal Python API via TCP socket 127.0.0.1:9000 (resolve_bridge.py running inside Resolve Py3 console)
- `C:\BDF\renders\export_log.jsonl` — append-only export log; mcp_ingest.py watermarks its read position in `mcp_ingest_state.json`
- Timeline markers set manually or via tool calls (Cream=in, Cyan=out, color-coded content tags)
- Render output MP4 files landing in `C:\BDF\renders\staging\`

## Active agents
- [[KnowledgeEnricher]] — TF-IDF cosine retrieval against soccer knowledge corpus; threshold 0.6801; query = "{subject} {content_type} {competition}"
- [[SubjectMemory]] — reads export_log.jsonl to recall per-subject clip history; case-insensitive subject filter on first `_`-separated token
- [[PatternDetector]] — recency-weighted export frequency by subject (decay over 30 days); saturation detection at count >= 5 per content type; reads exclusively through SubjectMemory
- [[ClipNameParser]] — parses subject / content_type / description from filename stem patterns (e.g. `Mbappe_goal_UCL.mov`)

## Architecture History

### April 18, 2026 — UI Control Phase (11 → 52 tools)
First approach: pyautogui keyboard simulation to drive Resolve UI directly.
Expanded from 11 basic tools (play_pause, cut_at_playhead, ripple_delete) to 52 tools across
editing, audio, export, and color page controls. Git initialized: commit `1dbece3`.

This approach was superseded because pyautogui requires the Resolve window to be visible,
is brittle across Resolve versions, and cannot read state from the application.

### Current Architecture — TCP Bridge + BDF Intelligence (31 tools)
Replaced pyautogui with `resolve_bridge.py` running inside Resolve's own Python console,
connected via TCP 127.0.0.1:9000. This gives direct API access to timeline, media pool,
render queue, and marker state. Tools focus on BDF workflow intelligence (export, captions,
knowledge enrichment, LanceDB) rather than raw UI simulation.

---

## Connected APIs
- [[Anthropic_Claude]] — claude-haiku-4-5-20251001; called by both `generate_captions` (tool) and `mcp_ingest.py` for platform-specific captions; requires `ANTHROPIC_API_KEY` in env
- [[DaVinci_Resolve_API]] — internal Resolve Python scripting API; only accessible inside the Resolve Py3 console; accessed via resolve_bridge.py over TCP 127.0.0.1:9000
- [[LanceDB]] — local vector store at `C:\BDF\lancedb`; table `mcp_clips`; written by mcp_ingest.py

## Outputs
- Rendered MP4 files per platform in `C:\BDF\renders\staging\` → routed to `C:\BDF\library\{category}\{Subject}\{content_type}\`
- `C:\BDF\renders\export_log.jsonl` — one JSON entry per export run (clip_name, subject, competition, platforms, verified files, output_dir, timestamp)
- LanceDB clip records at `C:\BDF\lancedb` table `mcp_clips` (enriched with knowledge facts + captions)
- Platform captions: YouTube {title, description, hashtags}, TikTok <=150 chars, Instagram <=150 chars with emojis, Twitter <=270 chars
- `C:\BDF\renders\marker_snapshot.json` — timeline marker snapshot (save_markers / restore_markers)
- `mcp_ingest_state.json` — ingest watermark (last_processed_timestamp) stored next to mcp_ingest.py

## Workflows
- [[TagAndExport]] — add_named_marker (Cream in, content tags, Cyan out) → get_highlight_ranges (tag validation) → batch_export_highlights → poll_export_status every 5s → post_export_cleanup (verify + clear markers + Orange flag + write export_log)
- [[McpIngest]] — `venv/Scripts/python mcp_ingest.py`; reads new export_log entries since watermark → KnowledgeEnricher enrichment → Claude Haiku captions → LanceDB write; `--dry-run` flag for single-entry test
- [[ExportAllReady]] — export_all_ready scans V1 for all Cream+Cyan pairs and fires batch_export_highlights sequentially for each; dry_run=True by default
- [[PostExportCleanup]] — three-tier competition detection (explicit arg → _detect_competition(clip_name) → get_project_info bridge call) → verify files → clear timeline markers → set Orange flag → append export_log entry → route to library
- [[MarkerSnapshot]] — save_markers before cleanup (snapshot to marker_snapshot.json); restore_markers at session start

## Key file paths
| Path | Purpose |
|---|---|
| `server_api.py` | MCP server v10.8 — 31 tools, stdio transport, `mcp.server` SDK |
| `resolve_bridge.py` | Resolve API bridge v16.10 — TCP listener inside Resolve Py3 console |
| `mcp_ingest.py` | Ingest pipeline v1.0 — export_log → LanceDB + captions |
| `knowledge_enricher.py` | TF-IDF knowledge retrieval v1.0 — distance threshold 0.6801 |
| `src/agent/memory.py` | Subject-history recall from export_log.jsonl |
| `src/agent/pattern_detector.py` | Content frequency + saturation signals |
| `src/agent/knowledge_enricher.py` | Agent-facing enricher wrapper |
| `mcp_ingest_state.json` | Ingest watermark (last_processed_timestamp) |
| `C:\BDF\renders\export_log.jsonl` | Append-only export log |
| `C:\BDF\renders\staging\` | Render output landing zone |
| `C:\BDF\renders\marker_snapshot.json` | Marker snapshot for session persistence |
| `C:\BDF\lancedb` | LanceDB vector store — table: mcp_clips |
| `C:\BDF\library\` | Structured clip library — {category}/{Subject}/{content_type}/ |

## Tool registry (31 tools in server_api.py v10.8)
**Timeline inspection:** get_project_info, get_clips, get_all_markers, get_export_range, get_current_timecode, scan_timeline, get_flagged_clips, get_highlight_ranges

**Marker editing:** add_named_marker, delete_marker_at, tag_current_frame, nuclear_clear_all, save_markers, restore_markers

**Clip flags:** set_clip_flag, detect_clip_subject

**Render & export:** get_render_presets, set_render_preset, add_render_job, batch_export_highlights, poll_export_status, export_all_ready, estimate_render_time, validate_presets

**Post-export:** post_export_cleanup, export_quality_report, route_to_library, check_duplicate_export, clean_staging

**Library & log:** browse_library, session_summary

**AI:** generate_captions (Claude Haiku, styles: hype/analytical/storytelling/minimal)

## Bridge protocol
- Socket: TCP 127.0.0.1:9000, timeout 30s, one request per connection
- Request: `{"tool": "<name>", "args": {...}}` encoded as UTF-8 JSON
- Response: JSON object, connection closed after reply
- Start bridge: paste into Resolve Py3 console — `exec(open(r"C:\Users\titit\Projects\resolve-mcp-server\resolve_bridge.py", encoding="utf-8").read())`
- Expected banner: `Resolve API Bridge v16.10 - RUNNING`
- server_api.py calls bridge from thread-pool executor so async event loop is never blocked

## Resolve Free tier constraints (hard-won)
- `LoadRenderPreset()` resets I/O points — always set I/O AFTER loading preset, within the same socket connection
- Queue ONE job → StartRendering() → poll → queue next (multiple queued jobs collapse to 1 frame on Free tier)
- `MarkIn/MarkOut` in SetRenderSettings are timeline OFFSETS, not absolute frames (subtract START_FRAME=216000)
- `SetCurrentTimecode` requires absolute timecode including start hour (e.g. `"01:00:02:00"`, not `"00:00:02:00"`)
- `SetFlagColor()` may return NoneType on Free — bridge wraps in try/except, returns `{"status": "unsupported"}`
- pyautogui keyboard I/O (i/o keypresses) used for In/Out because Resolve Free has no reliable API for setting them — Resolve window must not be minimized
