---
tags: [system, navigation, reference, shortcuts]
updated: 2026-05-02
---

# Navigation & Shortcuts Reference

Single source of truth for navigating to any project, running any tool, and
understanding the filesystem structure. This document lives in BRAIN_OS and
is accessible via Obsidian quick switcher (Ctrl+O → type "navigation").

**Key principle:** Absolute paths starting with C:\ work from anywhere.
Relative paths only work when you're already in the right directory.

---

## Core Navigation Pattern

From any directory, navigate to any project using absolute paths:

```powershell
cd C:\BRAIN_OS                                      # Knowledge vault and documentation
cd C:\Knowledge                                     # BDF Book, CA Book, compiled content
cd C:\Dev\CristianConstruction                      # CA FastAPI business OS
cd C:\Dev\Projects\soccer-content-generator        # BDF content pipeline
cd C:\Dev\Projects\custom-agent                    # TTS compiler
cd C:\Users\titit\Projects\resolve-mcp-server      # DaVinci Resolve MCP
cd C:\Users\titit\Projects\obs-mcp-server          # OBS control MCP
cd C:\Users\titit\Projects\read-along-app          # Whisper transcription
```

After navigating, launch Claude Code:
```powershell
claude
```

---

## All Projects — Detailed Reference

### Project 1 — BDF (BreakingDown Futbol) Soccer Bot

**What it is:** Automated soccer content pipeline. Generates Twitter posts with
branded image cards, routes through Telegram for human approval, then publishes
to Twitter @tititoluli1987. Targets World Cup 2026 and UCL knockout content.

**How it works:** Linear data pipeline on a 60-second heartbeat loop:
LanceDB (knowledge) → TopicRouter → RAG → Generator → Card Composer →
Telegram approval → Twitter publish. Uses Claude Sonnet for content,
gpt-image-1 for images, Pillow for card compositing, Kokoro for book TTS.

**State:** Mature, production. Most active project.

**Launch sequence (4 terminals):**
```powershell
# T1 — bot
cd C:\Dev\Projects\soccer-content-generator
& .\venv\Scripts\Activate.ps1
python bot_service.py

# T2 — API
cd C:\Dev\Projects\soccer-content-generator
& .\venv\Scripts\Activate.ps1
uvicorn dashboard_api:app --reload

# T3 — dashboard
cd C:\Dev\Projects\soccer-content-generator\dashboard
npm run dev

# T4 — one-off commands (book compile, diagnostics, etc.)
```

URLs: API http://localhost:8000 | Dashboard http://localhost:5173

**Key paths:**
- Code root: `C:\Dev\Projects\soccer-content-generator\`
- Venv: `C:\Dev\Projects\soccer-content-generator\venv\`
- Entry point: `bot_service.py`
- Dashboard API: `dashboard_api.py`
- TTS: `tts_local.py`, `converter.py`
- BDF Knowledge Base: `C:\Knowledge\BDF\`
  - Chapters: `BDF_Book\chapters\` (16 .txt files)
  - Audio: `BDF_Book\audio\` (.mp3, af_heart voice)
  - Incoming: `BDF_Book\incoming\` (drop here, run `bdf-book`)
  - Processed: `BDF_Book\_processed\`
  - Full book: `BDF_Book\BDF_Master_Book.txt`
  - Cost log: `BDF_Book\cost_log.txt`
- LanceDB vector store: `F:\lance_db_soccer\` (WD Elements, always plugged in)
- Generated card images: `src\images\cards\` (gitignored)
- Session audio format: `SESSION_YYYYMMDD_HHMM_audio.mp3`
- Cloud backup: Google Drive folder `BDF_Book_Audio\chapters\`

**Git:**
- Local: `C:\Dev\Projects\soccer-content-generator\`
- Remote: https://github.com/TititoBuilder/soccer-content-generator
- Latest: 91c3168 (gitignore cleanup, 4/14/2026)

**Workspace:** `C:\Dev\Projects\soccer-content-generator\bdf.code-workspace`

---

### Project 2 — Custom Agent (Construction Business OS)

**What it is:** 9-agent FastAPI business operating system for Custom Agent
Remodel & Skilltrade construction company in South CA. Handles leads, quotes,
reviews, scheduling, social posts, finances, proposals, reputation, and referrals.

**How it works:** Hub-and-spoke service mesh. Event-driven architecture.
Each of 9 agents waits for specific event types (SMS keywords, Telegram commands,
scheduled triggers). FastAPI backend on :8000, React dashboard on :3000.

**State:** Functional, has dedicated venv as of 4/14/2026.

**Launch sequence (2 terminals):**
```powershell
# T1 — API
cd C:\Dev\CristianConstruction
& .\venv\Scripts\Activate.ps1
uvicorn src.api.main:app --reload

