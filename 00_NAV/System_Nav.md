---
tags: [nav, system, overview]
updated: 2026-06-23
---

# System Navigation Map

Converted from `NAV_MAP.txt`, a personal quick-reference originally kept
on the Desktop for a fast glance outside Obsidian; moved into the vault
and given the folder's `.md` + frontmatter convention. Content kept as
written — much of it overlaps with [[Navigation_Shortcuts]] (project
paths/commands) and `Queue.md` (open items), which are the more current,
more detailed sources; this stays the terse single-page version.

## The Two Worlds (never mix them)

- **Windows** (`PS C:\>`) — all real projects, production work
- **WSL** (`titit@Cristian`) — Claude OS only (experiment/memory lab)

Windows terminal: Win+X → Terminal (NOT VS Code terminal, NOT admin)
WSL terminal: type `wsl` or open Ubuntu

## Your Projects (Windows) — where each lives

| Project | Path |
|---|---|
| BRAIN_OS (the hub) | `C:\BRAIN_OS` |
| BDF (soccer content) | `C:\Dev\Projects\soccer-content-generator` |
| Read-Along App | `C:\Users\titit\Projects\read-along-app` |
| CristianConstruction | `C:\Dev\CristianConstruction` |
| CA_Book | `C:\Knowledge\CA\CA_Book` |
| Resolve MCP Server | `C:\Users\titit\Projects\resolve-mcp-server` |

Every project has a `PROJECT_CARD.md` in its root as its quick reference.

## BRAIN_OS — key locations

| What | Path |
|---|---|
| Master queue | `C:\BRAIN_OS\00_DASHBOARD\Queue.md` |
| Navigation index | `C:\BRAIN_OS\00_DASHBOARD\Navigation.md` |
| System map (visual) | `C:\BRAIN_OS\07_SYSTEM\system_map.context.md` |
| System map (data) | `C:\BRAIN_OS\07_SYSTEM\system_map.json` |
| Principles | `C:\BRAIN_OS\07_SYSTEM\Cristian_Principles.md` |
| Tools registry | `C:\BRAIN_OS\07_SYSTEM\Tools_Registry.md` |
| Card template | `C:\BRAIN_OS\07_SYSTEM\templates\PROJECT_CARD_TEMPLATE.md` |
| Tools folder | `C:\BRAIN_OS\09_TOOLS\` |

## Everyday commands (Windows PowerShell 5.1)

```powershell
python C:\BRAIN_OS\09_TOOLS\session_start.py       # start a session
python C:\BRAIN_OS\09_TOOLS\session_close.py       # close a session
python C:\BRAIN_OS\09_TOOLS\graphify.py --cross-project   # rebuild system map
python C:\BRAIN_OS\09_TOOLS\vault_index.py         # rebuild navigation
```

GIT (always `cd` into the repo first):
```powershell
cd <project folder>
git status                       # look BEFORE you commit
git add <exact-filename>         # NEVER use -A
git commit -m "message"
git push
```

## Claude OS (WSL side — separate world)

```
Start:  bash ~/isolated-tools/boot.sh
        cd ~/isolated-tools/test-project && claude
Use:    /claude-os-remember <thing>   |   /claude-os-search <question>
Check:  /mcp   (code-forge connected = good)
Stop:   /exit  (inside Claude Code)
Ports:  8051 (MCP), 5173 (web UI), 6379 (redis), 11434 (ollama)
```
Setup notes / gotchas live in the claude-os-setup repo.

## Which world for what

- Ships / gets versioned (code, queue, deploys) → BRAIN_OS (Windows)
- "I want to recall this later" (decisions) → Claude OS (WSL)
- ONE rule: a fact lives in exactly ONE world. Never both.

## Hard rules (the ones that bite)

- git add by exact filename, NEVER -A
- Never Set-Content / ConvertTo-Json on JSON (mangles + BOM)
- Audio (.mp3/.wav/.mp4) lives on Google Drive, never in git
- Verify reality (read-only) BEFORE you write
- "For now" is forbidden — root fixes only
- obs = OBS Studio (streaming) | obsidian = the notes app. NEVER confuse.
- CA = the book project (`C:\Knowledge\CA`) | CC = CristianConstruction. Different.

## Open items (as of 2026-06-23 — check Queue.md for current state)

- BRAIN_OS dashboard build (spec ready; use ports 5273 + 8100)
- Railway token swap to a Project token (read-along-app)
- CA_Book\venv deletion decision (stale by evidence, parked)
- WSL: remove stale OAuth token in `.bashrc`, write `boot.sh`

---
Full detail per project: open that project's `PROJECT_CARD.md`.
Everything else: [[Queue]] (00_DASHBOARD).

---
**→** [[Navigation_Shortcuts]] · [[Queue]]
