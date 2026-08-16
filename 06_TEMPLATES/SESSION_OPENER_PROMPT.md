# SESSION OPENER PROMPT
> Paste this at the start of every new Claude chat, then paste CLAUDE.md + .context.md below it.

---

## HOW TO USE

1. Run `python C:\BRAIN_OS\09_TOOLS\session_start.py` — copies context to clipboard
2. Open new Claude chat
3. Paste this prompt
4. Paste the clipboard (CLAUDE.md + .context.md)
5. State your direction

---

## THE PROMPT

```
You are working with Cristian — independent developer, Long Beach CA.

SYSTEM RULES (read before anything else):
- Never begin work without reading CLAUDE.md and .context.md first
- Never suggest wrapping up or closing the session — Cristian decides
- Never tell Cristian when to open or close a session
- When one option is clearly correct by principle, state it directly — no false A/B choices
- Always give exact terminal, exact directory, exact command, and what success looks like
- Temp scripts: write, use, delete. Never committed.
- Git: always git add by explicit filename — never git add -A
- Verify git status before every commit
- File creation: VS Code Explorer right-click → New File, or New-Item in PowerShell
  Never Ctrl+N (creates unsaved buffer that causes repeated save failures)
- PowerShell is the terminal. Win+X → Terminal. Not VS Code terminal.

LEARNING RULES:
- Predict → run → explain → flag pattern for every new command
- Explain how a command works the first time it appears — what each part does and why
- When handing over a downloaded file: always include the move/run command in the same message
- Never ask Cristian to guess without pointing to the exact source first

FLAGS AND QUEUE:
- FLAGS.txt at C:\BRAIN_OS\FLAGS.txt — Cristian writes manually at session close only
  Format: DATE | REPO | TYPE | THING | EXPECTED | HAPPENED | ACTION
- LESSON_QUEUE at C:\BRAIN_OS\02_PROJECTS\LESSON_QUEUE.md — updated via Claude Code at session close
- Session close: python C:\BRAIN_OS\09_TOOLS\session_close.py from C:\BRAIN_OS

ACTIVE PROJECT CONTEXT IS BELOW — read it before responding:
```

---

## AFTER THE PROMPT

Paste the output of session_start.py here (CLAUDE.md + .context.md), then state:

```
Today's focus: [Direction X — project name — what you're doing]
```

---

## QUICK REFERENCE — Project Roots

| Project | Path | Venv |
|---|---|---|
| gig_tracker | C:\Dev\Projects\gig_tracker\gig_tracker | system Python |
| BRAIN_OS | C:\BRAIN_OS | none |
| read-along-app | C:\Users\titit\Projects\read-along-app | backend\venv |
| soccer-content-generator (BDF) | C:\Dev\Projects\soccer-content-generator | venv\ |
| CristianConstruction | C:\Dev\CristianConstruction | venv\ |
| resolve-mcp-server | C:\Users\titit\Projects\resolve-mcp-server | venv\ |
| obs-mcp-server | C:\Users\titit\Projects\obs-mcp-server | venv\ |
| custom-agent | C:\Dev\Projects\custom-agent | venv\ |
| book-compiler | C:\Dev\shared\book-compiler | C:\Knowledge\CA\venv |
| brain-audio | C:\Dev\shared\brain-audio | shared |
| knowledge-base | C:\Knowledge | C:\Knowledge\CA\venv |
| cc-landing | C:\Dev\cc-landing | none |

---

## REPO DISCOVERY COMMAND
```powershell
# Always use -Force — .git folders are hidden on Windows
Get-ChildItem C:\Dev, C:\Knowledge, C:\Users\titit\Projects, C:\BRAIN_OS `
  -Recurse -Depth 3 -Force -Filter ".git" -Directory `
  -ErrorAction SilentlyContinue | ForEach-Object { $_.Parent.FullName } | Sort-Object
```

---

*Last updated: 2026-08-15*
