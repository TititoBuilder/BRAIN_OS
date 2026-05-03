---
tags: [system, protocol, automation, knowledge-ingestion]
created: 2026-05-03
updated: 2026-05-03
---

# Knowledge Ingestion Protocol — Automated Intelligence Layer

**Purpose:** Automatically route session knowledge to correct BRAIN_OS nodes with smart merge logic.

**Execution:** Fully automated - Claude analyzes, routes, merges, commits. User reviews git diff after.

---

## Core Principle

**No knowledge gets lost. No manual copying. No duplicate data.**

Session compiles flow automatically into the knowledge graph. The system:
- Detects what's new vs changed vs superseded
- Routes content to correct nodes
- Performs intelligent merges (append/replace/update)
- Maintains link integrity
- Preserves history

---

## Routing Matrix: What Goes Where

| Session Section | Target Location | Merge Strategy |
|----------------|-----------------|----------------|
| **What Was Built** | `02_PROJECTS/[project].md` → Implementation | APPEND features, REPLACE if redesign |
| **What Was Decided** | `02_PROJECTS/[project].md` → Decisions | APPEND with date, never replace |
| **Problems Solved** | `02_PROJECTS/[project].md` → Troubleshooting | APPEND with date (history matters) |
| **Patterns Emerged** | `07_SYSTEM/[pattern].md` | MERGE if better, APPEND if new |
| **Commands/Aliases** | `07_SYSTEM/PowerShell_Aliases.md` | REPLACE if changed, APPEND if new |
| **Book Content** | `C:\Knowledge\CA\` or `BDF\` | EXTRACT to chapter drafts |

---

## Merge Strategy Rules

### APPEND (Add New Content)
**When to use:**
- New feature documented
- New problem solved
- New decision made
- Timeline/history matters
- Multiple valid approaches coexist

**How to apply:**
```markdown
## Features (existing content)
- Feature A (added 2026-04-15)
- Feature B (added 2026-04-20)

↓ APPEND ↓

## Features
- Feature A (added 2026-04-15)
- Feature B (added 2026-04-20)
- Feature C (added 2026-05-03)  ← NEW
```

### REPLACE (Correct Wrong Info)
**When to use:**
- Previous info was incorrect
- Architecture fundamentally changed
- Cost/pricing corrected
- Tool deprecated and replaced

**How to apply:**
```markdown
## Cost (old - wrong)
Kokoro TTS costs money via Claude API.

↓ REPLACE ↓

## Cost (corrected 2026-05-03)
Kokoro TTS is 100% FREE (local GPU inference).
Previous confusion: charges were Claude Opus compilation, not TTS.
```

### MERGE (Enhance Existing)
**When to use:**
- New details enhance existing info
- Better explanation of same concept
- Additional context for existing content

**How to apply:**
```markdown
## Setup (existing)
Install dependencies: pip install kokoro

↓ MERGE ↓

## Setup
Install dependencies: 
- `pip install kokoro` (TTS engine)
- `pip install numpy` (audio processing)
- `pip install soundfile` (WAV output)
- Requires CUDA-compatible GPU (RTX series)
```

### SKIP (Already Documented)
**When to use:**
- Content already exists with same details
- No new information provided
- Duplicate across multiple sessions

---

## Delta Detection Logic

```python
# Pseudo-code for automated analysis

def analyze_session_content(session_section, target_node):
    existing_content = read_node(target_node)
    new_content = extract_from_session(session_section)
    
    for item in new_content:
        if item NOT IN existing_content:
            → classify as NEW
        elif item CONTRADICTS existing_content:
            → classify as CORRECTION
        elif item EXPANDS existing_content:
            → classify as ENHANCEMENT
        else:
            → classify as DUPLICATE
    
    return delta_map
```

---

## Supersession Rules

**Date-based precedence:**
```
IF new_session.date > node.last_updated:
    IF content_contradicts:
        → REPLACE old + add correction note
    ELIF content_expands:
        → MERGE enhancement
    ELSE:
        → APPEND new
ELSE:
    → FLAG for manual review (newer info already exists)
