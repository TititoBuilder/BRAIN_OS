---
tags: [system, mcp, live]
---
# MCP Registry — all connected servers

## Active MCP servers

### Resolve MCP (local)
- Server: C:\Users\titit\Projects\resolve-mcp-server\server_api.py
- Transport: TCP PORT=9000
- Bridge: resolve_bridge.py
- GitHub: TititoBuilder/resolve-mcp-server
- Status: Live — 10/10 tools
- Used by: BDF Soccer Bot, Claude Code

### GitHub MCP
- Server: npx @modelcontextprotocol/server-github
- Scope: user-global (claude mcp add github -s user)
- Auth: GITHUB_PERSONAL_ACCESS_TOKEN env var
- Repos: TititoBuilder/soccer-content-generator, cristian-construction, BRAIN_OS, resolve-mcp-server
- Status: Live
- Used by: Claude Code — read/write all repos

### Context7 MCP
- Server: npx @upstash/context7-mcp
- Scope: user-global
- Purpose: Pulls live library docs into Claude Code context
- Status: Live
- Used by: Claude Code — active during migrations and new builds

### Google Calendar MCP
- URL: https://calendarmcp.googleapis.com/mcp/v1
- Status: Connected (claude.ai)

### Gmail MCP
- URL: https://gmailmcp.googleapis.com/mcp/v1
- Status: Connected (claude.ai)

### Google Drive MCP
- URL: https://drivemcp.googleapis.com/mcp/v1
- Status: Connected (claude.ai)

## Rules
- Pause Surfshark VPN before every BDF bot session
- Resolve MCP requires DaVinci Resolve to be open on Predator
- GitHub MCP token stored as Windows User env var
- Context7 activates automatically when Claude Code needs docs
