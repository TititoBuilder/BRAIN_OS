---
tags: [personal, learning, profile, meta]
updated: 2026-07-08
---

# Cristian's Learning Profile

Distilled from [[Cristian_Principles]] and the 08_SESSIONS archive history.
This is a meta-analysis of patterns in how Cristian learns and works —
not a restatement of the principles themselves. Regenerate with
`learning_profile_extractor.py` as new sessions accumulate.

## Core Working Style

Cristian works in tight build-verify-commit loops, rarely leaving work uncommitted at session end. The session archives show a consistent pattern: feat/fix commits cluster together within the same session, followed by chore/docs commits that lock in the state (graph updates, manifest updates, queue syncs). He does not separate "build" days from "clean up" days — hygiene happens in the same session as the feature.

He is strongly anti-redundancy in tooling. The 2026-05-17 commit `chore: delete stale book_compiler.py — canonical moved to C:\Dev\shared\book-compiler\` appears across multiple projects in the same session, indicating he eliminates redundancy immediately upon discovering it rather than scheduling a cleanup pass. The same behavior appears June 17: "chore: remove stale queue item + rebuild 09_TOOLS_INDEX with all 25 scripts" — once a stale reference is spotted, it is removed before the session closes.

His commit discipline is conventional-commits format throughout: `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, `perf:` — applied consistently across all projects from the earliest archived sessions. This is not something he adopted partway through; it appears fully formed from the first substantive commits (2026-05-13 BDF session).

He maintains parallel project contexts within single sessions. By late May, sessions routinely span BDF, CA, BRAIN_OS, and book-compiler simultaneously, with commits properly namespaced by repo. The session archive format itself (`[soccer-content-generator] feat: ...`) shows he tracks which project each commit belongs to without losing thread.

He has a strong preference for making automation honest. The "Audit What Your Automation Commits" principle (June 9) emerged from discovering `session_close.py` was doing a broad `git add`. The fix was not just to patch `session_close.py` — it was to articulate the rule that *all tools* must stage explicitly by name. He applies the same demand-for-honesty to MCP Connected status ("Connected status only confirms the process started — not that tools work") and to test signals ("A passing test against the wrong environment is worse than a failing test").

---

## How He Learns

Cristian learns by building the thing that forces him to encounter the real problem, then codifying what that collision taught him. Every principle entry requires demonstrated competence as a gate: "Only add knowledge here after completing a task that proves you've fully learned and can apply the principle." This is not a stated aspiration — the commit trail confirms it. The PowerShell BOM principle was committed `2026-05-19` alongside the actual fix to Obsidian's `graph.json` colorGroups reset bug. The principle did not precede the fix; it followed it.

His learning infrastructure is itself a project he continuously builds. The session archive traces a progression: manual session notes (pre-May 12) → `session_close.py` deployed (2026-05-12) → `distill_session.py` for knowledge extraction (2026-05-15) → KNOWLEDGE_INGESTION_PROTOCOL_V2 for vault integration (2026-05-12 pending) → `anchor_generator.py` for audio learning anchors (2026-05-23) → `vault_audio_generator.py` for 29 HIGH-priority nodes (2026-05-23) → Knowledge OS with three-tool loop (2026-05-27) → Gold Capstone 9-lesson structured course (2026-06-17). Each layer is built after the prior layer proved insufficient, not before.

He converts audio into a first-class learning medium. The `anchor_generator.py` with `am_adam` voice, the 74-track learning path with M3U playlists (2026-05-23), the `audio_stitcher.py`, and the Knowledge OS loop (score → export → sync → stitch → listen → score) all indicate he is designing a system where passively listening to his own content is a primary review mechanism — not reading notes.

He also learns through deliberate debt reduction. The "borrowed audio" worklist from June 17 (20 entries, cleared in three batches) represents a systematic audit of entries where one topic's audio was standing in for another. He cleared all 20 in a single session, re-voicing each batch and marking progress explicitly: "batch 1 complete — 3 of 20 done," then batch 2 (14 remaining), then batch 3 (6 remaining), then final 6. This is learn-by-fixing applied at inventory scale.

---

## Decision-Making Patterns

Cristian uses frameworks to prevent recurring decision errors, not to slow down decisions. The MCP Tool Selection Framework's three-question sequence (unique capability? simpler interface? learning mode?) is designed to stop him from defaulting to the highest-abstraction tool out of habit. The What/How/Where/Safety Framework for data transformation tools is similarly a pre-build checklist, not a design review — its purpose is to force separation of concerns before the first line of code is written.

