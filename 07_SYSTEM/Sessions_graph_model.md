# Sessions Tab — GRAPH MODEL decision (append to Sessions_Tab_Design_Notes.md)

## Key architectural decision (Cristian, confirmed)

The Sessions/Resumes view is GRAPH-SHAPED, not folder-shaped. A resume is a
NODE that can link into MULTIPLE contexts, with the right framing in each —
exactly how Obsidian backlinks work, which is how the whole BRAIN_OS already
thinks.

Example: `trigger_bdf_queue_check`
  - appears in  GRAPH > Triggers      (the general, reusable trigger architecture)
  - appears in  BDF > Automation      (the project-specific cross-reference)
  Same underlying node, two contexts. NOT duplicated — linked.

This means: one resume -> MANY (group, role) relationships, not one project tag.

## Conceptual correction that drove this

- BRAIN_OS is NOT a project. It is the GRAPH / vault layer — the .md files that
  hold architecture, principles, procedures, and the connective tissue the AI
  reads to operate across everything.
- PROJECTS are the things built: BDF, CA, Read-Along, resolve-mcp-server,
  obs-mcp-server (authoritative list = C:\Users\titit\Projects\ + BDF at
  soccer-content-generator + CA at C:\Knowledge\CA / C:\Dev\CristianConstruction).
- So resumes split into: PROJECT resumes (per project) + SYSTEM/GRAPH docs
  (principles, protocols, triggers, control) — and graph nodes can surface in
  BOTH (the trigger example above).

## Authoritative taxonomy = the filesystem, not keywords

Let actual project directories BE the taxonomy. Confirmed projects on disk:
  C:\Users\titit\Projects\  -> obs-mcp-server, read-along-app, resolve-mcp-server
  + BDF (soccer-content-generator), CA (Knowledge\CA / Dev\CristianConstruction)
The session_close.py _PROJECT_KEYWORDS were a useful proxy but the filesystem
is ground truth.

## Resume -> context mapping (31 resumes, from the live audit)

PROJECT: BDF (8): bdf_agent_pipeline, bdf_book_system, bdf_knowledge_build_flow,
  bdf_memory_agent, bdf_video_production_flow, content_orchestrator,
  data_orchestrator, video_orchestrator
PROJECT: CA (2): ca_book_system, cristian_construction
PROJECT: Read-Along (3): read_along_app_arch, read_along_app_session,
  read_along_app_build_session
PROJECT: resolve-mcp-server (3): davinci_resolve_mcp, resolve_mcp_server,
  resolve_editing_agent   (filesystem confirms these are ONE project, not MCP-vs-Resolve)
PROJECT: obs-mcp-server (0): exists on disk, no resume yet

SYSTEM/GRAPH (the meta-layer): active_environments, cristian_principles,
  knowledge_ingestion_protocol, master_control, memory_index, project_directory,
  session_protocol, tools_registry, mcp_registry, ai_engineering, creative_systems,
  trigger_architecture, trigger_render_complete, trigger_session_close,
  trigger_bdf_queue_check

CROSS-CONTEXT (live in Graph AND a project):
  - trigger_bdf_queue_check : Graph>Triggers + BDF>Automation
  - (pattern applies to any general mechanism that also serves a specific project)

## Build implications (future focused session)

1. DATA MODEL: a resume needs MULTIPLE (context, role) links, not a single
   project field. Likely a small relations file the backend reads:
   { machine_key: [ {context:"BDF", role:"automation"},
                    {context:"Graph", role:"trigger-architecture"} ] }
   Do NOT pollute obsidian_sync (these are resumes/graph docs, not learning topics).
2. Mirror how the vault already links nodes — reuse existing backlink data if
   the source .md files already cross-reference (CHECK: do the 07_SYSTEM /
   project .md files already have [[links]] that encode these relationships?).
3. BACKEND: expose type="resume" + contexts[] for these entries.
4. FRONTEND: graph-style view — a resume can render under multiple group
   headers; show it as linked, not duplicated (subtle "also in: X" marker).
5. Source/regeneration: converter.py -> tts_local.py (af_heart) from the
   07_SYSTEM / project .md docs; resumes are regeneratable, not static.

## Open question for build session
- Are the cross-context relationships ALREADY encoded as [[backlinks]] in the
  source .md files? If yes, derive contexts[] from the graph automatically
  (single source of truth, DRY) rather than hand-maintaining a relations file.
  THIS IS THE FIRST THING TO CHECK — it may make the data model nearly free.
