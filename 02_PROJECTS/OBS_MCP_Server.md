---
tags: [project, mcp, obs]
project: obs-mcp-server
status: active
updated: 2026-05-05
domain: Creative_Systems
---

# OBS MCP Server

MCP server exposing OBS Studio controls (scene switching, recording, replay buffer) as tools callable by Claude. Connects via OBS WebSocket v5.

## Key Paths
| Item | Path |
|---|---|
| Root | `C:\Users\titit\Projects\obs-mcp-server\` |
| Server | `server_api.py` |
| Venv | `venv\` |
| GitHub | `TititoBuilder/obs-mcp-server` (private) |

## Stack
Python 3.12.10 · `mcp` · `obsws-python` · `python-dotenv`
OBS WebSocket v5 — port 4455

## Run
Registered as MCP server only — do NOT run `server_api.py` standalone (stdio protocol).
Entry point: `venv\Scripts\python server_api.py`

## Connection Type
**Eager** — attempts OBS connection at startup. Shows Failed in `claude mcp list` when OBS is not running.

## .env Vars
```
TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID
OBS_PASSWORD
```

## Connected Nodes
- [[Creative_Systems]]
- [[Navigation_Shortcuts]]
