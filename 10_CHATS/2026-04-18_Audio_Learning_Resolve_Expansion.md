---
tags: [session, audio-learning, edge-tts, resolve-mcp, read-along, project-cheatsheets]
created: 2026-04-18
session_type: build/documentation/expansion
projects: [Edge_TTS_Learning_System, Read_Along_App, Resolve_MCP, Project_Cheatsheets]
---

# Session Compile — Audio Learning System + Read-Along Rebuild + Resolve Expansion

## SESSION METADATA
- **Date:** April 18-19, 2026 (2-day session)
- **Project(s):** Edge TTS Learning System, Read-Along App, Resolve MCP Server, Project Cheatsheet System
- **Session Type:** Build + Documentation + Expansion
- **Duration:** 2 days (major session)
- **Key Participants:** Claude + Cristian

---

## WHAT WAS BUILT

### Files Created

**Audio Learning Guides (5 complete MP3s):**
1. **Claude Code Extended Guide** (~25-30 min, 6 chapters)
   - What Claude Code is
   - 12 key terms (agentic, context window, compaction, CLAUDE.md, slash commands, permissions, tools, MCP, hooks, subagents, tokens, effort)
   - Windows installation
   - First session walkthrough
   - Advanced patterns
   - Common mistakes

2. **Claude AI Platform Extended Guide** (~25-30 min, 11 chapters)
   - LLM system
   - Memory system
   - All skills (docx, pdf, pptx, xlsx, frontend design, file reading, product self-knowledge, skill creator)
   - All tools (web search, fetch, code execution, file creation, image search, Google Drive, sports data, weather, places/maps, message compose, recipe display, visualizer)
   - Artifacts
   - Context window
   - Past conversation search
   - User preferences
   - Plans/pricing
   - Advanced terminology

3. **Project Regrouping Guide** (9 chapters)
   - Mapping all projects
   - Pending tasks
   - File locations
   - How everything connects

4. **Project Cheatsheet Guide** (10 chapters)
   - All 4 projects with April 18 updates
   - Session handoff workflow
   - Complete rules

5. **Resolve MCP Guide** (11 chapters)
   - MCP architecture
   - pyautogui workaround
   - All terminology
   - Startup sequence
   - File structure
   - Next steps

**Project Cheatsheet System:**
```
C:\Knowledge\Dev\
├── 00_index.txt          ← "Which file do I upload?" reference
├── 01_bdf.txt            ← BDF project only
├── 02_ca.txt             ← Custom Agent only
├── 03_readalong.txt      ← Read-Along App only
├── 04_cclanding.txt      ← CC-Landing only
├── 05_resolvemcp.txt     ← Resolve MCP only
├── 06_rules.txt          ← Shared rules, aliases, learning system
└── projects_cheatsheet.txt ← Full combined version
```

**Knowledge Library Structure:**
```
C:\Knowledge\
├── Claudeguide\    (8 files: 4 MP3s + 4 text scripts)
├── ResolveMCP\     (2 files: 1 MP3 + 1 text script)
├── BDF\
├── CA\
├── Dev\            (7 cheatsheet files + master index)
├── Hardware\
└── Personal\
```

### Systems Implemented

**Edge TTS Audio Learning System:**
- **Engine:** Microsoft Edge TTS
- **Voice:** en-US-GuyNeural
- **Rate:** -5% (slightly slower for comprehension)
- **Cost:** $0 (100% FREE Microsoft service)
- **Workflow:** Claude generates script → Python generator → user runs → MP3 created

**Evolution Path:**
1. Tried gTTS (Google Text-to-Speech) → too robotic despite being "neural"
2. Tried espeak → even worse, completely robotic
3. Edge TTS with en-US-GuyNeural → SOLUTION: clear, natural, human-sounding

**Memory Trigger Saved:**
"Create a learning guide for [topic] using my audio learning system"

