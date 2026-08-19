# BRAIN_OS — Master Queue

## In Progress
- [ ] RENAME compile_session.py / session_compiler.py (scoped 2026-08-19, not executed). Confirmed two different tools: compile_session.py = archive -> knowledge ingestion -> vault + Telegram + git; session_compiler.py = archive -> Claude distill -> Kokoro TTS -> Drive -> drive_index. Zero shared functions. Proposed: ingest_session.py / voice_session.py. CODE CALLERS (3): session_close.py:302, $PROFILE function compile_session, $PROFILE line 22. DOC REFS: Navigation.md x2 ([[Compile_Session_Workflow]]), PowerShell_Aliases.md, software_architecture.md x2, systems_operations.md, Sessions_Tab_Design_Notes.md, Domain_Taxonomy.md x3, artifacts.manifest.json x3, lesson_10_os_fundamentals.md (VOICED - re-voice debt). Graphify JSON self-corrects. Do it as one atomic commit.
- [ ] SYSTEM_MASTER alias table is half the profile: 15 documented, 30 live. Missing: compile_session, session-start, session_close, graph, git-session, audio-session, fix-session, build-session, ra, bdf, gig, bos, edit-brainconfig, edit-claude, edit-driveindex, edit-settings. generate_profile.py:270 only warns when the table has entries the script does not generate, never the reverse, so undocumented aliases pass silently. Add the rows; consider making the warning bidirectional.
- [ ] CC_Nav.md exists twice and diverged: 00_NAV (1473 bytes) vs 02_PROJECTS (1364). Pick canonical, delete the other. Then check BDF_Nav, CA_Nav, OBS_Nav, ReadAlong_Nav, ResolveMCP_Nav for the same split.
- [ ] RE-VOICE DEBT: three audio lessons state Railway as present-tense fact - lesson_10_os_fundamentals ("Railway runs Read-Along in a container", used as the process-isolation example), read_along_app_build_session, dev_workflow. Each is .md + .json + Drive audio. Fixing means re-running TTS, transcription, upload, index. Batch them.
- [ ] read-along-app: extract one API_BASE constant. The backend URL is inlined across 7 tab files under 3 different names (API_BASE, API, BACKEND) plus 5 bare inline literals. The Render migration required editing 7 files. Also: CLAUDE.md Architecture block still lists 4 tabs, there are 7.
- [ ] Memory_Index.md has two readers and no writer, one of them cross-repo (read-along-app/backend/populate_staging.py:83 reaches into the vault by hardcoded path). Either give it a generator or make the read contract explicit via a flag.
- [ ] Drive file ID duplicated across repos: drive_index.json and read-along-app/backend/update_index.py both hardcode id:1mPwHEovGlCBU8X8f5Uru4npXpmW8rT_i for memory_index. Two sources, silent divergence on re-upload.
- [ ] Telegram HTTP 401 on session_start. Possible cause found 2026-08-19: TWO .env files claim the bot - CLAUDE.md says 03_APIS/.env, watchdog.py loads from soccer-content-generator/.env. Check which holds the valid token.
- [ ] FLAGS_MANUAL.md documents 5 TYPEs, FLAGS.txt uses 11 (BUG DATA TOOL FEAT WORKFLOW SECURITY PROCESS undocumented; CODE documented but never used). REPO column holds categories (POWERSHELL, PROCESS, TOOL) not repos. Update the manual to match the file.
- [ ] NAME COLLISION (found 2026-08-19): session_compiler.py and compile_session.py both live in 09_TOOLS and both act on session archives. compile_session.py = Option C knowledge ingestion (reads latest archive, runs Ingestion Protocol V2, flags to Telegram + ingestion_flags.md, git commits). session_compiler.py = session-to-audio (distills archive via Claude API, Kokoro TTS, uploads to Drive, adds drive_index entry). Different jobs, near-identical names — a reader cannot tell them apart, and session_compiler.py was absent from 09_TOOLS_INDEX.md for months. ACTION: read both, confirm neither supersedes the other, then rename for clarity (candidates: ingest_session.py / voice_session.py). Blast radius: check $PROFILE functions and any caller before renaming.
- [ ] MANIFEST COVERAGE GAP (found 2026-08-19): projects.manifest.json calls itself the declared source of truth for project roots but lists 7 of 12 known repos. Missing: gig_tracker (C:\Dev\Projects\gig_tracker\gig_tracker, nested), book-compiler (C:\Dev\shared\book-compiler), cc-landing (C:\Dev\cc-landing), custom-agent (C:\Dev\Projects\custom-agent), obs-mcp-server (C:\Users\titit\Projects\obs-mcp-server). Each entry now needs name, aliases, root, venv, context_md — and four of the five have no context file yet, so decide per repo whether graphify should generate one or whether a vault note is the right context source (the CristianConstruction and Resolve MCP pattern). ACTION: add entries, then re-run project_paths.py self-test — it verifies every root and context_md exists.
- [x] TOKEN AUTO-FIX DONE (2026-06-15): token_sync.py in soccer-content-generator refreshes/re-auths local Drive token AND auto-pushes to Railway in one command. When audio 500s with invalid_grant: cd C:\Dev\Projects\soccer-content-generator then venv\Scripts\python token_sync.py. Replaces the manual 4-step dance.
- [ ] ARCHITECTURE: per-project session-start isolation (idea 2026-06-15). Goal: each project's session-start is isolated + lean (like the per-project DaVinci control docs), with SHARED content (principles, common rules) living in one file REFERENCED by all, never duplicated. FORK to decide: (A) split session_start.py into one-per-project = more isolation BUT duplicates health-check/Telegram logic unless shared logic moves to a common imported module; (B) keep ONE script (already project-aware via PROJECTS registry + CWD auto-detect) but trim its OUTPUT to be per-project + lean, referencing shared principles by link not dumping inline. LEAN = B (no script duplication; pairs with the queued 'trim session_start.py' study target). Decide A vs B with fresh head; relates to Four Pillars (modularity) + DRY + center-of-gravity.

