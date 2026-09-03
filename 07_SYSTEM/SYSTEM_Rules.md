---
tags: [nav, system, rules]
updated: 2026-05-05
---

# System Rules

## Machine
Predator Helios Neo · Windows 11 · User: titit
GPU: NVIDIA RTX 5070 Ti · CUDA 13.2 driver
Python: 3.12.10 · Shell: PowerShell
GitHub: TititoBuilder

## Core Rules
1. ONE workspace = ONE project. Never cd between projects.
2. ONE terminal = ONE venv. Fresh terminal when switching.
3. ONE file per BDF compile run. Never batch ($1-2.50/run, batching = $7-8).
4. ONE file per CA chapter. CA compiler stops at first tag.
5. Mixed-project chats = SEPARATE compile files per book.
6. Plain ASCII in PowerShell scripts. No emoji/Unicode.
7. Edit files via VS Code, never PowerShell Set-Content.
8. `where.exe python` not `where python` in PowerShell.
9. Never put Python projects or venvs inside OneDrive.
10. Verify cost estimate before token-consuming operations.
11. Load project nav file at START of every Claude chat.

## Storage (current)
- C: drive: 703 GB free — all active project data lives here
- WD Elements external: personal files only — no project dependencies
- LanceDB: `C:\lance_db_soccer\` (migrated from external, May 2026)

## Venv Workflow
```powershell
& .\venv\Scripts\Activate.ps1     # activate
where.exe python                   # verify (venv path must be first)
deactivate                         # deactivate
```
PyTorch CUDA pattern:
```powershell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
```

## PowerShell Profile
Location: `C:\Users\titit\OneDrive\Documents\WindowsPowerShell\`
Reload: `. $PROFILE`

## All Aliases
| Alias | Action |
|---|---|
| `bdf-log <file>` | Downloads → BDF Session_Resumes\processed\ |
| `bdf-compile <file>` | Downloads → BDF_Book\incoming\ |
| `bdf-book` | BDF compile + TTS + Drive sync |
| `ca-log <file>` | Downloads → CA Session_Resumes\processed\ |
| `ca-compile <file>` | Downloads → CA_Book\incoming\ |
| `ca-book` | CA compile + Drive sync |
| `ca-audio` | Run ca_audio.py with CA venv |
| `mcp-log <file>` | Downloads → MCP Session_Resumes\processed\ |
| `mcp-compile <file>` | Downloads → MCP_Book\incoming\ |
| `mcp-book` | MCP compile |
| `dev` | Watch cc_landing.html → auto-deploy to Vercel |

## Compile Session Workflow
```
1. Tell Claude: "compile session"
2. Claude produces compile file(s)
3. Save to Downloads
4. Run: bdf-compile "file.txt" → bdf-book
      ca-compile "file.txt"  → ca-book
      mcp-compile "file.txt" → mcp-book
```

## VS Code Workspaces
| Project | Workspace |
|---|---|
| BDF | `C:\Dev\Projects\soccer-content-generator\bdf.code-workspace` |
| CA Business OS | `C:\Dev\CristianConstruction\custom-agent.code-workspace` |
| Read-Along | `C:\Users\titit\Projects\read-along-app\read-along.code-workspace` |

## Obsidian MCP
Requires Obsidian app to be OPEN. If tool calls hang → open Obsidian first.
Vault name: `brain-os`

## Common Fixes
```powershell
# Aliases not loading
. $PROFILE

# Venv not active
& .\venv\Scripts\Activate.ps1
where.exe python

# Claude Code signal-leak (KeyboardInterrupt)
# Use /exit in another terminal tab
```

## Knowledge Registration Map
_Where a new thing must register so it does not get stranded (the gap that bit us 2026-06-11)._

**New knowledge_os lesson -> auto-registers by status (no manual list):**
1. Write lesson -> `02_PROJECTS/knowledge_os/{key}.md` with `knowledge_os_status: Learning` (or Practiced/Mastered). Status at Learning-or-above = auto-included in NODES. Below Learning (Not Started / no status) = excluded.
2. Run `populate_staging.py --skip-tts` (audio exists) or full run (needs TTS) -> auto: transcribe, upload Drive, write `id:` to `09_TOOLS/drive_index.json`. Confirm Drive ID with `get_ids.py`.

NODES is DERIVED, not hand-maintained: `derive_knowledge_os_nodes()` scans the folder + filters by status. A lesson registers the moment its status reaches Learning. No NODES edit, ever.

**Source-of-truth files:** index `09_TOOLS/drive_index.json` (app reads from GitHub raw, id: format) - queue `00_DASHBOARD/Queue.md` - principles `07_SYSTEM/Cristian_Principles.md` - tools `07_SYSTEM/Tools_Registry.md`

**App is decoupled from vault:** deleting or editing a lesson .md does NOT affect the live app. The app serves audio from Drive via the index; vault .md is the authoring source. Changes reach the app only when you re-run `populate_staging.py`.

**Known drift:** NODES drift FIXED 2026-06-11 (now auto-derives). Remaining: Drive has ~187 unmapped audio files - see `05_MEMORY/Drive_Audio_Audit_2026-06-11.md`.

---

**→** [[SYSTEM_MASTER]] · [[PowerShell_Aliases]]
