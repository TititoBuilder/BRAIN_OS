---
tags: [project, wip]
---

# PROJECT: Read-Along App

## Status
Active — backend complete; frontend source complete but Vite production build not yet run (no dist/)

## Brain Architecture coverage
- Input Layer: yes
- AI Agents: no
- Workflows: yes
- Knowledge Graph: no
- Output Layer: yes
- Infrastructure: yes

## Root path
C:\Users\titit\Projects\read-along-app\

## GitHub
Local only — no remote configured

## Inputs
- Audio files (MP3 / WAV / M4A) uploaded by user → direct Whisper transcription
- Text files (TXT / MD) in TTS mode → Kokoro TTS → Whisper transcription + generated audio URL
- Text files (TXT / MD) in read-only mode → browser FileReader only, no backend call
- User click events → word/line toggles (mark red for review)

## Active agents
- None — Whisper and Kokoro are local models, not LLM agents

## Connected APIs
- [[Whisper_Base]] — openai-whisper (local, model: base, CUDA 12.8); returns word-level timestamps with start/end/probability per word
- [[Kokoro_TTS]] — local Kokoro KPipeline (voice: af_heart) invoked via BDF venv; converts text to MP3 for karaoke playback
- [[BDF_Pipeline]] — external dependency on `C:\Dev\Projects\soccer-content-generator`; `converter.py` (text → TTS format) + `tts_local.py` (Kokoro runner) called via subprocess

## Outputs
- Karaoke word highlighting in browser — active word auto-scrolls, synced to audio playback via requestAnimationFrame
- `{filename}_review_notes.txt` download — marked words grouped into consecutive phrases with "STUDY ACTION" prompt
- In text-only mode: marked lines exported as `[Line N] ...` review notes file
- Generated MP3 files served from `generated_audio/` via FastAPI `/audio/*` static mount

## Workflows
- [[AudioMode]] — upload MP3/WAV/M4A → `POST /transcribe` → Whisper base (word_timestamps=True) → AudioPlayer + TranscriptDisplay karaoke view
- [[TextTTSMode]] — upload TXT/MD → `POST /transcribe` → converter.py (TTS format) → tts_local.py (Kokoro af_heart MP3 in BDF `converted/`) → move to `generated_audio/` → Whisper base → karaoke view + `/audio/{name}.mp3` URL
- [[TextReadMode]] — upload TXT/MD (read-only toggle) → browser FileReader only, no backend → TextDisplay line-by-line mark
- [[ExportFlow]] — user clicks words or lines → toggled red in UI → Export button → `exportMarkedWords` groups consecutive indices into phrases → `.txt` download via Blob URL

## Key file paths
- `backend/backend.py` — FastAPI app v0.2.0, port 8000; Whisper model loaded once at startup
- `frontend/src/App.tsx` — top-level state machine (idle → transcribing → ready → error), mode toggle, export trigger
- `frontend/src/components/AudioPlayer.tsx` — custom HTML5 audio player, requestAnimationFrame-based time tracking, playback rate control
- `frontend/src/components/TranscriptDisplay.tsx` — word-level karaoke display, auto-scrolls active word into view
- `frontend/src/components/TextDisplay.tsx` — line-level read-only display with click-to-mark
- `frontend/src/components/FileUpload.tsx` — drag-and-drop + click file selector
- `frontend/src/utils/export.ts` — consecutive-phrase grouping + .txt download logic
- `frontend/src/types.ts` — Word, TranscriptionResponse, ContentSource, AppState TypeScript interfaces
- `generated_audio/` — Kokoro MP3 output, served as `/audio/*` static files (persisted between sessions)
- `C:\Dev\Projects\soccer-content-generator\converter.py` — external dep: text → _TTS.txt format
- `C:\Dev\Projects\soccer-content-generator\tts_local.py` — external dep: _TTS.txt → Kokoro MP3
- `C:\Dev\Projects\soccer-content-generator\converted\` — intermediate TTS staging folder

## Tech stack
- Python 3.x, FastAPI, openai-whisper (base), torch 2.11 CUDA 12.8, numpy
- React 19, TypeScript ~6.0, Vite 8.x — no external UI libraries
- Backend: `uvicorn backend.backend:app --reload` (from project root)
- Frontend dev: `cd frontend && npm run dev` (port 5173, not yet production-built)
