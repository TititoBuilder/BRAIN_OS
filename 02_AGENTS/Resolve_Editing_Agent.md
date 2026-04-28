---
tags: [agent, live]
---

# AGENT: Resolve Editing Agent

## Project
Resolve MCP Server (BDF)

## Function
MCP server (31 tools) that lets Claude drive DaVinci Resolve via natural language — tagging timeline markers, firing multi-platform batch renders, polling render status, running post-export cleanup, generating captions, and managing the clip library — all over a TCP socket bridge to the Resolve Python console.

## Input
- MCP tool calls from Claude (stdio transport) — natural language commands routed to one of 31 tools
- DaVinci Resolve state via TCP 127.0.0.1:9000 (resolve_bridge.py running inside Resolve Py3 console)
- `C:\BDF\renders\export_log.jsonl` — read by session_summary, check_duplicate_export, browse_library
- `C:\BDF\renders\staging\` — render output landing zone; read by post_export_cleanup and export_quality_report

## Output
- Rendered MP4 files per platform in `C:\BDF\renders\staging\` → routed to `C:\BDF\library\{category}\{Subject}\{content_type}\`
- `C:\BDF\renders\export_log.jsonl` — one JSON entry per export (clip_name, subject, competition, platforms, verified, output_dir, timestamp)
- `C:\BDF\renders\marker_snapshot.json` — marker snapshot for cross-session persistence
- Platform captions (YouTube title/description/hashtags, TikTok, Instagram, Twitter) via Claude Haiku
- Telegram-friendly session summaries and export quality reports

## Trigger
Claude Desktop / Claude Code issues tool calls via stdio MCP transport. Bridge must be running first: paste `exec(open(r"C:\Users\titit\Projects\resolve-mcp-server\resolve_bridge.py", encoding="utf-8").read())` into Resolve Py3 console → banner: `Resolve API Bridge v16.10 - RUNNING`.

## Tools and APIs
- [[DaVinci_Resolve_API]] — internal Resolve Python scripting API; only accessible inside the Resolve Py3 console; accessed via TCP 127.0.0.1:9000 (timeout 30s, one request per connection, one JSON object per call)
- [[Anthropic_Claude]] — `claude-haiku-4-5-20251001` for `generate_captions` tool (styles: hype/analytical/storytelling/minimal); prompt caching on system message
- [[LanceDB]] — `C:\BDF\lancedb` table `mcp_clips`; written by mcp_ingest.py after export_log entry is created
- [[pyautogui]] — keyboard i/o keypresses for In/Out point setting (required because Resolve Free has no reliable API for I/O; Resolve window must not be minimized)

## Canonical file
C:\Users\titit\Projects\resolve-mcp-server\server_api.py (v10.8)
C:\Users\titit\Projects\resolve-mcp-server\resolve_bridge.py (v16.10)

## Connected to
- [[TagAndExport]] workflow — core editing loop: tag → batch_export → poll → cleanup
- [[BDF_Memory_Agent]] — post_export_cleanup writes export_log entry that mcp_ingest.py consumes
- [[Resolve_MCP]] project

## Status
Live

## Bridge protocol
- Transport: TCP 127.0.0.1:9000, SOCKET_TIMEOUT=30s, one connection per call
- Request: `{"tool": "<name>", "args": {...}}` UTF-8 JSON
- server_api.py calls bridge from thread-pool executor (never blocks async event loop)
- server_api.py communicates the opposite direction to Claude via stdio MCP transport

## 31 tools by category
**Timeline inspection (8):** get_project_info, get_clips, get_all_markers, get_export_range, get_current_timecode, scan_timeline, get_flagged_clips, get_highlight_ranges

**Marker editing (6):** add_named_marker, delete_marker_at, tag_current_frame, nuclear_clear_all, save_markers, restore_markers

**Clip flags (2):** set_clip_flag, detect_clip_subject

**Render & export (6):** get_render_presets, set_render_preset, add_render_job, batch_export_highlights, poll_export_status, export_all_ready

**Quality & time (3):** estimate_render_time, export_quality_report, validate_presets

**Post-export (4):** post_export_cleanup, route_to_library, check_duplicate_export, clean_staging

**Library & log (2):** browse_library, session_summary

**AI (1):** generate_captions

## Resolve Free tier constraints
- `LoadRenderPreset()` resets I/O — always set I/O within same socket connection, after preset load
- One job at a time: queue → StartRendering() → poll → next (multiple queued jobs collapse to 1 frame)
- `MarkIn/MarkOut` are timeline OFFSETS, not absolute frames (subtract START_FRAME=216000)
- `SetCurrentTimecode` requires full absolute timecode `"01:00:02:00"` — relative `"00:00:02:00"` silently fails