- [x] DEV MODE workflow (part of study cluster): learn npm run dev - a long-running terminal process that live-reloads the browser on every file save (Hot Module Reload), so app changes show in <1s instead of the slow build+deploy loop. Distinction to internalize: VS Code = the EDITOR (where you type code); npm run dev = a PROCESS that watches files + reloads; they run together (dev server can run in VS Code's built-in terminal). Use dev mode for iterating; use npm run build + npx vercel --prod ONLY to publish. Also learn: npx vercel (no --prod) = preview deploy. RESOLVED 2026-06-17 — HMR verified live, dev_workflow audio published to devops_deployment path
- [ ] TOKEN FRAGILITY — local refresh works (token_sync.py, soccer-content-generator). Railway push intermittently fails. PRIOR diagnosis "Cloudflare 403/1010" likely WRONG — 2026-06-22 investigation points to Railway TOKEN-TYPE (Team vs Project token), not Cloudflare bot-blocking. Duplicate RAILWAY_TOKEN line in .env removed 2026-06-22 (was on lines 27-28, now one). NEXT: in Railway dashboard regenerate RAILWAY_TOKEN as a Project token scoped to read-along-app, swap into .env as a single line. Verify across next several real token_sync.py runs (intermittent — one run can't prove the fix). Manual clipboard fallback still works meanwhile.
- [ ] CA_Book\venv DECISION (found 2026-06-22): CA_Book has its own venv at C:\Knowledge\CA\CA_Book\venv (36 pkgs, anthropic+google stack, NO brain_audio) but everything actually runs through the PARENT C:\Knowledge\CA\venv (all $PROFILE book functions point there; CA_Book code imports neither brain_audio nor anthropic directly). Nothing references CA_Book\venv. Stale by all evidence — but PARKED not deleted (Cristian may have a reason). Revisit: confirm no need, then delete. Harmless meanwhile.
- [x] TOKEN FRAGILITY (hit 3x on 2026-06-11): two Drive tokens - local gdrive_token.json + Railway GOOGLE_TOKEN_JSON - expire ~weekly, refreshed SEPARATELY. Refreshing local does NOT update Railway. Every expiry = re-auth local + manual base64 re-paste to Railway env var. FIX candidate: one script that refreshes local token AND pushes fresh base64 to Railway (Railway CLI/API). Symptom: audio 500s with invalid_grant. Stopgap: refresh local -> copy base64 ([Convert]::ToBase64String) -> paste to Railway GOOGLE_TOKEN_JSON -> wait for redeploy. PARTIALLY RESOLVED 2026-06-17 — refresh_drive_token.py created, Railway env vars still needed
- [ ] STUDY CLUSTER (priority): understand my own toolchain instead of running it blind. (a) read each .py in 09_TOOLS + read-along backend - know what each does and why, not just how to run it; (b) comprehend git software (the stated priority); (c) start point = 09_TOOLS_INDEX.md. Rationale: every surprise this session came from running tools I had not read (NODES hardcoded, populate_staging node-selection, session_close docstring drift). — git comprehension COMPLETE 2026-06-17 (5 phases, live on BRAIN_OS)
- [x] LEARNING PATH AUDIT 2026-06-17: 49 drive_index topics unpathed. Priority assignments: git -> devops_deployment path (before git_advanced); message_queues, edge_tts, kokoro_tts, active_environments, lancedb_vector_store need path design. cicd_pipelines has path assignment but missing audio — re-voice needed. Dedicated session: design full path additions before touching learning_paths.json. RESOLVED 2026-06-17 — 15 paths, tier system, all unpathed topics assigned or intentionally standalone
  - [x] BATCH 1 COMPLETE 2026-06-17: git, edge_tts, kokoro_tts, active_environments, lancedb_vector_store, llm_data_pipelines pathed. New claude_tooling path created. 36 intentionally standalone remain (BDF/CA project docs, system/vault docs, path intros).
- [x] CONTEXT_OPTIMIZATION — design isolated entry programs per task type (git-session, audio-session, fix-session). Each loads only task-relevant context (~1k tokens vs ~5k full load). Build after GOLD CAPSTONE. Pattern: session-start is the prototype — extend to task-specific launchers. RESOLVED 2026-06-17 — task_session.py created, 4 launchers in profile: git-session, audio-session, fix-session, build-session
- [x] REFRAMED 2026-06-15: the "convert path-format to id:" entries are NOT a format task - they are 20 BORROWED-AUDIO entries (topic key points at a book/guide chapter recorded for something else, NOT its own dedicated audio). Converting blindly to id: would LOCK IN the wrong audio and erase the path-string signal that flags 'borrowed/provisional'. Correct fix = re-voice each topic from its own .md, publish via fixed populate_staging (now writes id:). Inspection: 120 total entries, 100 id: (good), 20 path-format, NO duplicate filenames (so first-match-search risk is low for these). Backend serving root cause VERIFIED: populate_staging discarded upload file ID + wrote path-string; backend /audio-local else-branch does files().list name search + takes files[0] = wrong file when names collide. Two-line source fix applied (capture id -> new_entries[key]=f'id:{file_id}'). 20 borrowed entries below need per-topic re-voice decision. RESOLVED 2026-06-17 — all 20 borrowed entries re-voiced or converted to id:
- [x] session_close.py doc/code drift RESOLVED 2026-06-15: deleted stale `--project BDF` docstring usage line (parser only had --silent; _detect_projects() auto-detects from commit keywords so flag was redundant). Docstring now matches code. Committed via Claude Code (+0-1).
- [ ] FEATURE: separate Books/Sessions access path for long-form audio (distinct from topic dropdown)
- [ ] Sessions/Project-Resumes tab build (DESIGNED ? see 07_SYSTEM/Sessions_*.md; first step: check vault [[backlinks]] for cross-context relations)
- [x] Author + voice 3 topics: edge_tts, kokoro_tts, message_queues (DONE 2026-06-11 - live in LISTEN tab)
- [x] read-along-app CLAUDE.md RESOLVED 2026-06-15: doc was mostly already accurate (pipeline section + Drive index format matched code we read this session). Real fix = updated DRIVE_INDEX_JSON section to DEPRECATED/unset + removed base64 re-paste instructions, made necessary by deleting the Railway DRIVE_INDEX_JSON var (GitHub now single source of truth). Verified: DEPRECATED present, re-encode removed. Committed via Claude Code (+2-6).

- [x] Audit git history for audio that slipped past the 376-null .gitignore period (low priority) RESOLVED 2026-06-17 — 9 files found, none currently tracked, clean
- [x] anchor_generator.py batch mode — generate anchors for all 31 chapters RESOLVED 2026-06-17
- [ ] Learning path sequencing — generate audio for 30 HIGH priority vault nodes
- [x] Apply Knowledge Graphs Over Lists to 04_WORKFLOWS + 05_MEMORY + 03_APIS RESOLVED 2026-06-17 — all three folders complete
- [x] Add session-start command to all project CLAUDE.md files RESOLVED 2026-06-17
- [ ] FEATURE: Visual auto-generated study map ("the Wall") - NEW project off BRAIN_OS, syncs with Read-Along. Squares = systems/tasks, grow unlimited; each fills by TEMPERATURE COLOR as learned (status-driven: reads knowledge_os_status from vault, derive-don't-duplicate, never a 2nd registry). Every system task gets a color. Lines = topic relationships (Obsidian [[backlinks]]). Sequence/timeline left-to-right; interconnection vertical (Lego/brick-wall metaphor, live-filling). Shares Read-Along's 4-layer source (md->audio->index->app): same data, EYE-view (diagram/map) vs EAR-view (audio). Tap a square -> play that phase in Read-Along. PARKED design forks (Cristian to internalize first): (A) literal wall / (B) graph-with-wall-skin / (C) both-as-toggle - leaning C, build A first. Granularity of one square = topic vs path vs domain - undecided. Stack TBD after design lands.
- [x] session_start.py DRY: queue-parse state machine duplicated - load_context() and check_queue() both walk Queue.md for "## In Progress" / break-on-next-"## ". Same logic, two copies. Extract to one helper during trim pass (Documentation Must Reflect Reality + DRY). RESOLVED 2026-06-17
- [x] session_start.py bug: check_git_status() returns -1 on failure (couldn't check) but print_context_header() only branches git_dirty > 0 vs else="clean". So a BROKEN git check prints as "GIT: clean" - claim-vs-truth gap. Add explicit -1 branch (e.g. "GIT: check failed"). RESOLVED 2026-06-17
- [x] STALE QUEUE ITEM correction: the 'session_close.py: make git add surgical' item does NOT match reality - session_close.py has NO git add/commit anywhere (only reads via git log). Either the item is stale (older version committed, already removed) or it describes an unbuilt desired feature (auto-commit archive surgically). Rewrite or remove. [found while reading file 2026-06-15] RESOLVED 2026-06-17
- [x] session_close.py minor: archive_path.write_text(archive_md, encoding="utf-8") obeys encoding rule but omits newline="\n" - on Windows text mode translates \n->\r\n. Harmless for .md (renders fine) but off the canonical safe-write standard (encoding+newline both). Low priority cosmetic. RESOLVED 2026-06-17
- [x] vault_audio_generator.py MODEL DRIFT: hardcodes model="claude-sonnet-4-20250514" (older dated Sonnet) but Cristian standard is claude-sonnet-4-6 (never Opus). Vault audio is generated by an older model than other tools assume. Decide: bump to claude-sonnet-4-6. [verified in code 2026-06-15] RESOLVED 2026-06-17
- [x] vault_audio_generator.py docstring typo: pipeline step 3 says Kokoro voice "am_heart" but config + code correctly use af_heart (TTS_VOICE line ~36). One-letter fix to docstring (am->af). Documentation Must Reflect Reality. RESOLVED 2026-06-17
- [x] vault_audio_generator.py DEAD CODE: line ~75 has `"08_TRIGGERS/Trigger_Architecture.md" if False else "07_SYSTEM/Trigger_Architecture.md"` - the if-False branch can never execute (fossil from when file moved 08_TRIGGERS->07_SYSTEM). Collapse to plain string "07_SYSTEM/Trigger_Architecture.md". Clean up stale code when discovered. RESOLVED 2026-06-17
- [x] vault_audio_generator.py HARDCODED NODE LIST: HIGH_PRIORITY_NODES is hand-maintained (needs list(dict.fromkeys()) dedup as evidence of accidental-dupe risk; missing files only caught at runtime via exists-guard). Same pattern already eliminated in populate_staging.py (NODES auto-derive by status). Derive-don't-duplicate candidate: auto-derive from knowledge_os_status frontmatter. [GOLD CAPSTONE: this is the before-state of a lesson already learned] RESOLVED 2026-06-17
- [x] 09_TOOLS_INDEX.md STALE: claims "Master index for ALL tool documentation nodes" but lists only editor/hardware doc-nodes + session_close.py. Missing session_start.py and all 24 other .py tools in 09_TOOLS (graph_maintainer, graphify, vault_audio_generator, etc). The stated study-cluster start point is a map missing most of its territory. Rebuild to index actual scripts. RESOLVED 2026-06-17
- [x] populate_staging.py ROOT CAUSE of path-format index entries: upload_to_drive() RETURNS the Drive file ID (f["id"]) but main() Step 3 DISCARDS it - writes new_entries[key] = "{DRIVE_FOLDER}/{key}.mp3" (a path string), NOT "id:{file_id}". Contradicts documented hard rule (capture ID, store id: prefix; filename search unreliable for new uploads). This script is the SOURCE that keeps generating path-format entries - explains the existing 'convert path-format to id:' queue item never stays fixed. FIX: capture upload return -> new_entries[key] = f"id:{file_id}". [verified in code 2026-06-15] RESOLVED 2026-06-17
- [x] populate_staging.py re-voice-blind (revised from 'orphan' concern): main() filters pending = [n for n in NODES if key not in index], so already-indexed nodes are SKIPPED entirely - never re-uploaded. Means re-voicing an existing lesson requires manually removing its index entry first, or new audio never publishes. upload_to_drive uses files().create() (not update()), but the filter means it only ever fires for NEW keys, so not actually orphan-prone in normal use. Low severity; document the 're-voice = clear index entry first' step. RESOLVED 2026-06-17
- [x] populate_staging.py docstring drift (minor): docstring lists 4-step pipeline but code has Step 1 TTS / 2 transcribe / 2b copy-transcripts / 3 upload / 4 index. Step 2b (copy audio_staging/*.json -> backend/transcripts/) is undocumented. Code more elaborate than docstring. Third script this session with docstring-lags-code (also session_close.py, vault_audio_generator.py). Pattern for capstone. RESOLVED 2026-06-17
- [x] BORROWED-AUDIO RE-VOICE WORKLIST (20 entries, found 2026-06-15) - each topic key currently points at borrowed chapter/guide audio, needs its own .md voiced + republished via fixed populate_staging (writes id:). NO duplicate filenames so low wrong-audio risk until fixed. List: model_context_protocol->resolve_mcp_guide.wav | prompt_engineering->claudeguide_prompting_architecture.wav | python_venvs->guide_venv.wav | obsidian_workflows->guide_obsidian_claude.wav | function_calling->claudeguide_skills_system.wav | llm_fundamentals->programming_terminology_reference.wav | env_management->active_environments_audio.mp3 | etl_pipelines->ch01_pipeline_architecture | tts_systems->ch03_tts_audio | webhook_design->ch05_telegram_twitter | api_rate_limiting->ch16_cost_tracking | python_asyncio->ch14_async_export_pattern | event_driven_architecture->ch02_bridge_reload_discipline | cicd_pipelines->ch13_deploy_discipline | agent_orchestration->ch04_agents.wav | monolith_vs_microservices->ch07_deployment.wav | federated_systems->ch11_architecture.wav | audio_pipeline_design->ch01_origin.wav | llm_data_pipelines->bdf_knowledge_build_flow_audio.mp3 | knowledge_graph_design->content_orchestrator_audio.mp3. ACTION per topic: confirm .md exists -> voice -> publish (id:). Some MAY be acceptable as-is (e.g. a topic genuinely about that guide) - Cristian to triage which are truly borrowed vs legitimately mapped. COMPLETE 2026-06-17 — all 20 entries cleared across 4 batches
  - [x] BATCH 1 COMPLETE 2026-06-17: env_management, webhook_design, api_rate_limiting — re-voiced + published with id: entries. 6 remaining — batches 1-3 complete 2026-06-17: env_management, webhook_design, api_rate_limiting, etl_pipelines, event_driven_architecture, cicd_pipelines, python_asyncio, tts_systems, llm_fundamentals, function_calling, model_context_protocol, obsidian_workflows, prompt_engineering, python_venvs all cleared (re-voiced or converted to id:). Remaining: agent_orchestration, monolith_vs_microservices, federated_systems, audio_pipeline_design, llm_data_pipelines, knowledge_graph_design
- [x] graph_maintainer.py READ COMPLETE 2026-06-15 (study cluster). Findings: (1) DUPLICATE "Task 2" labels - both task_dependency_mapping AND audio_parity_check/_print_parity_report are labeled "Task 2" (confirmed in main() too: Task 0,1,2-audio,2-dependency,3). Task numbering incoherent - renumber. (2) Docstring claims only 3 tasks but file has Task 0 (manifest preflight + change-token/TTL auto-sync via drive_sync.py) + audio parity check. 6th docstring-lags-code instance this session. (3) TWO BYTE-IDENTICAL COPIES exist: C:\BRAIN_OS\09_TOOLS\ and C:\Dev\Projects\soccer-content-generator\scripts\ (MD5 verified identical). session_start.py calls the soccer one. Editing one silently leaves other stale - pick canonical, symlink or delete dup. (4) _is_alternate_chapter() classifies CORE vs ALTERNATE by counting filename underscore-segments (>2 = alternate) - powerful but naming-fragile; adding an underscore to a core chapter misclassifies it. RESOLVED 2026-06-17
- [x] NOTE (NOT a bug - corrected mid-read): session_start.py audio health check WORKS. Initially suspected it parsed ALTERNATES:/MISSING:/HEALTHY: labels graph_maintainer never emits - FALSE. _print_parity_report() emits exactly those labels (uppercase+colon), matching session_start's grep precisely. Reading the full file corrected a premature conclusion. No fix needed. Logged so the wrong finding doesn't resurface. RESOLVED 2026-06-17
- [x] graphify.py READ COMPLETE 2026-06-15 (study cluster). It is the GRAPH BUILDER (graph_maintainer consumes its output). Does: scan .py files, hash, classify imports (stdlib/internal/external, brain_audio flagged [shared-core]), extract signatures (big files) OR imports (small files) by header_only_threshold_kb (default 50), assign architectural layer, write graph JSON + .context.md. Both writes encoding-safe (json.dumps + write_text utf-8). Fully config-driven via .graphify.json (one tool, any project). Incremental: hash-skip unchanged nodes unless --force. FINDINGS: (1) shares _md5/_should_skip with graph_maintainer but maintainer RENAMED _parse_top_level_imports->_parse_imports when copying - partial duplication drift. (2) size-based node mode split means files >=50kb store signatures-only (no imports) - maintainer's _flat_imports reads EMPTY for such files. Watch graphify's printed 'header_only: N' - only matters if N>0 (likely 0 for current files). (3) _assign_layer + by-layer grouping = prior art for the parked WALL feature (layer-assignment-by-path-pattern already solved here). RESOLVED 2026-06-17
- [x] drive_sync.py READ COMPLETE 2026-06-15 (study cluster). The Drive<->local bridge (lives in soccer-content-generator/scripts/, NOT 09_TOOLS - that path has only a 1.2k STUB; graph_maintainer's 09_TOOLS copy would fail to find it). 5 modes: default sync (build manifest), --upload (orphan-SAFE: update-or-create), --get-token (changes().getStartPageToken - the maintainer's change-detection dependency, CONFIRMED working: main() captures start_page_token into manifest each sync, maintainer reads it next session), --normalize (renames non-canonical Drive files to canonical, with --dry-run preview + collision check - this is the REMEDIATION tool for the naming-drift we found), --dry-run (modifier). Manifest tracks 7 categories with drive_id per file. RESOLVED 2026-06-17
- [x] drive_sync.py FINDING - ENCODING: all THREE write_text calls omit encoding="utf-8" (token write ~L74, normalize manifest write ~L434, main sync write ~L517) AND use ensure_ascii=False. On Windows (cp1252 default) a non-ASCII filename could corrupt or raise UnicodeEncodeError. Works today only because filenames are ASCII. Against the hard encoding rule. FIX: add encoding="utf-8" to all 3 writes. RESOLVED 2026-06-17
- [x] drive_sync.py FINDING - upload pattern is CORRECT here (update-or-create, orphan-safe) but populate_staging.upload_to_drive is create-ONLY (orphan-prone). The good pattern exists in drive_sync; copy it to populate_staging. Cross-ref the id: fix. RESOLVED 2026-06-17
- [x] drive_sync.py FINDING - health coverage gap: manifest populates 7 categories (chapters, sessions, bdf_anchors, bdf_combined, brainos_chapters, brainos_sessions) but graph_maintainer audio_parity_check only validates 2 (chapters, sessions). Anchors/combined/brainos audio catalogued but never health-checked (stale/missing/orphaned invisible for them). RESOLVED 2026-06-17
- [x] drive_sync.py FINDING - docstring documents only 2 of 5 modes (sync + upload); --get-token, --normalize, --dry-run undocumented. Most under-documented file this session. RESOLVED 2026-06-17
- [x] USEFUL FOR BORROWED-AUDIO BACKFILL: the manifest (bdf_drive_manifest.json) already stores drive_id for every audio file across all 7 categories. To convert the 20 path-format index entries to id:, look up each key in the manifest and read its drive_id - cleaner/safer than re-searching Drive by filename. Also: drive_sync.py --normalize --dry-run can reveal which files have non-canonical names (overlaps the borrowed-audio worklist). RESOLVED 2026-06-17

## Next Sessions (ordered)

- [x] Session 3: Apply Knowledge Graphs Over Lists to 04_WORKFLOWS RESOLVED 2026-06-17 — 7 files updated
- [x] Session 4: Apply Knowledge Graphs Over Lists to 05_MEMORY + 03_APIS RESOLVED 2026-06-17
- [ ] Session 5: Update all project CLAUDE.md files with Triggers section
- [ ] CA Book Phase 3: Session_Resume pipeline (needs actual files first)

---

## Session 2026-06-24 (BRAIN_OS deep-dive + learning pipeline build)
- [x] token_sync.py ghost claim RESOLVED 2026-06-24 — file is real, lives in BDF root, works fine; prior audit was scoped to 09_TOOLS only
- [x] BDF sync_brain.py / distill_session.py "dead files" claim RESOLVED 2026-06-24 — both are live tools (system health monitor / book pipeline), not superseded, leave as-is
- [x] Cross-project hardcoded paths RESOLVED 2026-06-24 — session_start.py + anchor_generator.py now resolve via new project_paths.py helper + projects.manifest.json
- [x] Stale CLAUDE.md/PROJECT_CARD.md session-close instructions RESOLVED 2026-06-24 — both now point at canonical C:\BRAIN_OS\09_TOOLS\session_close.py
- [x] CORRECTED 2026-08-19: compile_session.py does NOT have zero callers. session_close.py:302 invokes it via subprocess, and $PROFILE defines `function compile_session`. The original claim was wrong and was reverified as wrong twice. Item closed.
- [ ] graph_maintainer_patch.py is load-bearing (watchdog.py imports from it) but named like a temp patch — needs careful rename, has blast radius
- [ ] BRAIN_OS root folder-prefix collisions (00,02,03,04,05,06,08,10 each map to 2+ folders) — structural reorg decision needed
- [ ] Drive OAuth token expired again mid-session (2026-06-24), blocked session_compiler.py upload — same root cause as existing TOKEN FRAGILITY item, now also blocks the learning-pipeline, raise priority
- [ ] session_compiler.py crashes with FileExistsError on re-run of same session (no cleanup before rename in synthesize()) — add target-file check/unlink before rename, low effort
- [ ] Evening "did you close today?" reminder — new watchdog.py mode + Task Scheduler entry, Telegram nudge if no session archived that day
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
- [x] Telegram env vars not loaded in plain PowerShell -> close-script notification silently skips; load .env RESOLVED 2026-06-17

## [DONE 2026-07-08] 4-Bucket Routing Layer — Phase 1 complete
Commit a931fcf. 00_INDEX/{Content,Business,Operations,Personal}.md written.
Verified inventory: 10 repos across 4 roots (C:\BRAIN_OS, C:\Knowledge,
C:\Dev, C:\Users\titit\Projects). Prior assumption of a single authoritative
project directory was FALSE.

Remaining phases (from 2026-06-20 concept):
- P2: Create 4 Claude.ai Projects, each with charter instructions.
- P3: Add routing line to session SOP (bucket -> Project -> index -> project CLAUDE.md).
- P4: Maintenance rule — new repo added to exactly one bucket index in same commit.

## [RESOLVED 2026-07-08] audio_staging/ is not gitignored — see resolution below (line ~145)
Operating contract states audio_staging is gitignored. `git status` shows it
untracked at C:\BRAIN_OS. Either the .gitignore entry is missing or malformed.
A gitignore believed to be protecting you is not. Investigate before next commit.

## [TASK] Rename CA_Book -> cc-audiobook
CA prefix collides with CC (CristianConstruction). Card flags this itself.
ATOMIC — one commit touching all four:
  1. Directory: C:\Knowledge\CA\CA_Book -> cc-audiobook
  2. 00_NAV\CA_Nav.md -> CCAudiobook_Nav.md
  3. graphify.py config: 02_PROJECTS/graphs/projects.manifest.json ("root" line)
  4. 00_INDEX\Content.md entry
DO NOT relocate out of C:\Knowledge — venv at C:\Knowledge\CA\venv is the
canonical AI/TTS venv (PyTorch nightly cu128, RTX 5070 Ti sm_120).

## [TASK] Four missing nav files
00_INDEX references these as TODO, not wikilinks (dead links would lie):
BRAINOS_Nav.md, Knowledge_Nav.md, BrainAudio_Nav.md, BookCompiler_Nav.md
Also: CCLanding_Nav.md (cc-landing has none).

## [FRAGILITY] Consolidate Google Drive credentials
gdrive_credentials.json / gdrive_token.json shared by 4-6 scripts, with copies
in C:\Knowledge\CA\CA_Book\. Same finding as the graphifyy (third-party CLI) adoption session 2026-06-19. Blast radius
is real. Flagged in 00_INDEX\Operations.md.

## [SMALL] 00_NAV\SYSTEM_Rules.md (4594b) is not a nav file
Likely belongs in 07_SYSTEM\ alongside Cristian_Principles.md. Flagged, not moved.

## [SMALL] cc-landing deploy target unrecorded
Last deploy 2026-04-10 (209d251). vercel.json deliberately removed (078294a).
Deploy target unknown — verify before next ship.

## [RESOLVED 2026-07-08] audio_staging gitignore
Not a broken gitignore. Patterns covered mp3/wav/json but not .txt, so one
staged narration file (session_20260617_2222_TTS.txt) left the directory
untracked. Confirmed artifact, not record — timestamp key 2222 matches
08_SESSIONS/2026-06-17_2222_bdf_ca_brain_os_resolve.md. Fixed by adding
audio_staging/*.txt and audio_staging/**/*.txt.


<!-- auto-ingested 2026-08-13 -->
- Direction 5: added
- Direction 7e: IN PROGRESS (van_build rename + is_onetime confirmed)

## Archived

- Direction 1 — complete: server.py read complete, architecture mapped
- Direction 2 — complete
- Direction 6 — complete: gig_tracker imports
- Direction 7b — complete
- Direction 7c — complete
- Direction 7d — complete


<!-- auto-updated 2026-08-14 -->
- Direction 7e: IN PROGRESS (queued as Direction 8 for next session)
- Direction 8: web.py dashboard (queued)


## 2026-08-16 — Claude.ai cross-check against today's 08_SESSIONS (graphify recovery + callchain audit)
- [ ] NEW: session_start.py Telegram POST failed with WinError 10054 (connection reset by remote host) at 07:10 this session start; self-recovered same run ("Telegram sent." printed immediately after). Distinct from the RESOLVED 2026-06-17 load_dotenv/silent-skip fix above — that was a missing-env-var skip in session_close.py, this is a live urllib POST failure inside session_start.py's direct HTTP call. ACTION: check session_start.py's Telegram-send function for retry/backoff; if none exists, decide add-retry vs log-as-one-off-network-flake.
- [x] WITHDRAWN 2026-08-19: this "confirmation" was wrong. session_close.py:302 calls compile_session.py. A line-by-line reverification reached a false conclusion twice - grep the caller, do not re-read the callee. Matches the 2026-06-24 open item two sections up ("compile_session.py has zero inbound callers... decide: wire in or confirm intentionally manual") — that item is accurate and still open, decision not yet made.
- [ ] Open items from 08_SESSIONS/2026-08-16_1127_brain_os_graphify.md not yet mirrored here (mirroring so they aren't lost the way that session almost was): (1) run `graphify.py --cross-project` — spliced into graphify.py, parses clean, never actually run; verify BRAIN_OS .gitignore first; (2) evaluate `graphify-mcp` (ships with graphifyy v0.8.44, never wired into .claude.json or a .mcp.json) — compare its mid-session-queryable integration path against the existing obs-mcp-server/resolve-mcp-server pattern; (3) record a `graphifyy` v0.8.44 baseline — the 2026-06-19 read-along-app pilot numbers (95%/5%/0%, 0.91 mean confidence) were recorded with no version attached, not valid as a v0.8.44 baseline; (4) `graphifyy` has never been run on soccer-content-generator, CristianConstruction, or BRAIN_OS itself — for BDF, scope to a subfolder first (read-along-app alone was 167 files / ~839k words, flagged as expensive).
- [ ] FLAG (left as-is, not edited): the "TELEGRAM CLUSTER (parked)" header text further up this file still reads "...session_close.py lacks it -> silent skip in plain PowerShell..." but the item directly beneath it is marked RESOLVED 2026-06-17 for exactly that gap. Header phrasing is stale relative to its own resolved child item. Not rewritten here to avoid a full-file replace from chat (this vault has a documented history of encoding corruption from careless edits — see 08_SESSIONS/2026-08-16_1127_brain_os_graphify.md section 2.3). Reword at next Claude Code trim pass.


## 2026-08-16 (cont.) — session-start isolation fork closed, one new bug found verifying it
- [x] ARCHITECTURE: per-project session-start isolation — FORK RESOLVED to (B). Built and verified: load_context()'s QUEUE section now reference-only (`check_queue()` count + path + "[read on demand]"), matching the existing CLAUDE.md/Context/LATEST SESSION pattern. Commit b009ad7. Verified via `python 09_TOOLS\session_start.py --project brainos --context-only` — output is 4 clean reference lines, no more raw Queue.md dump. Supersedes the "ARCHITECTURE: per-project session-start isolation" item further up this file — leaving that one in place rather than editing it in-line (see the standing note above about avoiding full-file rewrites from chat).
- [ ] NEW BUG (found verifying the above): LATEST SESSION candidate filter in load_context() only matches filenames containing `_bdf_ca_brain_os` or starting with `session_` — the newer single-project naming convention (e.g. `2026-08-16_1127_brain_os_graphify.md`, `2026-08-16_1158_brain_os_callchain.md`) matches neither pattern and is silently excluded, no error. Confirmed live: `--project brainos --context-only` on 2026-08-16 still surfaced `2026-08-15_1709_bdf_ca_brain_os.md` as "latest," skipping both of today's own session files. Distinct from (and sharper than) the earlier-flagged "LATEST SESSION isn't per-project" issue — this one drops real, relevant files outright regardless of project scoping. Needs a filter that recognizes both naming conventions, or a move to a single convention going forward.


## 2026-08-16 (cont. 2) — Wall data-model decided (not built), moving to Session 5
- [x] FEATURE: "the Wall" — GRANULARITY FORK RESOLVED (Claude.ai design session, 2026-08-16): one square = one topic (reads existing `knowledge_os_status` directly, no new field, no second registry). Columns = existing learning paths (from `learning_paths.json`, used only as layout grouping, not a new rollup value). Sequencing fork (A/B/C) unchanged from original note — still "leaning C, build A first." Mockup reviewed and approved by Cristian. NOT BUILT — this closes the design fork only. Implementation is real, cross-layer work in read-along-app (new FastAPI endpoint reading knowledge_os_status + learning_paths.json, new React tab consuming it), queued as its own dedicated session — requires read-along-app's own CLAUDE.md/.context.md loaded first per MANDATORY SESSION START, not started today.


## 2026-08-16 (cont. 3) — Session 5 Triggers complete
- [x] Session 5: Update all project CLAUDE.md files with Triggers section — RESOLVED 2026-08-16. Scope was the 3 projects actually covered in Trigger_Architecture.md's "Coverage by Project" table (BRAIN_OS, BDF, CA) — read-along-app, resolve-mcp-server, obs-mcp-server, gig_tracker, etc. have zero triggers defined and were correctly left untouched. Each CLAUDE.md got a `## Triggers` section linking to [[Trigger_Architecture]] (reference only, no duplication) plus that project's row from the coverage table. Commits: 0dfb34d (BRAIN_OS), soccer-content-generator CLAUDE.md, CristianConstruction CLAUDE.md — verified via `git diff` before commit on all three (CA and BDF diffs came back clean after a Claude Code terminal-preview scare turned out to be display truncation, not real corruption).


## 2026-08-16 (cont. 4) - Wall backend shipped, frontend queued for its own session
- [x] FEATURE: "the Wall" - BACKEND DATA LAYER SHIPPED 2026-08-16. Investigated the real data flow before building anything: source of truth is knowledge_os.html (Chrome app, localStorage) -> manual "Obsidian Sync" export -> obsidian_sync.py --input writes vault frontmatter -> same obsidian_sync.json already committed to 09_TOOLS and fetched by backend.py's /topics from GitHub raw. /topics was already pulling status+score+evidence per topic and discarding all but domain. Fix was additive only: /topics now also returns `status` and `path_id` per topic (read-along-app commit 24bc422, pushed to origin/main, Railway deploy). No new export pipeline needed - status freshness is bounded by the same manual-sync cadence learning_paths.json already has, not a new staleness source.
- [ ] FEATURE: "the Wall" - FRONTEND NOT STARTED. Queued as its own dedicated session. Scope: new tab in read-along-app frontend/src/tabs/, fetches /topics, groups entries by `path_id` into columns (path = layout only, not a rollup value), renders one square per topic colored by `status` (4-tier: Not Started / Learning / Practiced / Mastered - mockup during design only used 3, needs a 4th color stop), tap-to-play wired into existing audio player same as Books tab. Design already resolved in a 2026-08-16 Claude.ai session, mockup approved - this entry is pure frontend build, no more open data-model questions.

<!-- auto-ingested 2026-08-16 -->
- [BRAIN_OS] 2026-08-16: Disambiguated graphify.py vs graphifyy; closed duplicate audio_staging item; session-start isolation fork B built; naming-filter bug logged; narrowed gitignore 2026-*.md to daily notes only; committed 10 orphaned session logs; added session opener prompt template.


<!-- auto-ingested 2026-08-16 -->
- [BRAIN_OS] LATEST SESSION naming-filter bug — investigate and fix
- [BRAIN_OS] Wall backend closed; queue frontend work as its own session
- [CristianConstruction] Session 5 Triggers — closed
- [soccer-content-generator] BDF avatar pipeline patch, canvas, and operator manual — delivered


<!-- auto-ingested 2026-08-18 -->
- Wall frontend queued as its own session (backend closed 2026-08-18).
- Session 5 Triggers: closed across all three projects (2026-08-18).
