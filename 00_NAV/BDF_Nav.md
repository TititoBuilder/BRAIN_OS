---
tags: [nav, bdf]
updated: 2026-05-05
commit: 7c765fc
---

# BDF Navigation — BreakingDown Futbol

## Launch Sequence (4 terminals)
```powershell
# T1 — Bot (heartbeat loop)
cd C:\Dev\Projects\soccer-content-generator
.\venv\Scripts\Activate.ps1
python bot_service.py

# T2 — API
cd C:\Dev\Projects\soccer-content-generator
.\venv\Scripts\Activate.ps1
uvicorn dashboard_api:app --reload

# T3 — Dashboard
cd C:\Dev\Projects\soccer-content-generator\dashboard
npm run dev

# T4 — Claude Code
cd C:\Dev\Projects\soccer-content-generator
claude
```
**URLs:** API `http://localhost:8000` · Dashboard `http://localhost:5173`

## Key Paths
| Item | Path |
|---|---|
| Code | `C:\Dev\Projects\soccer-content-generator\` |
| Venv | `C:\Dev\Projects\soccer-content-generator\venv\` |
| LanceDB | `C:\lance_db_soccer\` |
| Cards | `src\images\cards\` (gitignored) |
| Book chapters | `C:\Knowledge\BDF\BDF_Book\chapters\` |
| Book incoming | `C:\Knowledge\BDF\BDF_Book\incoming\` |
| Session resumes | `C:\Knowledge\BDF\Session_Resumes\` |
| Workspace | `bdf.code-workspace` |
| Renders | `C:\BDF\renders\` |
| Staging | `C:\BDF\renders\staging\` |
| Export log | `C:\BDF\renders\export_log.jsonl` |

## Image Pipeline (current)
DaVinci Resolve exports → `card_composer.py` → branded cards
**NOT gpt-image-1** (deprecated May 12, 2026)

## Book Aliases
```powershell
bdf-log "file.txt"      # Downloads → Session_Resumes\processed\
bdf-compile "file.txt"  # Downloads → BDF_Book\incoming\
bdf-book                # compile + TTS + Drive sync ($1-2.50/run)
```

## GitHub
Remote: `https://github.com/TititoBuilder/soccer-content-generator`
HEAD: `7c765fc` — fix: correct CLAUDE.md paths, stale clip config, wire obs_mcp

## Secrets (gitignored)
`.env` · `gdrive_credentials.json` · `gdrive_token.json`

## Troubleshooting
```powershell
# Drive OAuth expired
Remove-Item gdrive_token.json
python -c "import book_compiler; book_compiler.get_drive_service()"

# Force book restitch without incoming
python -c "from book_compiler import stitch_master_book; stitch_master_book()"

# Bridge reload (after any resolve_bridge.py change)
# Paste in Resolve Py3 console:
exec(open(r"C:\Users\titit\Projects\resolve-mcp-server\resolve_bridge.py", encoding="utf-8").read())
```
