---
tags: [system, tools, infra, live]
---
# Tools registry

## Claude Code
- Type: CLI AI coding agent
- Version: installed globally via npm
- Launch: type "claude" or "cc" (alias) in any terminal
- Auto-accept: --dangerously-skip-permissions flag
  OR permissions.defaultMode: acceptEdits in settings.json
- Config: C:\Users\titit\.claude\settings.json (global)
- Project configs: .claude/settings.json in each project root
- GitHub: github.com/anthropics/claude-code

## Claude (claude.ai)
- Type: Web + desktop AI assistant
- Model: Claude Sonnet 4.6 (this session)
- MCPs connected: GitHub, Context7, Google Calendar, Gmail, Google Drive
- Projects: BRAIN_OS project (this conversation lives here)
- Role: System design, architecture decisions, canvas generation,
  node file generation prompts, debugging strategy

## Obsidian
- Type: Local markdown vault + visual canvas
- Vault: C:\BRAIN_OS\
- Key features: Canvas (Main_Canvas), Graph View (neural network),
  Quick switcher Ctrl+O, Full search Ctrl+Shift+F
- Version: latest stable
- Plugins: Canvas (core), Graph View (core)

## DaVinci Resolve
- Type: Professional video editor
- Machine: HP (OBS recording) + Predator (editing via MCP)
- MCP integration: resolve-mcp-server TCP:9000
- Export path: C:\BDF\renders\
- Log: export_log.jsonl (append-only)
- Version: Free (no Studio license)

## GitLens (VS Code extension)
- Type: Git history and blame overlay in VS Code
- Used for: tracking changes across all 4 projects

## SyncThing
- Type: LAN file sync
- Predator ID: PCUCH42-TPMQJKB-672R4EH-CDKYS2J
- HP ID: JUJFJ7O-IV7SIC5-65MDDGM-J75YYFA
- Shared folder: BDF-Clips
- Rule: Pause Surfshark VPN for LAN sync to work

## PowerShell
- Default terminal on Predator
- Key rule: never chain >> (use separate commands)
- Key rule: Select-String needs Get-ChildItem pipe, not -Recurse direct

## Connected to
- [[MCP_Registry]]
- [[Active_Environments]]
- [[DaVinci_Resolve_MCP]]
