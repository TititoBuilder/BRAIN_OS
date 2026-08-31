---
tags: [tools, index, system]
status: active
dependencies: []
parent: "[[07_SYSTEM/Master_Control]]"
---

# 09_TOOLS — Script Index

All Python scripts in `C:\BRAIN_OS\09_TOOLS\`.

---

<!-- TOOLS_INDEX:START -->

_Generated 2026-08-30 from module docstrings by `tools_index.py`. Do not edit by hand._

## Session Management

- `compile_session.py` — Option C Knowledge Ingestion Pipeline Reads the latest session archive, runs it through the Knowledge Ingestion Protocol V2, auto-handles routine updates, flags complex cases to Telegram + ingestion_flags.md, then git commits
- `session_close.py` — BRAIN OS Session Compiler Captures session work, writes a dated archive, and optionally notifies via Telegram
- `session_compiler.py` — Session-to-Audio Chapter Compiler Takes one session archive from 08_SESSIONS\, distills it into a clean reviewable chapter via the Claude API, converts that chapter into a spoken narration script, synthesizes audio via the existing Kokoro TTS chain, uploads the result to Google Drive, and adds an entry to drive_index.json so the Read-Along app can serve it
- `session_start.py` — BRAIN OS Session Orchestrator Runs automatically when a Claude Code session starts
- `task_session.py` — focused context launcher for task-specific Claude sessions

## Graph & Code Analysis

- `brain_graph.py` — unified BRAIN_OS code graph
- `graph_maintainer.py` — Lightweight BDF graph maintenance runner
- `graphify.py` — BDF project graph builder

## Audio Generation

- `anchor_batch.py` — Batch Learning Anchor Generator Runs anchor_generator.py on every _TTS.txt file in converted/ folder
- `anchor_generator.py` — AI Learning Anchor Generator Generates a closing "Learning Anchor" segment for any audio chapter
- `audio_stitcher.py` — Knowledge OS Phase 2 Reads audio_manifest.json exported from the Knowledge OS app
- `borrowed_audio_worklist.py` — Borrowed Audio Re-voice Worklist Generator Identifies drive_index.json entries with path-format values (not id:) and looks them up in the Drive manifest to find their drive_id
- `chapter_combiner.py` — Merge original chapter audio + learning anchor into one MP3 Uses ffmpeg to concatenate: [original_audio] + [anchor_audio] = [combined_audio] Usage: python chapter_combiner.py --dry-run python chapter_combiner.py --skip-existing python chapter_combiner.py --chapter ch01_pipeline_architecture
- `vault_audio_generator.py` — Vault Node Audio Generator Converts HIGH priority BRAIN_OS vault .md files into spoken audio

## Google Drive

- `download_brainos_chapters.py` — Download BRAIN OS guide WAVs from Drive
- `drive_browser.py` — Knowledge OS Drive Organizer Audits Google Drive audio folders and reorganizes them to match Knowledge OS machine_key naming convention
- `drive_cleanup_phases.py` — Clean up empty phase folders on Drive Deletes empty Phase_0X folders, keeps only folders with files
- `drive_download.py` — Download specific Drive files by folder_path, rename to machine_key
- `drive_learning_path_organizer.py` — Organize Drive audio into Phase 1-6 folders Creates subfolders under each Drive folder and moves files according to learning path
- `drive_setup_folders.py` — Creates the Knowledge_OS domain folder tree on Google Drive and moves session_01_knowledge_os.mp3 from root into Knowledge_OS/
- `get_drive_ids.py` — list file names and Drive IDs for one hardcoded folder

## Learning Path

- `learning_path_builder.py` — BRAIN OS Learning Path Sequencer Organizes all audio files into a Phase 1-6 sequential learning path
- `learning_profile_extractor.py` — Learning Profile Distiller Reads Cristian_Principles.md (earned-knowledge source) plus every session archive in 08_SESSIONS\, and calls the Claude API to distill a meta-level "Learning Profile": patterns in how Cristian learns, works, decides, and corrects course — evidenced across the principles doc and the session history, not a restatement of either

## Vault & Sync

- `brain_notes_sync.py` — Sync Railway Q&As → BRAIN_OS vault Pulls brain_notes.md from BRAIN_OS GitHub repo, parses new Q&A entries, appends them to dated vault notes, marks as processed, commits back to GitHub
- `obsidian_sync.py` — Knowledge OS Phase 3 Reads obsidian_sync.json exported from the Knowledge OS app
- `vault_index.py` — generates the auto-section of the BRAIN_OS navigation page

## System Utilities

- `artifact_paths.py` — single source for resolving vault artifacts by name or alias
- `audit_files.py` — Read-only file audit across the BRAIN_OS ecosystem
- `cost_guard.py` — Claude Cost Guard Estimates token cost before running expensive Claude Code tasks
- `generate_profile.py` — Generate PowerShell $PROFILE from SYSTEM_MASTER.md as single source of truth
- `project_paths.py` — single source for resolving project attributes from the manifest
- `tools_index.py` — regenerates 09_TOOLS_INDEX.md from module docstrings
- `watchdog.py` — Unified BRAIN OS System Watchdog Three modes: --check morning : 7:15am daily health check (run via Task Scheduler) --check bdf : on-demand BDF pipeline check --check session : post-session close check (called by session_close.py) Telegram config: loaded from C:\Dev\Projects\soccer-content-generator\.env

_33 scripts indexed._

<!-- TOOLS_INDEX:END -->

**→** [[07_SYSTEM/Master_Control]] · [[SYSTEM_MASTER]]
