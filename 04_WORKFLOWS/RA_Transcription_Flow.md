---
tags: [workflow, live]
---

# WORKFLOW: RA Transcription Flow

## Project
Read-Along App

## Flow
Audio file → Whisper CUDA → synchronized text output

## Steps
1. **User uploads audio** — file submitted to `POST /transcribe` endpoint (backend.py v0.2.0); accepted formats: WAV, MP3, M4A
2. [[RA_Whisper_Agent]] — Whisper `base` model (loaded once at startup, CUDA 12.8) transcribes audio with `word_timestamps=True`; returns word-level timing data
3. [[RA_Whisper_Agent]] — response includes full transcript + per-word `[word, start_sec, end_sec]` tuples
4. *(TTS path — triggered separately)* — `POST /synthesize` sends text to subprocess calling BDF venv's `converter.py` → `tts_local.py`; Kokoro `KPipeline(lang_code="a")`, voice `af_heart`, 24000 Hz WAV returned
5. **Frontend (INCOMPLETE)** — Vite+React app intended to display synchronized highlighted text as audio plays; **not yet built**

## Trigger
Manual — user submits audio file to backend endpoint. No automated trigger.

## Output
- JSON response from `/transcribe`: `{transcript: str, words: [{word, start, end}]}`
- WAV audio from `/synthesize`: Kokoro-synthesized speech at 24000 Hz
- Synchronized read-along display: **pending** (frontend not built)

## Rules and constraints
- Whisper `base` model is loaded **once at startup** — no per-request model loading; backend must stay running
- CUDA 12.8 required for GPU inference; CPU fallback available but significantly slower
- TTS subprocess calls into BDF venv (`C:\Dev\Projects\soccer-content-generator\`) — both projects must be present on same machine; `converter.py` and `tts_local.py` are external dependencies
- **Frontend gap**: Vite production build has never been run; `npm run build` not executed; output layer is incomplete — the synchronized highlighting UI does not exist yet
- GitHub remote is local only — no public/cloud remote configured
- Backend is complete and testable via direct HTTP calls (curl / Postman) independently of the frontend
