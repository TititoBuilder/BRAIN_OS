---
tags: [session, mcp, obsidian, audio-systems, knowledge-pipeline]
created: 2026-05-03
session_type: fix/documentation/build
projects: [BRAIN_OS, Custom_Agent, Edge_TTS_Learning_System]
---

# Session Compile — Obsidian MCP Fix + Audio Systems + Knowledge Pipeline

## SESSION METADATA
- **Date:** May 3, 2026
- **Project(s):** BRAIN_OS, Custom_Agent, Edge_TTS_Learning_System
- **Session Type:** Fix + Documentation + System Build
- **Duration:** ~2 hours
- **Key Participants:** Claude + Cristian

---

## WHAT WAS BUILT

### Files Created
- `08_TEMPLATES/SESSION_COMPILE_TEMPLATE.md` — Template for end-of-session knowledge extraction
- `10_CHATS/README.md` — Documentation for chat archive system
- This session compile (first test case)

### Systems Implemented
- **Knowledge Management Pipeline:**
  ```
  RAW CHAT → SESSION COMPILE → OBSIDIAN BRAIN_OS → BOOKS/PRODUCTS
  ```
- **10_CHATS/ directory structure** for session archives
- **SESSION_COMPILE_TEMPLATE** with 10 structured sections

### Features Added
- Obsidian MCP now functional (after config fix)
- Automated knowledge extraction workflow
- Wiki-linking between sessions and projects

---

## WHAT WAS DECIDED

### Architecture Decisions
1. **BRAIN_OS Structure Finalized:**
   - `02_PROJECTS/` = Project documentation
   - `07_SYSTEM/` = System-wide knowledge
   - `08_TEMPLATES/` = Reusable templates
   - `09_TOOLS/` = Raw session archives
   - `10_CHATS/` = Compiled session knowledge

2. **Knowledge Flow:**
   - End of session → Fill SESSION_COMPILE_TEMPLATE
   - Use Obsidian MCP to update affected nodes
   - Extract book content to C:\Knowledge\

3. **Template-Driven Compilation:**
   - Every session uses same structure
   - 10 sections cover all knowledge types
   - Wiki-links maintain project relationships

### Tool Choices
- **Obsidian MCP** for vault manipulation
- **SESSION_COMPILE_TEMPLATE** for consistency
- **Wiki-links** for knowledge graph connections

### Standards Established
- **File Naming:** `YYYY-MM-DD_Short_Descriptive_Title.md`
- **Always use template** for session compiles
- **Link everything** — sessions ↔ projects ↔ systems

---

## WHAT PROBLEMS WERE SOLVED

### Bugs Fixed
1. **Obsidian MCP hanging** 
   - **Root cause:** Wrong package registered (`obs-mcp` instead of `obsidian-mcp`)
   - **Confusion:** "obs" = OBS Studio (streaming), "obsidian" = Obsidian (notes)
   - **Fix:** Updated MCP config with correct package + vault path
   - **Memory updated:** Added permanent reminder about obs vs obsidian distinction

2. **Kokoro cost confusion**
   - **User thought:** Kokoro was charging via Claude API
   - **Reality:** Charges were from Claude Opus compilation, not Kokoro TTS
   - **Clarification:** Kokoro is 100% FREE, runs locally on GPU
   - **Documentation:** Full timeline from March 25, 2026 creation to present

### Blockers Removed
- Obsidian MCP now accessible for vault automation
- Knowledge extraction no longer manual/scattered
- Audio system costs fully understood

---

## WHAT PATTERNS EMERGED

### Workflows Established
1. **Session Close Workflow:**
   - Ask Claude to compile using SESSION_COMPILE_TEMPLATE
   - Claude fills all sections from conversation
   - Claude updates affected BRAIN_OS nodes
   - Claude extracts book content

2. **Name Verification Pattern:**
   - Never assume abbreviations
   - Always verify full names before making assumptions
   - Critical for tools/services (obs ≠ obsidian)

### Best Practices
- **Start simple, then investigate** — don't overcomplicate fixes
- **Memory updates immediately** when patterns emerge
- **Complete documentation** of cost/free distinctions

### Principles Discovered
- **Chat data is most valuable asset** — everything flows from it
- **Structure enables extraction** — templates make knowledge portable
- **Links create intelligence** — wiki-links turn notes into knowledge graph

---

## COMMANDS/ALIASES CREATED

No new aliases this session. Confirmed existing audio aliases:
- `ca-audio` = CA Book audio generation (Kokoro)
- Edge TTS uses generated Python scripts (no alias)

---

## TECHNICAL DETAILS

### Environment Changes
- Obsidian MCP configuration updated in claude.ai settings
- BRAIN_OS directory structure expanded (10_CHATS/ + templates)

### Dependencies Added
None

### Configuration Updates
```json
{
  "obsidian": {
    "command": "npx",
    "args": ["-y", "obsidian-mcp", "C:\\BRAIN_OS"]
  }
}
```

