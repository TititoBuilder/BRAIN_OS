# MCP Authentication ? How It Works

## Key file
C:\Users\titit\.claude.json ? global Claude Code config
This is where ALL MCP server connections are defined.
Not the repo-level .claude.json (that one is for project settings).

## Why it breaks
- GitHub auto-revokes PATs it detects in public pastes or logs
- Expired tokens (check expiration date when creating)
- Wrong format ? must be: Bearer TOKEN, not raw token

## Fix process
1. Go to https://github.com/settings/tokens/new
2. Scopes: repo + read:org
3. Note: brain-os-claude-code
4. Copy token (shown once only)
5. Open: notepad C:\Users\titit\.claude.json
6. Find Authorization key under mcpServers > github > headers
7. Replace value with: Bearer NEW_TOKEN
8. Save file
9. Restart Claude Code: close window, run claude in PowerShell
10. Verify: MCP server list shows github connected

## Verify token is valid before editing config
Invoke-WebRequest -Uri https://api.github.com/user -Headers @{Authorization="Bearer TOKEN"} | Select-Object -ExpandProperty StatusCode
Expected: 200

## Lesson
The config file is the single source of truth for MCP auth.
Editing it directly with notepad + restart is the reliable fix.
Never use Set-Content or PowerShell json tools on this file.
Always use Python json library or notepad for edits.
