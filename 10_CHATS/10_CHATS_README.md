---
tags: [system, chats, knowledge-base]
created: 2026-05-03
updated: 2026-05-03
---

# 10_CHATS — Session Archive & Knowledge Extraction

This directory contains compiled session notes from Claude conversations. Each chat file represents the **distilled knowledge** from a conversation, not a raw transcript.

---

## Purpose

Transform raw chat data into structured, searchable, linked knowledge that feeds into:
- **02_PROJECTS/** — Project documentation updates
- **07_SYSTEM/** — System-wide knowledge (tools, protocols, aliases)
- **C:\Knowledge\** — Book content (CA Book, BDF Book, learning guides)

---

## File Naming Convention

```
YYYY-MM-DD_Short_Descriptive_Title.md
```

Examples:
- `2026-05-03_Obsidian_MCP_Fix_Audio_Systems.md`
- `2026-04-18_Edge_TTS_Learning_System_Creation.md`
- `2026-04-30_Project_Standardization_Pass.md`

---

## File Structure

Each chat note follows the **SESSION_COMPILE_TEMPLATE.md** (located in 08_TEMPLATES/):

1. **Session Metadata** — Date, project(s), type, duration
2. **What Was Built** — Code, files, systems created
3. **What Was Decided** — Architecture, tools, standards
4. **What Problems Were Solved** — Bugs, blockers, errors
5. **What Patterns Emerged** — Workflows, best practices
6. **Commands/Aliases Created** — PowerShell, scripts
7. **Book-Worthy Content** — CA/BDF book candidates
8. **Project Links** — Wiki-links to affected nodes
9. **Outstanding Questions** — Future investigation needed
10. **Next Session Priorities** — Immediate follow-ups

---

## Knowledge Flow

```
RAW CHAT
  ↓
SESSION COMPILE (this directory)
  ↓
┌─────────────┬──────────────┬───────────────┐
│ 02_PROJECTS │  07_SYSTEM   │  C:\Knowledge │
│  (updates)  │  (updates)   │  (extracts)   │
└─────────────┴──────────────┴───────────────┘
         ↓            ↓              ↓
    OBSIDIAN     TOOLS/PROTO    BOOKS/GUIDES
   GRAPH VIEW    COLS/ALIASES
```

---

## How to Use

### At End of Session
1. Ask Claude: "Compile this session using the SESSION_COMPILE_TEMPLATE"
2. Claude fills in all sections based on conversation
3. Claude uses Obsidian MCP to:
   - Create chat note in 10_CHATS/
   - Update affected project nodes in 02_PROJECTS/
   - Update system nodes in 07_SYSTEM/
   - Extract book content to C:\Knowledge\

### During Research
1. Search chat notes: `search-vault` in Obsidian
2. Follow wiki-links to related projects/systems
3. Trace decision history across sessions

---

## Guidelines

### What Belongs Here
✅ Complete session compiles using the template  
✅ Multi-project sessions with clear delineation  
✅ Research sessions with findings and decisions  
✅ Major bug fixes with full context  

### What Does NOT Belong Here
❌ Raw chat transcripts (use 09_TOOLS/ for archives)  
❌ Quick fixes without broader context  
❌ Test/experimental sessions with no knowledge extracted  

---

## Related Nodes
- [[Session_Protocol]] — How to structure sessions
- [[Knowledge_Ingestion_Protocol]] — How to extract knowledge
- [[Project_Directory]] — List of all projects
- [[Tools_Registry]] — System tools and utilities

---

## Maintenance

- **Weekly:** Review new chat notes for cross-linking opportunities
- **Monthly:** Consolidate patterns into 07_SYSTEM/ best practices
- **Quarterly:** Extract book-worthy content to C:\Knowledge\
