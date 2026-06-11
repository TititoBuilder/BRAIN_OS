---
tags:
  - domain
  - systems-operations
  - runtime
  - deployment
  - graph
  - monitoring
created: 2026-06-10
updated: 2026-06-10
domain: Systems Operations Layer
topics:
  - cicd_pipelines
  - containerization
  - env_management
  - env_security
  - load_balancing
  - circuit_breaker_pattern
---

# Systems Operations - Runtime & Keep-It-Running Brain

**What This Is:** The runtime layer that keeps your knowledge flowing - the graph operation that scans your vault, regenerates context maps, and feeds every downstream system (Read-Along, AI sessions).

**Why It Exists:** To see how your systems actually run, deploy, and stay synced - the operations beneath the architecture.

---

## Core Concepts You are Operating With

- **Graph Maintenance** - graphify scans the vault, regenerates dependency + context maps
- **Context Generation** - the maps that feed Read-Along and every AI session
- **Environment Isolation** - per-workload venvs, CUDA, dependency separation
- **Deployment Operations** - Vercel + Railway, env-var sync, single source of truth
- **Session Lifecycle** - start to work to close to compile to notify
- **Health Monitoring** - session-start checks (audio parity, git tree, queue state)

---

## Active Systems

### [[Graph_Operation]] - THE SPINE
**Location:** C:\Dev\Projects\soccer-content-generator\scripts\graph_maintainer.py (17 KB)
**What:** The operational core - scans each project, regenerates its dependency graph + context map
**Status:** Operational; runs automatically at session start
**Config-driven:** each project has a .graphify.json config in 02_PROJECTS\graphs\

**How it runs:**
1. Config (input): {project}.graphify.json declares root, graph_output path, skip_patterns (venv, __pycache__, node_modules), external_packages, layer structure
2. Scan: graph_maintainer reads config, walks the project tree
3. Output (generated): {project}.json (dependency graph) + {project}.context.md (the context an AI loads)
4. Trigger: runs on session start via session_start.py health check

**Real artifacts (02_PROJECTS\graphs\):**
- soccer-content-generator: config 1.9 KB to output 41 KB + context 10.7 KB (largest graph)
- read-along-app: config 386 B to output 3.4 KB + context 719 B
- ca-book: config 1 KB to output 600 B + context 184 B

**Operational principle:** config over hardcoding. To change what gets scanned, edit the .graphify.json, never the maintainer. One config per project, one maintainer for all.

### [[Read_Along_Deploy]] - DEPLOYMENT OPERATIONS
**Location:** C:\BRAIN_OS\02_PROJECTS\Read_Along_Deploy.md
**What:** Live two-service deployment that CONSUMES the graph context output
**Status:** Stabilized after a multi-root crisis
**Tech:** Vercel (frontend) + Railway (backend), Google Drive (audio), GitHub (vault context)

**The crisis you solved (earned operations knowledge):**
- Multi-root path-doubling: Vercel Root Directory must be frontend, not ./ - wrong root caused frontend/frontend path-doubling. Confirmed via .vercel/project.json.
- Env-var sync: Railway GOOGLE_TOKEN_JSON holds the OAuth token separately from local gdrive_token.json - must be kept in sync or Drive streaming breaks.
- Single source of truth: Railway DRIVE_INDEX_JSON env var was deleted - GitHub is now the only source for drive_index.json.

**Operational principle:** deployment config is fragile and must be explicit; env vars across services must stay synced; one source of truth per artifact.

### [[Session_Lifecycle]] - DAILY OPERATIONS RHYTHM
**What:** The atomic work-session cycle that TRIGGERS graph maintenance
**Status:** Operational

**The cycle:**
1. session_start.py - loads full context bundle (CLAUDE.md + latest archive + queue), runs graph_maintainer health check, Telegram confirm
2. Active work - the session itself
3. session_close.py - writes dated archive to 08_SESSIONS, Telegram
4. compile_session.py - ingests archive into the knowledge graph (Option C hybrid)

**Operational principle:** every session is an atomic unit (init to work to compile); state persists across sessions via archives; notifications close the loop.

### [[Environment_Operations]] - VENV ISOLATION
**What:** Per-workload Python environments, isolated to prevent conflicts
**Status:** Operational, two canonical venvs (confirmed on disk)

- GPU/Whisper + Google Drive API: C:\Dev\Projects\soccer-content-generator\venv
- pydub/stitching + AI/TTS/PyTorch: C:\Knowledge\CA\venv
- Both have CUDA (sm_120 Blackwell, RTX 5070 Ti). Triton warnings are harmless fallbacks.
- System Python - no AI packages, never used for inference.

**Operational principle:** isolate environments by workload; never install CPU-only torch; venvs hardcode paths and cannot be moved (rebuild, do not relocate).

---

## Operational Principles (what emerges)

- **Sync with reality** - the graph must reflect the actual vault; stale maps cause false context. graph_maintainer re-scans every session.
- **Automate on boundaries** - maintenance + health checks run at session start, not manually.
- **Single source of truth** - one config per project, one source per artifact.
- **Monitor health** - session start reports audio parity, git tree, queue state before work begins.
- **Config over hardcoding** - .graphify.json drives the scan; tools stay generic.

---

## Pending Tasks (Systems Operations)

### Important
- [ ] gitignore the auto-regenerated 02_PROJECTS\graphs\*.json + *.context.md (they rebuild each session)
- [ ] session_close.py: make git add surgical (explicit files, not broad add)
- [ ] session_start.py: self-resolve path so it runs from any directory

### Someday
- [ ] Reconcile two session-archive locations (08_SESSIONS vs 09_TOOLS)
- [ ] Pre-commit check that rejects null bytes in tracked text files

---

## Connected Domains
- [[Software_Architecture]] - the design beneath these operations
- [[AI_Engineering]] - the automation tools that run here
- [[Data_Science]] - the indexes and maps operations keep synced

## Tools That Connect Here
- [[graph_maintainer.py]] - the graph operation core
- [[session_start.py]] - context loader + health check
- [[session_close.py]] - session archiver
- [[Read_Along_Deploy]] - deployment runbook
