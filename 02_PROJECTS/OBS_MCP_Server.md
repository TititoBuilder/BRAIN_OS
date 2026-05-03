---
tags: [obs, mcp, recording, live]
project: obs-mcp-server
status: live
updated: 2026-05-02
parent: "[[Project_Directory]]"
---

# OBS MCP Server — OBS Studio Controller

MCP server exposing OBS Studio controls (scene switching, recording start/stop, replay buffer) as tools callable by Claude. Connects to OBS via WebSocket v5 and runs as a stdio-based MCP process.

Root: `C:\Users\titit\Projects\obs-mcp-server\`

---

## Business Value

Lets Claude trigger OBS recording and scene changes during clip capture sessions — enables the BDF workflow to start/stop recording without leaving Claude Code. Complements [[Resolve_MCP_Server]] by covering the capture side of the pipeline.

---

## Architecture

```
Claude (MCP client)
      │  stdio
      ▼
server_api.py  (obs-mcp-server)
      │  WebSocket  localhost:4455 (OBS WS v5)
      ▼
OBS Studio (running on desktop)
```

---

## Stack

| Item | Detail |
|---|---|
| Language | Python 3.12.10 |
| MCP transport | `mcp` SDK — stdio |
| OBS connection | `obsws-python` — WebSocket v5 (default port 4455) |
| Env | `python-dotenv` |
| Venv | `venv\` — `venv\Scripts\Activate.ps1` |

**Model standard:** `claude-sonnet-4-6`. Never `claude-opus-*`.

---

## Key Files

| File | Role |
|---|---|
| `server_api.py` | Single entry point — all MCP tools defined here |
| `.env` | OBS password + Telegram credentials |
| `venv/` | Python 3.12 venv |

---

## Environment Variables

```
TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID
OBS_PASSWORD
```

---

## Running

```powershell
# Do NOT run standalone — register as MCP server in claude_desktop_config.json
# MCP entry point:
venv\Scripts\python server_api.py
```

OBS must be running with WebSocket server enabled:
Tools → WebSocket Server Settings → Enable → port 4455 → set password.

---

## Gotchas

- OBS WebSocket v5 requires authentication. `OBS_PASSWORD` in `.env` must match the OBS WebSocket server password exactly.
- OBS must be running **before** the MCP server starts — tool calls fail with a connection error otherwise.
- No Anthropic API calls — this server is a pure control bridge.
- Running `server_api.py` in a normal terminal produces no useful output; it speaks MCP over stdio.

---

## Do Not Run Standalone

`server_api.py` speaks MCP over stdio. Run only as a registered MCP server via `claude_desktop_config.json` or equivalent. Invoke through Claude Code only.

---

## Connected to

- [[BDF_Canvas]]
- [[Resolve_MCP_Server]]
- [[Tools_Registry]]
