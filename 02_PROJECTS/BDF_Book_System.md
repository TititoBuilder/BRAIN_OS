---
tags: [book, project]
book_project: bdf
book_status: active
created: 2026-05-05
updated: 2026-05-05
domain: Creative_Systems
---

# BDF Book System

**What This Is:** Automated knowledge compilation pipeline for BreakingDown Futbol. Session logs are compiled into structured chapters by Claude Opus, stitched into a master book, converted to audio via Kokoro TTS, and synced to Google Drive.

**Why It Exists:** Preserve and distribute BDF technical and creative knowledge built across sessions.

---

## Pipeline

```
Session log → incoming\ → bdf-book run → Claude Opus compiles chapter
→ chapter .txt saved → stitch_master_book() → BDF_Master_Book.txt
→ run_tts() → Kokoro audio → sync_audio_to_drive() → Google Drive
```

**Command:** `bdf-book run` (run from project root)

---

## File Locations

| Component | Path |
|---|---|
| Compiler | `C:\Dev\Projects\soccer-content-generator\book_compiler.py` |
| Chapters (canonical) | `C:\Knowledge\MCP\MCP_Book\chapters\` |
| Incoming sessions | `C:\Knowledge\MCP\MCP_Book\incoming\` |
| Under review | `C:\Knowledge\MCP\MCP_Book\_review\` |
| Processed | `C:\Knowledge\MCP\MCP_Book\_processed\` |
| Rejected | `C:\Knowledge\MCP\MCP_Book\_rejected\` |
| Audio output | `C:\Knowledge\MCP\MCP_Book\audio\` |
| Master book (derived) | `C:\Knowledge\MCP\MCP_Book\BDF_Master_Book.txt` |
| Cost log | `C:\Knowledge\MCP\MCP_Book\cost_log` |

---

## Architecture

### Canonical Source: Chapters
Chapter `.txt` files in `chapters\` are the source of truth. The master book is a **derived artifact** — deleted and regenerated on every run. Never edit the master book directly.

### stitch_master_book()
Loops `ch01 → ch16`, reads each `.txt` file, concatenates with dividers, writes `BDF_Master_Book.txt`. Fires automatically at end of every `bdf-book run`.

### Chapter Format
- Files: `ch01.txt` → `ch16.txt`
- Count: 16 chapters
- Encoding: UTF-8

### Post-Processing
1. `run_tts()` — Kokoro TTS generates audio from master book
2. `sync_audio_to_drive()` — uploads audio to Google Drive

---

## Chapter Inventory

| Chapter | Topic | Status |
|---|---|---|
| ch01-ch20 | Various BDF technical topics | Compiled |
| ch21 | Resolve 20 Free Tier NoneType Inventory | Compiled 2026-04-26 |
| ch21 | Bridge Reload Discipline | ⚠️ Duplicate number — needs fix |
| ch21 | Windows Encoding Patterns | ⚠️ Duplicate number — needs fix |
| ch21 | MCP Bridge Two-Process Architecture | ⚠️ Duplicate number — needs fix |

**Known issue:** Multiple chapters labeled "Chapter 21" — numbering bug in generation. Run audit to identify true chapter count and fix numbering before next compile.

---

## Known Issues

- Chapter 21 numbering collision — 4 chapters share the same number
- ⚠️ DALL-E 3 deprecated May 12, 2026 — migrate image generation calls before deadline

---

## Connected Nodes

- [[BDF_Avatar_Pipeline]] — avatar generation system documented in this book
- [[BDF_Agent_Pipeline]] — Telegram + async architecture
- [[BDF_Canvas]] — project overview
- [[Creative_Systems]] — parent domain
