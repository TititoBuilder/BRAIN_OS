# Ingestion Flags — 2026-08-26_2047_ca_brain_os.md
Generated: 2026-08-26 20:48
Items: 3

---

## Flag 1 of 3 — CONFLICT [MEDIUM]

**Description:** CA_Book ingestion pipeline has no 'processed' stage. Session notes flag this as a gap but it is unclear whether the pipeline spec in CA_Book_System.md or the orchestrator logic in CA_Orchestrator.md needs to be updated, or both.

**Nodes:** 02_PROJECTS/CA_Book_System.md, 02_AGENTS/CA_Orchestrator.md

**Old:** Pipeline stages as currently defined (no 'processed' stage present)

**New:** Pipeline should include a 'processed' stage between ingestion and output/publish

**Suggested resolution:** Review CA_Book_System.md pipeline stages and CA_Orchestrator.md processing logic together; add a 'processed' stage definition to the spec and ensure the orchestrator handles it. May require coordinated update to both nodes.

**Decision:** [ ] Approve  [ ] Modify  [ ] Skip

---

## Flag 2 of 3 — MULTI_NODE [HIGH]

**Description:** 25 harness-mapping findings were surfaced this session and a BRAIN_OS harness draft was added. Resolving these findings will likely require updates across multiple nodes in the knowledge graph, agent definitions, and dashboard spec.

**Nodes:** 02_PROJECTS/graphs/brain-os.context.md, 02_AGENTS/BDF_Memory_Agent.md, 02_PROJECTS/knowledge_os/brain_notes.md, 00_DASHBOARD/DASHBOARD_BUILD_SPEC.md

**Old:** No harness mapping defined for BRAIN_OS

**New:** BRAIN_OS harness draft exists; 25 findings need to be resolved and propagated to relevant nodes

**Suggested resolution:** Do a dedicated harness-mapping review session. Triage the 25 findings by node, group related changes, and process in batches to avoid partial-state corruption across the graph.

**Decision:** [ ] Approve  [ ] Modify  [ ] Skip

---

## Flag 3 of 3 — ARCHITECTURE [MEDIUM]

**Description:** settings.json sandbox was hardened for custom-agent security. This is a security architecture change that may affect how the agent is invoked, what paths/permissions are available, and downstream tool calls. The harness draft depends on the new sandbox boundaries.

**Nodes:** 02_PROJECTS/Custom_Agent_TTS.md, 02_AGENTS/CA_Orchestrator.md

**Old:** settings.json sandbox with prior (looser) security configuration

**New:** Hardened settings.json sandbox — specific constraints TBD from review of actual changes made this session

**Suggested resolution:** Document the new sandbox constraints in Custom_Agent_TTS.md and CA_Orchestrator.md. Confirm that the harness draft is written against the hardened settings, not the old permissive config. Flag any tool calls that previously relied on now-removed permissions.

**Decision:** [ ] Approve  [ ] Modify  [ ] Skip

---
