---
tags: [system, protocol, automation, knowledge-ingestion, intelligence, option-c]
created: 2026-05-03
updated: 2026-05-03
version: 2.0
---

# Knowledge Ingestion Protocol V2 — Hybrid Intelligence with Review Points

**Mode:** Option C (Hybrid Automated + Review Points)

**Philosophy:** Automate routine knowledge flow, flag complex cases for human judgment.

---

## Core Principle

**The system handles 90% automatically. You review the 10% that requires human judgment.**

Fast execution + quality checkpoints = optimal knowledge recovery velocity.

---

## Auto-Handle Rules (No Review Needed)

System automatically processes these cases:

### 1. Simple Appends
**Criteria:**
- New feature added to existing project
- No conflicts with existing documentation
- Single destination node
- Clear section to append to

**Action:** APPEND with timestamp

**Example:**
```
New: "Built jump_to_timecode tool for Resolve"
Target: Resolve_MCP.md → Tools section
Action: Append "jump_to_timecode (2026-05-10)" to tool list
```

### 2. Clear Corrections
**Criteria:**
- Old info demonstrably wrong
- New info demonstrably right
- No cross-dependencies
- Single node affected

**Action:** REPLACE + historical note

**Example:**
```
Old: "Kokoro costs money via Claude API"
New: "Kokoro is 100% FREE (local GPU)"
Action: Replace cost section, add note about previous confusion
```

### 3. Duplicate Detection
**Criteria:**
- Content already documented identically
- No new information added
- Same facts, same details

**Action:** SKIP

**Example:**
```
New: "Edge TTS uses en-US-GuyNeural voice"
Existing: Edge_TTS_Learning_System.md already documents this
Action: Skip (no changes needed)
```

### 4. Single-Destination Updates
**Criteria:**
- Affects only one node
- Clear target section
- No ripple effects to other nodes

**Action:** UPDATE with appropriate strategy

**Example:**
```
New: "Obsidian MCP now operational with 11 tools"
Target: Tools_Registry.md → Obsidian MCP entry
Action: Update status, add tool count
```

---

## FLAG for Review (Human Judgment Required)

System flags these cases and waits for approval:

### 1. Conflicts Detected ⚠️
**Criteria:**
- New info contradicts existing info
- Unclear which is correct
- Temporal ambiguity (which is more recent?)

**Flag Message:**
```
CONFLICT DETECTED:
Node: Custom_Agent_TTS.md
Section: Cost
Old (2026-03-25): "Kokoro has associated costs"
New (2026-05-03): "Kokoro is 100% FREE"

SUGGESTED RESOLUTION: REPLACE old with new + historical note
AFFECTED NODES: Audio_Systems_Comparison.md also mentions cost

Approve? [Y/N/Modify]
```

### 2. Multi-Destination Routing ⚠️
**Criteria:**
- Updates 3+ nodes simultaneously
- Cross-domain impacts (AI + Data + Creative)
- Complex dependency chains

**Flag Message:**
```
MULTI-NODE UPDATE:
Source: "Obsidian MCP fix"
Destinations:
  - Tools_Registry.md (update status)
  - AI_Engineering.md (update MCP ecosystem)
  - KNOWLEDGE_INGESTION_PROTOCOL.md (add example)

SUGGESTED ROUTING: All 3 updates
MERGE STRATEGIES: UPDATE, UPDATE, ENHANCE

Approve? [Y/N/Modify]
```

### 3. Cross-Domain Impacts ⚠️
**Criteria:**
- Affects AI Engineering + Data Science domains
- Affects Data Science + Creative Systems domains
- Affects all 3 domains

**Flag Message:**
```
CROSS-DOMAIN IMPACT:
Knowledge: "Knowledge Pipeline built"
Domains Affected:
  - AI_Engineering (automation system)
  - Data_Science (knowledge organization)
  - Creative_Systems (not affected)

ROUTING:
  - AI_Engineering.md → append to tools
  - Data_Science.md → update Knowledge_Pipeline status

Approve? [Y/N/Modify]
```

### 4. Cost/Pricing Changes ⚠️
**Criteria:**
- Financial information updated
- Cost model changed
- Pricing clarification