---

## BOOK-WORTHY CONTENT

### CA Book Candidates
- **Knowledge Management chapter:** How to structure personal knowledge systems
- **Tool Selection Framework:** Local/free vs cloud/paid decision criteria

### BDF Book Candidates
None this session

### Learning Guide Candidates
- **"Obsidian + Claude: Building a Second Brain"** — Full workflow from chat to vault
- **"Audio Generation Systems Compared"** — Kokoro vs Edge TTS vs paid services

---

## PROJECT LINKS

### Projects Documented
- [[Custom_Agent_TTS]] — Needs update: Kokoro cost clarification
- [[Edge_TTS_Learning_System]] — Needs creation: April 18, 2026 system
- [[BRAIN_OS]] — Structure expanded with 10_CHATS/

### System Nodes Updated
- [[Tools_Registry]] — Obsidian MCP now operational
- [[Session_Protocol]] — New knowledge extraction workflow

### New Nodes to Create
- [[Audio_Systems_Comparison]] — Kokoro vs Edge TTS side-by-side
- [[Knowledge_Ingestion_Protocol]] — End-of-session compilation process
- [[Edge_TTS_Learning_System]] — April 18, 2026 creation story

---

## OUTSTANDING QUESTIONS

### Needs Investigation
None

### Future Work
1. Create `Audio_Systems_Comparison.md` node
2. Create `Edge_TTS_Learning_System.md` node
3. Update `Custom_Agent_TTS.md` with cost clarification
4. Create `Knowledge_Ingestion_Protocol.md` system node

### Open Questions
None

---

## AUDIO SYSTEMS DEEP DIVE

### System 1: Kokoro (CA Book)
- **Engine:** Kokoro TTS (local, GPU-accelerated)
- **Voice:** af_heart (American English, warm female)
- **Cost:** $0 — 100% FREE, runs on RTX 5070 Ti
- **Format:** WAV (lossless, faster to write)
- **Automation:** High — single command `ca-audio ch01`
- **Location:** `C:\Dev\Projects\custom-agent\ca_audio.py`
- **Output:** `C:\Knowledge\CA\CA_Book\audio\`
- **Best for:** Repetitive chapter generation, batch processing

**Cost Confusion Timeline:**
- March 25, 2026: Created, confirmed free
- March-April: User saw $7-8 charges in cost logs
- **Reality:** Charges were Claude Opus compilation ($0.15-0.30/chapter)
- **Not Kokoro:** TTS generation is invisible in cost log (free)
- **batching problem:** Multiple files processed = 3-5x compilation costs

### System 2: Edge TTS (Learning Guides)
- **Engine:** Microsoft Edge TTS
- **Voice:** en-US-GuyNeural, rate -5%
- **Cost:** $0 — 100% FREE Microsoft service
- **Format:** MP3
- **Automation:** Low — 3-step manual (generate script → run → upload)
- **Created:** April 18, 2026
- **Output:** `C:\Knowledge\Claudeguide\`, `C:\Knowledge\ResolveMCP\`
- **Best for:** One-off documentation, learning guides

**Evolution:**
1. Tried gTTS (Google TTS) → too robotic
2. Tried espeak → even worse
3. Edge TTS → natural, human-sounding ✓

**Files Created (April 18):**
- `claude_code_extended_guide.mp3`
- `claude_ai_platform_extended_guide.mp3`
- `project_regrouping_guide.mp3`
- `project_cheatsheet_guide.mp3`
- `resolve_mcp_guide.mp3`

### When to Use Which
| Task | System | Why |
|------|--------|-----|
| CA Book chapters | Kokoro | Automated, batch-friendly |
| BDF Book chapters | Kokoro | Automated, batch-friendly |
| Learning guides | Edge TTS | One-off, natural voice |
| Documentation audio | Edge TTS | One-off, natural voice |

**Key Principle (March 25, 2026):**
> "Open-source locally-running tools are always preferred over cloud subscription services when quality is comparable."

---

## NEXT SESSION PRIORITIES
1. Deploy SESSION_COMPILE_TEMPLATE to `C:\BRAIN_OS\08_TEMPLATES\`
2. Deploy 10_CHATS README to `C:\BRAIN_OS\10_CHATS\`
3. Deploy this session compile to `C:\BRAIN_OS\10_CHATS\2026-05-03_Obsidian_MCP_Fix_Audio_Systems.md`
4. Create missing nodes:
   - `Audio_Systems_Comparison.md`
   - `Edge_TTS_Learning_System.md`
   - `Knowledge_Ingestion_Protocol.md`
5. Update `Custom_Agent_TTS.md` with cost clarification

---

## Connected to
- [[Session_Protocol]]
- [[Knowledge_Ingestion_Protocol]] (to be created)
- [[Project_Directory]]
- [[Custom_Agent_TTS]]
- [[Edge_TTS_Learning_System]] (to be created)
- [[Tools_Registry]]
- [[BRAIN_OS]]