His tool-selection decisions lean direct and transparent as the default, with abstraction layers used only where they provide unique value. Evidence: the MCP principle explicitly names `git commit` and `git push` as operations that need no MCP abstraction, while `GitHub PR creation with reviewers/labels` is identified as genuinely MCP-appropriate because the feature doesn't exist in git itself.

He scopes strictly and queues aggressively. The "Declared Start and Finish" principle emerged from recognizing that open-ended drift produces the subjective feeling of falling behind despite real progress. His fix: declare the finish line before starting, and route discoveries to the Queue rather than absorbing them into the current task. The Queue.md in BRAIN_OS is the concrete mechanism — there are repeated `chore: queue sync` and `chore: update Queue.md` commits showing it is actively maintained as a real routing system, not a wishlist.

He chooses relative thresholds over absolute ones when the underlying signal varies. The brain-audio fingerprint principle (`signal / noise_floor > 3.0` vs `signal > 0.0005`) reflects a broader instinct: hardcoded numeric boundaries are fragile against context change. This generalizes his approach to configuration — he externalizes configuration into `BRAIN_OS_CONFIG.json` (committed 2026-05-17: "Load drive folder IDs from BRAIN_OS_CONFIG.json at runtime") rather than hardcoding folder IDs.

When something has two competing implementations, he kills the stale one immediately. The `book_compiler.py` deletion appears in at least three separate session archives across different projects and dates (2026-05-17, 2026-05-18, 2026-05-20) because he encountered the stale copy in multiple repos and deleted it on contact each time.

---

## Correction Patterns

His most consistent correction instinct is to verify the actual state before writing any fix. The "Never Debug Assumptions. Debug Reality." principle (May 30) describes a three-layer check: code layer (`git show`, `Get-Content`), runtime layer (hit the endpoint directly, check Railway logs), data layer (`Get-ChildItem`, count files). The karaoke failure proof is striking: the wrong instinct was to rewrite `ListenTab.tsx`, but hitting `/transcript/lancedb` directly returned `{"detail":"No transcript for 'lancedb'"}`, pointing to missing pipeline output rather than broken code. The fix required no code changes.

His second instinct when debugging is to check the encoding layer. The BOM issue recurs as its own class of failure: Obsidian `graph.json` colorGroups reset (UTF-8 BOM from PowerShell `Set-Content`, May 19), `.gitignore` with 376 null bytes (from PowerShell `Add-Content`, June 9), `Next_Session_Prompt.md` BOM removal (June 17). Each incident produces or reinforces a specific rule. By June 9, the principle had generalized from "JSON edits via Python only" to "all text config files are edited via Python — never PowerShell," treating the encoding hazard as a file-type-agnostic class.

When a first fix attempt makes things worse, he stops and reads the file directly. The `.gitignore` corruption sequence is instructive: `git checkout` restored the already-corrupt committed version (nulls intact); `Add-Content -Encoding ASCII` made it worse. The actual fix was Python: strip null bytes, normalize to LF, rewrite clean UTF-8. He did not attempt a third PowerShell approach — he switched paradigm.

He uses explicit counters and tallies when clearing debt systematically. The borrowed-audio worklist (June 17) tracks: "3 of 20 done" → "batch 2 complete, 14 remaining" → "tally corrected to 14 remaining" → "6 borrowed entries remaining" → "all 20 cleared." The tally correction ("tally corrected to 14 remaining") shows he caught a counting error mid-process and adjusted the number explicitly rather than continuing with wrong state.

When automation produces incorrect output, his correction targets the automation's staging logic rather than the output itself. After `session_close.py` committed 7 temp scripts, the fix was: `git rm` the leaked files, add `__pycache__/` and `*.pyc` to `.gitignore`, and queue a follow-up to "make session_close.py stage explicitly." He patched the cause, not just the symptom.

---

## Values & Priorities

**Zero orphan nodes.** The May 21 session committed "fix: wire 20 vault orphans — zero isolated nodes" and "fix: watchdog orphan counter reads vault directly." Maintaining a fully-connected knowledge graph is treated as a health metric, not a nice-to-have. The watchdog system with morning/bdf/session modes was built specifically to surface this.

**Pipelines that run without asking for help.** Knowledge Management Principle #4 states: "A pipeline that runs without asking for help is the only kind that actually runs consistently." This is not a statement about laziness — it is a statement about reliability. The automation built across BRAIN_OS (session_start.py, session_close.py, watchdog.py, cost_guard.py with Telegram warnings) all target zero-friction operation.

**Visibility as motivation.** Knowledge Management Principle #5: "Seeing what you've built (domain dashboards, graph view) motivates continued building. Invisible progress feels like no progress." The 01_DOMAINS/ dashboards exist explicitly for this reason. The Focus Now cards being made clickable (May 27: "feat: Focus Now cards clickable — opens edit modal") is an instance of this value applied to the dashboard UI.