**Flag Message:**
```
FINANCIAL INFO CHANGE:
Type: Cost clarification
Old: "Charges detected in logs"
New: "Kokoro FREE, charges were Claude Opus compilation"

PRIORITY: HIGH (financial impact)
AFFECTED PROJECTS: Custom_Agent, BDF

Approve? [Y/N/Modify]
```

### 5. Architecture Pivots ⚠️
**Criteria:**
- Fundamental design change
- Tool replacement
- Workflow redesign

**Flag Message:**
```
ARCHITECTURE CHANGE:
Type: Tool evolution
Old: "gTTS for audio generation"
New: "Edge TTS adopted (gTTS rejected)"

REASONING: Voice quality (robotic → natural)
AFFECTED SYSTEMS: Audio learning pipeline

Approve? [Y/N/Modify]
```

### 6. Archival Decisions ⚠️
**Criteria:**
- Old info still potentially valuable
- Historical context needed
- Uncertain if superseded or archived

**Flag Message:**
```
ARCHIVAL DECISION:
Content: "Resolve MCP had 11 tools initially"
Current: "Resolve MCP has 52 tools"

QUESTION: Archive "11 tools" state or replace?
SUGGESTION: ARCHIVE (historical value for evolution story)

Approve? [Y/N/Modify]
```

---

## Learning System (Pattern Recognition)

**System improves over time based on your approvals:**

### Phase 1: Tuning (First 10 Chats)
**Flag Threshold:** CONSERVATIVE (flag 30-40% of cases)

**What system learns:**
- Which conflicts you approve auto-resolution for
- Which multi-node updates you trust
- Which domains cross-reference frequently
- Your preference for REPLACE vs ARCHIVE

### Phase 2: Calibration (Next 20 Chats)
**Flag Threshold:** MODERATE (flag 15-20%)

**System confidence grows:**
- Auto-handles patterns you approved 3+ times
- Only flags genuinely ambiguous cases
- Learns your merge strategy preferences

### Phase 3: Production (Remaining Chats)
**Flag Threshold:** MINIMAL (flag 5-10%)

**System operates autonomously:**
- Auto-handles 90% of routine cases
- Flags only truly complex decisions
- You review exceptions, not rules

---

## Execution Workflow (Option C)

```
INPUT: Compiled session with INGESTION MAP
  ↓
STEP 1: Extract all knowledge pieces
  ↓
STEP 2: For each piece, check auto-handle rules
  ↓
  ┌─ YES → Auto-handle queue
  └─ NO → Check flag rules
      ↓
      ┌─ YES → Flag for review queue
      └─ NO → Error (edge case, escalate)
  ↓
STEP 3: Execute auto-handle queue
  - Apply APPEND/REPLACE/MERGE/SKIP
  - Update timestamps
  - Maintain links
  ↓
STEP 4: Present flag queue to user
  - Show conflicts
  - Suggest resolutions
  - Wait for approval
  ↓
STEP 5: Execute approved flags
  - Apply user decisions
  - Update affected nodes
  ↓
STEP 6: Verify integrity
  - Check broken links
  - Validate timestamps
  - Confirm dependencies
  ↓
STEP 7: Git commit
  - Descriptive message
  - Clean, reviewable diff
  ↓
OUTPUT: Knowledge ingested, flagged items logged
```

---

## Flag Review Interface

**When system flags items, you see:**

```
====== INGESTION REVIEW REQUIRED ======

Session: 2026-05-03_Knowledge_Pipeline_Meta_Session
Flagged Items: 3

--- ITEM 1 of 3 ---
Type: CONFLICT
Priority: HIGH
Node: Custom_Agent_TTS.md
Section: Cost

Old (2026-03-25):
  "TTS generation has associated costs"

New (2026-05-03):
  "Kokoro TTS is 100% FREE (local GPU, zero API costs)"

Suggested Resolution:
  REPLACE old with new
  ADD historical note: "Previously documented as having costs, 
  corrected May 3, 2026 after full timeline analysis"

Affected Nodes:
  - Audio_Systems_Comparison.md (mentions Kokoro cost)

Your Decision:
  [1] Approve suggested resolution
  [2] Modify resolution
  [3] Skip this update
  [4] Manual edit (open file in editor)

Choice: _
```

**Your response:** Just type `1` and press Enter

