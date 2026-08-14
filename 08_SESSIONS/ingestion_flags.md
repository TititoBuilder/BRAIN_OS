# Ingestion Flags — 2026-08-13_2113_bdf_ca_brain_os.md
Generated: 2026-08-13 21:14
Items: 5

---

## Flag 1 of 5 — MULTI_NODE [HIGH]

**Description:** Two projects (custom-agent and soccer-content-generator) both adopted the .env + pathlib PathConfig pattern this session. This is an architecture-level convention change affecting multiple project nodes and potentially the knowledge_os env docs.

**Nodes:** 02_PROJECTS/Custom_Agent_TTS.md, 02_PROJECTS/graphs/soccer-content-generator.context.md, 02_PROJECTS/knowledge_os/env_management.md, 02_PROJECTS/knowledge_os/environment_variables.md

**Old:** Hardcoded paths in custom-agent and soccer-content-generator configs

**New:** Paths centralized into PathConfig class via .env + pathlib; .env.example added to soccer-content-generator

**Suggested resolution:** Review Custom_Agent_TTS.md and soccer-content-generator.context.md to add refactor notes. Confirm env_management.md and environment_variables.md are consistent and not duplicating guidance. Consider a single canonical 'PathConfig pattern' entry in knowledge_os.

**Decision:** [ ] Approve  [ ] Modify  [ ] Skip

---

## Flag 2 of 5 — MULTI_NODE [HIGH]

**Description:** 11 gig_tracker vault docs were populated this session (Direction 6 complete). Human review required to verify content accuracy across all 11 nodes before treating them as canonical.

**Nodes:** 02_PROJECTS/gig_tracker/00 Gig Tracker MOC.md, 02_PROJECTS/gig_tracker/Codebase Map.md, 02_PROJECTS/gig_tracker/Decision Log.md, 02_PROJECTS/gig_tracker/Financial Position.md, 02_PROJECTS/gig_tracker/Van Decision.md, 02_PROJECTS/gig_tracker/Daily Operating Procedure.md, 02_PROJECTS/gig_tracker/Offer Decision Rules.md, 02_PROJECTS/gig_tracker/Prop 22 Mechanics.md, 02_PROJECTS/gig_tracker/Unapplied - Backlog.md, 02_PROJECTS/gig_tracker/Wage Claim - Spark Underpayment.md, 02_PROJECTS/gig_tracker/Cost Findings.md

**Old:** gig_tracker docs were stubs or unpopulated

**New:** 11 docs populated from Direction 6 gig_tracker import session

**Suggested resolution:** Human should spot-check at least Van Decision.md (van_build rename + is_onetime field), Financial Position.md, and Wage Claim - Spark Underpayment.md for correctness. Confirm MOC links to all 11 files.

**Decision:** [ ] Approve  [ ] Modify  [ ] Skip

---

## Flag 3 of 5 — FINANCIAL [HIGH]

**Description:** Four gig_tracker files contain financial/cost/compensation data (Financial Position, Cost Findings, Wage Claim - Spark Underpayment, Prop 22 Mechanics) that were populated this session. These require human verification before being treated as accurate.

**Nodes:** 02_PROJECTS/gig_tracker/Financial Position.md, 02_PROJECTS/gig_tracker/Cost Findings.md, 02_PROJECTS/gig_tracker/Wage Claim - Spark Underpayment.md, 02_PROJECTS/gig_tracker/Prop 22 Mechanics.md

**Old:** N/A — newly populated

**New:** Financial data populated via Direction 6 import — unverified

**Suggested resolution:** Human must review all four files for numerical accuracy, especially Wage Claim - Spark Underpayment (legal/financial claim) and Financial Position (current balance data). Do not auto-propagate any figures from these files.

**Decision:** [ ] Approve  [ ] Modify  [ ] Skip

---

## Flag 4 of 5 — ARCHITECTURE [MEDIUM]

**Description:** STUDY_SYSTEM was added to BRAIN_OS this session with four layers, a domain map, and a learning principle. This is a structural addition to the OS architecture that may affect how the knowledge_os layer is organized going forward.

**Nodes:** 02_PROJECTS/graphs/brain-os.context.md, 00_DASHBOARD/Queue.md, 02_PROJECTS/knowledge_os/brain_notes.md

**Old:** No explicit STUDY_SYSTEM definition in vault

**New:** STUDY_SYSTEM added: four layers, domain map, learning principle (2026-08-13)

**Suggested resolution:** Confirm STUDY_SYSTEM definition is captured in brain_notes.md or a dedicated file. Verify it does not conflict with existing four-layer architecture described in lesson_02_four_layer_architecture.md.

**Decision:** [ ] Approve  [ ] Modify  [ ] Skip

---

## Flag 5 of 5 — ARCHIVAL [LOW]

**Description:** Directions 1, 2, 6, 7b, 7c, 7d are now complete and should be formally archived out of the active Queue into Queue_Archive. Direction 7e is in-progress and must remain active.

**Nodes:** 00_DASHBOARD/Queue.md, 00_DASHBOARD/Queue_Archive.md

**Old:** Directions 1, 2, 5, 6, 7, 7b, 7c, 7d, 7e listed in active queue

**New:** Directions 1, 2, 6, 7b, 7c, 7d archived; Direction 7e remains active

**Suggested resolution:** Move completed direction entries from Queue.md active section to Queue_Archive.md. Leave Direction 7e (van_build rename / is_onetime / web.py dashboard) in active queue.

**Decision:** [ ] Approve  [ ] Modify  [ ] Skip

---
