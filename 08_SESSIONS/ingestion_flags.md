# Ingestion Flags — 2026-09-07_1736_bdf_ca_brain_os.md
Generated: 2026-09-07 17:36
Items: 5

---

## Flag 1 of 5 — CONFLICT [HIGH]

**Description:** Session removed stale generic checklist and rewrote session-close procedure in 03_APIS/CLAUDE.md to match actual current flow. Need human review to confirm the removal of the checklist was intentional and the new procedure is correct before auto-applying.

**Nodes:** 03_APIS/CLAUDE.md

**Old:** Generic checklist + outdated session-close procedure (stale content per session notes)

**New:** Corrected session-close procedure matching actual current flow; stale generic checklist removed

**Suggested resolution:** Review the updated 03_APIS/CLAUDE.md to confirm stale checklist removal and corrected session-close procedure are accurate, then mark resolved.

**Decision:** [ ] Approve  [ ] Modify  [ ] Skip

---

## Flag 2 of 5 — CONFLICT [HIGH]

**Description:** Two flags need to be recorded: (1) ingest_session double-run produces non-idempotent results — a systemic BRAIN_OS bug; (2) CA_Book incoming triage finding. These may conflict with or duplicate existing flag entries.

**Nodes:** 08_SESSIONS/ingestion_flags.md

**Old:** Existing flags from prior sessions

**New:** ## 2026-09-07
- [BUG] ingest_session double-run produces non-idempotent results — investigate deduplication logic
- [TRIAGE] CA_Book incoming: CLAUDE.md was missing from harness (second gap); now added

**Suggested resolution:** Append both flags to ingestion_flags.md under a 2026-09-07 section. Flag 1: idempotency bug in ingest_session double-run. Flag 2: CA_Book incoming triage — CLAUDE.md was missing from harness.

**Decision:** [ ] Approve  [ ] Modify  [ ] Skip

---

## Flag 3 of 5 — ARCHITECTURE [MEDIUM]

**Description:** CA registry entry was corrected to point at CA_Book instead of CristianConstruction. This is a registry pointer fix that touches the MCP/system registry and the CA_Book project node — needs human confirmation that all downstream references are also updated.

**Nodes:** 07_SYSTEM/MCP_Registry.md, 02_PROJECTS/CA_Book_System.md

**Old:** CA registry entry → CristianConstruction

**New:** CA registry entry → CA_Book

**Suggested resolution:** Confirm MCP_Registry.md or equivalent registry file now points CA entry to CA_Book_System.md, and audit any other files that reference CristianConstruction as the CA entry point.

**Decision:** [ ] Approve  [ ] Modify  [ ] Skip

---

## Flag 4 of 5 — PROTECTED [HIGH]

**Description:** Protected: Navigation (writer: vault_index.py) - Vault navigation. Derived, auto-committed.

**Nodes:** 00_DASHBOARD/Navigation.md

**New:** Last Session: 2026-09-07_1736_bdf_ca_brain_os

**Suggested resolution:** Apply manually, or choose another target.

**Decision:** [ ] Approve  [ ] Modify  [ ] Skip

---

## Flag 5 of 5 — PROTECTED [HIGH]

**Description:** Protected: Next_Session_Prompt (writer: manual) - Session opener, pasted as the first message. Hand written.

**Nodes:** 00_DASHBOARD/Next_Session_Prompt.md

**New:** - Review and resolve ingestion idempotency issue (double-run produces non-idempotent results)
- Follow up on CA_Book incoming triage findings
- Verify CA registry entry now correctly points to CA_Book

**Suggested resolution:** Apply manually, or choose another target.

**Decision:** [ ] Approve  [ ] Modify  [ ] Skip

---
