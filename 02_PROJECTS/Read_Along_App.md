---
tags: [project, whisper, transcription, fastapi, react, tts, scaffolding]
project: read-along-app
status: active
updated: 2026-05-02
parent: "[[Project_Directory]]"
---

# Read-Along App — Karaoke-Style Transcription Tool

Karaoke-style read-along web app. Users upload audio or text files — the FastAPI backend transcribes audio with OpenAI Whisper (word-level timestamps), and the React frontend highlights each word in sync with playback. Text files are converted to speech via Kokoro TTS (delegated to the BDF soccer-content-generator project) before transcription.

Root: `C:\Users\titit\Projects\read-along-app\`
GitHub: `TititoBuilder/read-along-app` (private)

---

## Business Value

General-purpose transcription and read-along tool. Primary use case: make any document or recording listenable and followable with synchronized word highlighting. Runs entirely locally using GPU-accelerated Whisper on the RTX 5070 Ti.

---

## Architecture

```
Upload (audio or text file)
  ↓
backend.py (FastAPI)
  ├─ Audio file → Whisper base model (local GPU)
  │               → word-level timestamps JSON
  └─ Text file  → Kokoro TTS via BDF project (subprocess)
                  (C:\Dev\Projects\soccer-content-generator\tts_local.py)
                  → generated_audio/ .wav
                  → Whisper transcription → word-level timestamps JSON
  ↓
React 18 + TypeScript + Vite frontend
  → displays text synced with audio playback
  → highlights each word as it is spoken
```

---

## Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI (`backend/backend.py`) |
| Speech-to-text | OpenAI Whisper base model — local, GPU-accelerated (RTX 5070 Ti, CUDA 12.8) |
| TTS | Kokoro via `C:\Dev\Projects\soccer-content-generator\tts_local.py` (subprocess) |
| Frontend | React 18 + TypeScript + Vite |
| Backend venv | `backend/venv/` — PyTorch + Whisper + FastAPI (large) |

---

## Key Paths

| Item | Path |
|---|---|
| Project root | `C:\Users\titit\Projects\read-along-app\` |
| Backend | `backend/backend.py` |
| Backend venv | `backend/venv/` |
| Generated audio | `generated_audio/` (gitignored) |
| Frontend | `frontend/` |
| BDF project | `C:\Dev\Projects\soccer-content-generator\` |
| BDF Python | `C:\Dev\Projects\soccer-content-generator\venv\Scripts\python.exe` |
| Workspace file | `read-along.code-workspace` |

---

## Running

```powershell
# Backend
cd C:\Users\titit\Projects\read-along-app\backend
& .\venv\Scripts\Activate.ps1
uvicorn backend:app --reload

# Frontend (separate terminal)
cd C:\Users\titit\Projects\read-along-app\frontend
npm run dev
```

---

## Environment Variables

```
TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID
```

Telegram alerts fire on startup and on Whisper model load crash.

---

## Do Not Run Standalone

- `backend/venv/Scripts/python.exe` — use the project venv only inside `backend/`
- `C:\Dev\Projects\soccer-content-generator\tts_local.py` — called only by `backend.py` via subprocess
- `C:\Dev\Projects\soccer-content-generator\converter.py` — same

---

## TTS Delegation Note

Text-file uploads are converted to speech using Kokoro TTS from the BDF project (`tts_local.py`). This project does **not** have its own TTS venv — it calls the BDF Python interpreter as a subprocess. The fragile coqui-tts patches live in the [[Custom_Agent_TTS]] venv, but for this app the BDF project's `tts_local.py` is the entry point.

> **CA Book connection: DENIED.** This app has no dependency on CA Book WAV files or `ca_audio.py`. It is a general-purpose transcription tool.

---

## Venv Rebuild — April 18, 2026

**Problem:** All pip commands failed with "Unable to create process using..." after project folder was moved from `C:\Knowledge\` to `C:\Users\titit\Projects\`.

**Root Cause:** Python venvs hardcode absolute paths in their `.exe` launchers at creation time. Moving the folder breaks every script in `venv\Scripts\`.

**Fix:** Deleted old venv, created fresh with `python -m venv venv` at the new location.

**Verification:** PyTorch 2.11.0+cu128 installed, `torch.cuda.is_available() = True`, RTX 5070 Ti detected.

**Rule:** Create venvs at their final location. If a project moves, delete and recreate the venv — do not copy or move it.

---

## Open Items

- Word-level highlighting sync mechanism (word-level timestamps vs cursor) not yet implemented
- Supported upload formats not yet confirmed (document when frontend is built)

---

## Standardization Status (2026-04-30)

| Item | Status |
|---|---|
| `CLAUDE.md` | ✅ Created |
| `.claude/settings.json` | ✅ Scoped — 14 allow + 3 deny rules |
| `.gitignore` | ✅ Protects 3 GB venv from git |
| Telegram alerts | ✅ Added to `backend.py` — fires on startup and Whisper model load crash |
| Git | ✅ Local, branch `main` |
| GitHub | ✅ `TititoBuilder/read-along-app` (private), pushed 2026-04-30 |
| Model audit | ✅ Zero `claude-opus` references |

---

## Connected to

- [[BDF_Canvas]]
- [[Custom_Agent_TTS]]
- [[Project_Directory]]
- [[Tools_Registry]]
