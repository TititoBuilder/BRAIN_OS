---
tags: [system, tools, infra, live]
---
# Tools registry

> **Rule — before acquiring any new tool:**
> Check this file first. If a tool already exists that covers the need, use it.
> Example: we wasted 30min on Gmail SMTP + ntfy when Telegram was already here.

---

## Notification standard
- **Tool: Telegram** (existing bot — `clip_watcher.py`)
- Token: `TELEGRAM_BOT_TOKEN` in `.env`
- Chat ID: `TELEGRAM_CHAT_ID` in `.env`
- Rule: ALL system alerts route through this bot. No new notification services.
- Do NOT use: Gmail SMTP, ntfy, Slack, or any other service unless Telegram is broken.

---

## claude_monitor.py
- Type: Claude API cost monitor + budget alert
- Location: `C:\BRAIN_OS\03_APIS\claude_monitor.py`
- Config: `C:\BRAIN_OS\03_APIS\.env`
- Input: CSV exported from console.anthropic.com → Cost → Export
- Output: terminal report grouped by model + Telegram alert on budget breach
- Alerts: fires when daily > $5 or monthly projection > $20
- Notification: Telegram (same bot as soccer pipeline)
- Schedule: run on 1st of each month after exporting CSV
- Calendar event: "Export Claude CSV + Run Cost Monitor" — recurring monthly
- Usage:
  ```
  cd C:\BRAIN_OS\03_APIS
  python claude_monitor.py
  ```
- Lesson learned: Opus 4.5 = 87.9% of API bill. Always default to Sonnet.

---

## Claude Code
- Type: CLI AI coding agent
- Version: installed globally via npm
- Launch: type "claude" or "cc" (alias) in any terminal
- Auto-accept: --dangerously-skip-permissions flag
  OR permissions.defaultMode: acceptEdits in settings.json
- Config: C:\Users\titit\.claude\settings.json (global)
- Project configs: .claude/settings.json in each project root
- GitHub: github.com/anthropics/claude-code
- Cost rule: use Sonnet by default. Opus only for hard architecture decisions.
- Permission rule: never use Bash(*) or Read(*) wildcards — scope to project dir only
- .claudeignore: always add to projects to prevent large files bloating context

---

## Claude (claude.ai)
- Type: Web + desktop AI assistant
- Model: Claude Sonnet 4.6 (this session)
- MCPs connected: GitHub, Context7, Google Calendar, Gmail, Google Drive
- Projects: BRAIN_OS project (this conversation lives here)
- Role: System design, architecture decisions, canvas generation,
  node file generation prompts, debugging strategy

---

## Obsidian
- Type: Local markdown vault + visual canvas
- Vault: C:\BRAIN_OS\
- Key features: Canvas (Main_Canvas), Graph View (neural network),
  Quick switcher Ctrl+O, Full search Ctrl+Shift+F
- Version: latest stable
- Plugins: Canvas (core), Graph View (core)

### Obsidian MCP
- Status: ✅ Operational (fixed 2026-05-03)
- Tools: 11 (create-note, read-note, edit-note, search-vault, etc.)
- Config: `npx -y obsidian-mcp C:\BRAIN_OS`
- **Fix applied:** Was registered as "obs-mcp" (wrong package) - corrected to "obsidian-mcp"
- **Naming confusion:** "obs" = OBS Studio (streaming), "obsidian" = Obsidian (notes)

---

## Edge TTS
- Type: Microsoft text-to-speech service
- Engine: Microsoft Edge TTS (cloud, free)
- Voice: en-US-GuyNeural (male, American English, natural-sounding)
- Rate: -5% (slightly slower for learning comprehension)
- Cost: $0 — 100% FREE Microsoft service
- Format: MP3 output
- Installation: `pip install edge-tts` (global)
- Use case: one-off learning guides, documentation audio, tutorial narration
- NOT for: repetitive batch generation (use Kokoro for that)
- Added: 2026-04-18
- See: [[Edge_TTS_Learning_System]]

---

## DaVinci Resolve
- Type: Professional video editor
- Machine: HP (OBS recording) + Predator (editing via MCP)
- MCP integration: resolve-mcp-server TCP:9000
- Export path: C:\BDF\renders\
- Log: export_log.jsonl (append-only)
- Version: Free (no Studio license)

---

## GitLens (VS Code extension)
- Type: Git history and blame overlay in VS Code
- Used for: tracking changes across all 4 projects

---

## SyncThing
- Type: LAN file sync
- Predator ID: PCUCH42-TPMQJKB-672R4EH-CDKYS2J
- HP ID: JUJFJ7O-IV7SIC5-65MDDGM-J75YYFA
- Shared folder: BDF-Clips
- Rule: Pause Surfshark VPN for LAN sync to work

---

## PowerShell
- Default terminal on Predator
- Key rule: never chain >> (use separate commands)
- Key rule: Select-String needs Get-ChildItem pipe, not -Recurse direct
- Key rule: grep does not exist — use Select-String
- Key rule: URLs and code from chat must be typed manually, not copy-pasted (hyperlink corruption)

