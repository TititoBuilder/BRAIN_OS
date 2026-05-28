# Ingestion Flags — 2026-05-28_0740_bdf_ca_brain_os.md
Generated: 2026-05-28 10:07
Items: 3

---

## Flag 1 of 3 — MULTI_NODE [HIGH]

**Description:** Knowledge OS Phase 1-3 feature (encyclopedia, stitcher, obsidian sync) touches multiple nodes simultaneously: Knowledge OS internal nodes, soccer-content-generator context graph (brain sync), Read-Along App context graph, Memory Index (new audio-linked topics), and Dashboard Queue. The drive_index.json wiring (25 topics audio-linked, 28 Drive folders) is a structural change affecting how the entire knowledge system delivers content.

**Nodes:** 02_PROJECTS/knowledge_os/brain_notes.md, 02_PROJECTS/OBS_MCP_Server.md, 02_PROJECTS/graphs/soccer-content-generator.context.md, 02_PROJECTS/graphs/read-along-app.context.md, 05_MEMORY/Memory_Index.md, 00_DASHBOARD/Queue.md

**Old:** No prior Knowledge OS Phase 1-3 record in vault

**New:** Knowledge OS Phase 1-3 complete: encyclopedia builder (28 Drive folders, domain isolation), audio stitcher, obsidian sync. drive_index.json wired — 25 topics audio-linked. User manual documented.

**Suggested resolution:** Review Knowledge OS Phase 1-3 scope fully before propagating. Update Memory_Index.md to reflect 25 new audio-linked topics. Update Queue.md to clear or advance Knowledge OS tasks. Confirm drive_index.json schema is stable before marking nodes as dependent on it. Consider a dedicated Knowledge_OS_Phase1-3.md project node to anchor cross-links.

**Decision:** [ ] Approve  [ ] Modify  [ ] Skip

---

## Flag 2 of 3 — ARCHITECTURE [HIGH]

**Description:** Auto-fingerprinting every TTS output via brain-audio is an architectural change to the book-compiler and TTS pipeline. Every audio file produced by CA_Kokoro_TTS will now be fingerprinted at generation time, and integrity is verified post-stitch. This changes the data contract for any downstream consumer of TTS audio (Read-Along App, CA Book System, etc.) and introduces a new mandatory processing step.

**Nodes:** 02_PROJECTS/brain-audio.md, 02_PROJECTS/brain-audio/fingerprinting.md, 02_PROJECTS/Book_Compiler_Shared.md, 02_AGENTS/CA_Kokoro_TTS.md

**Old:** TTS outputs produced as plain WAV files; no fingerprinting step documented

**New:** TTS outputs auto-fingerprinted via brain-audio steganographic module (local-SNR FFT) at generation time. Master WAV stitch followed by integrity verification. All downstream consumers receive fingerprinted audio.

**Suggested resolution:** Confirm the fingerprint module API is stable (embed/verify interface). Update Book_Compiler_Shared.md to document the new mandatory fingerprint step. Update CA_Kokoro_TTS.md to note all outputs are now fingerprinted. Assess whether Read_Along_App.md and CA_Book_System.md need to document fingerprint-awareness.

**Decision:** [ ] Approve  [ ] Modify  [ ] Skip

---

## Flag 3 of 3 — CROSS_DOMAIN [MEDIUM]

**Description:** soccer-content-generator session close + brain sync (2026-05-27) implies state was captured and synced for that project, but the session archive does not include the specific changes made. The context graph node may be stale or updated externally. BDF Operations Status and Agent Pipeline may need to reflect the session close state.

**Nodes:** 02_PROJECTS/graphs/soccer-content-generator.context.md, 02_PROJECTS/BDF_Operations_Status.md, 02_PROJECTS/BDF_Agent_Pipeline.md

**Old:** Unknown — prior state of soccer-content-generator context graph not provided

**New:** Session closed 2026-05-27; brain sync committed. Context graph updated.

**Suggested resolution:** Pull the actual 2026-05-27 soccer-content-generator brain sync diff and ingest it separately. Verify BDF_Operations_Status.md reflects current pipeline state. If no substantive changes were made beyond the session close commit, this can be marked low-priority.

**Decision:** [ ] Approve  [ ] Modify  [ ] Skip

---