# T2 — dashboard
cd C:\Dev\CristianConstruction\dashboard
npm run dev
```

URLs: API http://localhost:8000 | Dashboard http://localhost:3000 | Docs http://localhost:8000/docs

**Key paths:**
- Code root (FastAPI app): `C:\Dev\CristianConstruction\`
- Venv: `C:\Dev\CristianConstruction\venv\`
- Agents: `src\agents\` (9 agents)
- API routes: `src\api\`
- Dashboard: `dashboard\` (React/Vite)
- Business data: `data\` (jobs.csv, clients.csv, schedule.csv, reviews.csv — gitignored)
- Brand assets: `CA_logo_*.svg`
- Landing page source: `cc_landing.html`
- Requirements: `requirements.txt` (31 pinned packages)
- TTS companion root: `C:\Dev\Projects\custom-agent\`
- TTS companion venv: `C:\Dev\Projects\custom-agent\venv\` (patched coqui-tts)
- TTS companion script: `C:\Dev\Projects\custom-agent\ca_audio.py`
- CA Knowledge Base: `C:\Knowledge\CA\`
  - Chapters: `CA_Book\chapters\` (10 .md files)
  - Audio: `CA_Book\audio\` (.wav files)
  - Incoming: `CA_Book\incoming\` (drop here, run `ca-book`)
  - Book compiler: `CA_Book\book_compiler.py` (lives here, not in code root)
  - Venv (compiler): `C:\Knowledge\CA\CA_Book\venv\`
  - Full book: `CA_Book\CA_Master_Book.txt`

**Git:**
- Local: `C:\Dev\CristianConstruction\`
- Remote: https://github.com/TititoBuilder/cristian-construction
- Latest: ec87b8a (foundation: dedicated venv, 4/14/2026)

**Workspace:** `C:\Dev\CristianConstruction\custom-agent.code-workspace`
(multi-root: includes both CristianConstruction AND custom-agent folders)

---

### Project 3 — Read-Along App (Learning Review Tool)

**What it is:** Karaoke-style learning review tool. Upload audio (MP3, WAV,
M4A) or text files (TXT, MD). Audio gets transcribed by Whisper with
word-level timestamps. Words highlight green as audio plays. Click any word
to mark it red for review. Export marked items to a study .txt file.

**Modes:**
- Audio mode: Upload → Whisper transcribes → karaoke playback → click to mark → export
- TTS mode: Upload .txt/.md → Kokoro generates audio → Whisper transcribes → karaoke playback
- Read-only mode: Upload .txt/.md → line numbers → click to mark → export (no audio)

**State:** MVP complete. Backend production-ready. Local git commit 203e6bc.
No GitHub remote yet. Venv has broken .exe launchers — always use `python -m uvicorn`.

**Launch sequence (2 terminals):**
```powershell
# T1 — backend
cd C:\Users\titit\Projects\read-along-app\backend
& ..\backend\venv\Scripts\Activate.ps1
python -m uvicorn backend:app --reload
# NOTE: use "python -m uvicorn" not "uvicorn" (broken .exe shebang)

