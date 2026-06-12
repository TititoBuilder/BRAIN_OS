---
tags:
  - domain
  - software-architecture
  - systems-design
  - separation
  - modularity
  - principles
created: 2026-06-10
updated: 2026-06-10
domain: Systems Design Layer
topics:
  - four_pillars_separation
  - blast_radius
  - shared_core_pattern
  - config_driven_design
  - dry_decoupling
  - brain_os_graph_layer
  - atomic_commits
  - trace_before_change
---

# Software Architecture - Systems Design Brain

**What This Is:** How you structure systems so they stay maintainable, isolated, and safe to change - the patterns and separation principles that keep one failure from cascading into ten.

**Why It Exists:** To make the architectural decisions explicit and reusable, so every new project inherits the same hard-won rules instead of relearning them.

---

## Core Concepts You're Building With

- **Blast Radius** - Scope every change so a failure can only reach as far as it must, never the whole system
- **Shared Core Pattern** - One canonical implementation (e.g. brain-audio) that many projects import, instead of copy-paste drift
- **Config-Driven Design** - Behavior lives in config, not hardcoded paths - tools adapt without code edits
- **DRY + Decoupling** - One source of truth per fact; components that can change independently
- **The Graph Layer** - BRAIN_OS as the vault that encodes architecture and principles AI reads to operate across all projects
- **Atomic Commits** - Both sides of a contract ship in one push, never half a change

---

## The Four Pillars of Architectural Separation

The discipline underneath every project: before two things share a boundary, decide *which* of these four separations applies. Most architecture mistakes are a missing pillar.

### Pillar 1 - Execution Environment
Each system runs in its own isolated environment so dependencies never collide.
- **Example:** Separate venvs per workload - GPU/Whisper + Drive API in the soccer-content-generator venv; pydub/stitching in `C:\Knowledge\CA\venv`. Both confirmed present.
- **Why it matters:** A venv hardcodes paths and can't be moved - environment is a boundary, not an afterthought.

### Pillar 2 - Node Type
Know what *kind* of thing each component is before wiring it. A graph/vault layer is not a project. A shared package is not an application. A session resume is not a topic lesson.
- **Example:** BRAIN_OS is the GRAPH layer (md files encoding architecture + principles), NOT a project. Projects hang off it: CristianConstruction, BDF, Read-Along App, the MCP servers.
- **Why it matters:** Misclassifying a node type is how a vault gets treated like an app and accumulates the wrong responsibilities.

### Pillar 3 - Failure Boundaries
Design where a failure is *allowed* to stop. Errors should hit a wall, not flow downstream.
- **Example:** Option C hybrid automation - auto-handle ~90%, flag the ~10% complex cases for a human decision rather than letting them fail silently or corrupt state.
- **Why it matters:** Git rollback is the safety net (`git checkout HEAD` recovered a live data-loss incident). A clean failure boundary is what makes rollback enough.

### Pillar 4 - Modularity
Components decouple so they can change independently. Swap one without rewriting the others.
- **Example:** brain-audio as an editable shared install across BDF, CA, and read-along-app venvs - the audio core changes once, every consumer inherits it.
- **Why it matters:** Modularity is what makes the Shared Core Pattern possible instead of three diverging copies.

---

## Active Projects

