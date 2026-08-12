# Lesson Queue — Active Directions
Location: C:\BRAIN_OS\02_PROJECTS\LESSON_QUEUE.md
Updated: 2026-08-10

---

## Status

    Lesson 01 — Repo Reconciliation          COMPLETE ✓ 2026-08-10
    Lesson 02 — .env + pathlib pattern       COMPLETE ✓ 2026-08-10
    Direction 3 — gig_tracker split          COMPLETE ✓ 2026-08-10
    Direction 4 — Downloads folder triage    COMPLETE ✓ 2026-08-10
    Direction 1 — resolve-mcp-server arch.   QUEUED — next session opener

---

## Direction 1 — Go Deeper into resolve-mcp-server
Status: QUEUED — opens next session

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