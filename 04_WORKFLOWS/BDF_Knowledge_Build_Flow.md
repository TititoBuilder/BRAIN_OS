---
tags: [workflow, live]
---

# WORKFLOW: BDF Knowledge Build Flow

## Project
BDF, CA

## Flow
markdown → book_compiler.py → Claude Opus → Kokoro TTS → Google Drive

## Steps
1. **Source markdown file** — author writes chapter content in BDF or CA format (see format rules below)
2. [[BDF_Memory_Agent]] / [[CA_Orchestrator]] — `book_compiler.py` reads the single markdown file, parses chapter blocks, sends each section to Claude Opus for prose expansion / narration scripting
3. **Claude Opus** — generates long-form narrative text from structured chapter blocks; returned as expanded prose per section
4. [[CA_Kokoro_TTS]] — `tts_local.py` (or `ca_audio.py`) synthesizes expanded text to WAV audio via Kokoro `KPipeline(lang_code="a")`, voice `af_heart`, 24000 Hz; markdown stripped before TTS input
5. **Google Drive** — `book_compiler.py` uploads generated WAV/MP3 to Drive under `chapters/` or `sessions/` folder via OAuth2 (`gdrive_credentials.json` + `gdrive_token.json`)

## Trigger
Manual — run `book_compiler.py` with a single source file path argument.
```bash
python book_compiler.py path/to/chapter.md
```

## Output
- Expanded prose text (saved locally and/or returned)
- WAV audio file (24000 Hz mono, synthesized by Kokoro)
- Google Drive file ID (uploaded to `chapters/` or `sessions/`)

## Rules and constraints
- **CRITICAL: ONE file per run, never batch** — running multiple files in sequence causes Claude Opus cost to multiply; each run is $1.50–$2.50; batch runs are $15+ and have been a source of unexpected bills
- Claude Opus cost: $15 input / $75 output per million tokens; use Haiku for drafts
- Google Drive OAuth2: tokens auto-refresh; if `gdrive_token.json` is missing or expired, browser auth prompt will appear on first run
- Shared Google account between BDF and CA projects — same credential files

## Format rules

**BDF format:**
```
[CH01_INTRO]
Section content here — multi-section blocks are allowed within one file.
[CH01_SECTION2]
More content.
```
- `[CHxx_KEY]` block headers required
- Multiple sections per file are OK
- File = one chapter

**CA format:**
```
#ch01
Chapter content here — single block only.
```
- `#chXX` tag must appear on **line 1 only**
- **One tag per file** — second `#chXX` tag in same file breaks the parser
- File = one chapter segment