### [[BRAIN_OS]]
**Location:** `C:\BRAIN_OS\` (git: TititoBuilder/BRAIN_OS)
**What:** The graph/vault layer - md files encoding architecture, principles, and procedures that AI reads to operate across every project
**Status:** Operational; the architectural backbone, not a project itself (tree clean at bf2b4c2)
**Tech:** Obsidian vault, Python tooling in `09_TOOLS\`, Git version control

**What lives here:**
- **Principles** - `07_SYSTEM\Cristian_Principles.md` (canonical earned-knowledge source)
- **Config** - `BRAIN_OS_CONFIG.json` (Drive folder IDs, TTL settings)
- **Tooling** - session lifecycle scripts (session_start.py, session_close.py, graph_maintainer.py, compile_session.py)
- **The two lenses** - 5-Layer encyclopedia (01_DOMAINS) and the app's learning domains are TWO intentional lenses, deliberately not collapsed (`Taxonomy_Decision.md`)

**Architectural rules encoded here:**
- Text config / JSON / .gitignore edited via Python ONLY - never PowerShell Set-Content (injects BOM/null bytes)
- `git add` by explicit filename, never `-A`; read status + diff before every commit
- "For now" is forbidden - root fixes only
- Trace before changing - "unreferenced" does not equal "safe to delete"

**Pending:**
- [ ] Make session_start.py resolve its own path (`Path(__file__).parent`) so it runs from any directory
- [ ] Gitignore the auto-regenerated `02_PROJECTS\graphs\*` files
- [ ] session_close.py: make `git add` surgical (broad-added temp scripts last session)

---

## Architectural Patterns In Practice

### The Shared Core Pattern
One implementation, many consumers.
- **brain-audio** (`C:\Dev\shared\brain-audio`) - TTS core installed editable into two project venvs (soccer-content-generator, CA)
- Beats copy-paste: a fix lands once and propagates, no diverging forks
- Connects to: [[Creative_Systems]] (audio production), [[AI_Engineering]] (the MCP layer)

### Config-Driven Over Hardcoded
- Drive folder IDs, TTL settings live in `BRAIN_OS_CONFIG.json`, not in code
- Tools read config; changing behavior never means editing logic
- Drive files referenced by ID (`id:` prefix), captured at upload time - filenames are machine keys, not reliable lookups

### Update-In-Place (Identity Preservation)
- `files().update()` keeps the same Drive file ID - no orphan, no index drift
- The architectural lesson: preserve identity across edits instead of recreating and re-linking

### Atomic Contracts
- Both sides of a contract ship in one commit (e.g. a producer and the index that tracks it)
- A change that spans two files is one push, not two

---

## Pending Tasks (Software Architecture)

### Critical (Do Soon)
- [ ] session_close.py surgical `git add` (stop broad-adding temp scripts)
- [ ] Decide on a gitignored `_scratch/` folder for temp scripts that straggle in vault root

### Important (Next)
- [ ] session_start.py path-independence (`Path(__file__).parent`)
- [ ] Gitignore auto-regenerated `02_PROJECTS\graphs\*`

### Someday/Maybe
- [ ] Audit git history for binaries committed during the 376-null .gitignore window
- [ ] Formalize the Blast Radius checklist as a reusable pre-change template

---

## Knowledge Base (Compiled Sessions)

**Sessions documenting architectural work:**
- [[2026-05-28_2041_bdf_ca_brain_os]] - recent architecture + cleanup work
- [[2026-05-29_1854_bdf_ca_brain_os]] - latest committed brain_os session
- [[2026-05-12_2100_brain-os-audio-library]] - shared audio-library structure
- More sessions in `08_SESSIONS\` (timestamped `YYYY-MM-DD_HHMM_project`)

---

## Learning Journey

**What you've built without realizing:**
- A graph layer that encodes architecture so every project inherits the same rules
- A shared-core package consumed by three separate environments
- A config-driven tooling system with identity-preserving Drive sync
- A failure-boundary discipline (Option C) with git rollback as the net

**Terms you now understand:**
- Blast radius, failure boundaries, separation of concerns
- Shared core vs copy-paste drift, DRY, decoupling
- Node-type classification (graph vs project vs package vs node)
- Atomic commits, surgical staging, trace-before-change
- BOM / null-byte corruption and BOM-free writes
- Config-driven design, identity preservation on update

---

## Connected Domains
- [[AI_Engineering]] - MCP servers, automation tooling, the agents that read this graph
- [[Systems_Operations]] - deployment, environments, the runtime side of these designs
- [[Creative_Systems]] - consumes the shared-core audio package

---

## Tools That Connect Here
- [[session_start.py]] - loads the full live architectural context bundle
- [[session_close.py]] - session lifecycle close + ingestion
- [[graph_maintainer.py]] - keeps the graph layer consistent
- [[compile_session.py]] - Option C knowledge ingestion
- [[cost_guard.py]] - cost-discipline enforcement (model standard)
- [[audit_files.py]] - audit-before-change tooling
- [[brain-audio]] - the shared-core package this domain's patterns produced
- [[BRAIN_OS_CONFIG.json]] - the config-driven source of truth