**Read-Along App Venv Rebuild:**
- **Problem:** Corrupted .exe launchers from folder move (C:\Knowledge\ → C:\Users\titit\Projects\)
- **Root Cause:** Python venvs hardcode absolute paths during creation
- **Fix:** Deleted old venv, created fresh at new location
- **Verification:** PyTorch 2.11.0+cu128 CUDA working, RTX 5070 Ti detected, FFmpeg system-wide, Whisper installed

**Resolve MCP Server Expansion (11 → 52 tools):**

**Phase 1: Core Editing (11 → 31):**
- stop, play_reverse, play_forward, go_to_end
- next_marker, prev_marker, next_clip, prev_clip
- nudge_forward, nudge_back
- select_clip_at_playhead, delete_selected
- redo, zoom_in, zoom_out
- fullscreen_preview
- go_to_media_page, go_to_cut_page, go_to_fusion_page, go_to_fairlight_page

**Phase 2: Audio & Export (31 → 43):**
- **In/Out Points:** set_in_point, set_out_point, clear_in_out, delete_between_in_out
- **Audio:** normalize_audio, add_fade_in, solo_audio_track, mute_audio_track
- **Editing:** split_audio_video (unlink audio from video)
- **Export:** quick_export, add_to_render_queue, start_render
- **Playback:** loop_playback

**Phase 3: Color Page (43 → 52):**
- **Node management:** add_serial_node, add_parallel_node, add_layer_node
- **Grading:** reset_grade, copy_grade, paste_grade, toggle_bypass
- **Navigation:** next_node, prev_node

**Git Initialized:**
```
C:\Users\titit\Projects\resolve-mcp-server\
├── .gitignore          (venv/, __pycache__/, *.pyc, .env)
├── server.py           (52 tools, committed)
└── test_resolve.py     (connection tests)
```
Initial commit: 1dbece3

**Guitar Project Media Structure:**
```
C:\Media\GuitarProject\
├── originals\
│   └── cristian_guitar_01.MOV  (54 MB, renamed from phone hash)
├── exports\
└── resolve_projects\
```

### Features Added
- Natural-sounding audio learning guides (Edge TTS)
- Project-specific cheatsheets (token-efficient handoffs)
- 41 new Resolve MCP tools (total 52)
- Organized media structure for guitar project
- Git version control for Resolve MCP server

---

## WHAT WAS DECIDED

### Architecture Decisions

1. **Audio Learning System Creation:**
   - Need natural-sounding voice for learning guides
   - Evolution: gTTS (rejected) → espeak (rejected) → Edge TTS (adopted)
   - Free is better than paid when quality is comparable
   
2. **Project Cheatsheet System:**
   - **Problem:** Claude kept losing track between sessions
   - **Solution:** Split master cheatsheet into individual files per project
   - **Workflow:** Upload project file + 06_rules.txt at START of every session
   - **Token Efficiency:** Only load what's needed for current work

3. **Resolve MCP Expansion Strategy:**
   - Start with basic tools (playback, cutting)
   - Add audio tools for guitar video workflow
   - Add color page tools for grading
   - Build incrementally, test after each phase

4. **Venv Management:**
   - **Lesson:** Python venvs hardcode absolute paths at creation
   - **Rule:** Moving project folder breaks venv - must delete and recreate
   - **Prevention:** Create venv at final location, don't move after

### Tool Choices
- **Edge TTS** over gTTS/espeak (natural voice quality)
- **Git** for Resolve MCP versioning
- **pyautogui** for Resolve automation (API limitations)

### Standards Established

**New Rules Added:**
- **Rule 11:** Always `where.exe python`, never `where python` in PowerShell
- **Rule 12:** Never put Python projects or venvs inside OneDrive (sync conflicts)
- **Rule 13:** Upload cheatsheet at START of every new Claude chat

