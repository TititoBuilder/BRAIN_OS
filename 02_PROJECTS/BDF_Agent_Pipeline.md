---
tags: [bdf, pipeline, live]
updated: 2026-05-01
parent: "[[BDF_Soccer_Bot]]"
---

# BDF Agent Pipeline — Book Compiler & Story Generator

This document covers the three Claude-powered scripts that form the creative and knowledge-retention layer of the BDF pipeline: `book_compiler.py`, `mcp_book_compiler.py`, and `story_generator.py`. All three live in `C:\Dev\Projects\soccer-content-generator\` and share the project venv and `.env`.

---

## book_compiler.py — BDF Knowledge Book Compiler

### Purpose

`book_compiler.py` maintains a living technical book documenting the entire BDF Soccer Content pipeline. Its job is to take raw session notes or transcripts and merge them into structured, long-form chapter files that accumulate knowledge across sessions. The book currently has 21 chapters covering everything from pipeline architecture to export sequences and library routing.

### Inputs and Outputs

The script watches `C:\Knowledge\BDF\BDF_Book\incoming\` for `.txt` and `.md` files. Each file placed in that folder is treated as a new session document to be processed. Processed files are moved to `incoming\_processed\`. Files with unknown tags are quarantined to `incoming\_review\`. Non-BDF content is moved to `incoming\_rejected\`.

Chapter files are written to `C:\Knowledge\BDF\BDF_Book\chapters\` using filenames like `ch04_lancedb_rag.txt`. After each compile run the script stitches all chapters into a single `BDF_Master_Book.txt` at the book root. TTS audio is generated for each updated chapter using `converter.py` and `tts_local.py`, with the resulting MP3s stored in `C:\Knowledge\BDF\BDF_Book\audio\`. A combined session audio file is also produced. Audio files are optionally synced to a Google Drive folder called `BDF_Book_Audio`.

### Processing Logic

When a session file arrives, the compiler first looks for explicit chapter tags in the format `[CH04_LANCEDB_RAG]` followed by content and `[END]`. Tagged sections are routed directly to the matching chapter. Files without tags are first evaluated for BDF relevance using a Claude call; non-BDF documents are rejected. BDF-relevant untagged files go through chapter auto-detection: Claude reads the first 2000 characters and returns a chapter key and a confidence score from 1 to 10. Files scoring 7 or below are sent to `_review\` for manual tagging rather than being silently misclassified.

Compilation itself is a Claude `claude-sonnet-4-6` call that either writes a first-draft chapter or merges new session material into an existing draft. The model is instructed to preserve all technical details, paths, and engineering decisions while eliminating pure repetition. Token usage and cost are appended to `cost_log.txt` at the book root after every run.

### Known Architecture Note

The cost constants in `book_compiler.py` are still labelled `OPUS_INPUT_COST_PER_MILLION` and `OPUS_OUTPUT_COST_PER_MILLION` but the model was switched to `claude-sonnet-4-6` on 2026-04-30 following the Opus cost spike. The constants are stale labels; the actual model used is Sonnet.

---

## mcp_book_compiler.py — MCP Knowledge Book Compiler

### Purpose

`mcp_book_compiler.py` is a structural sibling of `book_compiler.py` but manages a separate knowledge book for the `resolve-mcp-server` project. It watches `C:\Knowledge\MCP\MCP_Book\incoming\` and writes chapters to `C:\Knowledge\MCP\MCP_Book\chapters\`.

### Chapter Set

The MCP book has a distinct set of chapters covering DaVinci Resolve-specific concerns: the Free Tier NoneType inventory, bridge reload discipline, Windows encoding patterns, and the two-process MCP bridge architecture (server_api.py + bridge). It also carries a full copy of the BDF book chapters, making it a dual-purpose compiler that can accept session notes from either the Resolve MCP project or the soccer content pipeline into a single process.

### Shared Logic

The internal architecture of `mcp_book_compiler.py` is identical to `book_compiler.py`: the same `extract_tagged_sections`, `detect_chapter`, `compile_chapter`, `is_bdf_related`, `stitch_master_book`, `run_tts`, and `sync_audio_to_drive` functions appear in both files. The two scripts diverge only in their `BOOK_ROOT` path, their `CHAPTERS` dict, and the fallback value for `BOOK_ROOT` in the environment lookup. This duplication is intentional: the two knowledge books are kept completely independent so a run on one never touches the other.

---

## story_generator.py — Soccer Animation Story Generator

### Purpose

`story_generator.py` generates short 3-scene soccer story scripts intended for animation production using Cartoon Animator 5. Players are treated as fictional characters with defined personalities, voice styles, rivalries, and friendships based on their real-world reputations. The output is a complete screenplay-style document with visual descriptions, dialogue, a Twitter caption, and hashtags.

### Cast

The script maintains a hardcoded cast of 10 players: Haaland, Mbappe, Yamal, Vinicius, Bellingham, Salah, Pedri, Gavi, Endrick, and De Bruyne. Each entry records the player's club, country, personality archetype, voice style description, rivalries, and friendships. This cast is the editorial identity of the BDF animation channel.

### Scenario Templates

Ten scenario templates are defined covering UCL finals, World Cup clashes, training ground arguments, club swaps, record-breaking moments, injury crises, press conferences, red-card penalties, transfer deadline days, and shootouts. Templates contain format placeholders (`{player1}`, `{team1}`, etc.) that are filled in at generation time from the cast data.

### Generation

A `generate_story` call sends a prompt to `claude-sonnet-4-6` using a system prompt that defines the output format: `TITLE`, `DURATION`, `PLAYERS`, `COMPETITION`, then three scenes each containing a visual description and character dialogue lines, ending with `CAPTION` and `HASHTAGS`. Each story costs approximately $0.015. Output files are saved to `output/stories/` as `.txt` files named `story_{players}_{timestamp}.txt`.

The script supports three run modes via CLI: `--players` + `--scenario` for a targeted story; `--batch N` for N random stories; and interactive mode which presents a numbered menu.

### Connection to Pipeline

Stories produced by `story_generator.py` are standalone scripts intended for manual handoff to the CA5 animation pipeline. They are not automatically injected into the content queue. The generated captions and hashtags are formatted to BDF Twitter standards (280-char max, 5 tags) and can be copy-pasted into the queue if needed.

---

## Connected to

- [[BDF_Canvas]]
- [[Tools_Registry]]
- [[LanceDB_Vector_Store]]
