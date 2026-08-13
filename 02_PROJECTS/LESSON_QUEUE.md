# Lesson Queue — Active Directions
Location: C:\BRAIN_OS\02_PROJECTS\LESSON_QUEUE.md
Updated: 2026-08-12

---

## Status

    Lesson 01 — Repo Reconciliation          COMPLETE ✓ 2026-08-10
    Lesson 02 — .env + pathlib pattern       COMPLETE ✓ 2026-08-10
    Direction 3 — gig_tracker split          COMPLETE ✓ 2026-08-10
    Direction 4 — Downloads folder triage    COMPLETE ✓ 2026-08-10
    Direction 1 — resolve-mcp-server archaeology    COMPLETE ✓ 2026-08-12
    Direction 5 — resolve-mcp-server paths              QUEUED
    Direction 6 — gig_tracker imports and category coverage    COMPLETE ✓ 2026-08-12
    Direction 7 — gig_tracker web.py dashboard + automation    QUEUED

---

## Direction 1 — Go Deeper into resolve-mcp-server
Status: COMPLETE ✓ 2026-08-12

What it is:
  Phase 2 archaeology on the most complex repo in the stack.
  server_api.py is 1,700 lines. You deleted 45 backup files
  but never read the live code.

What you will do:
  - git log --oneline --graph on resolve-mcp-server
  - Hot-spot churn analysis (which files change most)
  - Shift+F12 on major functions to find dead code
  - Read server_api.py top to bottom with VS Code symbols

What you will learn:
  - Whether the codebase is healthy or carrying technical debt
  - How to read a large unfamiliar file systematically
  - git log --follow -p for file archaeology

---

## Direction 2 — Fix Hardcoded Path Problem Across All Repos
Status: COMPLETE ✓ 2026-08-10

Pattern learned: .env + pathlib
  - BASE_DIR = Path(os.getenv("BASE_DIR", r"fallback\path"))
  - Subdirs built with / operator: BASE_DIR / "chapters"
  - .env.example committed, .env never committed
  - os.getenv second argument is the fallback default
  - int() wrapper needed for numeric env vars

Done:
  [x] custom-agent — ca_audio.py refactored, .env.example added
  [x] soccer-content-generator — PathConfig class added to config.py,
      4 paths wired, .env.example added

Audit command (run inside any repo):
  Select-String -Path .\**\*.py -Pattern "Path\(r" | Select-Object Path, LineNumber, Line

---

## Direction 3 — Reconcile the gig_tracker Split
Status: COMPLETE ✓ 2026-08-10

What was done:
  - Identified OneDrive copy as authoritative (newest database Aug 8)
  - CLAUDE_HANDOFF.md and _generated/ reports committed to real repo
  - BRAIN_OS untracked copy deleted
  - Real repo moved from OneDrive Desktop to C:\Dev\Projects\gig_tracker
  - repo_inventory.txt updated with new path
  - gig_tracker/ added to BRAIN_OS .gitignore

---

## Direction 4 — Downloads Folder Triage
Status: COMPLETE ✓ 2026-08-10

What was done:
  - 82 .md files found in Downloads
  - 9 duplicate (1) files deleted
  - 16 batch files moved to C:\Knowledge\CA\CA_Book\incoming\
  - Lesson files → 05_LEARNING\
  - Guide files → 03_KNOWLEDGE\
  - Templates → 06_TEMPLATES\
  - Tools → 09_TOOLS\
  - Sessions → 08_SESSIONS\
  - Nav files → 02_PROJECTS\
  - BDF files → soccer-content-generator\
  - Downloads .md count: 0

---

## Direction 5 — Fix Hardcoded Paths in resolve-mcp-server
Status: QUEUED

What it is:
  46 hardcoded paths across 9 files. Two roots: C:\BDF\ and C:\Users\titit\
  resolve_bridge.py runs inside Resolve's Python console — cannot import
  from config.py. Needs a different path strategy than Directions 2-3.

What you will do:
  - Apply PathConfig to server_api.py, mcp_ingest.py, memory.py,
    cleanup_config.py, cleanup_plan.py, promote_server.py, seed_knowledge.py
  - Solve resolve_bridge.py separately — .env read directly at runtime
    without imports, using pathlib.Path and os.environ

What you will learn:
  - How to handle path configuration when you can't use standard imports
  - os.environ vs os.getenv vs load_dotenv — three ways to read env vars
  - Why runtime context determines your architecture choices

---

## Direction 6 — gig_tracker: Complete Imports + Automation
Status: COMPLETE ✓ 2026-08-12

What it is:
  AMEX still at 0 transactions. Other category at 26% — target is under 15%.
  Expired offer alerts cluttering day-start. Category rules need refinement.

What you will do:
  - Import AMEX statement
  - Run merchants command to find remaining Other merchants
  - Add targeted rules until Other under 15%
  - Fix expired offer auto-cleanup in alerts command
  - Explore web.py dashboard — connect spending data to visual output

What you will learn:
  - Flask routes and template rendering
  - How web.py connects to the same db.py layer
  - SQLite query optimization for dashboard queries

---

## Direction 7 — gig_tracker: web.py Dashboard + Automation
Status: QUEUED — next session opener

What it is:
  584 transactions live across 7 cards. web.py is a Flask dashboard
  that connects all imported data to a visual interface. The dashboard
  should show spending trends, Prop 22 status, and card balances in real time.

What you will do:
  - Read web.py architecture — Flask routes, template rendering
  - Connect spending data to visual charts
  - Fix hardcoded payment due dates in _show_alerts
  - Build dynamic due date tracking from cards table
  - Explore automation: auto-import statements on schedule

What you will learn:
  - Flask request/response cycle
  - Jinja2 templates
  - How web.py shares db.py with gig.py (same data layer)
  - Scheduled tasks vs event-driven automation

---

## Backlog — Future Directions

  B1 — Write .env.example for every repo that has a .env
  B2 — Add .gitignore to any repo missing one
  B3 — Write a 10-line README for each repo (CODE flag fix)
  B4 — Learn git log --follow and git show <sha>:path
       (recover any file from resolve-mcp-server history)
  B5 — Understand load_dotenv() internals — write your own
       in 10 lines of Python to cement the pattern

---

## Session Log

  2026-08-10  Lesson 01 — Full repo audit, 12 repos, 5 RISK flags fixed
  2026-08-10  Lesson 02 — .env + pathlib pattern, applied to custom-agent
  2026-08-10  Directions 2-4 — paths refactored, gig_tracker reconciled,
              82 Downloads files triaged and filed
  2026-08-10  Direction 1 — server.py read complete, full architecture mapped, Option B (live test) queued for next session
  2026-08-12  Direction 1 — resolve_bridge.py fully mapped, 23 CONCEPT flags,
              STUDY_SYSTEM.md created, FLAGS.txt sorted and deduplicated (41 entries)
  2026-08-12  gig_tracker deep dive — 555 transactions imported across 5 cards,
              category rules 51 to 84, Other category 90% to 26%,
              financial CSVs removed from GitHub, prop22.py db.py importer.py fully mapped
  2026-08-12  Direction 6 complete — 584 transactions imported across 7 cards,
              category rules 51→84, Other 90%→22%, format detectors fixed,
              financial CSVs removed from GitHub