System learns: "Kokoro cost corrections auto-approve in future"

---

## Learning Patterns (System Improves)

**After 5 approvals of similar cases:**

```
Pattern Detected: Cost corrections with historical notes
Auto-Handle Rule Created:
  IF: Financial info corrected
  AND: Historical note suggested
  AND: No cross-dependencies
  THEN: Auto-approve (no flag needed)

Next similar case: Auto-handled
Flag rate: 30% → 25%
```

**After 10 approvals:**

```
Pattern Detected: Multi-node MCP status updates
Auto-Handle Rule Created:
  IF: MCP status changed
  AND: Updates Tools_Registry + domain dashboards
  AND: Clear before/after state
  THEN: Auto-approve routing

Next similar case: Auto-handled
Flag rate: 25% → 18%
```

**After 20 approvals:**

```
Pattern Detected: Your preferences learned
Auto-Handle Rules: 15 patterns recognized
Flag rate: 18% → 10%

System now handles:
  - Cost clarifications (historical notes)
  - Tool status updates (cross-node)
  - Feature additions (clear append)
  - Simple corrections (single-node)
```

---

## Rollback Safety Net

**Every ingestion = git commit**

**If something goes wrong:**

```powershell
# See what changed
git diff HEAD~1

# Looks bad? Rollback immediately
git revert HEAD

# Or rollback specific file
git checkout HEAD~1 -- path/to/file.md

# System learns from rollback
System Notes: "User reverted cost clarification auto-approval"
Adjustment: Flag similar cases next time
```

**Learning from rollbacks:**
- System tracks which auto-approvals get reverted
- Adjusts confidence thresholds
- Re-flags similar patterns until pattern confirmed

---

## Performance Metrics

**System tracks:**
- Auto-handle rate (target: 90%)
- Flag rate (target: 10%)
- Approval rate (target: 95%+ of flagged items)
- Rollback rate (target: <1%)

**Monthly audit:**
```
INGESTION PERFORMANCE REPORT
Month: May 2026

Sessions compiled: 45
Knowledge pieces: 387
Auto-handled: 352 (91%)
Flagged: 35 (9%)
  - Approved: 34 (97%)
  - Modified: 1 (3%)
Rollbacks: 0 (0%)

Top flag reasons:
  1. Multi-node routing (40%)
  2. Cost clarifications (25%)
  3. Architecture changes (20%)
  4. Conflicts (15%)

System confidence: HIGH
Recommendation: Maintain current thresholds
```

---

## Claude Code Integration

**Implementation:** Claude Code executes ingestion with flag checkpoints

**Standard workflow:**

```bash
# User runs in C:\BRAIN_OS
claude

# In Claude Code, user says:
"Execute knowledge ingestion for 2026-05-03_session.md using Option C"

# Claude Code:
1. Loads session compile
2. Extracts knowledge pieces
3. Applies auto-handle rules
4. Flags complex cases
5. PAUSES and presents flags
6. Waits for user input (approve/modify/skip)
7. Executes approved changes
8. Git commits
9. Reports what changed
```

**User sees:**
```
Auto-handled: 18 pieces (85%)
Flagged for review: 3 pieces (15%)

--- FLAG 1 of 3 ---
[conflict details]

Your choice: 1

--- FLAG 2 of 3 ---
[multi-node routing]

Your choice: 1

--- FLAG 3 of 3 ---
[architecture change]

Your choice: 2 (modify)

Modification: [user types change]

Executing approved changes...
✓ Updated Custom_Agent_TTS.md
✓ Updated Tools_Registry.md
✓ Created Edge_TTS_Learning_System.md

Git commit: a7f3c9d
Changes: 3 files, 94 insertions, 12 deletions

Review: git diff HEAD~1
```

---

## Critical Safeguards

1. **Financial info always flagged** (never auto-approve cost/pricing)
2. **Architecture changes always flagged** (human approves design pivots)
3. **First 10 sessions conservative** (high flag rate for learning)
4. **Git commit per ingestion** (always reversible)
5. **Monthly audit** (review performance, adjust thresholds)

---

## Connected to
- [[Session_Protocol]]
- [[Session_Compile_Template_V2]]
- [[Past_Chat_Compilation_Protocol]]
- [[BRAIN_OS]]
