# Study System — How This Works
Location: C:\BRAIN_OS\07_SYSTEM\STUDY_SYSTEM.md
Updated: 2026-08-12

---

## The Four Layers

These are not the same thing. Each has a different job.

    LAYER 1 — THE VAULT (BRAIN_OS)
      Location:  C:\BRAIN_OS
      What:      Obsidian markdown files — knowledge graph
      Purpose:   Architecture docs, principles, session notes, domain maps
      Domains:   ai_engineering.md, software_architecture.md,
                 systems_operations.md, data_science.md, creative_systems.md
      How used:  READ — link concepts here, classify what you find in code
                 WRITE — only when something genuinely new is discovered

    LAYER 2 — THE CODE (repos)
      Location:  C:\Dev\Projects\, C:\Users\titit\Projects\
      What:      The actual working software
      Purpose:   The thing being built, studied, and fixed
      How used:  READ + WRITE + RUN

    LAYER 3 — FLAGS.txt (study surface)
      Location:  C:\BRAIN_OS\FLAGS.txt
      What:      One line per gap, seven pipe-separated columns
      Purpose:   Real-time record of gaps found while working in Layer 2
      How used:  WRITE — log during sessions, never at the end
      Format:    DATE | REPO | TYPE | THING | EXPECTED | HAPPENED | ACTION

    LAYER 4 — LESSON QUEUE (direction map)
      Location:  C:\BRAIN_OS\02_PROJECTS\LESSON_QUEUE.md
      What:      Active directions, status, session log
      Purpose:   Tracks what direction we're in, what's done, what's next
      How used:  WRITE — updated at session close only, not mid-session

---

## How the Layers Work Together

Reading a function in Layer 2 triggers all other layers simultaneously:

    find a hardcoded path        → log DESIGN flag in Layer 3
    find an unfamiliar concept   → log CONCEPT flag in Layer 3
    recognize a CS pattern       → classify to a domain in Layer 1
    find something fixable now   → fix it in Layer 2 immediately

One pass does all four. This is the core learning discipline.

---

## The Vault Domains — Classification Reference

When you find a CS concept in code, classify it to one of these:

    ai_engineering.md       — AI system design, MCP protocol, tool definitions,
                              Claude integration, prompt engineering, RAG,
                              embeddings, vector databases

    software_architecture.md — Design patterns, abstraction layers, separation
                               of concerns, client-server, command pattern,
                               three-layer architecture, DRY, single source
                               of truth, fallback chains

    systems_operations.md   — OS interaction, TCP sockets, port binding,
                              localhost networking, process management,
                              UI automation, pyautogui, pywinauto,
                              Windows accessibility tree, focus model,
                              race conditions, lazy initialization

    data_science.md         — Data flow, logging, state management,
                              SQLite, LanceDB, vector stores, JSONL,
                              export logs, data pipelines

    creative_systems.md     — Content pipelines, BDF automation,
                              DaVinci Resolve integration, soccer content
                              generation, audio synthesis, TTS

Classification is a mental connection — not an edit to the domain file.
Add a line to a domain file only when something genuinely new is found
that isn't covered yet.

---

## The Learning Principle

Understanding code and fixing design debt happen in parallel.
You do not finish reading, then fix. You fix as you go.

    Read function → understand what it does
    Find a gap    → log it immediately, don't batch flags at end
    Fix if small  → one-line fixes happen in the same session
    Study if big  → log it, add to queue, come back next session

FLAGS.txt is your syllabus. The queue sorts what comes next.
FreeCodeCamp fills the gap that FLAGS.txt identifies — never the
whole curriculum, only the flagged concept.

---

## The resolve-mcp-server Architecture (current study target)

Three layers inside the system:

    Claude Desktop              — the brain, sends commands via MCP
         ↓  stdio JSON-RPC
    server_api.py (venv)        — MCP translator, 31 tools, runs in venv
         ↓  TCP socket 127.0.0.1:9000
    resolve_bridge.py           — runs INSIDE DaVinci Resolve's Python console
         ↓  Resolve internal API (bmd.scriptapp)
    DaVinci Resolve             — the video editor being controlled

    Key concepts in this system:
      - Lazy initialization (server starts without Resolve open)
      - TCP socket bridge (localhost networking, port 9000)
      - Three-layer architecture (separation of concerns)
      - Command pattern (31 named tools, each atomic)
      - Fallback chain (start_render: 3 strategies before giving up)
      - UI tree traversal (pywinauto reads Windows accessibility tree)
      - exec() reload pattern (bridge reloaded inside Resolve console)

---

## Design Debt Tracker — resolve-mcp-server

Found 2026-08-12 via path audit:

    46 hardcoded paths across 9 files
    Two problem roots:
      C:\BDF\         — BDF content directory
      C:\Users\titit\ — user-specific paths

    Complication: resolve_bridge.py runs inside Resolve's Python console
    and cannot use standard imports. Needs its own path solution.

    Files affected:
      server_api.py, resolve_bridge.py, mcp_ingest.py,
      memory.py, cleanup_config.py, cleanup_plan.py,
      promote_server.py, seed_knowledge.py, resolve_bridge_test.py

    Status: IDENTIFIED — fix planned for Direction 1 continuation

---

## Session Close Checklist

At the end of every session, in order:

    1. Commit FLAGS.txt with new entries
    2. Update LESSON_QUEUE.md — mark directions, add session log line
    3. Commit LESSON_QUEUE.md
    4. Push BRAIN_OS
    5. Run session_close.py if in Claude Code

Never update the queue mid-session. All queue writes happen at close.
