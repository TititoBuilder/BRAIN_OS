---
tags: [memory, live]
---

# MEMORY: BDF Knowledge Book

## Purpose
Long-form structured knowledge base for the BDF soccer content system — compiled into prose chapters by Claude Opus and synthesized to audio by Kokoro TTS. Serves as the authoritative narrative reference for the BDF brand voice, soccer analysis methodology, and content creation guidelines.

## Type
Compiled knowledge book — markdown source → Claude Opus prose → Kokoro TTS audio

## Location
**Source markdown:** `C:\Knowledge\BDF\BDF_Book\`
**Audio sync:** Google Drive → `BDF_Book_Audio/`
**Compiler:** `book_compiler.py` (project root of soccer-content-generator)
**Audio engine:** `tts_local.py` via Kokoro `KPipeline(lang_code="a")`, voice `af_heart`, 24000 Hz WAV

## Format
```
[CH01_INTRO]
Chapter content here.

[CH01_SECTION2]
Second section content — multiple sections per file are allowed.
```
- Block headers use `[CHxx_KEY]` syntax
- Multiple `[CHxx_KEY]` blocks are permitted within a single file
- Each file = one chapter or chapter group
- Compiler parses all blocks in sequence

## Connected agents
- [[BDF_Memory_Agent]]
- [[CA_Kokoro_TTS]]

## Rules
- **ONE file per run** — never batch multiple files in a single `book_compiler.py` invocation; each run costs $1.50–$2.50 with Claude Opus; batching triggers $15+ surprise bills
- Claude Opus pricing: $15 input / $75 output per million tokens — use Haiku for draft/test passes
- Google Drive OAuth2: `gdrive_credentials.json` + `gdrive_token.json` at project root; browser auth required if token is missing or expired
- Audio files uploaded to Drive under `BDF_Book_Audio/` folder; Drive file IDs logged locally

## Status
Active. Source files in `C:\Knowledge\BDF\BDF_Book\`. Audio chapters synced to Google Drive.

## Connected to
- [[BDF_Knowledge_Build_Flow]]
- [[BDF_Analysis_Agent]]
- [[Anthropic_Claude]]
