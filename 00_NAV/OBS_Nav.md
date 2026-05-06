---
tags: [nav, obs]
updated: 2026-05-05
---

# OBS MCP Navigation

## Launch Sequence
```powershell
# OBS must be open FIRST — MCP is eager connection
# 1. Open OBS Studio manually
# 2. Verify WebSocket server enabled: Tools → obs-websocket Settings → port 4455
# 3. MCP auto-connects when Claude Code starts (registered at user scope)

cd C:\Users\titit\Projects\obs-mcp-server
claude
```

## Key Paths
| Item | Path |
|---|---|
| Code | `C:\Users\titit\Projects\obs-mcp-server\` |
| Venv | `venv\` |
| Server | `server_api.py` |

## Connection Type
**Eager** — shows `Failed` in `claude mcp list` when OBS is closed. Expected behavior.
Open OBS first, then start Claude Code.

## .env Required
```
OBS_PASSWORD=
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
```
