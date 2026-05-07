# Obsidian Update Protocol

## RULE: Obsidian is the Map - Never Create Empty Files

**Problem:** Files referenced in docs but never created = broken map

**Solution:** Every reference must be backed by real content

---

## Protocol for Updating BRAIN_OS

### Step 1: Change Happens (Code, Config, Decision)
**Action:** Document immediately in session notes

### Step 2: Session Close
**Action:** Run `session_close.py` → creates session file in 10_CHATS

### Step 3: Session Ingestion
**Action:** 
```bash
cd C:\BRAIN_OS
claude chat "Ingest latest session using KNOWLEDGE_INGESTION_PROTOCOL_V2"
```

**Result:** Updates project nodes, agent nodes, creates wiki-links

### Step 4: Verification
**Action:** Open Obsidian → Graph View → verify new blue node connected

---

## When Something Touches Obsidian

### Creating New Files
**NEVER create empty placeholder files**
- If referenced in docs → create with content immediately
- If template → use 06_TEMPLATES as base
- If navigation → populate with current paths

### Updating Existing Files
**Flow:**
1. Use Claude Code to update
2. Commit with clear message
3. Verify in Obsidian graph

### Referencing Files in Docs
**Rule:** Only reference files that exist
- Check file exists before wiki-linking
- If missing → create before linking

---

## File Creation Checklist

Before creating any .md file in BRAIN_OS:

- [ ] Content is prepared (not empty)
- [ ] Location is correct (right folder)
- [ ] Wiki-links are valid
- [ ] Commit message describes what/why
- [ ] Graph verified (new node appears)

---

## Red Flags (Stop Immediately)

🚫 **Empty file created**
→ Delete or populate before commit

🚫 **Broken wiki-link**
→ Create target file or remove link

🚫 **Reference to non-existent file in docs**
→ Create file or update docs

🚫 **Outdated information in any file**
→ Update immediately or flag for review

---

## File Organization Rules

### Naming Convention
✅ **GOOD:** 2026-05-06_BRAIN_OS_Graph_Session.md
❌ **BAD:** Untitled 2, temp file, test.md

**Rules:**
- Always use descriptive names
- Include date for time-based files (YYYY-MM-DD_Title)
- No 'Untitled' files (delete or rename immediately)
- Use underscores, not spaces

### Folder Structure
All files must live in numbered folders:
- 00_DASHBOARD - Canvas files only
- 01_PROJECTS - Project documentation
- 02_AGENTS - Agent files
- 03_APIS - API connections
- 04_WORKFLOWS - Process flows
- 05_MEMORY - Knowledge storage
- 06_TEMPLATES - Template files
- 07_SYSTEM - System documentation
- 08_TRIGGERS - Trigger definitions
- 09_TOOLS - Tool documentation
- 10_CHATS - Session compiles

**Never store files in root directory**

### Weekly Cleanup Checklist
Every Friday:
- [ ] Search for 'Untitled' files → delete or rename
- [ ] Check root directory → move to proper folders
- [ ] Review empty files → populate or delete
- [ ] Verify all templates in 06_TEMPLATES

### Quick Search for Problems
In Obsidian:
- Search: `Untitled` → Delete all results
- Search: `/` (root files) → Move to proper folders
- Graph view → Look for orphan nodes → Connect or delete

---

## Maintenance Schedule

**Weekly:** Check 07_SYSTEM files for accuracy
**Monthly:** Audit 01_PROJECTS nodes
**Per Session:** Update relevant nodes via ingestion

---

## Cost Control

**Free operations:**
- Manual file creation in VS Code
- Git commits
- Obsidian graph viewing

**Paid operations:**
- Claude Code file updates ($0.01-0.50 per file typically)
- Session ingestion ($2-5 per session)
- Full vault audit ($8-25)

**Recommendation:** Update incrementally, not in bulk