---

## obs_relay.py
- Type: Multi-machine OBS clip bridge
- Location: `C:\Dev\Projects\soccer-content-generator\obs_relay.py`
- Watches: `C:\Media\Recordings` (OBS replay buffer output)
- Routes to: `C:\BDF_Share` (direct on Predator) · SyncThing folder on HP
- Machine detection: hostname `CRISTIAN` = Predator (direct); any other = HP (SyncThing)
- Usage: `python obs_relay.py --match UCL_Atletico_Arsenal`

---

## clip_watcher.py
- Type: Clip Factory pipeline engine
- Location: `C:\Dev\Projects\soccer-content-generator\clip_watcher.py`
- Watches: `C:\BDF_Share` (AUTO track) · `master_edit\ready\` (MASTER EDIT track)
- Output: injects to `src/queue/content_queue.json` with `status=pending`
- Telegram: optional (wrapped in try/except) — dashboard is primary approval UI
- Usage: standalone `python clip_watcher.py` or imported by `bot_service.py`

---

## trigger_watcher.py
- Type: Match-day content trigger system
- Location: `C:\Dev\Projects\soccer-content-generator\trigger_watcher.py`
- Watches: `triggers\` folder (polls every 10s)
- File format: `{content_type}_{topic}.txt` e.g. `hot_take_Atletico_Arsenal_goal.txt`
- Output: SoccerBot-generated content injected to queue as `status=pending`
- Usage: `python trigger_watcher.py` · `--once` flag for single pass

---

## sync_brain.py
- Type: Weekly system health snapshot
- Location: `C:\Dev\Projects\soccer-content-generator\sync_brain.py`
- Collects: queue counts, weekly cost, LanceDB doc count, git status, clip stats
- Output: `data/brain_sync_{YYYY-MM-DD}.json` + git commit
- Usage: `python sync_brain.py` · `--no-commit` to skip git

---

## obs_mcp.py
- Type: OBS WebSocket v5 controller (FastAPI + importable class)
- Location: `C:\Dev\Projects\soccer-content-generator\obs_mcp.py`
- Library: `simpleobsws` 1.4.x — replaces broken `obsws-python` (v4 only)
- Port: 8001 · WebSocket: `ws://localhost:4455` · Password: `OBS_WS_PASSWORD` in `.env`
- Endpoints: `/obs/status` · `/obs/save_replay` · `/obs/start_replay_buffer` · `/obs/stop_replay_buffer` · `/obs/start_recording` · `/obs/stop_recording` · `/obs/set_scene`
- Import: `from obs_mcp import OBSController`
- Usage: `python obs_mcp.py`

---

## Edge TTS
- Type: Local text-to-speech for audio learning guides
- Install: `pip install edge-tts` (global, not project-specific)
- Voice: `en-US-GuyNeural` — clear, natural, human-sounding
- Rate: `-5%` (slightly slower for comprehension)
- Output: MP3 files generated on Predator, saved to `C:\Knowledge\[TopicFolder]\`
- Workflow: Claude generates narration script (.txt) + generator script (.py) → Cristian runs generator → MP3 output → Google Drive backup (drag-and-drop)
- Trigger phrase: "Create a learning guide for [topic] using my audio learning system"
- Decision log: gTTS tried (robotic), espeak tried (worse), Edge TTS chosen (2026-04-18)
- Do NOT use: gTTS, espeak, ElevenLabs, or OpenAI TTS — Edge TTS is the standard

---

## Connected to
- [[MCP_Registry]]
- [[Active_Environments]]
- [[DaVinci_Resolve_MCP]]

## Session Log
- 2026-04-30 — Session 2026-04-30 complete. Cost monitor live, Telegram wired, CLAUDE.md in
- 2026-04-30 — Session 2026-04-30 complete. Cost monitor live, Telegram wired, CLAUDE.md in
- 2026-04-30 — Session 2026-04-30 — Claude API cost forensics and knowledge
- 2026-04-30 — Telegram fix test
- 2026-04-30 — Session 2026-04-30 — Knowledge continuity architecture complete.
- 2026-04-30 — Session 2026-04-30 — Full session close pipeline operational.
- 2026-04-18 — Resolve MCP expanded 11→52 tools (3 phases). Read-Along venv rebuilt. Edge TTS audio learning system established. Rules 11-13 added.
- 2026-05-01 — UTF-8 encoding fix verified — em dashes now render correctly
- 2026-05-01 — Session 2026-04-30 final close. Full system standardization
- 2026-05-02 — Context7 MCP audit complete - verified fully operational with HTTP
- 2026-05-03 — Obsidian MCP fixed (obs-mcp → obsidian-mcp), 11 tools operational; Kokoro + Edge TTS costs documented; knowledge pipeline initiated
- 2026-05-04 — Built complete knowledge management pipeline for BRAIN_OS:
