# BRAIN_OS INGESTION — CLAUDE CODE EXECUTION PLAN
# Run from: C:\BRAIN_OS (git checkout main first)
# All patch files assumed to be in C:\Users\titit\Downloads\brain_os_ingestion\

---

## STEP 1 — Write new node: CristianConstruction.md

Write the contents of CristianConstruction.md exactly as provided to:
  C:\BRAIN_OS\02_PROJECTS\CristianConstruction.md

No modifications. Confirm file written before proceeding.

---

## STEP 2 — Patch Custom_Agent.md

Open C:\BRAIN_OS\02_PROJECTS\Custom_Agent.md.

2A. Append the ## TTS Environment section (from Custom_Agent_patch.md)
    BEFORE the ## Connected to section.

2B. REPLACE the existing ## Open Questions section with the updated
    ## Open Items section from Custom_Agent_patch.md.

2C. Add [[CristianConstruction]] to the ## Connected to section
    (it should already be there from the previous ingestion batch —
    verify before adding to avoid duplicates).

Confirm changes before proceeding.

---

## STEP 3 — Patch PowerShell_Aliases.md

Open C:\BRAIN_OS\07_SYSTEM\PowerShell_Aliases.md.

3A. REPLACE the entire ## Profile File Locations section with the
    updated version from PowerShell_Aliases_patch.md.

3B. APPEND the ## Known Issues section BEFORE ## Connected to.

Confirm changes before proceeding.

---

## STEP 4 — Commit everything

git add 02_PROJECTS/CristianConstruction.md
git add 02_PROJECTS/Custom_Agent.md
git add 07_SYSTEM/PowerShell_Aliases.md
git commit -m "docs: ingestion batch 2 — CristianConstruction node, TTS patches, PowerShell profile fixes"
git push origin main

Report final commit hash and file change summary.
