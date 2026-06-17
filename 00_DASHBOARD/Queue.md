# BRAIN_OS — Master Queue

## In Progress

- [ ] DEV MODE workflow (part of study cluster): learn npm run dev - a long-running terminal process that live-reloads the browser on every file save (Hot Module Reload), so app changes show in <1s instead of the slow build+deploy loop. Distinction to internalize: VS Code = the EDITOR (where you type code); npm run dev = a PROCESS that watches files + reloads; they run together (dev server can run in VS Code's built-in terminal). Use dev mode for iterating; use npm run build + npx vercel --prod ONLY to publish. Also learn: npx vercel (no --prod) = preview deploy.
- [ ] TOKEN FRAGILITY (hit 3x on 2026-06-11): two Drive tokens - local gdrive_token.json + Railway GOOGLE_TOKEN_JSON - expire ~weekly, refreshed SEPARATELY. Refreshing local does NOT update Railway. Every expiry = re-auth local + manual base64 re-paste to Railway env var. FIX candidate: one script that refreshes local token AND pushes fresh base64 to Railway (Railway CLI/API). Symptom: audio 500s with invalid_grant. Stopgap: refresh local -> copy base64 ([Convert]::ToBase64String) -> paste to Railway GOOGLE_TOKEN_JSON -> wait for redeploy.
- [ ] STUDY CLUSTER (priority): understand my own toolchain instead of running it blind. (a) read each .py in 09_TOOLS + read-along backend - know what each does and why, not just how to run it; (b) comprehend git software (the stated priority); (c) start point = 09_TOOLS_INDEX.md. Rationale: every surprise this session came from running tools I had not read (NODES hardcoded, populate_staging node-selection, session_close docstring drift).
- [ ] Telegram silent-skip — add load_dotenv() to session_close.py (root cause: .env not loaded in plain PowerShell)
- [ ] FEATURE: separate Books/Sessions access path for long-form audio (distinct from topic dropdown)
- [ ] Sessions/Project-Resumes tab build (DESIGNED — see 07_SYSTEM/Sessions_*.md; first step: check vault [[backlinks]] for cross-context relations)
- [ ] Audit git history for audio that slipped past the 376-null .gitignore period (low priority)
- [ ] anchor_generator.py batch mode — generate anchors for all 31 chapters
- [ ] Learning path sequencing — generate audio for 30 HIGH priority vault nodes
- [ ] Apply Knowledge Graphs Over Lists to 04_WORKFLOWS + 05_MEMORY + 03_APIS
- [ ] Add session-start command to all project CLAUDE.md files
- [ ] drive_sync.py: add encoding="utf-8" to all 3 write_text calls (token ~L74, normalize ~L434, main sync ~L517)
- [ ] populate_staging.upload_to_drive: copy drive_sync's orphan-safe update-or-create pattern (currently create-only)
- [ ] audio_parity_check: extend to cover all 7 manifest audio categories (currently validates only 2)
- [ ] Borrowed-audio RE-VOICE worklist (~20 entries): re-voice from manifest drive_ids, NOT blind id: conversion — backfill source = manifest
- [ ] drive_sync / graphify / graph_maintainer: read-complete — log findings before touching
- [ ] Wall feature (parked — design undecided)

## Next Sessions (ordered)

- [ ] Session 3: Apply Knowledge Graphs Over Lists to 04_WORKFLOWS
- [ ] Session 4: Apply Knowledge Graphs Over Lists to 05_MEMORY + 03_APIS
- [ ] Session 5: Update all project CLAUDE.md files with Triggers section
- [ ] CA Book Phase 3: Session_Resume pipeline (needs actual files first)

---

**→** [[SYSTEM_MASTER]] · [[Master_Control]]