# T2 — frontend
cd C:\Users\titit\Projects\read-along-app\frontend
npm run dev
```

URLs: Frontend http://localhost:5173 | Backend http://localhost:8000 | Swagger http://localhost:8000/docs

**Key paths:**
- Root: `C:\Users\titit\Projects\read-along-app\`
- Backend: `backend\backend.py`
- Venv: `backend\venv\` (PyTorch + Whisper + FastAPI)
- Frontend: `frontend\src\`
  - `components\AudioPlayer.tsx` — play/pause, seek, speed
  - `components\FileUpload.tsx` — drag-drop, audio + text files
  - `components\TextDisplay.tsx` — line-by-line view + marking
  - `components\TranscriptDisplay.tsx` — karaoke word sync + marking
  - `utils\export.ts` — marked items → .txt download
  - `App.tsx` — main layout + state management
- Generated audio: `generated_audio\` (TTS output, served to frontend)

**Git:**
- Local: `C:\Users\titit\Projects\read-along-app\`
- Remote: NONE (deferred until more content), latest: 203e6bc

**Workspace:** `C:\Users\titit\Projects\read-along-app\read-along.code-workspace`

**IMPORTANT:** TTS mode calls BDF's `tts_local.py` via subprocess. Do NOT run
`bdf-book` or `bot_service.py` at the same time — Kokoro will fight over GPU memory.

---

### Project 4 — CC-Landing (Marketing Landing Page)

**What it is:** Mobile-optimized landing page for Custom Agent Remodel &
Skilltrade. Single HTML file with embedded CSS/JS.

**Workflow:**
```powershell
# Edit
code C:\Dev\CristianConstruction\cc_landing.html

# Deploy manually
C:\Dev\deploy-landing.ps1

# Watch mode (auto-deploys on save)
dev
```

**Live at:** https://cc-landing-v2-eta.vercel.app

**Git:** Separate deploy repo — https://github.com/TititoBuilder/cc-landing
(NOT inside cristian-construction — Vercel pulls from this repo)

---

## PowerShell Aliases Reference

**Profile locations:**
```
C:\Users\titit\OneDrive\Documents\WindowsPowerShell\Microsoft.VSCode_profile.ps1     (VS Code terminal)
C:\Users\titit\OneDrive\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1 (regular PowerShell)
```

Reload after editing: `. $PROFILE`

### BDF Book Aliases

```powershell
bdf-log "filename.txt"
# Moves file from Downloads to BDF Session_Resumes\processed\

bdf-compile "filename.txt"
# Moves file from Downloads to BDF_Book\incoming\

bdf-book
# Activates BDF venv, runs python book_compiler.py
# Compiles all files in incoming\, generates audio, syncs to Drive
```

### CA Book Aliases

```powershell
ca-log "filename.txt"
# Moves file from Downloads to CA Session_Resumes\processed\

ca-compile "filename.txt"
# Moves file from Downloads to CA_Book\incoming\

ca-book
# Activates CA venv, runs CA book_compiler.py
# IMPORTANT: CA compiler stops at first #chXX tag.
# For multi-chapter sessions, use ONE FILE PER CHAPTER.

ca-audio chXX_name
# Activates TTS venv, runs ca_audio.py for specified chapter
# Output: .wav format to C:\Knowledge\CA\CA_Book\audio\
```

### Landing Page Alias

```powershell
dev
# File watcher — auto-deploys cc_landing.html on save
```

---

## Compile Session Workflow

End of chat — to capture session into books:

1. Type "compile session" to Claude
2. Claude produces compile file(s):
   - BDF content → `session_compile_bdf.txt` (multi-section OK)
   - CA content → ONE FILE PER CHAPTER (CA compiler stops at first tag)
3. Save to `C:\Users\titit\Downloads\`
4. Run aliases:

```powershell
bdf-compile "session_compile_bdf.txt"
bdf-book

