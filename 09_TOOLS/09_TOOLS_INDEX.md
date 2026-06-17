---
tags: [tools, index, system]
status: active
dependencies: []
parent: "[[07_SYSTEM/Master_Control]]"
---

# 09_TOOLS — Script Index

All Python scripts in `C:\BRAIN_OS\09_TOOLS\`. Last updated: 2026-06-17.

---

## Session Management

- `session_start.py` — BRAIN OS Session Orchestrator: loads project context, runs health check, sends Telegram notification on session start
- `session_close.py` — Interactive session compiler: prompts for accomplished/pending/notes, writes dated archive to 08_SESSIONS/, fires Telegram summary

## Graph & Code Analysis

- `graphify.py` — BDF project graph builder: scans .py files, hashes, classifies imports, assigns architectural layers, writes graph JSON + .context.md
- `graph_maintainer.py` — Lightweight BDF graph maintenance runner: manifest pre-flight, hash check, audio parity, dependency mapping, graphify update (5 tasks)
- `graph_maintainer_patch.py` — Integration instructions patch for adding Task 2 Audio Parity Check into graph_maintainer.py

## Audio Generation

- `vault_audio_generator.py` — Vault Node Audio Generator: converts HIGH priority BRAIN_OS vault .md files to spoken audio via Claude API + Kokoro TTS
- `anchor_generator.py` — AI Learning Anchor Generator: generates closing "Learning Anchor" segment for any audio chapter (am_michael voice, Kokoro TTS)
- `anchor_batch.py` — Batch Learning Anchor Generator: runs anchor_generator.py on every _TTS.txt file in converted/
- `chapter_combiner.py` — Merge original chapter audio + learning anchor into one MP3 using ffmpeg
- `audio_stitcher.py` — Knowledge OS Phase 2: reads audio_manifest.json, generates TTS transition narrations (Edge TTS, en-US-GuyNeural)

## Google Drive

- `drive_setup_folders.py` — Creates the Knowledge_OS domain folder tree on Google Drive, moves session_01 from root
- `drive_browser.py` — Audits Google Drive audio folders and reorganizes to match Knowledge OS machine_key naming convention
- `drive_download.py` — Downloads specific Drive files by folder_path, renames to machine_key
- `drive_cleanup_phases.py` — Cleans up empty Phase_0X folders on Drive, creates BRAIN_OS Learning Path shortcut folder
- `drive_learning_path_organizer.py` — Organizes Drive audio into Phase 1-6 folders: creates subfolders, moves files per learning path
- `download_brainos_chapters.py` — Downloads BRAIN OS guide WAVs from Google Drive
- `get_drive_ids.py` — Utility: reads Drive token and lists file IDs for a given folder

## Learning Path

- `learning_path_builder.py` — BRAIN OS Learning Path Sequencer: organizes all audio files into Phase 1-6 learning path, creates manifest JSON + Drive folder structure plan

## Vault & Sync

- `brain_notes_sync.py` — Syncs Railway Q&As → BRAIN_OS vault: pulls brain_notes.md from GitHub, appends to dated vault notes, marks processed, commits back
- `obsidian_sync.py` — Knowledge OS Phase 3: reads obsidian_sync.json from the app, finds matching .md files in vault by machine_key
- `compile_session.py` — Option C Knowledge Ingestion Pipeline: reads latest session archive, runs Knowledge Ingestion Protocol V2, auto-handles routine updates, flags complex cases to Telegram

## System Utilities

- `generate_profile.py` — Generates PowerShell $PROFILE from SYSTEM_MASTER.md as single source of truth
- `audit_files.py` — Read-only file audit across BRAIN_OS ecosystem: measures disk reality against Naming_Contract.md, never renames or deletes
- `cost_guard.py` — Claude Cost Guard: estimates token cost before expensive Claude Code tasks, sends Telegram warning if over threshold
- `watchdog.py` — Unified BRAIN OS System Watchdog: morning/bdf/session health checks with Telegram reports

---

**→** [[07_SYSTEM/Master_Control]] · [[SYSTEM_MASTER]]
