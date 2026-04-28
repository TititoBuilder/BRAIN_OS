---
tags: [agent, mcp, live]
---
# AGENT: DaVinci Resolve MCP

## Project
Resolve MCP + BDF Soccer Bot

## Function
Controls DaVinci Resolve from Claude Code via TCP bridge — timeline, 
color grading, render queue, media pool, markers, clip export.

## Transport
TCP PORT=9000 — resolve_bridge.py connects to server_api.py

## Canonical files
C:\Users\titit\Projects\resolve-mcp-server\server_api.py (v10.7)
C:\Users\titit\Projects\resolve-mcp-server\resolve_bridge.py

## Input
- export_log.jsonl render events
- Claude Code MCP tool calls

## Output
- Rendered mp4 files
- .meta.json sidecar per render
- export_log.jsonl entries
- C:\BDF_Share mp4 drop

## MCP tools available
add_marker, add_render_job, get_clips, get_project_info,
move_playhead, set_clip_flag, scan_timeline, tag_current_frame,
batch_export_highlights, post_export_cleanup, session_summary

## Status
Live — 10/10 tools active

## Connected to
- [[BDF_Video_Production_Flow]]
- [[BDF_Memory_Agent]]
- [[Resolve_Export_Log]]
