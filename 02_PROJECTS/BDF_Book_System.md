---
tags: [book, project]
book_project: bdf
book_status: active
created: 2026-05-05
updated: 2026-05-20
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

**Command (updated 2026-05-20 — canonical moved to shared plugin):**
```powershell
# Preferred: use alias (runs via CA venv automatically)
bdf-book

# Direct:
C:\Knowledge\CA\venv\Scripts\python.exe C:\Dev\shared\book-compiler\book_compiler.py --book bdf
```

> ⚠️ `book_compiler.py` was deleted from `C:\Dev\Projects\soccer-content-generator\` on 2026-05-20.
> Canonical: `C:\Dev\shared\book-compiler\book_compiler.py`
> Venv: always use `C:\Knowledge\CA\venv` (never BDF dev venv for book compilation).
> See [[Book_Compiler_Shared]] for full plugin architecture.

---

## File Locations

| Component | Path |
|---|---|
| Compiler | `C:\Dev\shared\book-compiler\book_compiler.py` ← shared plugin (moved 2026-05-20) |
| Chapters (canonical) | `C:\Knowledge\BDF\BDF_Book\chapters\` |
| Incoming sessions | `C:\Knowledge\BDF\BDF_Book\incoming\` |
| Under review | `C:\Knowledge\BDF\BDF_Book\_review\` |
| Processed | `C:\Knowledge\BDF\BDF_Book\_processed\` |
| Rejected | `C:\Knowledge\BDF\BDF_Book\_rejected\` |
| Audio output | `C:\Knowledge\BDF\BDF_Book\audio\` |
| Master book (derived) | `C:\Knowledge\BDF\BDF_Book\BDF_Master_Book.txt` |
| Cost log | `C:\Knowledge\BDF\BDF_Book\cost_log` |

---

## Architecture

### Canonical Source: Chapters
Chapter `.txt` files in `chapters\` are the source of truth. The master book is a **derived artifact** — deleted and regenerated on every run. Never edit the master book directly.

### stitch_master_book()
Loops `ch01 → ch27`, reads each `.txt` file, concatenates with dividers, writes `BDF_Master_Book.txt`. Fires automatically at end of every run.

### Chapter Format
- Files: `.txt`
- Count: 27 files on disk (see inventory — duplicates exist)
- Encoding: UTF-8
- Size: 385,886 characters total

### Post-Processing
1. `run_tts()` — Kokoro TTS generates audio from master book
2. `sync_audio_to_drive()` — uploads audio to Google Drive

---

## Chapter Inventory

| File | Topic | Size |
|---|---|---|
| ch01_pipeline_architecture | Pipeline Architecture | 16 KB |
| ch02_predator_setup | Predator Setup | 15 KB |
| ch03_tts_audio | TTS Audio | 11 KB |
| ch04_lancedb_rag | LanceDB RAG | 16 KB |
| ch05_telegram_twitter | Telegram + Twitter | 16 KB |
| ch06_obs_clips | OBS Clips | 16 KB |
| ch07_dashboard_ui | Dashboard UI | 16 KB |
| ch08_methodology | Methodology | 16 KB |
| ch09_roadmap | Roadmap | 17 KB |
| ch10_cartoon_animator | Cartoon Animator | 17 KB |
| ch11_first_end_to_end_export | First End-to-End Export | 15 KB |
| ch11_image_gallery | Image Gallery | 18 KB ⚠️ duplicate number |
| ch12_nuclear_clear_tool | Nuclear Clear Tool | 9 KB |
| ch12_terminology_glossary | Terminology Glossary | 18 KB ⚠️ duplicate number |
| ch13_deploy_discipline | Deploy Discipline | 10 KB |
| ch13_evolution_decisions | Evolution Decisions | 18 KB ⚠️ duplicate number |
| ch14_async_export_pattern | Async Export Pattern | 9 KB |
| ch14_ideas_discoveries | Ideas + Discoveries | 20 KB ⚠️ duplicate number |
| ch15_clip_type_system | Clip Type System | 13 KB |
| ch15_learning_discoveries | Learning + Discoveries | 17 KB ⚠️ duplicate number |
| ch16_cost_tracking | Cost Tracking | 7 KB |
| ch16_knowledge_enricher | Knowledge Enricher | 8 KB ⚠️ duplicate number |
| ch17_clip_name_parser | Clip Name Parser | 10 KB |
| ch18_competition_detection | Competition Detection | 13 KB |
| ch19_export_pipeline | Export Pipeline | 15 KB |
| ch20_format_b_path_resolution | Format B Path Resolution | 9 KB |
| ch21_library_routing | Library Routing | 13 KB |

**⚠️ Duplicate chapter numbers: ch11–ch16 each have 2 files (27 files, ~21 unique chapters). Renumbering needed before next compile.**

---

## Drive Pipeline — Improvements (2026-05-20)

The `sync_audio_to_drive()` / upload functions in soccer-content-generator were hardened:

| Change | Detail |
|---|---|
| `build_manifest()` extended | Now scans BRAIN_OS_Handbook Drive folders in addition to existing folders |
| Dedup uploads | Files already on Drive are updated in-place (no duplicate uploads) |
| `drive_cleanup.py --delete-files` | New CLI flag to delete Drive files matching a list |
| Runtime config | Drive folder IDs loaded from `BRAIN_OS_CONFIG.json` at startup (not hardcoded) |
| Chunk size | Increased to **50 MB** for faster large-file transfers |

### TTS / HuggingFace Auth
`tts_local.py` now calls `huggingface_hub.login(token=HF_TOKEN)` at startup. `HF_TOKEN` must be set in `.env` and `load_dotenv()` is called at module import. Without this, model downloads fail silently.

## Known Issues

- ch11–ch16 duplicate numbering — 6 pairs need sequential renaming
- GDrive credentials shared with CA book compiler (by design — both point to BDF project dir)

---

## Connected Nodes

- [[BDF_Avatar_Pipeline]] — avatar generation system documented in this book
- [[BDF_Agent_Pipeline]] — Telegram + async architecture
- [[BDF_Canvas]] — project overview
- [[CA_Book_System]] — sister book, identical architecture
- [[Creative_Systems]] — parent domain
