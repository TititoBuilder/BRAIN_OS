# Ingestion Flags — 2026-05-28_0740_bdf_ca_brain_os.md
Generated: 2026-05-28 09:59
Items: 4

---

## Flag 1 of 4 — MULTI_NODE [HIGH]

**Description:** Knowledge OS Phase 1-3 introduces an encyclopedia + stitcher + Obsidian sync pipeline, a 28-folder Drive structure, and drive_index.json wired to 25 audio-linked topics. This affects at minimum: obsidian_workflows.md (new sync method), OBS_Nav.md (navigation may need new KnowledgeOS section), and all book-compiler nodes that now auto-fingerprint via brain-audio. Full blast radius unclear without source file diffs.

**Nodes:** 02_PROJECTS/knowledge_os/obsidian_workflows.md, 00_NAV/OBS_Nav.md, 02_PROJECTS/Book_Compiler_Shared.md, 02_PROJECTS/CA_Book_System.md, 02_PROJECTS/MCP_Book_System.md

**Old:** Not available — source file diffs not provided in session archive

**New:** Knowledge OS Phase 1-3: encyclopedia generation, audio stitcher, Obsidian sync. Drive: 28 folders, domain isolation. drive_index.json: 25 topics audio-linked.

**Suggested resolution:** Review obsidian_workflows.md and OBS_Nav.md to add Knowledge OS sync section. Audit all book-compiler project nodes (Book_Compiler_Shared, CA_Book_System, MCP_Book_System) to confirm fingerprint integration is documented consistently. Assign human review before bulk update.

**Decision:** [ ] Approve  [ ] Modify  [ ] Skip

---

## Flag 2 of 4 — ARCHITECTURE [HIGH]

**Description:** Steganographic fingerprinting is now auto-applied to every TTS output and verified post-stitch. This is an architectural addition to the audio pipeline — all TTS outputs are now marked at generation time. This changes assumptions in any node that describes audio output format, storage, or integrity guarantees.

**Nodes:** 02_PROJECTS/brain-audio.md, 02_PROJECTS/brain-audio/fingerprinting.md, 02_PROJECTS/Book_Compiler_Shared.md, 02_PROJECTS/CA_Book_System.md

**Old:** TTS outputs generated and stitched without embedded fingerprints

**New:** Every TTS output is auto-fingerprinted via brain-audio (local-SNR FFT steganography) at generation time; master WAV stitch verified for fingerprint integrity post-assembly.

**Suggested resolution:** Update audio pipeline design docs (02_PROJECTS/knowledge_os/audio_pipeline_design.md, audio_formats.md) to note fingerprint embedding as a standard step. Confirm CA_Book_System and Book_Compiler_Shared explicitly document the fingerprint dependency on brain-audio module.

**Decision:** [ ] Approve  [ ] Modify  [ ] Skip

---

## Flag 3 of 4 — CROSS_DOMAIN [MEDIUM]

**Description:** The steganographic fingerprint module (brain-audio domain) now intersects with Knowledge OS audio pipeline knowledge nodes. The local-SNR FFT technique is a cross-domain concept touching audio engineering, security/integrity, and the TTS pipeline. These knowledge nodes may need to reference the fingerprinting implementation.

**Nodes:** 02_PROJECTS/knowledge_os/audio_pipeline_design.md, 02_PROJECTS/knowledge_os/audio_formats.md, 02_PROJECTS/knowledge_os/audio_manipulation.md, 02_PROJECTS/brain-audio/fingerprinting.md

**Old:** Knowledge OS audio nodes describe pipeline and formats without integrity/fingerprinting layer

**New:** Audio pipeline now includes steganographic fingerprinting step; knowledge nodes should cross-reference brain-audio/fingerprinting.md

**Suggested resolution:** Add a backlink from audio_pipeline_design.md and audio_manipulation.md to fingerprinting.md. Consider adding a brief entry in audio_formats.md about fingerprint-bearing WAV files as a new format concern.

**Decision:** [ ] Approve  [ ] Modify  [ ] Skip

---

## Flag 4 of 4 — ARCHIVAL [LOW]

**Description:** Admin key file was removed from tracking this session. If CLAUDE.md or any API node previously referenced or relied on that key file path, those references are now stale and should be audited or archived.

**Nodes:** 03_APIS/CLAUDE.md

**Old:** Admin key file tracked in repository

**New:** Admin key file removed from tracking (2026-05-28); should be managed via secrets_management workflow only

**Suggested resolution:** Review CLAUDE.md and any secrets_management / env_security knowledge nodes to confirm no stale references to the removed admin key file. If the file was a local secret, confirm .gitignore entry is present and document the removal in env_security.md.

**Decision:** [ ] Approve  [ ] Modify  [ ] Skip

---
