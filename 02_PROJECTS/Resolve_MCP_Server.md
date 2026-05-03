---
tags: [resolve, mcp, davinci, pipeline, live]
project: resolve-mcp-server
status: live
updated: 2026-05-02
parent: "[[BDF_Canvas]]"
---

# Resolve MCP Server — DaVinci Resolve Bridge

Two-process MCP bridge that lets Claude drive DaVinci Resolve Free. `server_api.py` runs as an MCP stdio server and forwards tool calls over TCP 9000 to `resolve_bridge.py`, which executes them inside Resolve's own Python 3 console.

Root: `C:\Users\titit\Projects\resolve-mcp-server\`
GitHub: `TititoBuilder/resolve-mcp-server` (private)

---

## Business Value

Enables Claude Code to tag timeline markers, batch-export clips, and trigger the full BDF export pipeline without manual mouse/keyboard interaction in Resolve. The bridge translates MCP tool calls into Resolve's scripting API — the automation backbone of the BDF clip factory.

---

## Architecture

```
Claude (MCP client)
      │  stdio
      ▼
server_api.py  (MCP server, v10.8)
      │  TCP socket  127.0.0.1:9000
      ▼
resolve_bridge.py  (v16.10, running inside Resolve Py3 console)
      │  DaVinci Resolve scripting API  (fusion injected)
      ▼
DaVinci Resolve Free
```

**Two-process design is required** — the Resolve scripting API (`fusion.GetResolve()`) is only accessible from within Resolve's embedded interpreter. `server_api.py` runs as a normal Python process and communicates via socket.

---

## Stack

| Item | Detail |
|---|---|
| Language | Python 3.12.10 |
| MCP transport | `mcp` SDK — stdio (`server_api.py`) |
| Resolve API | `fusion.GetResolve()` (DaVinci built-in Py3) |
| IPC | TCP socket 127.0.0.1:9000 — JSON req/response per call |
| HTTP / AI | `httpx` + `anthropic` SDK (caption generation) |
| Keyboard I/O | `pyautogui`, `pywinauto`, `win32gui` |
| Knowledge | `knowledge_enricher.py` — TF-IDF cosine (threshold 0.6801) |
| Venv | `venv\` (server_api.py only; bridge runs in Resolve's Python) |

**Model standard:** `claude-sonnet-4-6`. Never `claude-opus-*`.

---

## Component Versions

| File | Version | Role |
|---|---|---|
| `server_api.py` | v10.8 | MCP server — 31 tools, caption generation, export log |
| `resolve_bridge.py` | v16.10 | Socket listener inside Resolve |
| `knowledge_enricher.py` | v1.0 | TF-IDF knowledge retrieval, threshold 0.6801 |
| `mcp_ingest.py` | v1.0 | Export-log → LanceDB ingestion (lives in BDF project) |
| `src/agent/pattern_detector.py` | — | Subject/pattern frequency tracking |
| `src/agent/memory.py` | — | Agent session memory |

---

## Starting the Bridge

Paste into the Resolve Py3 console (Workspace → Console → Py3 tab):

```python
exec(open(r"C:\Users\titit\Projects\resolve-mcp-server\resolve_bridge.py", encoding="utf-8").read())
```

Expected banner: `Resolve API Bridge v16.10 - RUNNING`

Socket protocol: each call is `{"tool": "<name>", "args": {...}}`. Bridge replies with a JSON object and closes the connection.

---

## Environment Variables

```
ANTHROPIC_API_KEY
```

All other credentials (Telegram, Twitter, LanceDB path) live in the soccer-content-generator `.env` and are consumed by `mcp_ingest.py`.

---

## Free Tier Constraints — Critical Engineering Notes

Every item was discovered through a broken render. Violations silently produce 1-frame outputs.

### Render queue resets on preset load
`LoadRenderPreset()` **resets the timeline I/O points**. Fix (v16): inside the batch loop, call `LoadRenderPreset` → `SetRenderSettings` → move playhead to in-frame → press `i` → move to out-frame → press `o` → `AddRenderJob` — all within the **same socket connection**, no gaps.

### One job at a time
Queuing multiple jobs then calling `StartRendering()` causes Resolve Free to re-read current timeline I/O at render time. Only the last job renders correctly. Fix: queue one job → `StartRendering()` → poll until done → queue next job.

### Timeline start offset (01:00:00:00)
`START_FRAME = 216000` = `01:00:00:00`. `SetCurrentTimecode` requires absolute timecode including start hour (e.g. `"01:00:00:09"`). Passing `"00:00:00:09"` silently fails — playhead does not move. `_frame_to_tc()` in the bridge handles conversion.

### SetRenderSettings takes offsets, not absolute frames
`MarkIn`/`MarkOut` must be timeline **offsets** (`frame - START_FRAME`), not absolute frame numbers. Passing absolute frames causes Resolve to interpret the range past timeline end → collapses to 1 frame. `_to_offset()` handles this.

### pyautogui keyboard I/O
Setting In (`i`) and Out (`o`) points uses `pyautogui` keypresses. Resolve must not be minimized. `win32gui.SetForegroundWindow` is called first; `pyautogui.click` on window center is the fallback. `fusion.Sleep(100)` between `i` and `o` lets Resolve register the In point.

### SetFlagColor on Free tier
`SetFlagColor()` may return `NoneType`. Bridge returns `{"status": "unsupported"}` rather than crashing.

---

## Export Pipeline

```
1. Tag markers: Cream=in, content markers, Cyan=out
2. batch_export_highlights  → bridge fires one render job per platform
3. poll_export_status       → poll every 5s until status=done
4. post_export_cleanup      → verify files → clear markers → flag Orange
                               → detect competition → write export_log.jsonl
                               → auto-route to library
