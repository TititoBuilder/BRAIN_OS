# Ingestion Flags — 2026-09-04_2157_bdf_ca_brain_os.md
Generated: 2026-09-04 21:58
Items: 7

---

## Flag 1 of 7 — MULTI_NODE [HIGH]

**Description:** All 13 trigger nodes were annotated with 'implemented_by' field this session, and Trigger_Architecture tables are now derived from node frontmatter. This is a coordinated multi-node schema change across the entire triggers layer.

**Nodes:** 08_TRIGGERS/Trigger_Morning_Watchdog.md, 07_SYSTEM/Trigger_Architecture.md, 08_TRIGGERS/Trigger_BDF_Queue_Check.md, 08_TRIGGERS/Trigger_Book_Compile.md, 08_TRIGGERS/Trigger_BrainOS_Daily_Review.md, 08_TRIGGERS/Trigger_Clip_Detected.md, 08_TRIGGERS/Trigger_Daily_Log_Update.md, 08_TRIGGERS/Trigger_Drive_Change_Token.md, 08_TRIGGERS/Trigger_Graph_TTL_Expired.md, 08_TRIGGERS/Trigger_Match_Scheduled.md, 08_TRIGGERS/Trigger_New_Idea.md, 08_TRIGGERS/Trigger_Render_Complete.md, 08_TRIGGERS/Trigger_Script_Ready.md, 08_TRIGGERS/Trigger_Session_Close.md, 08_TRIGGERS/Trigger_Telegram_Message.md

**Old:** Trigger nodes lacked implemented_by frontmatter; Trigger_Architecture tables were manually maintained.

**New:** All 13 trigger nodes annotated with implemented_by; Trigger_Architecture tables now derived from node frontmatter automatically.

**Suggested resolution:** Human review: confirm the implemented_by annotation schema is correct and consistent across all 13 nodes before treating as canonical. Update Trigger_Architecture.md to reflect the new derivation approach.

**Decision:** [ ] Approve  [ ] Modify  [ ] Skip

---

## Flag 2 of 7 — MULTI_NODE [HIGH]

**Description:** session_compiler.py was split into two tools: distill_session and voice_chapter. voice_chapter.py also now serves as both the drive_index writer and BRAIN_OS_CONFIG reader. This changes the tool registry, tools index, and any project nodes that reference session_compiler.py.

**Nodes:** 07_SYSTEM/Tools_Registry.md, 09_TOOLS/09_TOOLS_INDEX.md, 02_PROJECTS/BDF_Agent_Pipeline.md

**Old:** session_compiler.py — monolithic tool handling session compilation, drive index writing, and config reading.

**New:** distill_session.py — session compilation. voice_chapter.py — drive_index writer and BRAIN_OS_CONFIG reader.

**Suggested resolution:** Update Tools_Registry.md and 09_TOOLS_INDEX.md to remove session_compiler.py and register distill_session and voice_chapter. Audit any project/workflow nodes that reference session_compiler.py and update their references.

**Decision:** [ ] Approve  [ ] Modify  [ ] Skip

---

## Flag 3 of 7 — ARCHITECTURE [MEDIUM]

**Description:** The manifest was extended with four new fields (bucket, status, context_kind, claude_md) across all 12 projects, making the manifest load-bearing and adding manifest_check as a validation gate. This is an architecture change to the project manifest schema.

**Nodes:** 07_SYSTEM/Master_Control.md, 02_PROJECTS/BDF_Agent_Pipeline.md

**Old:** Manifest fields: (previous schema without bucket, status, context_kind, claude_md)

**New:** Manifest fields: bucket, status, context_kind, claude_md added to all 12 project entries; manifest_check tool validates before load.

**Suggested resolution:** Review and confirm the new manifest schema fields. Update any manifest-reading tools or documentation that describes the manifest structure. Ensure manifest_check is wired into the session-start or CI flow.

**Decision:** [ ] Approve  [ ] Modify  [ ] Skip

---

## Flag 4 of 7 — CONFLICT [MEDIUM]

**Description:** The session notes that 08_SESSIONS has two naming conventions (e.g. YYYYMMDD_session_compile_* vs YYYY-MM-DD_HHMM_*). This is an unresolved naming inconsistency in the sessions layer.

**Nodes:** 08_SESSIONS/2026-09-04_2157_bdf_ca_brain_os.md

**Old:** 08_SESSIONS contains files with two naming conventions: YYYYMMDD_session_compile_* and YYYY-MM-DD_HHMM_*

**New:** Proposed: standardize on YYYY-MM-DD_HHMM_<tags>.md; archive or alias legacy files.

**Suggested resolution:** Decide on a single naming convention for 08_SESSIONS. Migrate legacy files to the chosen pattern or document the two-convention coexistence explicitly in the Naming_Contract.md.

**Decision:** [ ] Approve  [ ] Modify  [ ] Skip

---

## Flag 5 of 7 — ARCHIVAL [LOW]

**Description:** SYSTEM_Rules.md was moved from 00_NAV to 07_SYSTEM (closes queue item 153). Any nav files or indexes that previously linked to 00_NAV/SYSTEM_Rules.md will have broken references.

**Nodes:** 07_SYSTEM/SYSTEM_Rules.md, 00_NAV/OBS_Nav.md

**Old:** SYSTEM_Rules.md located at 00_NAV/SYSTEM_Rules.md

**New:** SYSTEM_Rules.md relocated to 07_SYSTEM/SYSTEM_Rules.md

**Suggested resolution:** Search vault for links to 00_NAV/SYSTEM_Rules.md and update them to 07_SYSTEM/SYSTEM_Rules.md. Confirm Queue item 153 is marked closed in 00_DASHBOARD/Queue.md.

**Decision:** [ ] Approve  [ ] Modify  [ ] Skip

---

## Flag 6 of 7 — PROTECTED [HIGH]

**Description:** Protected: 07_SYSTEM is a dashboard or doctrine directory

**Nodes:** 07_SYSTEM/SYSTEM_Rules.md

**New:** <!-- Moved from 00_NAV to 07_SYSTEM 2026-09-04, closes queue item 153 -->

**Suggested resolution:** Apply manually, or choose another target.

**Decision:** [ ] Approve  [ ] Modify  [ ] Skip

---

## Flag 7 of 7 — PROTECTED [HIGH]

**Description:** Protected: TOOLS_INDEX (writer: tools_index.py) - Script index from docstrings. Derived, auto-committed.

**Nodes:** 09_TOOLS/09_TOOLS_INDEX.md

**New:** <!-- 2026-09-04: Removed generated date field — caused every run to dirty the tree. Tools added this session: manifest_check. session_compiler.py split into distill_session and voice_chapter. -->

**Suggested resolution:** Apply manually, or choose another target.

**Decision:** [ ] Approve  [ ] Modify  [ ] Skip

---