ca-compile "session_compile_ca_chXX.txt"
ca-book
# (one ca-compile + ca-book pair per CA chapter)
```

**Cost discipline:**
- ONE file per BDF run = $1–2.50 normal
- Batching causes overlap = $7–8 (avoid)
- Always state estimated cost before running

---

## Project Folder Tree

```
C:\Dev\
├── Projects\
│   ├── soccer-content-generator\     (BDF code)
│   │   ├── venv\                     (BDF Python env)
│   │   ├── src\                      (agents, publishers, composers)
│   │   ├── dashboard\                (React/Vite UI)
│   │   ├── data\                     (cost_log, runtime state)
│   │   ├── book_compiler.py
│   │   ├── bot_service.py            (heartbeat loop entry point)
│   │   ├── dashboard_api.py          (FastAPI backend)
│   │   ├── tts_local.py              (Kokoro audio for book)
│   │   └── converter.py              (text -> TTS-ready format)
│   │
│   └── custom-agent\                 (CA TTS companion)
│       ├── venv\                     (TTS env, patched coqui-tts)
│       ├── ca_audio.py               (CA book audio synth)
│       └── TTS_PATCH_NOTES.md
│
├── CristianConstruction\             (CA app code)
│   ├── venv\                         (CA Python env, dedicated)
│   ├── src\
│   │   ├── agents\                   (9 FastAPI agents)
│   │   └── api\                      (FastAPI routes)
│   ├── dashboard\                    (React/Vite UI)
│   ├── data\                         (CSV business data)
│   ├── cc_landing.html               (Project 4 source)
│   ├── cc_door_hanger.html
│   ├── cc_business_card.html
│   ├── CA_logo_*.svg                 (brand assets)
│   └── requirements.txt              (31 pinned packages)
│
└── deploy-landing.ps1                (Vercel deploy script)


C:\Users\titit\Projects\
└── read-along-app\                   (Project 3)
    ├── backend\
    │   ├── venv\                     (PyTorch + Whisper + FastAPI)
    │   └── backend.py
    ├── frontend\
    │   └── src\
    │       ├── components\
    │       │   ├── AudioPlayer.tsx
    │       │   ├── FileUpload.tsx
    │       │   ├── TextDisplay.tsx
    │       │   └── TranscriptDisplay.tsx
    │       ├── utils\export.ts
    │       ├── App.tsx
    │       └── types.ts
    └── generated_audio\


C:\Knowledge\
├── BDF\                              (BDF book + sessions + archives)
│   ├── BDF_Book\
│   │   ├── chapters\                 (16 chapter .txt files)
│   │   ├── audio\                    (.mp3, af_heart voice)
│   │   ├── incoming\                 (drop here, run bdf-book)
│   │   ├── _processed\
│   │   ├── _review\
│   │   └── _rejected\
│   └── Session_Resumes\
│       ├── processed\
│       └── Working on\
├── CA\                               (CA book + sessions)
│   ├── CA_Book\
│   │   ├── chapters\                 (10 chapter .md files)
│   │   ├── audio\                    (.wav files)
│   │   ├── incoming\
│   │   ├── book_compiler.py          (CA compiler lives here)
│   │   └── venv\
│   └── Session_Resumes\
├── Claudeguide\
├── Dev\
├── Hardware\
└── Personal\


