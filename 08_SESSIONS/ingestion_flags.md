# Ingestion Flags — 2026-09-04_2157_bdf_ca_brain_os.md
Generated: 2026-09-04 21:59
Items: 9

---

## Flag 1 of 9 — CONFLICT [MEDIUM]

**Description:** Session log notes 08_SESSIONS has two coexisting naming conventions (YYYYMMDD vs YYYY-MM-DD_HHMM). This is an unresolved conflict in vault naming standards.

**Nodes:** 08_SESSIONS/ingestion_flags.md, 07_SYSTEM/Naming_Contract.md

**Old:** Mixed: 20260315_session_compile_story_kling.md and 2026-09-04_2157_bdf_ca_brain_os.md both exist in 08_SESSIONS

**New:** Standardize on YYYY-MM-DD_HHMM_tags.md for all session files; archive or rename legacy YYYYMMDD files

**Suggested resolution:** Decide on one canonical naming convention for 08_SESSIONS, document it in Naming_Contract.md, and schedule a rename pass for non-conforming files. Recommend YYYY-MM-DD_HHMM_tags.md as it matches the majority of recent session files.

**Decision:** [ ] Approve  [ ] Modify  [ ] Skip

---

## Flag 2 of 9 — MULTI_NODE [MEDIUM]

**Description:** session_compiler.py was split into distill_session and voice_chapter this session. References to session_compiler.py likely exist in multiple vault nodes (tools index, BDF ops status, possibly workflow docs) and all need updating to reflect the new split.

**Nodes:** 07_SYSTEM/Tools_Registry.md, 09_TOOLS/09_TOOLS_INDEX.md, 02_PROJECTS/BDF_Operations_Status.md

**Old:** session_compiler.py — monolithic tool handling session compilation and voice chapter generation

**New:** distill_session — handles session distillation; voice_chapter — handles voice chapter generation and owns drive_index writer + BRAIN_OS_CONFIG reader

**Suggested resolution:** Search vault for 'session_compiler' references and update each to point to the correct successor tool (distill_session or voice_chapter depending on context). Flag here because this touches 3+ files.

**Decision:** [ ] Approve  [ ] Modify  [ ] Skip

---

## Flag 3 of 9 — ARCHITECTURE [LOW]

**Description:** Trigger_Architecture tables are now derived from node frontmatter rather than maintained manually. This is a pipeline/generation architecture change that affects how the Trigger_Architecture doc is maintained going forward.

**Nodes:** 07_SYSTEM/Trigger_Architecture.md, 08_TRIGGERS/Trigger_Morning_Watchdog.md

**Old:** Trigger_Architecture tables maintained manually

**New:** Trigger_Architecture tables derived from node frontmatter `implemented_by` field — do not hand-edit

**Suggested resolution:** Document the new generation approach in Trigger_Architecture.md — note that the table is auto-derived from frontmatter `implemented_by` fields and should not be hand-edited. Add a warning comment at the top of the file.

**Decision:** [ ] Approve  [ ] Modify  [ ] Skip

---

## Flag 4 of 9 — PROTECTED [HIGH]

**Description:** Protected: Tools_Registry (writer: soccer-content-generator/sync_brain.py) - Check before adopting any new tool.

**Nodes:** 07_SYSTEM/Tools_Registry.md

**New:** - `manifest_check` — validates manifest before it becomes load-bearing (added this session)
- `distill_session` — extracted from session_compiler.py split
- `voice_chapter` — extracted from session_compiler.py split; also owns drive_index writer and BRAIN_OS_CONFIG reader

**Suggested resolution:** Apply manually, or choose another target.

**Decision:** [ ] Approve  [ ] Modify  [ ] Skip

---

## Flag 5 of 9 — PROTECTED [HIGH]

**Description:** Protected: TOOLS_INDEX (writer: tools_index.py) - Script index from docstrings. Derived, auto-committed.

**Nodes:** 09_TOOLS/09_TOOLS_INDEX.md

**New:** Generated date field removed — it caused every run to dirty the tree.

**Suggested resolution:** Apply manually, or choose another target.

**Decision:** [ ] Approve  [ ] Modify  [ ] Skip

---

## Flag 6 of 9 — PROTECTED [HIGH]

**Description:** Protected: 07_SYSTEM is a dashboard or doctrine directory

**Nodes:** 07_SYSTEM/SYSTEM_Rules.md

**New:** Moved from 00_NAV to 07_SYSTEM this session. Closes queue item 153.

**Suggested resolution:** Apply manually, or choose another target.

**Decision:** [ ] Approve  [ ] Modify  [ ] Skip

---

## Flag 7 of 9 — PROTECTED [HIGH]

**Description:** Protected: 07_SYSTEM is a dashboard or doctrine directory

**Nodes:** 07_SYSTEM/Trigger_Architecture.md

**New:** All 13 trigger nodes annotated with `implemented_by` frontmatter field. Trigger_Architecture tables now derived from node frontmatter rather than maintained manually.

**Suggested resolution:** Apply manually, or choose another target.

**Decision:** [ ] Approve  [ ] Modify  [ ] Skip

---

## Flag 8 of 9 — PROTECTED [HIGH]

**Description:** Protected: Navigation (writer: vault_index.py) - Vault navigation. Derived, auto-committed.

**Nodes:** 00_DASHBOARD/Navigation.md

**New:** - 2026-09-04 21:57 — BDF, CA, BRAIN_OS — manifest fields, trigger annotations, tool split, vault housekeeping

**Suggested resolution:** Apply manually, or choose another target.

**Decision:** [ ] Approve  [ ] Modify  [ ] Skip

---

## Flag 9 of 9 — PROTECTED [HIGH]

**Description:** Protected: ingestion_flags (writer: ingest_session.py) - MACHINE-WRITTEN per session. Never hand-edit.

**Nodes:** 08_SESSIONS/ingestion_flags.md

**New:** Closed this session:
- Manifest refresh — verified
- Hardcoded default — verified
- Tool names — verified
- MSIX flag — closed as misdiagnosis

Added this session:
- C:/AI purpose unrecoverable; 08_SESSIONS has two naming conventions (needs resolution)
- PAT rotation: a probe during rotation proves nothing

**Suggested resolution:** Apply manually, or choose another target.

**Decision:** [ ] Approve  [ ] Modify  [ ] Skip

---
