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
