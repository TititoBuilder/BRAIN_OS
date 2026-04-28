# MEMORY: CA Knowledge Book

## Purpose
Long-form business knowledge base for CristianConstruction — defines pricing logic, client handling philosophy, trade workflows, and operational procedures. Compiled to audio for owner review during commute or job site.

## Type
Compiled knowledge book — markdown source → Claude Opus prose → Kokoro TTS audio

## Location
**Source markdown:** `C:\Dev\CristianConstruction\` (chapter files colocated with agent source)
**Audio sync:** Google Drive → `CA_Book_Audio/`
**Compiler:** `book_compiler.py` (shared with BDF project; invoked from CA context)
**Audio engine:** `ca_audio.py` (`C:\Dev\Projects\custom-agent\ca_audio.py`) — Kokoro `KPipeline(lang_code="a")`, voice `af_heart`, 24000 Hz WAV

## Size
- Source: ~63 KB raw markdown across 10 chapters
- Expanded: ~115 KB compiled prose (Claude Opus expansion)

## Format
```
#ch01
Chapter content here — single continuous block.
```
- `#chXX` tag must appear on **line 1 only** — compiler stops parsing at the first tag per file
- **ONE tag per file** — a second `#chXX` tag anywhere in the file breaks the parser; content after second tag is silently dropped
- Each file = exactly one chapter segment

## Aliases
`ca-book`, `ca-compile`, `ca-audio` — shorthand used in terminal and notes to refer to this pipeline

## Connected agents
- [[CA_Orchestrator]]
- [[CA_Kokoro_TTS]]

## Rules
- **ONE file per run** — same constraint as BDF book; never batch; $1.50–$2.50 per run with Claude Opus
- **ONE `#chXX` tag per file** — compiler stops at first tag; second tag = silent data loss
- `#chXX` must be line 1 — not line 2, not after a blank line; parser is strict
- Google Drive OAuth2: same `gdrive_credentials.json` + `gdrive_token.json` as BDF (shared Google account); same token refresh behavior
- `ca_audio.py` strips markdown before TTS: code fences, headers, bold/italic, links (keeps label text), HTML tags

## Status
Active. 10 chapters compiled. Audio synced to Google Drive `CA_Book_Audio/`.