```

**Correction notation:**
```markdown
## Section
[Current correct info]

**Historical note:** Previously documented as [old info], corrected [date] after [reason].
```

---

## Node Structure Requirements

Every project/system node MUST have:

```yaml
---
tags: [relevant, tags]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

**Updated field** determines ingestion precedence.

---

## Automated Ingestion Workflow

### Phase 1: Analysis (Claude)
```
1. Load SESSION_COMPILE
2. Identify all affected nodes from INGESTION MAP
3. Load each affected node from BRAIN_OS
4. Generate delta analysis:
   - What's NEW
   - What's CORRECTED
   - What's ENHANCED
   - What's DUPLICATE
```

### Phase 2: Routing (Claude)
```
For each delta:
1. Determine target node + section
2. Choose merge strategy (APPEND/REPLACE/MERGE/SKIP)
3. Build update plan
```

### Phase 3: Execution (Claude)
```
For each node:
1. Apply merges in correct sections
2. Update timestamp
3. Add/verify wiki-links
4. Write updated node
```

### Phase 4: Commit (Claude)
```
1. Git add all changed nodes
2. Commit with descriptive message:
   "ingest: [session-title] → updated [node1], [node2], created [node3]"
3. Push to origin/main
```

### Phase 5: Review (User)
```
User runs:
  git log -1 --stat
  git diff HEAD~1

Review changes, rollback if needed:
  git revert HEAD
```

---

## Link Integrity Maintenance

**After every ingestion:**
```
1. Scan for broken wiki-links [[Node_That_Doesnt_Exist]]
2. Create placeholder nodes for new references
3. Update bidirectional links
4. Verify all [[connections]] resolve
```

---

## Session Compile INGESTION MAP

The SESSION_COMPILE_TEMPLATE includes this section:

```markdown
## INGESTION MAP
<!-- Automated routing for knowledge ingestion -->

### [Node_Name].md
- **Target Section:** [section name]
- **Merge Strategy:** [APPEND|REPLACE|MERGE|SKIP]
- **Reasoning:** [why this strategy]
- **Content Summary:** [brief description]
- **Supersedes:** [what old info this replaces, if any]
```

Claude fills this out during session compile, then executes automatically.

---

## Error Handling

**If ingestion detects:**
- **Conflicting dates** → FLAG for manual review, don't auto-merge
- **Broken links** → Create placeholder, note in commit message
- **Unknown node** → Create from template, link to parent
- **Merge conflict** → Preserve both versions with timestamps, FLAG

---

## Validation Checks

**Before committing ingestion:**
```
✓ All affected nodes have updated timestamps
✓ No broken wiki-links
✓ All content mapped to correct sections
✓ Git diff is reviewable (clean, logical changes)
✓ Commit message describes what changed
```

---

## Example: This Session's Ingestion

**Session:** 2026-05-03 Obsidian MCP Fix + Audio Systems

**Affected Nodes:**
- `Custom_Agent_TTS.md` → Cost clarification (REPLACE)
- `Tools_Registry.md` → Obsidian MCP status update (UPDATE)
- `Edge_TTS_Learning_System.md` → New node creation (CREATE)
- `Audio_Systems_Comparison.md` → New node creation (CREATE)

**Actions Executed:**
1. REPLACE cost section in Custom_Agent_TTS.md
2. UPDATE Obsidian MCP entry in Tools_Registry.md
3. CREATE Edge_TTS_Learning_System.md from template
4. CREATE Audio_Systems_Comparison.md from template
5. UPDATE wiki-links in all affected nodes
6. Commit: "ingest: obsidian-mcp-audio-systems → 2 updated, 2 created"

**User review:** `git diff HEAD~1` shows clean, logical changes

---

## Maintenance

**Weekly:** Review ingestion commit history for patterns
**Monthly:** Refine merge strategies based on outcomes
**Quarterly:** Audit nodes for duplicate/outdated content

---

## Connected to
- [[Session_Protocol]]
- [[Session_Compile_Template]]
- [[Project_Directory]]
- [[Tools_Registry]]
