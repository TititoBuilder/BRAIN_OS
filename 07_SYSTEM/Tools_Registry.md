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

## obs_relay.py
- Type: Multi-machine OBS clip bridge
- Location: `C:\Dev\Projects\soccer-content-generator\obs_relay.py`
- Watches: `C:\Media\Recordings` (OBS replay buffer output)
- Routes to: `C:\BDF_Share` (direct on Predator) · SyncThing folder on HP
- Machine detection: hostname `CRISTIAN` = Predator (direct); any other = HP (SyncThing)
- Usage: `python obs_relay.py --match UCL_Atletico_Arsenal`

## clip_watcher.py
- Type: Clip Factory pipeline engine
- Location: `C:\Dev\Projects\soccer-content-generator\clip_watcher.py`
- Watches: `C:\BDF_Share` (AUTO track) · `master_edit\ready\` (MASTER EDIT track)
- Output: injects to `src/queue/content_queue.json` with `status=pending`
- Telegram: optional (wrapped in try/except) — dashboard is primary approval UI
- Usage: standalone `python clip_watcher.py` or imported by `bot_service.py`

## trigger_watcher.py
- Type: Match-day content trigger system
- Location: `C:\Dev\Projects\soccer-content-generator\trigger_watcher.py`
- Watches: `triggers\` folder (polls every 10s)
- File format: `{content_type}_{topic}.txt` e.g. `hot_take_Atletico_Arsenal_goal.txt`
- Output: SoccerBot-generated content injected to queue as `status=pending`
- Usage: `python trigger_watcher.py` · `--once` flag for single pass

## sync_brain.py
- Type: Weekly system health snapshot
- Location: `C:\Dev\Projects\soccer-content-generator\sync_brain.py`
- Collects: queue counts, weekly cost, LanceDB doc count, git status, clip stats
- Output: `data/brain_sync_{YYYY-MM-DD}.json` + git commit
- Usage: `python sync_brain.py` · `--no-commit` to skip git

## obs_mcp.py
- Type: OBS WebSocket v5 controller (FastAPI + importable class)
- Location: `C:\Dev\Projects\soccer-content-generator\obs_mcp.py`
- Library: `simpleobsws` 1.4.x — replaces broken `obsws-python` (v4 only)
- Port: 8001 · WebSocket: `ws://localhost:4455` · Password: `OBS_WS_PASSWORD` in `.env`
- Endpoints: `/obs/status` · `/obs/save_replay` · `/obs/start_replay_buffer` · `/obs/stop_replay_buffer` · `/obs/start_recording` · `/obs/stop_recording` · `/obs/set_scene`
- Import: `from obs_mcp import OBSController`
- Usage: `python obs_mcp.py`

## Connected to
- [[MCP_Registry]]
- [[Active_Environments]]
- [[DaVinci_Resolve_MCP]]
