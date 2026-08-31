# Ingestion Flags — 2026-08-30_2050_ca_brain_os.md
Generated: 2026-08-30 20:51
Items: 4

---

## Flag 1 of 4 — ARCHITECTURE [HIGH]

**Description:** Three architectural changes made to the BRAIN_OS scanner system in one session: (1) vault exclusion list unified across both scanners, (2) vault directories now excluded at any path depth (not just top-level), (3) flags staged unconditionally with empty-index guard added. These collectively change scanner behavior and could affect all future ingestion runs.

**Nodes:** 07_SYSTEM/KNOWLEDGE_INGESTION_PROTOCOL_V2.md, 07_SYSTEM/Trigger_Architecture.md, 08_TRIGGERS/Trigger_Session_Close.md

**Old:** Vault exclusion applied at top-level paths only; parse_mode included in Telegram session_close payload; flags staged conditionally.

**New:** Vault exclusion applied at any path depth; parse_mode dropped from Telegram session_close.py payload; flags staged unconditionally with empty-index guard.

**Suggested resolution:** Update KNOWLEDGE_INGESTION_PROTOCOL_V2.md to document the new exclusion behavior and unconditional flag staging. Update Trigger_Session_Close.md to reflect the drop of parse_mode from the Telegram payload. Review Trigger_Architecture.md for any exclusion-path references that need updating.

**Decision:** [ ] Approve  [ ] Modify  [ ] Skip

---

## Flag 2 of 4 — MULTI_NODE [MEDIUM]

**Description:** The git_commit early return was flagged during this session but not resolved. This issue may affect Navigation.md accumulation behavior and should be tracked in the ingestion flags log. Needs decision on whether to fix, defer, or document as known behavior.

**Nodes:** 00_DASHBOARD/Navigation.md, 07_SYSTEM/KNOWLEDGE_INGESTION_PROTOCOL_V2.md, 08_SESSIONS/ingestion_flags.md

**Old:** git_commit early return behavior undocumented.

**New:** git_commit early return identified as causing Navigation.md accumulation; fix deferred or pending dedicated session.

**Suggested resolution:** Add an open item to 08_SESSIONS/ingestion_flags.md for the git_commit early return issue. Determine if it belongs in KNOWLEDGE_INGESTION_PROTOCOL_V2.md as a known limitation or if a fix session should be queued.

**Decision:** [ ] Approve  [ ] Modify  [ ] Skip

---

## Flag 3 of 4 — PROTECTED [HIGH]

**Description:** Protected: Navigation (writer: vault_index.py) - Vault navigation. Derived, auto-committed.

**Nodes:** 00_DASHBOARD/Navigation.md

**New:** Remove any machine-written tail appended by automated processes; retain only human-curated navigation content.

**Suggested resolution:** Apply manually, or choose another target.

**Decision:** [ ] Approve  [ ] Modify  [ ] Skip

---

## Flag 4 of 4 — PROTECTED [HIGH]

**Description:** Protected: ingestion_flags (writer: compile_session.py) - MACHINE-WRITTEN per session. Never hand-edit.

**Nodes:** 08_SESSIONS/ingestion_flags.md

**New:** 2026-08-30: Navigation.md accumulation issue identified and machine-written tail removed. git_commit early return flagged for review.

**Suggested resolution:** Apply manually, or choose another target.

**Decision:** [ ] Approve  [ ] Modify  [ ] Skip

---
