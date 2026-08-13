---
tags: [nav, resolve, mcp]
updated: 2026-05-05
commit: 503645c
---

# Resolve MCP Navigation

## Launch Sequence
```powershell
# Step 1 — Start MCP server (registered, auto-starts with Claude Code)
cd C:\Users\titit\Projects\resolve-mcp-server
claude

# Step 2 — Load bridge inside Resolve Py3 console
exec(open(r"C:\Users\titit\Projects\resolve-mcp-server\resolve_bridge.py", encoding="utf-8").read())
# Expected: Resolve API Bridge v16.10 - RUNNING
```

## Key Paths
| Item | Path |
|---|---|
| Code | `C:\Users\titit\Projects\resolve-mcp-server\` |
| Venv | `venv\` (server_api.py only) |
| MCP server | `server_api.py` v10.8 (31 tools) |
| Bridge | `resolve_bridge.py` v16.10 (inside Resolve) |
| Archive | `archive\` (rollback copies) |
| Renders | `C:\BDF\renders\` |
| Staging | `C:\BDF\renders\staging\` |
| Export log | `C:\BDF\renders\export_log.jsonl` |

## Architecture
```
Claude → server_api.py (stdio) → TCP 127.0.0.1:9000 → resolve_bridge.py (inside Resolve)
```
Connection type: **Lazy** — shows Connected even when Resolve offline

## Critical Rules
- NEVER run `resolve_bridge.py` standalone — exec inside Resolve Py3 only
- NEVER run `server.py` + `server_api.py` simultaneously
- NEVER call `nuclear_clear_all` without `save_markers` first
- Bridge reload requires `encoding="utf-8"` — omitting it = silent fail

## GitHub
HEAD: `503645c` — docs: add .env.template