5. mcp_ingest.py (BDF)      → reads export_log → enriches → captions → LanceDB
```

---

## Marker Conventions

| Color | Tag | Meaning |
|---|---|---|
| Cream | `in` | Export In point |
| Cyan | `out` | Export Out point |
| Red | `shot` | Shot on goal |
| Green | `goal` | Goal scored |
| Blue | `skill` | Skill move |
| Yellow | `assist` | Assist |
| Pink | `magic` | Magic moment |
| Purple | `legendary` | Legendary moment |
| Sky | `pro` | Professional-level play |
| Mint | `save` | Goalkeeper save |
| Cocoa | `defensive` | Defensive action |
| Orange | `buildup` | Build-up play |
| Rose | `reaction` | Reaction moment |
| Sand | `title` | Title card |
| Lemon | `slowmo` | Slow-motion |

White is automatically remapped to Cream by the bridge on write.

---

## Render Presets

| Preset name (case-sensitive) | Platform slug in filename |
|---|---|
| YouTube 1080p | `YouTube-1080p` |
| TikTok 1080p | `TikTok-1080p` |
| Instagram Reels | `Instagram-Reels` |
| Twitter 720p | `Twitter-720p` |
| Facebook 1080p | `Facebook-1080p` |

---

## Knowledge Enricher

`knowledge_enricher.py` uses TF-IDF cosine distance against a curated soccer knowledge corpus.

```python
facts = enrich(subject, content_type, competition)
# e.g. enrich("guler", "goal", "UCL")
```

`KNOWLEDGE_DISTANCE_THRESHOLD = 0.6801` — calibrated 2026-04-25.

Competition detection cascade: 1) explicit arg → 2) `_detect_competition(clip_name)` keyword scan → 3) `get_project_info` bridge call.

---

## Key Paths

| Path | Purpose |
|---|---|
| `C:\BDF\renders\export_log.jsonl` | Append-only export log |
| `C:\BDF\renders\staging\` | Render output staging area |
| `C:\BDF\renders\marker_snapshot.json` | Marker snapshot (save_markers / restore_markers) |
| `C:\BDF\library\` | Structured clip library |

---

## Do Not Run

| Action | Reason |
|---|---|
| `resolve_bridge.py` standalone | Requires Resolve's embedded interpreter — fails in normal shell |
| `server.py` + `server_api.py` simultaneously | Only one MCP server can bind stdio; duplicate tools in Claude Desktop |
| `nuclear_clear_all` | Irreversibly wipes all markers — call `save_markers` first |
| Scripts in `archive\` | Superseded planning scripts — do not execute |

---

## Connected to

- [[BDF_Canvas]]
- [[BDF_Agent_Pipeline]]
- [[BDF_Twitter_Publisher]]
- [[OBS_MCP_Server]]
- [[Tools_Registry]]
