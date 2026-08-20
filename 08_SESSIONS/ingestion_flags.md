# Ingestion Flags — 2026-08-19_1822_bdf_ca_brain_os.md
Generated: 2026-08-19 18:23
Items: 4

---

## Flag 1 of 4 — FINANCIAL [HIGH]

**Description:** Gig tracker Jul 20–Aug 2 base pay is double-counted by $635.53. This is a confirmed financial data error flagged during the session.

**Nodes:** 02_PROJECTS/gig_tracker/Financial Position.md, 02_PROJECTS/gig_tracker/Daily Operating Procedure.md, 02_PROJECTS/gig_tracker/00 Gig Tracker MOC.md

**Old:** Jul 20–Aug 2 base pay as currently recorded (includes erroneous $635.53 double-count)

**New:** Jul 20–Aug 2 base pay corrected by subtracting $635.53 from the double-counted line

**Suggested resolution:** Audit Financial Position.md to locate the double-counted base pay entry for Jul 20–Aug 2, subtract $635.53 from the affected total, and verify the corrected figure against Daily Operating Procedure.md records. Confirm before writing.

**Decision:** [ ] Approve  [ ] Modify  [ ] Skip

---

## Flag 2 of 4 — ARCHIVAL [MEDIUM]

**Description:** Session deleted: duplicate KNOWLEDGE_OS_MANUAL (07_SYSTEM canonical), 8 duplicate docs (00_NAV and 07_SYSTEM canonical), 5 CRLF duplicate compiles, and merged 08_TEMPLATES into 06_TEMPLATES. Archival README should reflect these deletions. Also, audio nodes were added for lesson_10 and lesson_11 but no archival record exists.

**Nodes:** 02_PROJECTS/_archive/README.md, 02_PROJECTS/knowledge_os/lesson_10_os_fundamentals.md, 02_PROJECTS/knowledge_os/lesson_11_acid_transactions.md

**Old:** Archive README does not reflect 2026-08-19 bulk deletions

**New:** Archive README updated with: KNOWLEDGE_OS_MANUAL (duplicate, 07_SYSTEM canonical), 8 duplicate nav/system docs, 5 CRLF duplicate compiles, 08_TEMPLATES merged into 06_TEMPLATES — all 2026-08-19

**Suggested resolution:** Update 02_PROJECTS/_archive/README.md to log all deleted duplicates from this session with dates and canonical paths. Verify lesson_10 and lesson_11 audio node references are recorded in the appropriate audio pipeline docs.

**Decision:** [ ] Approve  [ ] Modify  [ ] Skip

---

## Flag 3 of 4 — MULTI_NODE [MEDIUM]

**Description:** Manifest was expanded to cover all 12 repos (added gig_tracker, book-compiler, custom-agent, obs-mcp-server, cc-landing). The artifact registry was added with a new schema. .context.md resolution is now wired through the manifest. These changes touch the brain-os context graph, the operations status, the queue, and potentially MCP docs — 4+ nodes need coordinated updates.

**Nodes:** 02_PROJECTS/graphs/brain-os.context.md, 02_PROJECTS/BDF_Operations_Status.md, 00_DASHBOARD/Queue.md, 02_PROJECTS/knowledge_os/model_context_protocol.md

**Old:** Manifest covered 8 repos (pre-session)

**New:** Manifest covers 12 repos: includes gig_tracker, book-compiler, custom-agent, obs-mcp-server, cc-landing added 2026-08-19

**Suggested resolution:** Update brain-os.context.md to list all 12 manifest repos. Verify BDF_Operations_Status.md reflects the expanded manifest. Clear any queue items related to manifest expansion. Confirm MCP docs don't need manifest-path references updated.

**Decision:** [ ] Approve  [ ] Modify  [ ] Skip

---

## Flag 4 of 4 — MULTI_NODE [LOW]

**Description:** Session logged 5 flags related to compiler map and three copy-then-diverge folder pairs. These are structural issues across the book compiler ecosystem that require human review before any merging or deduplication.

**Nodes:** 02_PROJECTS/knowledge_os/compiler_map.md, 02_PROJECTS/Book_Compiler_Shared.md, 02_PROJECTS/BDF_Book_System.md, 02_PROJECTS/CA_Book_System.md, 02_PROJECTS/MCP_Book_System.md

**Old:** Compiler map and folder pairs in undocumented diverged state

**New:** Pending human review: 5 compiler-map flags logged 2026-08-19 covering three copy-then-diverge folder pairs

**Suggested resolution:** Review the 5 flagged compiler-map issues. Identify which folder pairs have diverged and decide whether to merge, keep separate with explicit divergence documentation, or archive one branch. Coordinate changes across book system nodes.

**Decision:** [ ] Approve  [ ] Modify  [ ] Skip

---
