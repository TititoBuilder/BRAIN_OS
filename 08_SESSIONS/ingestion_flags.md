# Ingestion Flags — 2026-05-28_2041_bdf_ca_brain_os.md
Generated: 2026-05-28 20:42
Items: 3

---

## Flag 1 of 3 — ARCHITECTURE [HIGH]

**Description:** Knowledge OS Drive structure established with 28 folders and domain isolation. drive_index.json wired to 25 audio-linked topics. This is a significant architecture change affecting how the entire Knowledge OS stores, retrieves, and links audio content to knowledge nodes. The fix to drive_index (using file IDs for BRAIN_OS_Vault entries) may change how all vault references resolve.

**Nodes:** 02_PROJECTS/knowledge_os/api_gateway_design.md, 02_PROJECTS/knowledge_os/cloud_storage_apis.md, 02_PROJECTS/knowledge_os/audio_pipeline_design.md, 02_PROJECTS/knowledge_os/knowledge_graph_design.md, 00_NAV/SYSTEM_Rules.md

**Old:** drive_index uses path-based references for BRAIN_OS_Vault entries

**New:** drive_index uses file IDs for BRAIN_OS_Vault entries; 28-folder Knowledge OS Drive structure with domain isolation; 25 topics audio-linked via drive_index.json

**Suggested resolution:** Human review needed: (1) Confirm 28-folder Drive structure is canonical and document folder names/domains in knowledge_graph_design.md or a new drive_structure.md node. (2) Verify drive_index.json file-ID fix does not break existing audio links. (3) Update SYSTEM_Rules.md if the file-ID convention is now a hard rule for all vault entries.

**Decision:** [ ] Approve  [ ] Modify  [ ] Skip

---

## Flag 2 of 3 — MULTI_NODE [HIGH]

**Description:** 22 vault audio nodes added to dropdown + read_along_app_session audio node added + audio_staging binaries excluded from git. This touches audio pipeline, TTS, brain-audio, and staging infrastructure across 6+ nodes simultaneously. The git exclusion of audio_staging binaries is an infrastructure decision that affects all projects using that path.

**Nodes:** 02_PROJECTS/knowledge_os/audio_pipeline_design.md, 02_PROJECTS/knowledge_os/audio_formats.md, 02_PROJECTS/knowledge_os/audio_manipulation.md, 02_PROJECTS/Custom_Agent_TTS_Audio.md, 02_PROJECTS/brain-audio.md, 02_AGENTS/CA_Kokoro_TTS.md

**Old:** audio_staging binaries tracked in git; vault audio dropdown had fewer nodes

**New:** audio_staging binaries excluded from git; 22 vault audio nodes + read_along_app_session added to dropdown

**Suggested resolution:** Review and update audio_pipeline_design.md with the new vault audio node inventory (22 nodes listed). Confirm audio_staging exclusion is documented in brain-audio.md or a .gitignore note. Verify CA_Kokoro_TTS and Custom_Agent_TTS_Audio are consistent with the new audio node structure.

**Decision:** [ ] Approve  [ ] Modify  [ ] Skip

---

## Flag 3 of 3 — CROSS_DOMAIN [MEDIUM]

**Description:** soccer-content-generator (separate project domain) had a session close and brain sync on 2026-05-27 included in this BRAIN_OS session archive. Cross-domain sync means soccer project state is embedded in BRAIN_OS memory index. Need to ensure soccer project context graph is updated independently and not conflated with BRAIN_OS ingestion.

**Nodes:** 02_PROJECTS/graphs/soccer-content-generator.context.md, 02_PROJECTS/knowledge_os/brain_notes.md, 05_MEMORY/Memory_Index.md

**Old:** soccer-content-generator context graph last updated prior to 2026-05-27

**New:** soccer-content-generator session close 2026-05-27 + brain sync 2026-05-27 completed

**Suggested resolution:** Update 02_PROJECTS/graphs/soccer-content-generator.context.md with 2026-05-27 session close note. Verify soccer-content-generator has its own session log and that BRAIN_OS memory index only holds a cross-reference pointer, not the full soccer state.

**Decision:** [ ] Approve  [ ] Modify  [ ] Skip

---
