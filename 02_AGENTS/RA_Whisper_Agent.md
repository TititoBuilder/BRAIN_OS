---
tags: [agent, live]
---

# AGENT: RA Whisper Agent

## Project
Read-Along App

## Function
FastAPI backend that accepts audio files (MP3/WAV/M4A) or text files (TXT/MD) and returns word-level timestamps for karaoke highlighting — for audio files it runs Whisper directly; for text files it first generates audio via Kokoro TTS (through the BDF soccer-content-generator pipeline), then transcribes the result.

## Input
- Audio upload (MP3/WAV/M4A) via `POST /transcribe` — direct Whisper transcription
- Text upload (TXT/MD) in TTS mode via `POST /transcribe` — Kokoro TTS → Whisper transcription
- Text upload in read-only mode — handled entirely in the browser (no backend call)

## Output
- JSON response: `{language, duration, text, words: [{word, start, end, probability}], audio_url}`
- `audio_url` is `null` for audio uploads (frontend uses the local file); `/audio/{name}.mp3` for text uploads
- Generated MP3 files persisted in `generated_audio/` and served as static files at `/audio/*`

## Trigger
HTTP `POST /transcribe` from the React frontend (Vite dev server, port 5173 → backend port 8000). Whisper model loaded once at startup — not reloaded per request.

## Tools and APIs
- [[Whisper_Base]] — `openai-whisper`, model `base`, CUDA 12.8 (torch 2.11); `word_timestamps=True`; loaded once at startup via `model = whisper.load_model("base")`
- [[Kokoro_TTS]] — invoked via subprocess through BDF venv (`C:\Dev\Projects\soccer-content-generator\venv\Scripts\python.exe`); pipeline: `converter.py` (text → `_TTS.txt`) → `tts_local.py` (Kokoro `af_heart` → MP3)
- [[BDF_Pipeline]] — external dependency on `C:\Dev\Projects\soccer-content-generator`; must be present with its venv active for text-file TTS mode to work

## Canonical file
C:\Users\titit\Projects\read-along-app\backend\backend.py

## Connected to
- [[AudioMode]] workflow — audio upload → Whisper → words array → frontend AudioPlayer + TranscriptDisplay
- [[TextTTSMode]] workflow — text upload → Kokoro (BDF pipeline) → Whisper → karaoke view + audio URL
- [[Read_Along_App]] project

## Status
Live — backend complete; Vite frontend source complete, production build not yet run

## Key paths
| Path | Purpose |
|---|---|
| `backend/backend.py` | FastAPI v0.2.0, port 8000 |
| `generated_audio/` | Kokoro MP3 output, served as `/audio/*` |
| `C:\Dev\Projects\soccer-content-generator\converter.py` | External dep: text → TTS format |
| `C:\Dev\Projects\soccer-content-generator\tts_local.py` | External dep: Kokoro runner |
| `C:\Dev\Projects\soccer-content-generator\converted\` | Intermediate TTS staging |
