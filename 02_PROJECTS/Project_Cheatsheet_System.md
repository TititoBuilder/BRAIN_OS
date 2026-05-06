---
tags: [project, cheatsheets, session-handoff, token-efficiency, workflow]
project: project-cheatsheet-system
status: active
created: 2026-04-18
updated: 2026-04-18
parent: "[[07_SYSTEM]]"
---

# Project Cheatsheet System — Token-Efficient Session Handoff

Seven-file cheatsheet system at `C:\Knowledge\Dev\` that solves Claude session context loss. Instead of uploading one giant master file, only the relevant project file + shared rules are loaded at the start of each session.

---

## Why It Exists

**Problem:** Master cheatsheet was too large — Claude lost track of which projects were already complete (nearly rebuilt the Read-Along App from scratch, which was MVP complete).

**Solution:** Split master into per-project files. Load only what's needed for the current work session.

**Result:** Token efficiency via targeted context + no accidental re-work.

---

## File Structure

```
C:\Knowledge\Dev\
├── 00_index.txt          ← "Which file do I upload?" reference
├── 01_bdf.txt            ← BDF project only
├── 02_ca.txt             ← Custom Agent only
├── 03_readalong.txt      ← Read-Along App only
├── 04_cclanding.txt      ← CC-Landing only
├── 05_resolvemcp.txt     ← Resolve MCP only
├── 06_rules.txt          ← Shared rules, aliases, learning system
└── projects_cheatsheet.txt ← Full combined version (legacy, rarely used)
```

---

## Session Handoff Protocol

**Start of session:**
1. Upload relevant project file (e.g. `01_bdf.txt`)
2. Upload `06_rules.txt` (shared rules always needed)

**During session:**
- Work normally

**End of session:**
- Ask Claude to update the cheatsheet if things changed

**Next session:**
- Repeat with updated files

| Working on | Upload |
|---|---|
| BDF | `01_bdf.txt` + `06_rules.txt` |
| Custom Agent | `02_ca.txt` + `06_rules.txt` |
| Read-Along App | `03_readalong.txt` + `06_rules.txt` |
| Resolve MCP | `05_resolvemcp.txt` + `06_rules.txt` |

---

## Rules This System Enforces

- **Rule 11:** Always `where.exe python`, never `where python` in PowerShell
- **Rule 12:** Never put Python projects or venvs inside OneDrive (sync conflicts)
- **Rule 13:** Upload cheatsheet at START of every new Claude chat

---

## Created

April 18, 2026 — built after the Read-Along near-rebuild incident.

---

## Connected to

- [[AI_Engineering]]
- [[Edge_TTS_Learning_System]]
- [[Session_Protocol]]
- [[Tools_Registry]]