**Filenames are for machines; metadata belongs in the manifest.** The principle "Filenames Are Machine Keys, Not Metadata Stores" (May 20) is a direct encoding of a preference for separating structural identity (timestamp-based, unique, predictable) from human-readable context (manifest). This surfaces in the `--normalize` flag design for `drive_sync.py`.

**Every project is backed up from day zero.** "Every new project directory must have a GitHub remote configured at creation time." The principle was earned when `book-compiler` was found locally without a remote after weeks of work. He treats local-only repos as unbacked work.

**Documentation must match the actual codebase.** The "Documentation Must Reflect Reality" principle (May 19) was triggered by finding camelCase names in a doc while the project used snake_case. He treats naming divergence as a corrupted map — because every AI session that reads the doc starts with wrong assumptions. This is a systems-thinking framing: the error isn't aesthetic, it's downstream contamination.

---

## Session Rhythm

Sessions are not uniform in length. The archive shows extremely short sessions (2026-05-13 06:50 and 2026-05-13 06:53 are 3 minutes apart, both near-empty) alongside long compound sessions spanning multiple projects (2026-05-18 19:26 touches soccer-content-generator, book-compiler, and BRAIN_OS with 40+ commits). The short sessions appear to be session_close.py test runs or system-check sessions rather than work sessions.

He does not wait for a "clean" stopping point to commit — he commits incrementally within sessions, then produces a session archive at close. The session archive tool (`session_close.py`) was built early (deployed 2026-05-12) and used consistently throughout all subsequent sessions, indicating it became a genuine close ritual rather than an occasional documentation effort.

Multiple sessions on the same day are common: May 16 has sessions at 18:19, 18:50, and 18:52 (likely iterating on the `--get-token` fix); May 28 has sessions at 06:07, 07:40, 14:17, and 20:41. This indicates he works in bursts with context restoration between them, relying on the session archive infrastructure to reload state.

By June 17, sessions are running multiple hours with 60+ commit entries per archive. This is partly because the archive format accumulates all commits since last archive (including prior sessions' commits that hadn't been archived yet), but the June 17 sessions are genuinely massive — clearing the borrowed-audio worklist, auditing 49 unpathed topics, re-voicing 20 entries in three batches, creating task_session.py, adding 4 new learning paths, and resolving 20+ queue items, all in one day across four timestamped session closes (16:39, 18:50, 19:08, 20:09, 22:22).

He closes sessions with a standard set of chore commits: graph update, manifest update, queue sync, session archive. This is visible as a pattern across sessions: `chore: session close — graph, manifest, workspace updates` (May 24), `chore: session close + launch commands + brain notes` (May 27), `chore: session close 2026-05-27` (May 27). The close ritual is automated but still explicitly committed.

---

## Collaboration Preferences (with AI Assistants)

Cristian's collaboration model centers on context-first initialization. "Never Start Blind" is a hard rule: "Always feed CLAUDE.md and .context.md to any AI before starting work. No exceptions across all projects." He then built infrastructure to make this automatic — `session_start.py` as an "autonomous context loader" (May 23) and the Graphify principle (proven May 9) which generates a `.context.md` from the dependency graph so raw file-dumping is replaced with structured signatures. The context budget problem (files ≥ 50KB get header_only mode) is solved at the tool level, not by asking the AI to manage it.

He treats AI assistants as co-pilots within his declared scope, not as autonomous agents. The "Declared Start and Finish" principle explicitly states: "the assistant shows options and the start/finish for each unit" while "I decide the cadence." Discoveries made during the work go to the Queue — the AI does not get to expand scope unilaterally. The `task_session.py` tool (June 17: "focused context launchers for git/audio/fix/build tasks") extends this: different task types get different context bundles, so the AI receives only the context relevant to the declared unit of work.

He reads automation output line-by-line rather than trusting it. The "Audit What Your Automation Commits" principle states: "you must READ the tool's commit output every time." This same verification posture applies to AI outputs — the "Verify Before Write" principle (June 10) describes catching a case where a parallel AI chat wrote a domain file from memory with VERIFY placeholder markers, claimed it was "final," then a download loop wrote the wrong version to disk with 3 markers surviving. His fix: verify every claim with read-only filesystem commands before writing, then write once, clean.

He has built cost monitoring into the collaboration infrastructure. `cost_guard.py` (May 23) is a "Claude Code cost estimator with Telegram warning," and `feat: add cost safety limit check after each chapter compile` (May 17) shows per-operation cost gates in the book compiler. He is not trying to minimize AI use — he is trying to make AI use auditable and bounded.
