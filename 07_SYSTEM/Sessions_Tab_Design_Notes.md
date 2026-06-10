# Sessions / Project Resumes — Design Notes (TRACED, not yet built)

**Status:** AUDIT COMPLETE. Design + build deferred to a focused session.
**Origin:** While closing Queue [2], the 31 "uncategorized" topics were
identified as project audio-resumes, not failed learning topics — a distinct
content type. This documents the trace so the future build starts informed.

---

## What the 31 "uncategorized" entries actually are

NOT learning topics. They are narrated audio summaries of BRAIN_OS system
internals and per-project state. They cluster cleanly:

- Protocols / Control (9): active_environments, knowledge_ingestion_protocol,
  master_control, memory_index, project_directory, read_along_app_build_session,
  read_along_app_session, session_protocol, tools_registry
- Project / Identity Docs (6): ai_engineering, ca_book_system, creative_systems,
  cristian_construction, cristian_principles, read_along_app_arch
- BDF (5): bdf_agent_pipeline, bdf_book_system, bdf_knowledge_build_flow,
  bdf_memory_agent, bdf_video_production_flow
- MCP / Resolve (4): davinci_resolve_mcp, mcp_registry, resolve_editing_agent,
  resolve_mcp_server
- Triggers (4): trigger_architecture, trigger_bdf_queue_check,
  trigger_render_complete, trigger_session_close
- Orchestrators (3): content_orchestrator, data_orchestrator, video_orchestrator

They are indexed (id: entries, playable) but have no knowledge_os_domain —
which is correct: they are not learning-OS topics.

---

## Pipeline trace (what makes/handles sessions)

Two scripts named, both audited — both are TEXT side, neither makes audio:

- session_close.py  — "Session Compiler." Captures session work, writes a dated
  .md archive to 08_SESSIONS, optional Telegram. Has --project flag +
  _PROJECT_KEYWORDS map: {BDF, CA, BRAIN_OS, MCP, Resolve}. **Already categorizes
  sessions by project.**
- compile_session.py — "Option C Knowledge Ingestion." Reads latest archive,
  runs Knowledge Ingestion Protocol V2, updates graph, git commits. Text only.

NEITHER generates audio and NEITHER writes to Drive. The 31 audio resumes came
from a SEPARATE audio pass (Kokoro TTS over project/session docs → uploaded to
Drive). **That audio-generation pipeline is NOT yet identified — first task of
the build session is to find it** (likely gen_tts_staging.py pointed at session
or project markdown).

---

## The design idea (Cristian's intent)

A third content type alongside Learning Paths and Single Topics:
"Sessions" / "Project Resumes" — per-project audio you listen to in order to
stay current on how your own systems work (not to study a subject).

Natural grouping = the EXISTING project taxonomy already in session_close.py
(_PROJECT_KEYWORDS): BDF, CA, BRAIN_OS, MCP, Resolve. Reuse it — do NOT invent
new taxonomy. This is the same DRY principle that made obsidian_sync the single
source for learning domains.

---

## Build plan (future focused session)

1. IDENTIFY the audio-generation pipeline for these resumes (the missing third
   script). Trace what markdown it reads and where it uploads.
2. DECIDE the data source for project-tagging the 31 (mirror _PROJECT_KEYWORDS,
   or add a project field where the backend reads). Avoid polluting obsidian_sync
   (these aren't learning topics).
3. BACKEND: extend /topics (or a new endpoint) to expose type="session" +
   project for these entries.
4. FRONTEND: a Sessions tab (or a third section in LISTEN) grouped by project,
   reusing the Scheme C pattern (collapsible groups, same CSS).
5. The 31 leave "Uncategorized" and become "Sessions, by project."

## Why not now
- New content type = real design work, deserves fresh focus (not session-tail).
- The audio-gen pipeline must be identified first (trace before design).
- Leaving the 31 as Uncategorized is the honest holding state meanwhile —
  they play fine; they're just not yet grouped.

## Related deferred items
- 3 topics need AUTHORING then TTS: edge_tts, kokoro_tts, message_queues
  (no lesson body exists — kokoro/message_queues frontmatter is mis-tagged on
  an agent doc + the Queue.md dashboard; minor data-hygiene note).
- ~21 {key}_audio staging twins: local file-naming residue, harmless, hygiene pass.
