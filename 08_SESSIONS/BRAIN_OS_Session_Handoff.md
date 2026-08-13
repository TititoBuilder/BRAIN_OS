# BRAIN OS — Session Handoff & Execution Plan
**Date:** 2026-04-27  
**Session:** Brain OS v1 → v2 build, Obsidian setup, Graph View, Claude Code integration  
**Continue in:** New Claude chat — paste this file as first message

---

## #WHAT_WE_BUILT — Complete system built today

Everything below was generated from real source code across 4 projects and committed to GitHub at TititoBuilder/BRAIN_OS.

**Vault location:** C:\BRAIN_OS  
**Obsidian vault:** Open Obsidian → C:\BRAIN_OS  
**Canvas:** 00_DASHBOARD/Main_Canvas.canvas  
**GitHub:** https://github.com/TititoBuilder/BRAIN_OS

### #FILE_STRUCTURE — Complete folder map
```
C:\BRAIN_OS\
├── 00_DASHBOARD/     ← Main_Canvas.canvas (your visual brain map)
├── 01_PROJECTS/      ← BDF_Soccer_Bot, Custom_Agent, Read_Along_App, Resolve_MCP
├── 02_AGENTS/        ← 12 agent files including 3 new orchestrators + DaVinci
├── 03_APIS/          ← 9 API files (Anthropic, OpenAI, Twitter, Telegram, etc)
├── 04_WORKFLOWS/     ← 7 workflow files
├── 05_MEMORY/        ← LanceDB, Knowledge Books, Content Queue, Memory Index
├── 06_TEMPLATES/     ← PROJECT_NODE, AGENT_NODE, WORKFLOW_NODE, API_NODE
├── 07_SYSTEM/        ← Master_Control, MCP_Registry, Tools_Registry, 
│                        Active_Environments, Canonical_File_Map, State_System
└── 08_TRIGGERS/      ← Trigger_Match_Scheduled, Trigger_Render_Complete,
                         Trigger_Script_Ready, Trigger_New_Idea
```

---

## #GRAPH_COLORS — What every color means in Graph View

When you open Graph View in Obsidian (graph icon, left sidebar), every colored node is a real file in your vault. The color tells you instantly which layer of the Brain OS that file belongs to.

**Orange nodes** = your 4 active projects (01_PROJECTS folder)  
BDF_Soccer_Bot, Custom_Agent, Read_Along_App, Resolve_MCP

**Purple nodes** = AI agents and orchestrators (02_AGENTS folder)  
Research Agent, Creative Agent, Content Orchestrator, Video Orchestrator, etc.

**Green nodes** = workflows and process flows (04_WORKFLOWS folder)  
BDF_Content_Research_Flow, BDF_Video_Production_Flow, etc.

**Yellow nodes** = memory and knowledge storage (05_MEMORY folder)  
LanceDB_Vector_Store, BDF_Knowledge_Book, Content_Queue, etc.

**Blue nodes** = APIs and external connections (03_APIS folder)  
Anthropic_Claude, Football_API, Twitter_API_v2, etc.

**Gray nodes** = system files and infrastructure (07_SYSTEM folder)  
Master_Control, MCP_Registry, Tools_Registry, etc.

**Coral/orange nodes** = triggers (08_TRIGGERS folder)  
Trigger_Match_Scheduled, Trigger_Render_Complete, etc.

**Red node** = critical alert — OpenAI_gpt-image-1 (DALL-E 3 deprecates May 12 2026)

---

## #LINK_LINES — What the lines between nodes mean

Lines in the graph are drawn automatically from [[double bracket links]] inside your .md files. When BDF_Research_Agent.md contains the text [[Football_API]], Obsidian draws a line between those two nodes. The line means "these two things are connected in your real system." Thicker lines = more connections. The direction arrow shows which file references which.

A node with many lines coming out of it = a hub component that many things depend on. In your graph, Anthropic_Claude and LanceDB_Vector_Store have the most lines because almost every agent in your system uses them.

---

## #ARCHITECTURE — Brain OS v2 layer structure

```
TRIGGERS (coral)     → What starts everything
       ↓
MASTER CONTROL (gray) → Routes triggers to correct orchestrator  
       ↓
ORCHESTRATORS (purple) → Content / Video / Data / CA
       ↓
AGENTS (purple)      → Where work actually happens
       ↓
MEMORY (yellow)      → LanceDB, queues, knowledge books
       ↓
INFRASTRUCTURE       → Predator, WD Elements, GitHub
```

