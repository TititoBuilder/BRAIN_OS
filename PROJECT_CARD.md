# PROJECT_CARD — BRAIN_OS

> One-line identity: Personal knowledge operating system — the Obsidian vault + tooling that is shared memory and architectural map across all projects.
> Backed up at: https://github.com/TititoBuilder/BRAIN_OS.git

---

## 1. Identity
The hub. An Obsidian vault at C:\BRAIN_OS, git-managed, holding session lifecycle tools, the cross-project system map, the master queue, and the graph system. Not just notes — the connective layer of the whole dev ecosystem.

## 2. Context / Boundary Rule
- Runs on: Windows PowerShell 5.1 (Win+X Terminal only — never VS Code terminal)
- Venv: none (BRAIN_OS tools borrow the BDF venv for the dashboard API)
- Do NOT confuse with: Claude OS (the separate WSL2 system) — different world entirely
- Prompt looks like: PS C:\BRAIN_OS>

## 3. Daily Use (start / stop / commands you actually run)
START:  python C:\BRAIN_OS\09_TOOLS\session_start.py
USE:    python 09_TOOLS\graphify.py --cross-project   (regenerate system map)
        git add <file> ; git commit ; git push        (explicit filenames, never -A)
STOP:   python C:\BRAIN_OS\09_TOOLS\session_close.py   (auto-refreshes Navigation.md)

## 4. What is Installed and Where
| Thing | Path / detail |
|---|---|
| Root | C:\BRAIN_OS |
| Tools | 09_TOOLS\ (graphify.py, session_start/close.py, vault_index.py) |
| System map | 07_SYSTEM\system_map.json (+ .context.md render) |
| Queue | 00_DASHBOARD\Queue.md |
| Config | BRAIN_OS_CONFIG.json (Drive folder IDs, TTL) |

## 5. Connections (what it touches)
- brain-audio: no (it is the consumer/orchestrator, not an installer)
- Google Drive: yes — audio lives on Drive only, never committed
- Deploys to: none
- Other projects: maps all 7 via projects.manifest.json

## 6. Gotchas (hard-won — read before troubleshooting)
1. Audio files (*.mp3/*.wav) must stay gitignored — Drive only, never commit binaries.
2. Never Set-Content / ConvertTo-Json on JSON files (mangles structure, adds BOM).
3. PowerShell 5.1 console reads UTF-8 wrong — fixed in AllHosts profile.ps1.

## 7. Principles in Force
Single Source of Truth (system_map.json derived, never hand-edited), Verify-Before-Write, git add by explicit filename, No Dead Code, "For now" is forbidden.

## 8. Queues (this project open items)
Tracked centrally in C:\BRAIN_OS\00_DASHBOARD\Queue.md

## 9. Navigation (where to find things)
- This card: C:\BRAIN_OS\PROJECT_CARD.md
- CLAUDE.md: C:\BRAIN_OS\CLAUDE.md
- System map: 07_SYSTEM\system_map.context.md
- Nav index: 00_DASHBOARD\Navigation.md
- Principles: 07_SYSTEM\Cristian_Principles.md

---
Last updated: 2026-06-23 - Card format v1
