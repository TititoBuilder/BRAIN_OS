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

_Generated 2026-09-01 from module docstrings by `tools_index.py`. Do not edit by hand._

## Session Management

- `compile_session.py` — Option C Knowledge Ingestion Pipeline
- `session_close.py` — BRAIN OS Session Closer
- `session_compiler.py` — Session-to-Audio Chapter Compiler
- `session_start.py` — BRAIN OS Session Orchestrator
- `task_session.py` — focused context launcher for task-specific Claude sessions

## Graph & Code Analysis

- `brain_graph.py` — unified BRAIN_OS code graph
- `graph_maintainer.py` — Lightweight BDF graph maintenance runner
- `graphify.py` — BDF project graph builder

## Audio Generation

- `anchor_batch.py` — Batch Learning Anchor Generator
- `anchor_generator.py` — AI Learning Anchor Generator
- `audio_stitcher.py` — Knowledge OS Phase 2
- `borrowed_audio_worklist.py` — Borrowed Audio Re-voice Worklist Generator
- `chapter_combiner.py` — Merge original chapter audio + learning anchor into one MP3
- `vault_audio_generator.py` — Vault Node Audio Generator

## Google Drive

- `download_brainos_chapters.py` — Download BRAIN OS guide WAVs from Drive
- `drive_browser.py` — Knowledge OS Drive Organizer
- `drive_cleanup_phases.py` — Clean up empty phase folders on Drive
- `drive_download.py` — Download specific Drive files by folder_path, rename to machine_key
- `drive_learning_path_organizer.py` — Organize Drive audio into Phase 1-6 folders
- `drive_setup_folders.py` — Creates the Knowledge_OS domain folder tree on Google Drive and moves session_01_knowledge_os.mp3 from root into Knowledge_OS/
- `get_drive_ids.py` — list file names and Drive IDs for one hardcoded folder

## Learning Path

- `learning_path_builder.py` — BRAIN OS Learning Path Sequencer
- `learning_profile_extractor.py` — Learning Profile Distiller

## Vault & Sync

- `brain_notes_sync.py` — Sync Railway Q&As → BRAIN_OS vault
- `obsidian_sync.py` — Knowledge OS Phase 3
- `vault_index.py` — generates the auto-section of the BRAIN_OS navigation page

## System Utilities

- `artifact_paths.py` — single source for resolving vault artifacts by name or alias
- `audit_files.py` — Read-only file audit across the BRAIN_OS ecosystem
- `cost_guard.py` — Claude Cost Guard
- `generate_profile.py` — Generate PowerShell $PROFILE from SYSTEM_MASTER.md as single source of truth
- `project_paths.py` — single source for resolving project attributes from the manifest
- `tools_index.py` — regenerates 09_TOOLS_INDEX.md from module docstrings
- `watchdog.py` — Unified BRAIN OS System Watchdog

_33 scripts indexed._

<!-- TOOLS_INDEX:END -->

**→** [[07_SYSTEM/Master_Control]] · [[SYSTEM_MASTER]]