**Strict rule:** Triggers → Master Control → Orchestrators → Agents → APIs/Memory.  
Agents never call other agents directly. Orchestrators route between them.

---

## #ACTIVE_PROJECTS — Current status of all 4 projects

**BDF Soccer Bot** — #live  
Path: C:\Dev\Projects\soccer-content-generator\  
GitHub: TititoBuilder/soccer-content-generator  
Launch: T1=python bot_service.py | T2=uvicorn dashboard_api:app | T3=npm run dev  
CRITICAL: DALL-E 3 deprecates May 12 — migrate media_agent.py to gpt-image-1  

**Custom Agent (CA)** — #live  
Path: C:\Dev\CristianConstruction\  
GitHub: TititoBuilder/cristian-construction  
9-agent FastAPI construction business OS + cc-landing on Vercel  

**Read-Along App** — #wip  
Path: C:\Users\titit\Projects\read-along-app\  
Backend complete (FastAPI + Whisper CUDA). Vite frontend NOT YET BUILT.  
Local git only — no GitHub remote yet.  

**Resolve MCP** — #live  
Path: C:\Users\titit\Projects\resolve-mcp-server\  
GitHub: TititoBuilder/resolve-mcp-server  
TCP PORT=9000, server_api.py v10.7, additionalDirectories: soccer-content-generator/src  

---

## #MCP_CONNECTED — All active MCP servers

**Resolve MCP (local):** TCP PORT=9000, C:\Users\titit\Projects\resolve-mcp-server\  
**GitHub MCP:** npx @modelcontextprotocol/server-github (global, GITHUB_PERSONAL_ACCESS_TOKEN)  
**Context7 MCP:** npx @upstash/context7-mcp (global, live docs for migrations)  
**Google Calendar MCP:** https://calendarmcp.googleapis.com/mcp/v1 (claude.ai connected)  
**Gmail MCP:** https://gmailmcp.googleapis.com/mcp/v1 (claude.ai connected)  
**Google Drive MCP:** https://drivemcp.googleapis.com/mcp/v1 (claude.ai connected)  

---

## #CLAUDE_CODE_SETUP — Auto-permissions configured

All 5 projects have .claude/settings.json with auto-accept.  
Global: claude config set --global preferredNotificationsMode auto-accept-edits  
Alias: type "cc" to launch Claude Code with --dangerously-skip-permissions  

---

## #CRITICAL_BUGS_FIXED — What was repaired today

LanceDB path inconsistency — 8 files had 3 different fallback defaults.  
All standardized to: C:/Dev/Projects/soccer-content-generator/lance_db_soccer  
rebuild_lancedb.py was hardcoded to shutil.rmtree('./lance_db') — would have  
deleted wrong directory. Fixed to use LANCE_DB_PATH env var.  
Stale F:/lance_db_soccer comment in mcp_ingest.py corrected.  

Dual Telegram libraries surfaced — BDF uses python-telegram-bot, CA uses httpx direct.  
Both share same bot token. If bot config changes, BOTH codebases need separate updates.

---

## #EXECUTION_PLAN — What to do in the new chat

### PHASE 1 — Familiarize (Day 1, today or tomorrow)
#TASK_1: Open Obsidian, open Main_Canvas, press Ctrl+Shift+H to fit canvas.  
Spend 10 minutes clicking every node card — single click = preview, double click = full file.  
Goal: recognize every component by name and know which layer it belongs to.

#TASK_2: Open Graph View (connected dots icon, left sidebar).  
Hover over BDF_Soccer_Bot — watch everything it connects to highlight.  
Hover over Anthropic_Claude — see how many agents depend on it.  
Click Animate — watch 4 project clusters find their natural positions.

#TASK_3: Press Ctrl+O (quick switcher) and type "LanceDB".  
Open LanceDB_Vector_Store.md — read the canonical path and bug fix log.  
This is how you navigate the system without touching the canvas.

### PHASE 2 — Daily workflow setup (Day 1-2)
#TASK_4: Add Google Calendar MCP to daily schedule workflow.  
In new chat: "Use Google Calendar MCP to create a daily Brain OS review event  
at 9am — 15 minutes, recurring, titled 'Brain OS daily review'"

