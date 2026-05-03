# EXAMPLE: Automated Ingestion for 2026-05-03 Session

## How This Works

This document shows the **automated ingestion plan** Claude would execute for this session. After session compile, Claude:

1. **Analyzes** what knowledge was generated
2. **Detects deltas** (new/corrected/enhanced/duplicate)
3. **Routes** content to correct nodes
4. **Executes** merges with appropriate strategy
5. **Commits** all changes with descriptive message
6. **User reviews** git diff afterward

---

## INGESTION MAP (Auto-Generated)

### Custom_Agent_TTS.md
- **Target Section:** Cost and Pricing
- **Merge Strategy:** REPLACE
- **Reasoning:** Previous cost info was incorrect - session provided full clarification
- **Content Summary:** 
  - Kokoro TTS is 100% FREE (local GPU inference, zero API costs)
  - Previous confusion: charges in cost logs were Claude Opus compilation ($0.15-0.30/chapter), NOT Kokoro
  - Timeline: March 25 creation (free) → March-April cost confusion → May 3 clarification
- **Supersedes:** Any previous text stating "Kokoro costs money" or "charged via Claude API"
- **Date Stamp:** 2026-05-03

**Delta detected:** CORRECTION (old info wrong)

**Merge execution:**
```markdown
BEFORE (incorrect):
## Cost
TTS generation has associated costs.

AFTER (corrected):
## Cost (Corrected 2026-05-03)
Kokoro TTS is 100% FREE - runs locally on RTX 5070 Ti via CUDA with zero API costs.

**Cost Confusion Clarified:**
The charges visible in cost logs ($0.37, $7.15, $8.56) were from Claude Opus 
compilation of book chapters, NOT from Kokoro audio generation. The confusion 
arose because both operations run in the same `bdf-book` command:
- Step 1: Claude Opus compiles chapter (COSTS $0.15-0.30)
- Step 2: Kokoro generates audio (FREE)
- Step 3: Google Drive sync (FREE)

Kokoro is invisible in cost logs because it costs nothing.

**Previous note:** Previously documented as having costs, corrected May 3, 2026 
after full timeline analysis from March 25 creation to present.
```

---

### Tools_Registry.md
- **Target Section:** MCP Servers
- **Merge Strategy:** UPDATE
- **Reasoning:** Obsidian MCP status changed from "broken" to "operational"
- **Content Summary:**
  - Obsidian MCP fixed (config error corrected)
  - Root cause: "obs" (OBS Studio) vs "obsidian" (Obsidian notes) confusion
  - Now operational with 11 tools available
- **Supersedes:** Previous status showing Obsidian MCP as "hangs on tool calls"
- **Date Stamp:** 2026-05-03

**Delta detected:** UPDATE (status changed)

**Merge execution:**
```markdown
BEFORE:
### Obsidian MCP
- Status: ⚠️ Connected but hangs on tool calls
- Issue: Under investigation

AFTER:
### Obsidian MCP
- Status: ✅ Operational (fixed 2026-05-03)
- Tools: 11 (create-note, read-note, edit-note, search-vault, etc.)
- Config: `npx -y obsidian-mcp C:\BRAIN_OS`
- **Fix applied:** Was registered as "obs-mcp" (wrong package) - corrected to "obsidian-mcp"
- **Naming confusion:** "obs" = OBS Studio (streaming), "obsidian" = Obsidian (notes)
```

---

### Edge_TTS_Learning_System.md
- **Action:** CREATE NEW NODE
- **Parent:** [[07_SYSTEM]]
- **Tags:** [audio, tts, learning, edge-tts, free]
- **Initial Content:**
  - Created April 18, 2026 for learning guide generation
  - Voice: en-US-GuyNeural, rate -5%
  - 100% FREE Microsoft service
  - Evolution: tried gTTS (robotic) → espeak (worse) → Edge TTS (natural)
  - Files created: 5 learning guides (Claude Code, Claude AI, Project Regrouping, Cheatsheet, Resolve MCP)
  - Workflow: Claude generates script → user runs → MP3 created → manual upload to Drive
