---
tags: [protocol, system, knowledge-recovery, past-chats]
created: 2026-05-03
updated: 2026-05-03
---

# Past Chat Compilation Protocol

**Purpose:** Systematically recover knowledge from past Claude conversations and ingest into BRAIN_OS.

**Scope:** Works for any past chat, session archive, or compile document.

---

## When to Compile Past Chats

### High-Priority Sessions (Do These First)
- **Major system builds** (Edge TTS creation, Resolve MCP expansion, venv rebuilds)
- **Architecture decisions** (MCP ecosystem setup, project organization)
- **Problem solutions** (bugs fixed, blockers removed, major troubleshooting)
- **Cost/pricing clarifications** (like Kokoro free vs paid confusion)

### Medium-Priority Sessions
- **Feature additions** (new tools, new workflows)
- **Learning sessions** (understanding new concepts, terminology)
- **Optimization work** (workflow improvements, efficiency gains)

### Low-Priority Sessions (Just-In-Time)
- **Quick fixes** (minor bugs, small changes)
- **Routine work** (standard tasks, repetitive operations)
- **Experiments** (tests, explorations that didn't lead anywhere)

---

## How to Compile a Past Chat

### Method 1: Direct from Chat URL

**Step 1: Open the chat**
- Navigate to the chat URL (e.g., https://claude.ai/chat/[chat-id])
- Conversation history loads in interface

**Step 2: Request compilation**
```
"Compile this session using SESSION_COMPILE_TEMPLATE_V2"
```

**Step 3: Claude fills the template**
- Analyzes full conversation history
- Fills all sections (What Was Built, What Was Decided, etc.)
- Creates INGESTION MAP with routing instructions

**Step 4: Deploy and execute**
- Download the session compile .md file
- Move to `C:\BRAIN_OS\10_CHATS\`
- Pass to Claude Code for automated ingestion
- Review git diff

**Step 5: Done**
- Knowledge recovered
- BRAIN_OS updated
- Git commit preserves changes

---

### Method 2: From Session Archive (09_TOOLS/)

**Step 1: Locate archive**
```
C:\BRAIN_OS\09_TOOLS\
├── 2026-04-30_Project_Standardization.txt
├── 2026-04-18_Audio_Learning_System.txt
└── [other session archives]
```

**Step 2: Upload to chat**
- Upload the .txt session archive
- Or paste content into chat

**Step 3: Request compilation**
```
"Compile this session using SESSION_COMPILE_TEMPLATE_V2"
```

**Step 4-5: Same as Method 1**

---

### Method 3: From Pre-Existing Session Compile

**Step 1: Locate compile**
- Google Drive session compiles folder
- Or any .md/.txt compile you have

**Step 2: Upload/paste**
- Upload file or paste content

**Step 3: Request enhanced compilation**
```
"Enhance this session compile using SESSION_COMPILE_TEMPLATE_V2 and create INGESTION MAP"
```

**Step 4-5: Same as Method 1**

---

## Finding Past Chats

### Source 1: conversation_search Tool
```
Use conversation_search to find chats by topic:
- "kokoro audio generation"
- "resolve mcp expansion"
- "venv rebuild corruption"
```

**Returns:** Chat snippets with URIs and URLs

### Source 2: recent_chats Tool
```
Use recent_chats to find by date range:
- Last 20 chats
- Specific date range (before/after)
- Sort chronological or reverse
```

**Returns:** Chat metadata with URIs

### Source 3: 09_TOOLS/ Archives
```
dir C:\BRAIN_OS\09_TOOLS\
```

**Returns:** Existing session archives (plain text)

### Source 4: Google Drive
```
Search Google Drive for session compiles
```

**Returns:** Previously created compile documents

---

## Compilation Standards

### What to Include
✅ **Complete context** - Full "What Was Built" section  
✅ **All decisions** - Architecture, tools, standards  
✅ **Every problem solved** - Bugs, blockers, errors  
✅ **Patterns emerged** - Workflows, best practices  
✅ **INGESTION MAP** - Required for automation  
✅ **Book candidates** - CA Book, BDF Book extracts  

### What to Skip
❌ **Chat meta-commentary** - "I understand", "Let me help"  
❌ **Redundant explanations** - Don't repeat same info  
❌ **Off-topic tangents** - Stick to session knowledge  

---

## Automated Ingestion After Compilation

**Standard Process:**
1. Session compiled → .md file created
2. Move to `C:\BRAIN_OS\10_CHATS\`
3. Pass INGESTION MAP to Claude Code
4. Claude Code executes routing
5. Git commit with changes
6. User reviews `git diff HEAD~1`

**Ingestion Actions:**
- CREATE new nodes (projects, systems)
- UPDATE existing nodes (status changes)
- APPEND new content (features, decisions)
- REPLACE wrong info (corrections)
- SKIP duplicates (already documented)

---

## Batch Compilation Strategy

### Option A: Systematic (Chronological)
1. List all past sessions (conversation_search + 09_TOOLS/)
2. Sort by date (oldest to newest)
3. Compile one per day
4. Track progress: compiled_sessions.txt

**Pro:** Nothing missed, complete history  
**Con:** Time-intensive upfront

### Option B: Priority-First (High-Value)
1. Identify critical sessions (major builds, key decisions)
2. Compile those first
3. Rest on-demand as needed

**Pro:** Fast recovery of important knowledge  
**Con:** Some sessions might never get compiled

### Option C: Just-In-Time (As Referenced)
1. Don't pre-compile everything
2. When you reference old work, compile that session
3. Gradually build coverage

**Pro:** Minimal upfront work  
**Con:** Easy to forget what exists

---

## Recommended Approach (Hybrid)

**Week 1: High-Priority Recovery**
- Compile 5-10 most critical sessions
- Major system builds (Edge TTS, Resolve MCP, venv rebuilds)
- Key architecture decisions
- Major problem solutions

**Week 2+: Just-In-Time**
- Compile sessions as you reference them
- "What did we do about X?" → find session → compile
- Gradually expand coverage

**Monthly: Gap Analysis**
- Review 09_TOOLS/ for uncompiled archives
- conversation_search for major topics
- Compile any high-value sessions discovered

---

## Quality Checks

**Before Ingestion:**
- [ ] All 10 template sections filled
- [ ] INGESTION MAP complete with strategies
- [ ] Book candidates identified
- [ ] Wiki-links to affected nodes
- [ ] Pending tasks extracted

**After Ingestion:**
- [ ] Git diff reviewed and approved
- [ ] No broken wiki-links
- [ ] Timestamps updated
- [ ] Commit message clear
- [ ] Knowledge searchable in BRAIN_OS

---

## Common Issues

### Issue: "Can't find the chat URL"
**Solution:** Use conversation_search with topic keywords

### Issue: "Session is too long/complex"
**Solution:** Break into multiple compiles if needed (Day 1, Day 2)

### Issue: "Not sure which domain this belongs to"
**Solution:** Can belong to multiple domains - cross-link

### Issue: "Duplicate knowledge already in BRAIN_OS"
**Solution:** INGESTION MAP will detect and SKIP

---

## Progress Tracking

**Create:** `C:\BRAIN_OS\10_CHATS\COMPILATION_PROGRESS.md`

```markdown
# Past Session Compilation Progress

## Completed (Date - Title)
- 2026-05-03 - Knowledge Pipeline Meta-Session ✅
- 2026-04-18 - Audio Learning + Resolve Expansion ✅

## In Progress
- 

## High-Priority Queue
- [Date] - [Topic]
- [Date] - [Topic]

## Medium-Priority Queue
-

## Low-Priority (Just-In-Time)
-
```

---

## Connected to
- [[Knowledge_Ingestion_Protocol]]
- [[Session_Protocol]]
- [[Session_Compile_Template_V2]]
- [[10_CHATS]]