#TASK_5: Create a daily log template in 05_MEMORY.  
In new chat: "Create C:\BRAIN_OS\05_MEMORY\Daily_Log_Template.md with sections  
for Date, Projects active today, Tasks completed, Bugs found, Brain OS updates needed"

#TASK_6: Create the first daily log entry for today (2026-04-27) documenting  
everything built in this session.

### PHASE 3 — Canvas completion (Day 2-3)
#TASK_7: Add 08_TRIGGERS nodes to Main_Canvas.  
In new chat: "Add the 4 trigger files from 08_TRIGGERS to Main_Canvas.canvas  
positioned above the BRAIN OS hub with arrows pointing down to Master_Control"

#TASK_8: Add Master_Control and the 3 orchestrators to Main_Canvas  
between the hub and the AI AGENTS group.

#TASK_9: Create per-project canvases.  
In new chat: "Generate BDF_Canvas.canvas in 00_DASHBOARD showing only BDF  
Soccer Bot nodes — all 5 BDF agents, 5 BDF workflows, BDF APIs, arrows showing flow"

### PHASE 4 — Critical execution (Before May 12)
#TASK_10: DALL-E 3 → gpt-image-1 migration.  
In new chat: "Read media_agent.py and image_agent.py in  
C:\Dev\Projects\soccer-content-generator\ and migrate all DALL-E 3 calls  
to gpt-image-1 using Context7 to pull live OpenAI docs"

### PHASE 5 — System automation (Week 2)
#TASK_11: Build Python trigger watcher.  
"Build a Python script that watches ContentWindow enum and export_log.jsonl  
and calls the appropriate orchestrator automatically — wire to bot_service.py"

#TASK_12: Build weekly Brain OS sync script.  
"Build sync_brain.py that scans all 4 project directories, compares against  
BRAIN_OS node files, and outputs a diff of what needs updating"

#TASK_13: Read-Along App Vite frontend scaffold.  
"Scaffold a Vite + React frontend for C:\Users\titit\Projects\read-along-app\  
that connects to the FastAPI backend at localhost:8000"

---

## #GOOGLE_CALENDAR_WORKFLOW — Daily schedule integration

Google Calendar MCP is connected and ready at claude.ai.  
In the new chat, the first workflow to build is a daily Brain OS review schedule:

Morning (9:00am): Brain OS daily review — check graph for red/yellow nodes  
Midday (12:00pm): Check content queue status for BDF bot  
Evening (6:00pm): Log what was built today, update node files via Claude Code  

Command for new chat:  
"Use Google Calendar MCP to set up a recurring daily Brain OS review schedule  
with 3 events: 9am Brain OS review (15min), 12pm BDF queue check (10min),  
6pm daily log update (20min). Make them recurring on weekdays."

---

## #HOW_TO_UPDATE — Keeping Brain OS current

Every time you build something new, open Claude Code in VS Code and say:  
"I just built [what you built] in [project name].  
Update the relevant node files in C:\BRAIN_OS to reflect this change.  
Then commit and push to TititoBuilder/BRAIN_OS."

Claude Code reads your real Python files, writes the updated .md node,  
commits to GitHub, and Obsidian refreshes automatically. Zero manual work.

---

## #QUICK_REFERENCE — Most important commands

Open Claude Code: type "cc" in VS Code terminal (alias = --dangerously-skip-permissions)  
Fit canvas to screen: Ctrl+Shift+H in Obsidian Canvas  
Quick file jump: Ctrl+O in Obsidian  
Search all notes: Ctrl+Shift+F in Obsidian  
Graph View: click connected-dots icon in left sidebar  

BDF launch sequence (all from C:\Dev\Projects\soccer-content-generator\):  
T1: python bot_service.py  
T2: uvicorn dashboard_api:app --reload  
T3: cd dashboard then npm run dev  
BEFORE launching: pause Surfshark VPN  
BEFORE launching: connect ethernet MiFi LAN → Predator RJ45  

---

## #NEW_CHAT_OPENER — Paste this at the start of your next conversation

"I am continuing the Brain OS project from a previous session.  
The complete system is built and documented at C:\BRAIN_OS and  
GitHub TititoBuilder/BRAIN_OS. The session handoff file contains  
all context. Today I want to work on: [choose a task from the execution plan above]  
My active projects are BDF Soccer Bot, Custom Agent, Read-Along App, and Resolve MCP.  
All Claude Code permissions are configured. Google Calendar, Gmail, and Google Drive  
MCPs are connected."