C:\BRAIN_OS\                          (this vault — Obsidian)
F:\lance_db_soccer\                   (LanceDB, WD Elements — always plugged in)
```

---

## VS Code Workspaces

| Workspace | Path |
|---|---|
| BDF | `C:\Dev\Projects\soccer-content-generator\bdf.code-workspace` |
| Custom Agent | `C:\Dev\CristianConstruction\custom-agent.code-workspace` |
| Read-Along | `C:\Users\titit\Projects\read-along-app\read-along.code-workspace` |

Open: File → Open Workspace from File...

Note: `custom-agent.code-workspace` is multi-root — includes both CristianConstruction
AND custom-agent folders, each using its own venv via `.vscode\settings.json`.

---

## Git Repositories

| Project | Local | Remote |
|---|---|---|
| BDF | `C:\Dev\Projects\soccer-content-generator\` | github.com/TititoBuilder/soccer-content-generator |
| Custom Agent | `C:\Dev\CristianConstruction\` | github.com/TititoBuilder/cristian-construction |
| CC-Landing | N/A | github.com/TititoBuilder/cc-landing |
| Read-Along | `C:\Users\titit\Projects\read-along-app\` | NONE (local only) |
| Knowledge Base | `C:\Knowledge\` | github.com/TititoBuilder/knowledge-base (private) |
| BRAIN_OS | `C:\BRAIN_OS\` | (this vault) |

---

## Key Rules

1. ONE workspace = ONE project. Don't `cd` between project folders in the same terminal.
2. ONE terminal = ONE venv. Open a fresh terminal when switching projects.
3. ONE file per BDF compile run. Never batch.
4. ONE file per CA chapter. CA compiler stops at first `#chXX` tag.
5. Mixed-project chats produce SEPARATE compile files per book. Never cross-contaminate.
6. Plain ASCII in PowerShell scripts. No emoji, no Unicode in command-line code.
7. Edit existing files via VS Code Explorer right-click — never PowerShell here-strings.
8. WD Elements (F:\lance_db_soccer) stays plugged into Predator permanently.
9. C: drive has limited free space — large data goes to F:.
10. Verify cost estimate before any token-consuming operation.

---

## Troubleshooting Quick Reference

**Venv not active:**
```powershell
& .\venv\Scripts\Activate.ps1
where.exe python    # should show venv path first
```

**Profile aliases not loading:**
```powershell
. $PROFILE
Get-Command bdf-log, bdf-compile, bdf-book
```

**Google Drive OAuth expired:**
```powershell
cd C:\Dev\Projects\soccer-content-generator
Remove-Item gdrive_token.json
python -c "import book_compiler; book_compiler.get_drive_service()"
# Browser opens — approve — token refreshed
```

**Claude Code signal-leak (Python imports interrupted):**
- Symptom: `KeyboardInterrupt` without pressing Ctrl+C
- Cause: Claude Code running in another VS Code terminal tab
- Fix: close Claude Code with `/exit`, retry import

**Custom Agent venv shows wrong interpreter:**
- Workspace setting: `${workspaceFolder:CristianConstruction}/venv/Scripts/python.exe`
- custom-agent companion uses its own `.vscode\settings.json`

**Audio file stale (text newer than audio):**
```powershell
python -c "from book_compiler import run_tts; from pathlib import Path; run_tts(Path('C:/Knowledge/BDF/BDF_Book/chapters/chXX_name.txt'))"
```

**Read-Along venv .exe launchers broken:**
- Symptom: `Unable to create process using C:\Knowledge\read-along-app...`
- Cause: venv was moved from `C:\Knowledge\` to `C:\Users\titit\Projects\`
- Fix: always use `python -m uvicorn` instead of `uvicorn`

**Read-Along TTS subprocess encoding crash:**
- Symptom: `UnicodeEncodeError cp1252 can't encode emoji`
- Fix: already resolved — `backend.py` passes `env={"PYTHONUTF8": "1"}` to subprocess
- Do not remove the `utf8_env` lines from `backend.py`

---

## Mental Model — Absolute vs Relative Paths

**Absolute path** starts with a drive letter (`C:\`, `D:\`, `F:\`). Works from anywhere
on your system. Example: `cd C:\BRAIN_OS` always takes you to BRAIN_OS regardless
of where you currently are.

**Relative path** starts from your current location. Only works if you're already
in the right parent directory. Example: `cd Projects\obs-mcp-server` only works
if you're currently at `C:\Users\titit\`.

When in doubt, use absolute paths. They're longer to type but they always work.

---

## Common Navigation Mistakes

**Mistake:** Trying to `cd BRAIN_OS` from Desktop
**Why it fails:** BRAIN_OS doesn't exist inside Desktop. It's at `C:\BRAIN_OS` which
is a completely different location.
**Fix:** Use the absolute path: `cd C:\BRAIN_OS`

**Mistake:** Getting lost in nested directories and not knowing where you are
**How to check:** Run `pwd` to see your current location
**How to reset:** Use `cd C:\` to go to the drive root, then navigate from there