**Session Handoff Protocol:**
- Start: Upload relevant project cheatsheet + rules
- End: Update cheatsheet if things changed
- Working on BDF? Upload 01_bdf.txt + 06_rules.txt
- Working on Read-Along? Upload 03_readalong.txt + 06_rules.txt

---

## WHAT PROBLEMS WERE SOLVED

### Bugs Fixed

1. **Read-Along Venv Corruption (CRITICAL)**
   - **Symptom:** All pip commands failed with "Unable to create process"
   - **Root Cause:** Shebang paths pointed to old location (C:\Knowledge\) after folder move
   - **Diagnosis:** .exe launchers in venv\Scripts\ hardcoded old paths
   - **Fix:** Deleted old venv, created fresh with `python -m venv venv`
   - **Verification:** PyTorch CUDA working, torch.cuda.is_available() = True, RTX 5070 Ti detected
   - **Lesson:** Venvs cannot be moved - absolute paths are hardcoded during creation

2. **Claude Session State Loss**
   - **Symptom:** Claude nearly rebuilt Read-Along App from scratch (already MVP complete)
   - **Problem:** Master cheatsheet too large, Claude loses context
   - **Solution:** Split into 7 individual files (one per project + rules)
   - **Result:** Only load relevant context for current work

### Blockers Removed
- Read-Along venv functional again (PyTorch CUDA verified)
- Resolve MCP expanded to handle full editing workflow
- Session handoff system prevents context loss
- Guitar project ready for editing practice

---

## WHAT PATTERNS EMERGED

### Workflows Established

1. **Audio Learning Guide Creation:**
   - User requests guide on topic
   - Claude generates narration script (.txt)
   - Claude generates Python generator (.py) with Edge TTS calls
   - User runs generator → MP3 created
   - User saves to C:\Knowledge\[TopicFolder]\
   - User drag-and-drop to Google Drive

2. **Resolve Editing Workflow (Explained):**
   - **Marking pass:** Watch video, drop markers at important moments (markers are bookmarks, not cuts)
   - **Cutting pass:** Go to each marker, make cuts, delete unwanted sections
   - **In/out points:** Define range for looping, exporting, or bulk deletion
   - **Ripple delete:** Removes clips AND closes gaps (regular delete leaves black space)

3. **Session Handoff (New Standard):**
   - START: Upload project cheatsheet + rules
   - WORK: Build/fix/document
   - END: Ask Claude to update cheatsheet if things changed
   - NEXT SESSION: Repeat with updated files

### Best Practices
- **Edge TTS** installation: `pip install edge-tts` (global)
- **Venv creation:** Always at final project location, never move after
- **Git initialization:** Early and often (Resolve MCP committed on day 1)
- **Media organization:** originals/ + exports/ + resolve_projects/ structure

### Principles Discovered
- **Natural voice matters** for learning comprehension
- **Token efficiency** via targeted context (small cheatsheets > giant master file)
- **Incremental expansion** beats big-bang rewrites (11 → 31 → 43 → 52 tools)
- **Venv isolation** prevents dependency conflicts between projects

---

## COMMANDS/ALIASES CREATED

No new aliases created this session.

**Confirmed existing:**
- Edge TTS uses generated Python scripts (no dedicated alias)
- Resolve MCP uses manual `python server.py` start (no alias yet)

---

## TECHNICAL DETAILS

### Environment Changes

**Python Packages (Read-Along venv rebuilt):**
- PyTorch 2.11.0+cu128 (CUDA verified)
- FFmpeg (already installed system-wide)
- Whisper (already installed and linked to CUDA PyTorch)
- **Still Remaining:** fastapi, uvicorn, python-multipart

**Git Repositories:**
- Resolve MCP server initialized (commit 1dbece3)

**Directory Structure:**
- C:\Knowledge\ expanded with Claudeguide/ and Dev/ folders
- C:\Media\GuitarProject\ created with proper structure

### Dependencies Added
- Edge TTS (global install)

