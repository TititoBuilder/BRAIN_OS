# BRAIN_OS — Master Queue
## In Progress
- [ ] DEV MODE workflow (part of study cluster): learn npm run dev - a long-running terminal process that live-reloads the browser on every file save (Hot Module Reload), so app changes show in <1s instead of the slow build+deploy loop. Distinction to internalize: VS Code = the EDITOR (where you type code); npm run dev = a PROCESS that watches files + reloads; they run together (dev server can run in VS Code's built-in terminal). Use dev mode for iterating; use npm run build + npx vercel --prod ONLY to publish. Also learn: npx vercel (no --prod) = preview deploy.
- [ ] TOKEN FRAGILITY (hit 3x on 2026-06-11): two Drive tokens - local gdrive_token.json + Railway GOOGLE_TOKEN_JSON - expire ~weekly, refreshed SEPARATELY. Refreshing local does NOT update Railway. Every expiry = re-auth local + manual base64 re-paste to Railway env var. FIX candidate: one script that refreshes local token AND pushes fresh base64 to Railway (Railway CLI/API). Symptom: audio 500s with invalid_grant. Stopgap: refresh local -> copy base64 ([Convert]::ToBase64String) -> paste to Railway GOOGLE_TOKEN_JSON -> wait for redeploy.
- [ ] STUDY CLUSTER (priority): understand my own toolchain instead of running it blind. (a) read each .py in 09_TOOLS + read-along backend - know what each does and why, not just how to run it; (b) comprehend git software (the stated priority); (c) start point = 09_TOOLS_INDEX.md. Rationale: every surprise this session came from running tools I had not read (NODES hardcoded, populate_staging node-selection, session_close docstring drift).
- [ ] Convert remaining path-format index entries to id: format (low priority - backend handles both)
- [ ] session_close.py doc/code drift: docstring claims --project flag the parser lacks - reconcile
- [ ] Telegram env vars not loaded in plain PowerShell -> close-script notification silently skips; load .env
- [ ] FEATURE: separate Books/Sessions access path for long-form audio (distinct from topic dropdown)
- [ ] Sessions/Project-Resumes tab build (DESIGNED ? see 07_SYSTEM/Sessions_*.md; first step: check vault [[backlinks]] for cross-context relations)
- [x] Author + voice 3 topics: edge_tts, kokoro_tts, message_queues (DONE 2026-06-11 - live in LISTEN tab)
- [ ] read-along-app CLAUDE.md drift: remove stale DRIVE_INDEX_JSON ref + fix pipeline section (transcribe_batch/populate_staging refs don't match reality)
- [ ] session_close.py: make git add surgical (explicit files, not broad add) ? see Cristian_Principles
- [ ] Audit git history for audio that slipped past the 376-null .gitignore period (low priority)
- [ ] Queue.md hygiene: collapse duplicate 'Completed ? 2026-05-28' sections (low priority)
- [ ] anchor_generator.py batch mode — generate anchors for all 31 chapters
- [ ] Learning path sequencing — generate audio for 30 HIGH priority vault nodes
- [ ] Apply Knowledge Graphs Over Lists to 04_WORKFLOWS + 05_MEMORY + 03_APIS
- [ ] Add session-start command to all project CLAUDE.md files

## Next Sessions (ordered)
- [x] Session 2: Apply Knowledge Graphs Over Lists to 02_AGENTS
- [ ] Session 3: Apply Knowledge Graphs Over Lists to 04_WORKFLOWS  
- [ ] Session 4: Apply Knowledge Graphs Over Lists to 05_MEMORY + 03_APIS
- [ ] Session 5: Update all project CLAUDE.md files with Triggers section
- [x] Update calendar events (DALL-E 3 deadline May 12 is stale — needs cleanup)
- [ ] CA Book Phase 3: Session_Resume pipeline (needs actual files first)

## Completed
<!-- updated 2026-05-28: Multiple deliverables completed this session; queue should reflect completions -->
## Completed — 2026-05-28
- Knowledge OS Phase 1-3 (encyclopedia, stitcher, obsidian sync) ✓
- drive_index.json wired into Knowledge OS — 25 topics audio-linked ✓
- Knowledge OS Drive structure — 28 folders, domain isolation ✓
- Read-Along App full architecture documented ✓
- Dashboard header visibility + button hover fixes ✓
- Focus Now cards clickable (edit modal) ✓
- BRAIN_OS admin key file removed from tracking ✓
<!-- updated 2026-05-28: Dashboard queue should reflect session completions -->
## Completed — 2026-05-28
- [x] brain-audio steganographic fingerprint module
- [x] book-compiler fingerprint integration (auto + post-stitch verify)
- [x] Knowledge OS Phase 1-3 (encyclopedia, stitcher, obsidian sync)
- [x] Knowledge OS Drive structure (28 folders)
- [x] drive_index.json wired (25 topics audio-linked)
- [x] Read-Along App full architecture docs
- [x] Whisper GPU analysis doc
- [x] RAG chapter ingested
- [x] Focus Now cards clickable
- [x] Dashboard header/button fixes
- [x] Admin key removed from tracking
- [x] 3 Q&A notes ingested This Session (2026-05-20)
- [x] Obsidian graph colors fixed (UTF-8 BOM root cause)
- [x] restore_graph_colors.ps1 built + committed
- [x] BRAIN_OS duplicate file audit + cleanup
- [x] .env secrets purged from 117 commits
- [x] GitHub PAT rotated
- [x] Cristian_Principles.md: PowerShell Encoding rule added
- [x] Cristian_Principles.md: Documentation Must Reflect Reality added
- [x] Cristian_Principles.md: Knowledge Graphs Over Lists added
- [x] Trigger_Architecture.md: 13-trigger master index built
- [x] 08_TRIGGERS: all 13 trigger files created/rewritten with full bidirectional links

---
**→** [[SYSTEM_MASTER]] · [[Master_Control]]


<!-- auto-ingested 2026-05-28 -->
## Completed — 2026-05-28
- [x] Read-Along App full architecture docs (4-tab interface)
- [x] Whisper GPU analysis (42x realtime, Triton fallback)
- [x] RAG chapter (Cristian's build-first explanation)
- [x] Knowledge OS Drive structure (28 folders, domain isolation)
- [x] drive_index.json wired — 25 topics audio-linked
- [x] Knowledge OS user manual
- [x] Dashboard UI fixes (header visibility, button hover states)
- [x] Focus Now cards clickable (edit modal)
- [x] 22 vault audio nodes added to dropdown
- [x] read_along_app_session audio node added
- [x] Excluded audio_staging binaries from git
- [x] Removed admin key file from tracking
- [x] BRAIN_OS principle: never start without feeding context
- [x] drive_index fix: file IDs for BRAIN_OS_Vault entries
- [x] soccer-content-generator: session close + brain sync 2026-05-27
