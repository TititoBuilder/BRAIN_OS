# Read-Along App — Knowledge OS Learning Interface

## What It Is
Full-stack learning app built on top of the read-along project.
The unified interface for the entire Knowledge OS system.

## Stack
- Frontend: React 19 + Vite (localhost:5173)
- Backend: FastAPI + Uvicorn (localhost:8000)
- AI: OpenAI Whisper base (local GPU — RTX 5070 Ti)
- RAG: GitHub API vault search (TititoBuilder/BRAIN_OS)
- Storage: Google Drive API + audio_staging/ hybrid cache

## Four Tabs
- LISTEN — topic dropdown → Drive download → karaoke playback
- ASK — voice/text → GitHub RAG → Claude streaming answer
- NOTES — Q&A log → brain_notes.md
- KNOWLEDGE OS — embedded encyclopedia tracker (iframe)

## Key Files
- backend/backend.py — FastAPI endpoints
- backend/transcribe_batch.py — batch Whisper transcription
- backend/gen_tts_staging.py — markdown → TTS audio pipeline
- frontend/src/App.tsx — 4-tab shell
- frontend/src/tabs/ListenTab.tsx — karaoke player
- frontend/src/tabs/AskTab.tsx — RAG question interface
- frontend/src/tabs/NotesTab.tsx — Q&A log viewer

## Architecture
<!-- updated 2026-05-28: Read-Along App full architecture documented this session; update project file to reflect current state -->
## Architecture — Full (4-Tab Unified Interface)
- Documented 2026-05-28
- Full architecture covering 4-tab unified interface
- Details captured in session docs; see also 02_PROJECTS/graphs/read-along-app.context.md
<!-- updated 2026-05-28: Full Read-Along App architecture documented this session; project node needs update -->
## Full Architecture — 2026-05-28
- **Interface:** 4-tab unified interface
- **Tabs:** (populate from source docs)
- **Status:** Full architecture documented this session Pattern
Federated Hybrid Model:
- Local machine = heavy compute (Whisper, TTS, Drive sync)
- Cloud server = lightweight coordinator (when deployed)
- Pre-process locally → push JSON manifests → deployed app reads instantly

## Milestones Built This Session
1. GitHub RAG — vault search via GitHub API (cloud-ready)
2. Drive API audio — no subprocess, direct API calls
3. Karaoke highlighting — word-level timestamps via Whisper
4. Unified 4-tab interface — both apps in one window
5. gen_tts_staging.py — reusable markdown-to-audio pipeline
   Fixed: cp1252 encoding, venv isolation, env config

## Launch Commands
Terminal 1 (backend):
  cd C:\Users\titit\Projects\read-along-app\backend
  .\venv\Scripts\Activate.ps1
  uvicorn backend:app --reload --port 8000

Terminal 2 (frontend):
  cd C:\Users\titit\Projects\read-along-app\frontend
  npm run dev

Then open: http://localhost:5173

## Connected To
- [[Knowledge_OS_Manual]]
- [[Predator_Node]]
- [[BDF_Book_System]]
- [[CA_Book_System]]


<!-- auto-ingested 2026-05-28 -->
## Full Architecture — 4-Tab Unified Interface (2026-05-28)
- Documented full Read-Along App architecture this session
- 4-tab unified interface design finalized
- Whisper GPU transcription: 42x realtime, Triton fallback supported
- See: `02_PROJECTS/graphs/read-along-app.context.md` for context graph
- See: `02_AGENTS/RA_Whisper_Agent.md` and `04_WORKFLOWS/RA_Transcription_Flow.md` for agent/flow details