### Configuration Updates
None

---

## BOOK-WORTHY CONTENT

### CA Book Candidates
- **Chapter: "Building Audio Learning Systems"**
  - Edge TTS vs other TTS engines
  - Evolution from robotic to natural voices
  - Creating personal learning libraries
  - Memory trigger systems

- **Chapter: "Session Handoff Protocols"**
  - Maintaining context across conversations
  - Token-efficient knowledge transfer
  - Project-specific cheatsheets

### BDF Book Candidates
None this session

### Learning Guide Candidates
- **"Understanding Python Virtual Environments"**
  - Why venvs exist
  - How they work (path hardcoding)
  - Common mistakes (moving folders)
  - Best practices

---

## INGESTION MAP

### Edge_TTS_Learning_System.md
- **Action:** ALREADY CREATED (via May 3 ingestion)
- **Target Section:** N/A
- **Merge Strategy:** VERIFY
- **Reasoning:** This node was created from this session's knowledge on May 3
- **Content Summary:** Verify all April 18 details are present
- **Supersedes:** N/A
- **Date Stamp:** 2026-05-03 (created from April 18 session)

### Read_Along_App.md (in 02_PROJECTS/)
- **Action:** CREATE NEW NODE
- **Parent:** [[02_PROJECTS]]
- **Tags:** [project, transcription, whisper, react, pytorch]
- **Initial Content:**
  - Project overview (Whisper transcription with sync playback)
  - Tech stack (Python backend, React frontend, PyTorch CUDA)
  - Venv rebuild story (April 18 corruption + fix)
  - Current status (MVP complete, needs FastAPI install)
  - File locations
- **Connected to:** [[Creative_Systems]]

### Resolve_MCP.md (in 02_PROJECTS/)
- **Action:** UPDATE (if exists) or CREATE
- **Target Section:** Tool Evolution
- **Merge Strategy:** APPEND
- **Reasoning:** Document the 11 → 52 expansion
- **Content Summary:**
  - Timeline: 11 → 31 → 43 → 52
  - Phase 1, 2, 3 details
  - Git initialization (1dbece3)
  - Guitar project media structure
- **Supersedes:** N/A (addition)
- **Date Stamp:** 2026-04-18

### Tools_Registry.md (in 07_SYSTEM/)
- **Target Section:** Development Tools
- **Merge Strategy:** APPEND
- **Reasoning:** Edge TTS is a new tool in the ecosystem
- **Content Summary:**
  - Edge TTS: Microsoft TTS service, en-US-GuyNeural voice
  - Free, natural-sounding
  - Installation: `pip install edge-tts`
- **Supersedes:** N/A
- **Date Stamp:** 2026-04-18

### PowerShell_Aliases.md (in 07_SYSTEM/)
- **Target Section:** N/A
- **Merge Strategy:** SKIP
- **Reasoning:** No new aliases created
- **Content Summary:** N/A
- **Supersedes:** N/A
- **Date Stamp:** N/A

### AI_Engineering.md (in 01_DOMAINS/)
- **Target Section:** Active Projects → Resolve_MCP
- **Merge Strategy:** UPDATE
- **Reasoning:** Document tool expansion
- **Content Summary:** Update tool count: "52 tools (up from 11 on April 18)", note git initialization
- **Supersedes:** Old tool count
- **Date Stamp:** 2026-04-18

### AI_Engineering.md
- **Target Section:** Tools & Integrations → Audio
- **Merge Strategy:** VERIFY
- **Reasoning:** Edge TTS should already be listed (added May 3)
- **Content Summary:** Confirm Edge TTS entry exists
- **Supersedes:** N/A
- **Date Stamp:** 2026-05-03

### Creative_Systems.md (in 01_DOMAINS/)
- **Target Section:** Active Projects → Read_Along_App
- **Merge Strategy:** UPDATE
- **Reasoning:** Document venv rebuild
- **Content Summary:** Add venv rebuild story (corrupted → fixed April 18), note pending FastAPI install
- **Supersedes:** N/A (addition)
- **Date Stamp:** 2026-04-18

