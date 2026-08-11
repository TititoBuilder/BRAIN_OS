# Lesson Queue — Active Directions
Location: C:\BRAIN_OS\09_TOOLS\ or C:\BRAIN_OS\02_PROJECTS\
Updated: 2026-08-10

---

## Status

    Lesson 01 — Repo Reconciliation          COMPLETE
    Lesson 02 — .env + pathlib pattern       IN PROGRESS

---

## Direction 1 — Go Deeper into resolve-mcp-server
Status: QUEUED

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

Opens when:
  Direction 2 is fully complete across all repos

---

## Direction 2 — Fix Hardcoded Path Problem Across All Repos
Status: IN PROGRESS — 50% done

Pattern learned: .env + pathlib
  - BASE_DIR = Path(os.getenv("BASE_DIR", r"fallback\path"))
  - Subdirs built with / operator: BASE_DIR / "chapters"
  - .env.example committed, .env never committed
  - os.getenv second argument is the fallback default
  - int() wrapper needed for numeric env vars

Done:
  [x] custom-agent — ca_audio.py refactored, .env.example added

Remaining — run audit on each, apply same pattern:
  [ ] soccer-content-generator
  [ ] BRAIN_OS tools (compile_session.py, session_close.py)

Audit command (run inside each repo):
  Select-String -Path .\**\*.py -Pattern "Path\(r" | Select-Object Path, LineNumber, Line

What to look for:
  Any Path(r"C:\...") that is not built from an env var

---

## Direction 3 — Reconcile the gig_tracker Split
Status: QUEUED

What it is:
  Two copies of gig_tracker exist:
    - C:\BRAIN_OS\02_PROJECTS\gig_tracker\  (untracked inside vault)
    - C:\Users\titit\OneDrive\Desktop\gig_tracker_v3\gig_tracker  (separate repo)

  One is authoritative. The other is either a stale copy or
  an accidental duplicate.

What you will do:
  - Compare last commit dates on both
  - Diff the two directories
  - Decide which is the real repo
  - Move the winner to C:\Dev\Projects\gig_tracker
  - Delete the OneDrive Desktop copy
  - Add the BRAIN_OS version to .gitignore or remove it

What you will learn:
  - How to compare two directories with git
  - Why OneDrive + git is a bad combination
  - How to move a repo without losing its history

Opens when:
  Direction 2 is complete

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

