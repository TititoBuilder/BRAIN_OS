---
tags: [project, whisper, transcription, fastapi, react, scaffolding]
project: read-along-app
status: scaffolding
updated: 2026-05-01
parent: "[[Project_Directory]]"
---

# Read-Along App — Whisper Transcription Tool

Standalone audio transcription tool. User uploads an audio file,
gets back timestamped transcribed text synced with audio playback.

> **CA Book connection: DENIED.**
> This project has no dependency on CA Book WAV files or `ca_audio.py`.
> It is a general-purpose transcription tool, not a CA Book listener.

---

## What It Does

Upload endpoint receives audio → Whisper transcribes on local GPU
(RTX 5070 Ti) → returns timestamped text → frontend displays text
synced with audio playback.

---

## Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI (`backend/backend.py`) |
| Speech-to-text | OpenAI Whisper (local, GPU-accelerated) |
| Frontend | React/Vite (**not yet scaffolded** as of 2026-04-16) |
| Venv | `backend/venv/` (PyTorch + Whisper + FastAPI — large) |

---

## Launch

```powershell
cd C:\Users\titit\Projects\read-along-app\backend
& .\venv\Scripts\Activate.ps1
uvicorn backend:app --reload
```

Frontend: pending Vite scaffold.

---

## Key Paths

| Item | Path |
|---|---|
| Project root | `C:\Users\titit\Projects\read-along-app\` |
| Backend | `backend/backend.py` |
| Frontend | `frontend/` (empty) |
| Workspace file | `read-along.code-workspace` |

---

## Standardization Status (2026-04-30)

| Item | Status |
|---|---|
| `CLAUDE.md` | ✅ Created (auto-generated from filesystem) |
| `.claude/settings.json` | ✅ Scoped — 14 allow + 3 deny rules |
| `.gitignore` | ✅ Protects 3GB venv from git |
| Telegram alerts | ✅ Added to `backend.py` — fires on startup and Whisper model load crash |
| Git | ✅ Local, branch `main`, commit `3fb91ae` (initial, 2026-04-14) |
| GitHub | ✅ `TititoBuilder/read-along-app` (private), pushed 2026-04-30 |
| Model audit | ✅ Zero `claude-opus` references |

---

## Venv History

| Date | Event |
|---|---|
| 2026-04-14 | Initial venv created at `backend/venv/` |
| 2026-04-18 | Venv REBUILT — corrupted .exe launchers, shebang paths pointed to old location, all pip commands failing |

**Rebuild state (2026-04-18):**
- PyTorch 2.11.0+cu128 (from CUDA wheels)
- CUDA verified: RTX 5070 Ti detected
- FFmpeg: system-wide install confirmed
- Whisper: installed
- FastAPI: **still pending** (needs install before backend can serve)

**Key lesson — venv path corruption:**
Python venvs hardcode absolute paths into `.exe` launchers and `pyvenv.cfg`.
Moving or renaming the project folder breaks those paths silently.
Fix: always delete and recreate the venv at the new location. Never move a venv.

---

## Open Items

- Vite frontend scaffold is pending — project is in scaffolding phase
- FastAPI install pending in rebuilt venv (as of 2026-04-18)
- Supported upload formats not yet documented (confirm when frontend is built)
- Highlighting sync mechanism (word-level timestamps vs cursor) not yet implemented

---

## Connected to

- [[Project_Directory]]
- [[Tools_Registry]]
- [[Session_Protocol]]