### Creative_Systems.md
- **Target Section:** Active Projects → Resolve_Workflows
- **Merge Strategy:** UPDATE
- **Reasoning:** Document tool expansion and workflow
- **Content Summary:** Update tool count, add editing workflow pattern (marking → cutting → audio → color → export)
- **Supersedes:** Old tool count
- **Date Stamp:** 2026-04-18

---

## AUTOMATED INGESTION CHECKLIST

**Pre-Ingestion:**
- [x] All affected nodes identified
- [x] Delta analysis complete
- [x] Merge strategies assigned
- [x] Supersession conflicts resolved (none)

**Post-Ingestion:**
- [x] All nodes have updated timestamps
- [x] No broken wiki-links
- [x] Bidirectional links verified
- [ ] Git diff is clean and reviewable
- [ ] Commit message describes changes

---

## PROJECT LINKS

### Projects Updated
- [[Resolve_MCP]] - 11 → 52 tools
- [[Read_Along_App]] - Venv rebuilt
- [[Edge_TTS_Learning_System]] - Created
- [[Project_Cheatsheet_System]] - Created

### System Nodes Updated
- [[Tools_Registry]] - Edge TTS added
- [[AI_Engineering]] - Resolve tool count updated
- [[Creative_Systems]] - Read-Along and Resolve updates

### New Nodes to Create
- [[Read_Along_App]] - Full project documentation
- [[Resolve_MCP]] - Full project documentation (if doesn't exist)
- [[Project_Cheatsheet_System]] - System documentation

---

## OUTSTANDING QUESTIONS

### Needs Investigation
None

### Future Work
1. Install fastapi, uvicorn, python-multipart in Read-Along venv
2. Test all 52 Resolve MCP tools on guitar footage
3. Build jump_to_timecode tool for Resolve
4. Practice full editing workflow: mark → cut → delete → export
5. Push Resolve MCP server to GitHub

### Open Questions
None

---

## NEXT SESSION PRIORITIES
1. Install FastAPI packages in Read-Along venv
2. Test Resolve MCP tools end-to-end
3. Build jump_to_timecode tool
4. Practice full editing workflow on guitar footage
5. Push Resolve MCP to GitHub

---

## INGESTION EXECUTION LOG

**Execution Date:** 2026-05-04
**Nodes Modified:** 3
**Nodes Created:** 1
**Git Diff:** `git diff HEAD~1`

**Changes Applied:**
- `07_SYSTEM/Tools_Registry.md` — APPENDED Edge TTS tool entry (name, engine, voice, cost, install, use cases)
- `02_PROJECTS/Read_Along_App.md` — APPENDED Venv Rebuild section (April 18 corruption root cause, fix, rule)
- `02_PROJECTS/Project_Cheatsheet_System.md` — CREATED new node (7-file structure, session protocol, rules)
- `07_SYSTEM/Edge_TTS_Learning_System.md` — VERIFIED complete (created May 3 from this session)
- `01_DOMAINS/AI_Engineering.md` — VERIFIED (Resolve 52 tools + Edge TTS already present from May 4)
- `01_DOMAINS/Creative_Systems.md` — VERIFIED (Read-Along venv rebuild + Resolve workflow already present)
- `02_PROJECTS/Read_Along_App.md` project node — VERIFIED exists (created May 2)
- `02_PROJECTS/Resolve_MCP_Server.md` — VERIFIED (evolved beyond April 18 architecture; evolution captured in AI_Engineering.md)

---

## Connected to
- [[Edge_TTS_Learning_System]]
- [[Read_Along_App]]
- [[Resolve_MCP]]
- [[AI_Engineering]]
- [[Creative_Systems]]
- [[Tools_Registry]]
