---
type: schema-decision
enforces: "[[Cristian_Principles]]"
status: active
---
# Domain Taxonomy

## The rule
`01_DOMAINS` is a personal map of computer science. Each domain is a
FIELD, named with standard CS terminology so personal knowledge connects
to the world's knowledge (books, courses, experts already use these names
as sorting keys). Topics inside a domain are descriptively named for the
concept they teach.

- DOMAIN  = broad field, standard terminology  (e.g. software_architecture)
- TOPIC   = specific concept, descriptive name  (e.g. naming-and-information-architecture)

Field = broad and standard. Topic = specific and descriptive.
Same altitude discipline as enforces/enforced_by: right granularity per level.

## Current domains
- ai_engineering
- creative_systems
- data_science
- software_architecture   <- added 2026-06-02

## Why standard names (the map principle)
A standard field name is an automatic sorting key the whole world already
uses. It connects personal islands to global knowledge, reveals gaps (the
known sub-topics of a field show what you haven't learned yet), and lets
the same principle transfer across fields. Cheaper future learning: new
knowledge attaches to existing structure instead of forming isolated islands.

## QUEUE (do not build before grounding names)
1. Regroup all read-along-app/backend/transcripts/*.json under correct domains.
2. Today's session writeup -> topic in software_architecture
   (working title: naming-and-information-architecture).
3. Verify each existing transcript maps to a real CS field; rename domains
   if any current name is non-standard.
---

## Top-level separation: Domains vs Projects (decided 2026-06-02)

Two fundamentally different kinds of information must not be mixed:

- **01_DOMAINS** = declarative knowledge ("what I know"). Universal CS
  fields, standard names, anchors to the world's books/courses. Timeless.
- **02_PROJECTS** = operational records ("what I do"). Local builds,
  session logs, business ventures. Time-stamped, project-specific.

### The sorting test
"Would this still be true if I'd never built any of my projects?"
  YES -> universal -> 01_DOMAINS
  NO  -> exists only because of a build -> 02_PROJECTS

Mixing them breaks the Map Principle: domains stop being clean global
sorting keys, and reusable knowledge gets buried in execution history.

### The five domains (final)
ai_engineering | software_architecture | data_science |
creative_systems | systems_operations

Orchestrators sort by WHAT THEY BUILD, not that they are orchestrators
(functional cohesion): data_orchestrator->data_science,
video_orchestrator->creative_systems, agent_orchestration->ai_engineering.

### QUEUE (transcript regroup, deferred)
1. Diagnose knowledge_graph_design: semantically overloaded. Read it,
   split/rename (obsidian_knowledge_graph vs graph_rag_architectures),
   then sort to true domain. Do not guess.
2. Move project records out of learning shelf into 02_PROJECTS:
   read_along_app_*, bdf_book_system, ca_book_system,
   cristian_construction, *_build_session, *_session.
3. Sort remaining transcripts into the five domains per the agreed map.
4. Verify every 01_DOMAINS file passes the sorting test above.
---

## Open items grounded from session 2026-06-02

These were decided in-session and are recorded here so they survive:

1. **Write up session 2026-06-02 as a topic** in software_architecture
   (working title: naming-and-information-architecture). Covers: audit/
   cleanup loop, Naming Contract, stub pattern, granularity, Map Principle,
   domains-vs-projects split. Deferred until transcript regroup is done so
   it lands on a clean shelf.

2. **Cleanup-loop remaining targets** (audit_files + cleanup_proposer):
   - brain-os  (vault itself; care with wiki-links)
   - soccer-content-generator  (LAST; most coupled, 295 machine-key files;
     many _BACKUP/_OLD files are dead-named but code-wired -> migration,
     not cleanup)
---

## HIGH PRIORITY — transcript content-integrity check (found 2026-06-02)

knowledge_graph_design.json was found to contain content IDENTICAL to
content_orchestrator.json — a mislabeled duplicate. The label said
"knowledge graph design"; the audio was the content orchestrator. This is
a LIVE APP bug: users tapping that topic heard the wrong lecture.

Action taken: mislabeled duplicate moved to transcripts/_trash.

OPEN: verify every transcript's 	ext matches its machine_key. One
proven mismatch means others may exist. Write a small checker that flags
any transcript whose content looks unrelated to its key (or duplicates
another file's text). This affects what users actually hear — treat as
correctness, not cleanup. Also: real knowledge-graph content may live in
brain-os\knowledge_graph_design.md (was an orphan) — reconcile.
---

## ROOT CAUSE FOUND — transcript content mismatch (investigated 2026-06-02)

### Symptom
5 transcripts had correct machine_key but WRONG text (a copy of another
topic's content): knowledge_graph_design, env_management, llm_data_pipelines,
mcp_protocol, lancedb. Live-app bug — users heard the wrong lecture.

### Investigation trail
- Timestamps: canonical files = 5/28 batch; bad copies = 5/30 batch.
- Internal machine_key matched filename in every case -> NOT a file-copy bug.
- transcribe_batch.py exonerated: it binds key+text to one audio path
  (machine_key = audio_path.stem; transcribes that same file). No misroute
  possible there. The AUDIO itself was wrong.
- Bad .mp3 files confirmed on disk in audio_staging, dated 5/30.
- Traced to TTS generator: backend/gen_tts_staging.py.

### Root cause (gen_tts_staging.py)
Three compounding faults around CONVERTED_DIR (shared, in
soccer-content-generator/converted, never purged between runs):
1. After exact-path miss, falls back to glob("*{output_name}*_TTS.txt")
   and glob("*{output_name}*_audio.mp3") — fuzzy match catches unrelated
   files (e.g. "mcp" matches mcp_registry outputs).
2. Picks candidates[0] with NO verification it's the correct file —
   arbitrary glob order selects a stale leftover from a prior topic's run.
3. CONVERTED_DIR is never cleaned, so leftovers survive to be mis-picked.
Result: correct machine_key (set by caller from output filename) + wrong
audio body (stale file from converted/). 5/28 worked because dir was clean;
5/30 had leftovers.

### Fix (to implement)
- Remove the glob fallbacks. Use the deterministic exact path; if the
  expected _TTS.txt / _audio.mp3 is absent, FAIL LOUD (sys.exit) rather
  than guess. Fail-loud > guess-wrong.
- Purge CONVERTED_DIR at the start of each run so no stale file can be
  selected.
- After fix: regenerate the 4 bad topics (env_management, llm_data_pipelines,
  mcp_protocol, lancedb-as-needed) + knowledge_graph_design, then re-run
  transcript_integrity.py to verify zero duplicates / mismatches.

### Tool
transcript_integrity.py (at C:\Users\titit\) — read-only checker:
hashes text for exact-duplicate detection + scores key/text overlap.
Note: acronym keys (llm, pkm, etl) score low as false positives because
narration spells terms out; duplicates section is the reliable signal.
---

## UPDATE — deeper cause confirmed (2026-06-02)

The 4 topics' .md SOURCES are empty stubs (~70 chars: title + "Auto-created
by Knowledge OS Obsidian Sync"). Knowledge OS auto-creates shell notes that
were never filled. Chain: empty stub -> converter.py makes ~no _TTS.txt ->
exact-path miss -> OLD glob grabbed stale audio. The glob bug MASKED missing
source content.

gen_tts_staging.py glob fallback now removed (fails loud) — these would now
ERROR instead of producing wrong audio. Correct.

### Corrected fix path
1. Cannot regenerate — no source content exists. Author real content for:
   mcp_protocol, env_management, llm_data_pipelines, knowledge_graph_design
   (in C:\BRAIN_OS\02_PROJECTS\knowledge_os\*.md).
2. THEN run gen_tts_staging.py per topic -> transcribe_batch.py -> verify
   with transcript_integrity.py.
3. Trash the 4 mislabeled duplicate transcripts only AFTER real audio exists
   (env_management, llm_data_pipelines, lancedb, mcp_protocol .json).
4. AUDIT: how many other Knowledge-OS auto-created stubs are empty? Run a
   body-length check across 02_PROJECTS\knowledge_os\*.md — any near-empty
   stub is a topic with no real content and will fail TTS.
---

## SCOPE CORRECTION — systemic empty stubs (2026-06-02)

Stub audit of 02_PROJECTS\knowledge_os\*.md: ~75 of ~78 topics are EMPTY
stubs (58-80 body chars: title + "Auto-created by Knowledge OS"). Only 4
have real content: whisper_gpu_analysis, brain_notes, rag_chapter,
read_along_app_build_session.

Implication: the transcript mismatch was a symptom of a much larger gap —
the Knowledge OS SOURCE LAYER is almost entirely unwritten. Knowledge OS
auto-creates topic shells; content was never authored. The 4 bad transcripts
are just the stubs where the (now-fixed) glob grabbed stale audio.

This is a CONTENT project, not a code fix. Real path:
1. Decide which topics matter (don't author all 75 blindly — prioritize by
   what you actually study / need narrated).
2. Author content per chosen topic in its .md.
3. Generate audio (gen_tts_staging now fails loud on empty input - good).
4. Verify with transcript_integrity.py.

Code side is DONE: glob bug fixed, can no longer mask empty sources.
---

## QUEUE — link-aware rename (brain-os, 2026-06-02)

cleanup_proposer checks CODE refs but not WIKI-LINK refs. In the vault,
wiki-links are a real dependency. Two files need rename + link rewrite:
  Twitter_API_v2.md           -> twitter-api.md            (3 inbound links)
  SESSION_COMPILE_TEMPLATE_V2 -> session-compile-template  (4 inbound links)
Build a link-aware rename: rename file AND rewrite [[old]] -> [[new]] in all
linking notes, atomically. Until then, do NOT rename linked vault files
(would create dead links). CristianConstruction_OLD already renamed (0 links).
---

## QUEUE — consolidate MCP duplicate (migration, 2026-06-02)

mcp_protocol and model_context_protocol are the same concept. model_context_protocol
is machine-key (referenced by drive_index.json, knowledge_os.html, drive_browser.py,
drive_download.py) so cannot be trashed without a migration. Both now have content
(not byte-identical, to avoid integrity-flag). To consolidate: pick one canonical key,
update all 4+ references, then trash the other. Deferred - touches live app.
---

## QUEUE — remaining transcript duplicates (2026-06-03)

After Tier 1 regen, 2 duplicate pairs remain, both machine-key (app-referenced
via drive_index.json, knowledge_os.html) so NOT trashable:

1. llm_data_pipelines == bdf_knowledge_build_flow
   llm_data_pipelines is an unwritten stub showing bdf content. FIX: author
   real llm_data_pipelines content (Tier 2), regenerate audio, transcribe.

2. lancedb == lancedb_vector_store (+ lancedb_vector_store_audio)
   Same LanceDB content under multiple keys, all app-wired. FIX: consolidate
   to one canonical key, update refs, trash others. Migration - touches app.

Tier 1 (12 topics) COMPLETE: authored, audio regenerated with fixed converter
(frontmatter strip now covers .md AND .txt path), transcribed clean, copied to
app transcripts/. Integrity: 4 dup sets -> 2, mismatch list shrank.
---

## QUEUE — verify GitHub remote wiring (2026-06-03)

User flagged: GitHub remotes may not be correctly wired to the system
architecture. Audit each repo's remote (BRAIN_OS, soccer-content-generator,
read-along-app, brain-audio, book-compiler, resolve-mcp-server): confirm
git remote -v points to correct TititoBuilder repo, branches track properly,
nothing pushing to wrong place. Separate from routine commits. Own session.
---

## QUEUE — clean existing duplicate auto-blocks (2026-06-03)

compile_session.py idempotency fix is IN (future dupes stopped). Existing
stacked blocks remain in ~12 files but are now STATIC (not growing). Cleanup
needs PER-FILE judgment, not batch:
- Pure-duplicate files (whisper_gpu_analysis: 6 identical 42x blocks) -> collapse
  to authored top content.
- MIXED files (Cristian_Principles: blocks 1-2 dupe "Build the Loop" but block 3
  is a DISTINCT real principle "never start without feeding context") -> dedup
  carefully, KEEP unique blocks. Do NOT blind-strip - would lose real content.
Cristian_Principles is canonical/highest-stakes - hand-verify.
Affected (worst first): QA_Notes_2026-05-28, whisper_gpu_analysis, rag_chapter,
Daily_Log_2026-04-28, soccer-content-generator.context, fingerprinting,
Cristian_Principles, brain_notes, brain-audio, Read_Along_App.
---

## QUEUE — clean existing duplicate auto-blocks (2026-06-03)

compile_session.py idempotency fix is IN (future dupes stopped). Existing
stacked blocks remain in ~12 files but are now STATIC (not growing). Cleanup
needs PER-FILE judgment, not batch:
- Pure-duplicate files (whisper_gpu_analysis: 6 identical 42x blocks) -> collapse
  to authored top content.
- MIXED files (Cristian_Principles: blocks 1-2 dupe "Build the Loop" but block 3
  is a DISTINCT real principle "never start without feeding context") -> dedup
  carefully, KEEP unique blocks. Do NOT blind-strip - would lose real content.
Cristian_Principles is canonical/highest-stakes - hand-verify.
Affected (worst first): QA_Notes_2026-05-28, whisper_gpu_analysis, rag_chapter,
Daily_Log_2026-04-28, soccer-content-generator.context, fingerprinting,
Cristian_Principles, brain_notes, brain-audio, Read_Along_App.