---
tags: [domain, ai-engineering, infrastructure, automation, mcp]
created: 2026-05-03
updated: 2026-05-04
domain: AI Engineering Layer
---

# AI Engineering — Infrastructure & Automation Brain

**What This Is:** Your AI infrastructure work - agents, MCP servers, APIs, orchestration, automation systems.

**Why It Exists:** To see all your AI engineering progress in one place and track what's next.

---

## Core Concepts You're Building With

- **MCP (Model Context Protocol)** - How AI agents connect to tools and data
- **Agent Architecture** - Specialized AI agents working together
- **API Integration** - Connecting Claude, Google Drive, Obsidian, Context7
- **Automation Systems** - Workflows that run without manual work
- **Local + Cloud** - Running AI locally (Kokoro) + cloud services (Claude API)
- **Tool Chaining** - One tool's output feeds another automatically

---

## Active Projects

### [[Custom_Agent]] (CA)
**Location:** `C:\Dev\CristianConstruction\`  
**What:** AI assistant with Telegram interface, book compilation, audio generation  
**Status:** MVP complete, Kokoro TTS working  
**Tech:** Python, Claude API, Kokoro (local TTS), Telegram Bot  
**Book:** CA Book (personal development, AI learning)

**Key Components:**
- `ca_audio.py` - Kokoro TTS audio generation for book chapters
- `book_compiler.py` - Compiles sessions into book chapters using Claude Opus
- Telegram interface for mobile access
- Google Drive sync for audio files

**Cost Clarification (2026-05-03):** Kokoro TTS is 100% FREE (local GPU inference, zero API costs). Prior confusion: charges were Claude Opus compilation ($0.15-0.30/chapter), not TTS. See [[Custom_Agent_TTS]] for full breakdown.

**Pending:**
- [ ] Separate CA venv from BDF venv (currently sharing)
- [ ] Each project needs isolated venv before LanceDB migration

### [[Resolve_MCP]] Server
**Location:** `C:\Users\titit\Projects\resolve-mcp-server\`  
**What:** MCP server controlling DaVinci Resolve via automation  
**Status:** 52 tools operational, pyautogui bridge working  
**Tech:** Python, MCP stdio transport, pyautogui, DaVinci Resolve API

**Evolution:**
- Started: 11 basic tools
- Now: 52 tools (editing, audio, export, color grading)
- Git: Initialized, commit 1dbece3

**Pending:**
- [ ] Test all 52 tools on guitar footage
- [ ] Build jump_to_timecode tool
- [ ] Practice full editing workflow: mark → cut → delete → export
- [ ] Install Resolve 18.6.6 for native API access

### [[BDF_Platform]]
**Location:** `C:\Dev\Projects\soccer-content-generator\`  
**What:** Soccer content generation with AI + DaVinci automation  
**Status:** Production, generates highlight videos with custom graphics  
**Tech:** Python, Claude API, DaVinci Resolve bridge, image generation

**Key Systems:**
- Card generation (player stats graphics)
- Video compilation automation
- Social media formatting
- Book compilation (BDF Book)

**Pending:**
- [ ] Migrate LanceDB from external WD Elements to C: drive
- [ ] Complete data migration from external drive

---

## MCP Ecosystem (Your AI Operating System)

**Connected MCP Servers:**

### Production MCPs
- **Context7** - Documentation search, library resolution
- **Google Drive** - File search, read, create, permissions
- **Gmail** - Email search, drafts, labels, threads
- **Google Calendar** - Events, scheduling, time suggestions
- **Obsidian** - ✅ Operational (fixed 2026-05-03), 11 tools (create, read, edit, search)

### Custom MCPs (You Built These)
- **davinci-resolve** - 52 tools for Resolve control
- **davinci-resolve-api** - API-based Resolve access

### Broken/Investigating
- **OBS Studio** - Streaming control (was confused with Obsidian)

---

## Tools & Integrations

### AI/LLM
- **Claude API** (Sonnet 4.6, Opus 4.6) - Text generation, compilation
- **Claude Desktop** - MCP server integration platform
- **Claude Code** - Terminal-based coding agent

### Audio
- **Kokoro TTS** - Local text-to-speech (100% FREE, GPU-accelerated)
- **Edge TTS** - Microsoft TTS for learning guides (100% FREE)

### Development
- **Python 3.12.10** - Primary language
- **Git** - Version control
- **VS Code** - Main IDE
- **PowerShell** - Windows automation

### Infrastructure
- **PyTorch 2.11.0+cu128** - CUDA-accelerated ML
- **FFmpeg** - Audio/video processing
- **Virtual Environments** - Project isolation

---

## Pending Tasks (AI Engineering)

### Critical (Do Soon)
- [ ] Separate CA venv from BDF venv
- [ ] Complete LanceDB migration to C: drive
- [ ] Test all 52 Resolve MCP tools

### Important (Next)
- [ ] Build jump_to_timecode for Resolve
- [ ] Install Resolve 18.6.6 for native API
- [ ] Create agent architecture diagram

### Someday/Maybe
- [ ] Build delivery monitoring agent
- [ ] Explore specialized agent orchestration
- [ ] Research: one mega-agent vs specialized agents

---

## Knowledge Base (Compiled Sessions)

**Sessions documenting AI engineering work:**
- [[2026-05-03_Obsidian_MCP_Fix_Audio_Systems]] - MCP troubleshooting, audio systems
- [[2026-04-18_Edge_TTS_Learning_System_Creation]] - Audio learning guides built
- More sessions to compile from 09_TOOLS/ and past chats

---

## Book Content Candidates

**For CA Book (Personal Development + AI Learning):**
- Building your first MCP server
- Understanding agent architecture
- Local vs cloud AI decision framework
- Tool integration patterns
- Automation workflow design

**For BDF Book (Soccer + Technology):**
- AI-powered content generation
- Automated video production workflows

---

## Learning Journey

**What you've built without realizing:**
- Complete MCP ecosystem with 8+ connected services
- Custom MCP servers from scratch
- Agent automation systems
- Hybrid local/cloud AI architecture
- Audio generation pipeline (2 systems)

**Terms you now understand:**
- MCP, stdio transport, API handshakes
- Agent orchestration, tool chaining
- Context windows, tokens, prompting
- CUDA acceleration, GPU inference
- Virtual environments, package isolation

---

## Connected Domains
- [[Data_Science]] - Monitoring, analytics, knowledge organization
- [[Creative_Systems]] - Video editing, OBS, content workflows

---

## Tools That Connect Here
- [[Tools_Registry]] - Full tool inventory
- [[Session_Protocol]] - How to work with Claude
- [[Knowledge_Ingestion_Protocol]] - How knowledge flows into BRAIN_OS
