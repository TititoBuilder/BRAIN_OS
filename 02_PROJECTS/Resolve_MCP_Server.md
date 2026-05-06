---
tags: [project, mcp, resolve, davinci]
project: resolve-mcp-server
status: active
updated: 2026-05-05
domain: Creative_Systems
---

# Resolve MCP Server

Two-process bridge: `server_api.py` (MCP stdio) + `resolve_bridge.py` (inside Resolve's Py3 console). Enables Claude to drive DaVinci Resolve Free via 31 MCP tools.

## Architecture
```
Claude → server_api.py (stdio) → TCP 127.0.0.1:9000 → resolve_bridge.py (inside Resolve)
```

## Key Paths
| Item | Path |
|---|---|
| Root | `C:\Users\titit\Projects\resolve-mcp-server\` |
| MCP server | `server_api.py` v10.8 (31 tools) |
| Bridge | `resolve_bridge.py` v16.10 |
| Venv | `venv\` (server_api.py only) |
| Renders | `C:\BDF\renders\` |
| Staging | `C:\BDF\renders\staging\` |
| Export log | `C:\BDF\renders\export_log.jsonl` |
| Clip library | `C:\BDF\library\` |
| GitHub | `TititoBuilder/resolve-mcp-server` (private) |

## Stack
Python 3.12.10 · `mcp` SDK · `httpx` · `anthropic` · `pyautogui` · `pywinauto` · `win32gui`

## Connection Type
**Lazy** — starts stdio loop immediately, shows Connected even when Resolve is offline. TCP bridge only attempted when tools are invoked.

## Bridge Reload (mandatory after any change)
```python
exec(open(r"C:\Users\titit\Projects\resolve-mcp-server\resolve_bridge.py", encoding="utf-8").read())
```
Expected banner: `Resolve API Bridge v16.10 - RUNNING`

## Component Versions
| File | Version | Role |
|---|---|---|
| server_api.py | v10.8 | 31 MCP tools, caption gen, export log |
| resolve_bridge.py | v16.10 | Socket listener inside Resolve |
| knowledge_enricher.py | v1.0 | TF-IDF threshold 0.6801 |
| mcp_ingest.py | v1.0 | export_log → LanceDB |

## Resolve Free Tier Constraints
- `IsRenderingInProgress()` returns None → wrap in `bool()`
- `SetFlagColor()` NoneType → try/except
- `DeleteRenderJobByUUID()` NoneType → try/except pass
- One job at a time — queue → render → poll → next
- Timeline starts at 01:00:00:00 = frame 216000 (START_FRAME)
- `SetRenderSettings` takes offsets not absolute frames

## Do NOT Run
- `resolve_bridge.py` standalone — must be exec'd inside Resolve's Py3 console
- `server.py` + `server_api.py` simultaneously — port conflict
- `nuclear_clear_all` without `save_markers` first

## .env Vars
```
ANTHROPIC_API_KEY
```

## Connected Nodes
- [[BDF_Canvas]]
- [[Creative_Systems]]
- [[Navigation_Shortcuts]]