- **Connected to:** [[Audio_Systems_Comparison]], [[Custom_Agent_TTS]], [[Knowledge_Management]]

**Delta detected:** NEW (node doesn't exist)

**Node creation:**
```markdown
---
tags: [audio, tts, learning, edge-tts, free, system]
created: 2026-04-18
updated: 2026-05-03
parent: [[07_SYSTEM]]
---

# Edge TTS Learning System

## Purpose
Generate natural-sounding audio learning guides using Microsoft Edge TTS.
Created April 18, 2026 as the second audio generation system alongside Kokoro.

## System Architecture

**Engine:** Microsoft Edge TTS
**Voice:** en-US-GuyNeural (male, American English)
**Rate:** -5% (slightly slower for learning comprehension)
**Cost:** $0 - 100% FREE Microsoft service
**Format:** MP3

## Workflow

1. **User requests learning guide** on a topic
2. **Claude generates narration script** (.txt file)
3. **Claude generates Python generator** (.py file with Edge TTS calls)
4. **User runs generator** on Predator → MP3 created
5. **User manually uploads** to `C:\Knowledge\[TopicFolder]\`
6. **User drag-and-drop** to Google Drive

### Automation Level
**Low** - 3 manual steps (generate → run → upload)

Contrast with Kokoro: **High** - 1 command (`ca-audio ch01`)

## Evolution Timeline

### April 18, 2026 - Creation
**Problem:** Needed natural-sounding audio for learning guides

**Attempt 1 - gTTS:**
- Google Text-to-Speech (neural voice)
- Result: Too robotic despite being "neural"
- Rejected

**Attempt 2 - espeak:**
- Open-source speech synthesizer
- Result: Even more robotic than gTTS
- Rejected

**Solution - Edge TTS:**
- Microsoft Edge TTS service
- en-US-GuyNeural voice
- Result: ✅ Clear, natural, human-sounding
- **Adopted**

### Installation
```bash
pip install edge-tts
```

## Files Created (April 18, 2026)

All saved to `C:\Knowledge\Claudeguide\`:

1. **claude_code_extended_guide.mp3** (~25-30 min)
   - 6 chapters: What is Claude Code, 12 key terms, installation, first session, advanced patterns, mistakes

2. **claude_ai_platform_extended_guide.mp3** (~25-30 min)
   - 11 chapters: LLM system, memory, skills, tools, artifacts, context window, search, preferences, pricing, terminology

3. **project_regrouping_guide.mp3**
   - 9 chapters: All projects, pending tasks, file locations, connections

4. **project_cheatsheet_guide.mp3**
   - 10 chapters: 4 projects with updates, session handoff, complete rules

5. **resolve_mcp_guide.mp3**
   - 11 chapters: MCP architecture, workarounds, terminology, startup, file structure, next steps

All files also backed up to Google Drive `Claudeguide/` folder.

## When to Use

**Best for:**
- One-off learning guides
- Documentation audio
- Tutorial narration
- Knowledge transfer sessions

**NOT for:**
- Repetitive chapter generation (use Kokoro)
- Batch processing (workflow is manual)
- Automated pipelines (3-step manual process)

## Memory Trigger

**Phrase:** "Create a learning guide for [topic] using my audio learning system"

Claude generates narration script + Python generator using Edge TTS.

## Connected to
- [[Audio_Systems_Comparison]]
- [[Custom_Agent_TTS]]
- [[Knowledge_Management]]
- [[Session_Protocol]]
```

---

### Audio_Systems_Comparison.md
- **Action:** CREATE NEW NODE
- **Parent:** [[07_SYSTEM]]
- **Tags:** [audio, tts, comparison, kokoro, edge-tts]
- **Initial Content:**
  - Side-by-side comparison of Kokoro vs Edge TTS
  - Cost breakdown (both FREE)
  - Automation levels
  - When to use which
  - Decision framework
- **Connected to:** [[Edge_TTS_Learning_System]], [[Custom_Agent_TTS]]

**Delta detected:** NEW (node doesn't exist)

---

### PowerShell_Aliases.md
- **Target Section:** Audio Aliases
- **Merge Strategy:** SKIP
- **Reasoning:** No new aliases created this session, existing aliases verified
- **Content Summary:** Confirmed `ca-audio` alias exists and works
- **Supersedes:** N/A
- **Date Stamp:** 2026-05-03

**Delta detected:** DUPLICATE (already documented)

**Action:** No changes needed

---

## INGESTION EXECUTION PLAN

**Phase 1 - Load & Analyze:**
1. Load 5 identified nodes (1 doesn't exist yet, will create)
2. Generate delta analysis for each
3. Assign merge strategies

**Phase 2 - Execute Merges:**
1. Custom_Agent_TTS.md → REPLACE cost section
2. Tools_Registry.md → UPDATE Obsidian MCP entry
3. Edge_TTS_Learning_System.md → CREATE new node
4. Audio_Systems_Comparison.md → CREATE new node
5. PowerShell_Aliases.md → SKIP (no changes)

**Phase 3 - Verify & Commit:**
1. Update timestamps on all modified nodes
2. Verify wiki-links resolve
3. Git add all changes
4. Commit message:
   ```
   ingest: obsidian-mcp-audio-systems → 2 updated, 2 created
   
   - Custom_Agent_TTS: corrected cost info (Kokoro is FREE)
   - Tools_Registry: Obsidian MCP now operational
   - Edge_TTS_Learning_System: new node documenting April 18 system
   - Audio_Systems_Comparison: new comparison node
   ```
5. Push to origin/main

**Phase 4 - User Review:**
```bash
git log -1 --stat
git diff HEAD~1
```

User sees clean, logical changes. If anything looks wrong, rollback:
```bash
git revert HEAD
```

---

## EXPECTED GIT DIFF PREVIEW

```diff
M  02_PROJECTS/Custom_Agent_TTS.md
   +15 -3    Cost section replaced with clarification

M  07_SYSTEM/Tools_Registry.md
   +4 -2     Obsidian MCP status updated to operational

A  07_SYSTEM/Edge_TTS_Learning_System.md
   +150      New node documenting Edge TTS system

A  07_SYSTEM/Audio_Systems_Comparison.md
   +80       New comparison node

4 files changed, 249 insertions(+), 5 deletions(-)
```

---

## POST-INGESTION STATE

**BRAIN_OS Knowledge Graph:**
```
02_PROJECTS/
├── Custom_Agent_TTS.md [UPDATED 2026-05-03]
└── ...

07_SYSTEM/
├── Tools_Registry.md [UPDATED 2026-05-03]
├── Edge_TTS_Learning_System.md [CREATED 2026-05-03]
├── Audio_Systems_Comparison.md [CREATED 2026-05-03]
├── PowerShell_Aliases.md [no changes]
└── ...

10_CHATS/
└── 2026-05-03_Obsidian_MCP_Fix_Audio_Systems.md [SOURCE]
```

**Links Established:**
- Edge_TTS_Learning_System ↔ Custom_Agent_TTS
- Edge_TTS_Learning_System ↔ Audio_Systems_Comparison
- Audio_Systems_Comparison ↔ Custom_Agent_TTS
- All point back to session compile in 10_CHATS/

---

## KEY OUTCOMES

✅ **No manual copying** - Claude routed all knowledge automatically
✅ **No duplicate data** - SKIP strategy prevented redundant entries
✅ **Smart corrections** - REPLACE strategy fixed wrong cost info
✅ **New nodes created** - System recognized missing documentation
✅ **Links maintained** - Wiki-link graph stays connected
✅ **Clean git history** - Single commit, reviewable diff
✅ **Zero knowledge lost** - Everything from session captured

**This is what Option B (Fully Automated) looks like in practice.**
