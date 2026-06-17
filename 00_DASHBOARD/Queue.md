# BRAIN_OS — Master Queue
## In Progress
- [ ] GOLD CAPSTONE LESSON (priority next session): author the ENTIRE project's lessons as ONE linear, expanded, reinforced learning sequence - then voice it. Pull from project chat history across sessions (May-June). Cover: the deploy crisis (3 root causes - Vercel root dir, Railway token, stale DRIVE_INDEX_JSON), token fragility (local+Railway split), verify-before-write, declared-start-finish, derive-don't-duplicate, four pillars of separation, BOM/encoding (Python-only writes), stale-download trap, the app's 4-layer architecture (md->audio->index->app), for-now-is-forbidden. Make it timeline/linear so lessons reinforce each other. Then full pipeline: author .md -> vault_audio_generator -> stage -> populate_staging -> id: index -> commit. This is gold content for Cristian - do it justice with fresh energy, not a tail-end rush.
- [ ] DEV MODE workflow (part of study cluster): learn npm run dev - a long-running terminal process that live-reloads the browser on every file save (Hot Module Reload), so app changes show in <1s instead of the slow build+deploy loop. Distinction to internalize: VS Code = the EDITOR (where you type code); npm run dev = a PROCESS that watches files + reloads; they run together (dev server can run in VS Code's built-in terminal). Use dev mode for iterating; use npm run build + npx vercel --prod ONLY to publish. Also learn: npx vercel (no --prod) = preview deploy.
- [ ] TOKEN FRAGILITY (hit 3x on 2026-06-11): two Drive tokens - local gdrive_token.json + Railway GOOGLE_TOKEN_JSON - expire ~weekly, refreshed SEPARATELY. Refreshing local does NOT update Railway. Every expiry = re-auth local + manual base64 re-paste to Railway env var. FIX candidate: one script that refreshes local token AND pushes fresh base64 to Railway (Railway CLI/API). Symptom: audio 500s with invalid_grant. Stopgap: refresh local -> copy base64 ([Convert]::ToBase64String) -> paste to Railway GOOGLE_TOKEN_JSON -> wait for redeploy.
- [ ] STUDY CLUSTER (priority): understand my own toolchain instead of running it blind. (a) read each .py in 09_TOOLS + read-along backend - know what each does and why, not just how to run it; (b) comprehend git software (the stated priority); (c) start point = 09_TOOLS_INDEX.md. Rationale: every surprise this session came from running tools I had not read (NODES hardcoded, populate_staging node-selection, session_close docstring drift).
- [ ] REFRAMED 2026-06-15: the "convert path-format to id:" entries are NOT a format task - they are 20 BORROWED-AUDIO entries (topic key points at a book/guide chapter recorded for something else, NOT its own dedicated audio). Converting blindly to id: would LOCK IN the wrong audio and erase the path-string signal that flags 'borrowed/provisional'. Correct fix = re-voice each topic from its own .md, publish via fixed populate_staging (now writes id:). Inspection: 120 total entries, 100 id: (good), 20 path-format, NO duplicate filenames (so first-match-search risk is low for these). Backend serving root cause VERIFIED: populate_staging discarded upload file ID + wrote path-string; backend /audio-local else-branch does files().list name search + takes files[0] = wrong file when names collide. Two-line source fix applied (capture id -> new_entries[key]=f'id:{file_id}'). 20 borrowed entries below need per-topic re-voice decision.
- [x] session_close.py doc/code drift RESOLVED 2026-06-15: deleted stale `--project BDF` docstring usage line (parser only had --silent; _detect_projects() auto-detects from commit keywords so flag was redundant). Docstring now matches code. Committed via Claude Code (+0-1).
- [ ] FEATURE: separate Books/Sessions access path for long-form audio (distinct from topic dropdown)
- [ ] Sessions/Project-Resumes tab build (DESIGNED ? see 07_SYSTEM/Sessions_*.md; first step: check vault [[backlinks]] for cross-context relations)
- [x] Author + voice 3 topics: edge_tts, kokoro_tts, message_queues (DONE 2026-06-11 - live in LISTEN tab)
- [x] read-along-app CLAUDE.md RESOLVED 2026-06-15: doc was mostly already accurate (pipeline section + Drive index format matched code we read this session). Real fix = updated DRIVE_INDEX_JSON section to DEPRECATED/unset + removed base64 re-paste instructions, made necessary by deleting the Railway DRIVE_INDEX_JSON var (GitHub now single source of truth). Verified: DEPRECATED present, re-encode removed. Committed via Claude Code (+2-6).
- [ ] session_close.py: make git add surgical (explicit files, not broad add) ? see Cristian_Principles
- [ ] Audit git history for audio that slipped past the 376-null .gitignore period (low priority)
- [ ] Queue.md hygiene: collapse duplicate 'Completed ? 2026-05-28' sections (low priority)
- [ ] anchor_generator.py batch mode — generate anchors for all 31 chapters
- [ ] Learning path sequencing — generate audio for 30 HIGH priority vault nodes
- [ ] Apply Knowledge Graphs Over Lists to 04_WORKFLOWS + 05_MEMORY + 03_APIS
- [ ] Add session-start command to all project CLAUDE.md files
- [ ] FEATURE: Visual auto-generated study map ("the Wall") - NEW project off BRAIN_OS, syncs with Read-Along. Squares = systems/tasks, grow unlimited; each fills by TEMPERATURE COLOR as learned (status-driven: reads knowledge_os_status from vault, derive-don't-duplicate, never a 2nd registry). Every system task gets a color. Lines = topic relationships (Obsidian [[backlinks]]). Sequence/timeline left-to-right; interconnection vertical (Lego/brick-wall metaphor, live-filling). Shares Read-Along's 4-layer source (md->audio->index->app): same data, EYE-view (diagram/map) vs EAR-view (audio). Tap a square -> play that phase in Read-Along. PARKED design forks (Cristian to internalize first): (A) literal wall / (B) graph-with-wall-skin / (C) both-as-toggle - leaning C, build A first. Granularity of one square = topic vs path vs domain - undecided. Stack TBD after design lands.
- [ ] session_start.py DRY: queue-parse state machine duplicated - load_context() and check_queue() both walk Queue.md for "## In Progress" / break-on-next-"## ". Same logic, two copies. Extract to one helper during trim pass (Documentation Must Reflect Reality + DRY).
- [ ] session_start.py bug: check_git_status() returns -1 on failure (couldn't check) but print_context_header() only branches git_dirty > 0 vs else="clean". So a BROKEN git check prints as "GIT: clean" - claim-vs-truth gap. Add explicit -1 branch (e.g. "GIT: check failed").
- [ ] STALE QUEUE ITEM correction: the 'session_close.py: make git add surgical' item does NOT match reality - session_close.py has NO git add/commit anywhere (only reads via git log). Either the item is stale (older version committed, already removed) or it describes an unbuilt desired feature (auto-commit archive surgically). Rewrite or remove. [found while reading file 2026-06-15]
- [ ] session_close.py minor: archive_path.write_text(archive_md, encoding="utf-8") obeys encoding rule but omits newline="\n" - on Windows text mode translates \n->\r\n. Harmless for .md (renders fine) but off the canonical safe-write standard (encoding+newline both). Low priority cosmetic.
- [ ] vault_audio_generator.py MODEL DRIFT: hardcodes model="claude-sonnet-4-20250514" (older dated Sonnet) but Cristian standard is claude-sonnet-4-6 (never Opus). Vault audio is generated by an older model than other tools assume. Decide: bump to claude-sonnet-4-6. [verified in code 2026-06-15]
- [ ] vault_audio_generator.py docstring typo: pipeline step 3 says Kokoro voice "am_heart" but config + code correctly use af_heart (TTS_VOICE line ~36). One-letter fix to docstring (am->af). Documentation Must Reflect Reality.
- [ ] vault_audio_generator.py DEAD CODE: line ~75 has `"08_TRIGGERS/Trigger_Architecture.md" if False else "07_SYSTEM/Trigger_Architecture.md"` - the if-False branch can never execute (fossil from when file moved 08_TRIGGERS->07_SYSTEM). Collapse to plain string "07_SYSTEM/Trigger_Architecture.md". Clean up stale code when discovered.
- [ ] vault_audio_generator.py HARDCODED NODE LIST: HIGH_PRIORITY_NODES is hand-maintained (needs list(dict.fromkeys()) dedup as evidence of accidental-dupe risk; missing files only caught at runtime via exists-guard). Same pattern already eliminated in populate_staging.py (NODES auto-derive by status). Derive-don't-duplicate candidate: auto-derive from knowledge_os_status frontmatter. [GOLD CAPSTONE: this is the before-state of a lesson already learned]
- [ ] 09_TOOLS_INDEX.md STALE: claims "Master index for ALL tool documentation nodes" but lists only editor/hardware doc-nodes + session_close.py. Missing session_start.py and all 24 other .py tools in 09_TOOLS (graph_maintainer, graphify, vault_audio_generator, etc). The stated study-cluster start point is a map missing most of its territory. Rebuild to index actual scripts.
- [ ] populate_staging.py ROOT CAUSE of path-format index entries: upload_to_drive() RETURNS the Drive file ID (f["id"]) but main() Step 3 DISCARDS it - writes new_entries[key] = "{DRIVE_FOLDER}/{key}.mp3" (a path string), NOT "id:{file_id}". Contradicts documented hard rule (capture ID, store id: prefix; filename search unreliable for new uploads). This script is the SOURCE that keeps generating path-format entries - explains the existing 'convert path-format to id:' queue item never stays fixed. FIX: capture upload return -> new_entries[key] = f"id:{file_id}". [verified in code 2026-06-15]
- [ ] populate_staging.py re-voice-blind (revised from 'orphan' concern): main() filters pending = [n for n in NODES if key not in index], so already-indexed nodes are SKIPPED entirely - never re-uploaded. Means re-voicing an existing lesson requires manually removing its index entry first, or new audio never publishes. upload_to_drive uses files().create() (not update()), but the filter means it only ever fires for NEW keys, so not actually orphan-prone in normal use. Low severity; document the 're-voice = clear index entry first' step.
- [ ] populate_staging.py docstring drift (minor): docstring lists 4-step pipeline but code has Step 1 TTS / 2 transcribe / 2b copy-transcripts / 3 upload / 4 index. Step 2b (copy audio_staging/*.json -> backend/transcripts/) is undocumented. Code more elaborate than docstring. Third script this session with docstring-lags-code (also session_close.py, vault_audio_generator.py). Pattern for capstone.
- [ ] BORROWED-AUDIO RE-VOICE WORKLIST (20 entries, found 2026-06-15) - each topic key currently points at borrowed chapter/guide audio, needs its own .md voiced + republished via fixed populate_staging (writes id:). NO duplicate filenames so low wrong-audio risk until fixed. List: model_context_protocol->resolve_mcp_guide.wav | prompt_engineering->claudeguide_prompting_architecture.wav | python_venvs->guide_venv.wav | obsidian_workflows->guide_obsidian_claude.wav | function_calling->claudeguide_skills_system.wav | llm_fundamentals->programming_terminology_reference.wav | env_management->active_environments_audio.mp3 | etl_pipelines->ch01_pipeline_architecture | tts_systems->ch03_tts_audio | webhook_design->ch05_telegram_twitter | api_rate_limiting->ch16_cost_tracking | python_asyncio->ch14_async_export_pattern | event_driven_architecture->ch02_bridge_reload_discipline | cicd_pipelines->ch13_deploy_discipline | agent_orchestration->ch04_agents.wav | monolith_vs_microservices->ch07_deployment.wav | federated_systems->ch11_architecture.wav | audio_pipeline_design->ch01_origin.wav | llm_data_pipelines->bdf_knowledge_build_flow_audio.mp3 | knowledge_graph_design->content_orchestrator_audio.mp3. ACTION per topic: confirm .md exists -> voice -> publish (id:). Some MAY be acceptable as-is (e.g. a topic genuinely about that guide) - Cristian to triage which are truly borrowed vs legitimately mapped.
- [ ] graph_maintainer.py READ COMPLETE 2026-06-15 (study cluster). Findings: (1) DUPLICATE "Task 2" labels - both task_dependency_mapping AND audio_parity_check/_print_parity_report are labeled "Task 2" (confirmed in main() too: Task 0,1,2-audio,2-dependency,3). Task numbering incoherent - renumber. (2) Docstring claims only 3 tasks but file has Task 0 (manifest preflight + change-token/TTL auto-sync via drive_sync.py) + audio parity check. 6th docstring-lags-code instance this session. (3) TWO BYTE-IDENTICAL COPIES exist: C:\BRAIN_OS\09_TOOLS\ and C:\Dev\Projects\soccer-content-generator\scripts\ (MD5 verified identical). session_start.py calls the soccer one. Editing one silently leaves other stale - pick canonical, symlink or delete dup. (4) _is_alternate_chapter() classifies CORE vs ALTERNATE by counting filename underscore-segments (>2 = alternate) - powerful but naming-fragile; adding an underscore to a core chapter misclassifies it.
- [ ] NOTE (NOT a bug - corrected mid-read): session_start.py audio health check WORKS. Initially suspected it parsed ALTERNATES:/MISSING:/HEALTHY: labels graph_maintainer never emits - FALSE. _print_parity_report() emits exactly those labels (uppercase+colon), matching session_start's grep precisely. Reading the full file corrected a premature conclusion. No fix needed. Logged so the wrong finding doesn't resurface.
- [ ] graphify.py READ COMPLETE 2026-06-15 (study cluster). It is the GRAPH BUILDER (graph_maintainer consumes its output). Does: scan .py files, hash, classify imports (stdlib/internal/external, brain_audio flagged [shared-core]), extract signatures (big files) OR imports (small files) by header_only_threshold_kb (default 50), assign architectural layer, write graph JSON + .context.md. Both writes encoding-safe (json.dumps + write_text utf-8). Fully config-driven via .graphify.json (one tool, any project). Incremental: hash-skip unchanged nodes unless --force. FINDINGS: (1) shares _md5/_should_skip with graph_maintainer but maintainer RENAMED _parse_top_level_imports->_parse_imports when copying - partial duplication drift. (2) size-based node mode split means files >=50kb store signatures-only (no imports) - maintainer's _flat_imports reads EMPTY for such files. Watch graphify's printed 'header_only: N' - only matters if N>0 (likely 0 for current files). (3) _assign_layer + by-layer grouping = prior art for the parked WALL feature (layer-assignment-by-path-pattern already solved here).
- [ ] drive_sync.py READ COMPLETE 2026-06-15 (study cluster). The Drive<->local bridge (lives in soccer-content-generator/scripts/, NOT 09_TOOLS - that path has only a 1.2k STUB; graph_maintainer's 09_TOOLS copy would fail to find it). 5 modes: default sync (build manifest), --upload (orphan-SAFE: update-or-create), --get-token (changes().getStartPageToken - the maintainer's change-detection dependency, CONFIRMED working: main() captures start_page_token into manifest each sync, maintainer reads it next session), --normalize (renames non-canonical Drive files to canonical, with --dry-run preview + collision check - this is the REMEDIATION tool for the naming-drift we found), --dry-run (modifier). Manifest tracks 7 categories with drive_id per file.
- [ ] drive_sync.py FINDING - ENCODING: all THREE write_text calls omit encoding="utf-8" (token write ~L74, normalize manifest write ~L434, main sync write ~L517) AND use ensure_ascii=False. On Windows (cp1252 default) a non-ASCII filename could corrupt or raise UnicodeEncodeError. Works today only because filenames are ASCII. Against the hard encoding rule. FIX: add encoding="utf-8" to all 3 writes.
- [ ] drive_sync.py FINDING - upload pattern is CORRECT here (update-or-create, orphan-safe) but populate_staging.upload_to_drive is create-ONLY (orphan-prone). The good pattern exists in drive_sync; copy it to populate_staging. Cross-ref the id: fix.
- [ ] drive_sync.py FINDING - health coverage gap: manifest populates 7 categories (chapters, sessions, bdf_anchors, bdf_combined, brainos_chapters, brainos_sessions) but graph_maintainer audio_parity_check only validates 2 (chapters, sessions). Anchors/combined/brainos audio catalogued but never health-checked (stale/missing/orphaned invisible for them).
- [ ] drive_sync.py FINDING - docstring documents only 2 of 5 modes (sync + upload); --get-token, --normalize, --dry-run undocumented. Most under-documented file this session.
- [ ] USEFUL FOR BORROWED-AUDIO BACKFILL: the manifest (bdf_drive_manifest.json) already stores drive_id for every audio file across all 7 categories. To convert the 20 path-format index entries to id:, look up each key in the manifest and read its drive_id - cleaner/safer than re-searching Drive by filename. Also: drive_sync.py --normalize --dry-run can reveal which files have non-canonical names (overlaps the borrowed-audio worklist).

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


---
## TELEGRAM CLUSTER (parked - review as ONE dedicated pass, not piecemeal)
Telegram touches env-loading across multiple scripts + the local/Railway token split. Fix all together so one script isn't patched while related items rot. Known correct pattern (verified 2026-06-15): call load_dotenv() before reading TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID (session_close.py lacks it -> silent skip in plain PowerShell; vault_audio_generator.py + backend.py do it right).
- [ ] Telegram env vars not loaded in plain PowerShell -> close-script notification silently skips; load .env
