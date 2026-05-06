# Claude Code Implementation Guide — Option C Knowledge Ingestion

**Purpose:** Instructions for Claude Code to execute hybrid automated ingestion with intelligent flagging.

---

## System Overview

Claude Code will:
1. Load session compile with INGESTION MAP
2. Extract knowledge pieces
3. Apply auto-handle rules (process without review)
4. Flag complex cases (present for user review)
5. Execute approved changes
6. Git commit with clean diff

---

## Execution Command

**User runs in C:\BRAIN_OS:**
```powershell
claude
```

**User says:**
```
Execute knowledge ingestion for [session-file.md] using KNOWLEDGE_INGESTION_PROTOCOL_V2 (Option C)
```

---

## Implementation Steps

### STEP 1: Load and Parse

**Claude Code actions:**
```
1. Read session compile from 10_CHATS/[session-file.md]
2. Extract INGESTION MAP section
3. Parse each entry:
   - Target node
   - Section
   - Merge strategy
   - Content summary
   - Supersedes info
   - Assessment flags
```

### STEP 2: Classify Each Piece

**For each knowledge piece, check:**

```python
def classify_piece(piece):
    # Check auto-handle rules first
    if is_simple_append(piece):
        return "AUTO_HANDLE", "APPEND"
    
    if is_clear_correction(piece):
        return "AUTO_HANDLE", "REPLACE"
    
    if is_duplicate(piece):
        return "AUTO_HANDLE", "SKIP"
    
    if is_single_destination(piece):
        return "AUTO_HANDLE", "UPDATE"
    
    # Check flag rules
    if has_conflicts(piece):
        return "FLAG", "CONFLICT"
    
    if is_multi_destination(piece):
        return "FLAG", "MULTI_NODE"
    
    if is_cross_domain(piece):
        return "FLAG", "CROSS_DOMAIN"
    
    if is_financial_change(piece):
        return "FLAG", "COST_PRICING"
    
    if is_architecture_pivot(piece):
        return "FLAG", "ARCHITECTURE"
    
    if needs_archival_decision(piece):
        return "FLAG", "ARCHIVAL"
    
    # Edge case - escalate
    return "UNKNOWN", "ESCALATE"
```

### STEP 3: Process Auto-Handle Queue

**For each auto-handle piece:**

```python
def auto_handle(piece, strategy):
    node_path = f"C:\\BRAIN_OS\\{piece.destination}"
    
    if strategy == "APPEND":
        append_to_section(node_path, piece.section, piece.content)
        update_timestamp(node_path)
    
    elif strategy == "REPLACE":
        replace_section(node_path, piece.section, piece.content)
        add_historical_note(node_path, piece.supersedes)
        update_timestamp(node_path)
    
    elif strategy == "SKIP":
        log_skipped(piece, reason="duplicate")
    
    elif strategy == "UPDATE":
        update_section(node_path, piece.section, piece.content)
        update_timestamp(node_path)
    
    log_action(piece, strategy, "AUTO")
```

### STEP 4: Present Flag Queue

**For flagged pieces, show user:**

```
====== INGESTION REVIEW REQUIRED ======

Session: [session-file.md]
Flagged Items: [count]

--- ITEM 1 of [count] ---
Type: [CONFLICT|MULTI_NODE|etc.]
Priority: [HIGH|MEDIUM|LOW]
Node: [target-node.md]
Section: [section-name]

[Details specific to flag type]

Suggested Resolution:
  [What system recommends]

Affected Nodes:
  - [list of dependent nodes]

Your Decision:
  [1] Approve suggested resolution
  [2] Modify resolution
  [3] Skip this update
  [4] Manual edit (open file in editor)

Choice: _
```

**Wait for user input:** 1, 2, 3, or 4

### STEP 5: Execute Approved Flags

**Process user decisions:**

```python
def execute_flag(piece, user_choice):
    if user_choice == 1:  # Approve
        apply_suggested_resolution(piece)
        learn_pattern(piece, approved=True)
    
    elif user_choice == 2:  # Modify
        modified_resolution = get_user_modification()
        apply_modified_resolution(piece, modified_resolution)
        learn_pattern(piece, approved=False, modification=modified_resolution)
    
    elif user_choice == 3:  # Skip
        log_skipped(piece, reason="user_declined")
        learn_pattern(piece, approved=False)
    
    elif user_choice == 4:  # Manual
        open_in_editor(piece.destination)
        wait_for_manual_edit()
        log_manual_edit(piece)
```

### STEP 6: Verify Integrity

**Post-ingestion checks:**

```python
def verify_integrity():
    checks = {
        "broken_links": scan_for_broken_wikilinks(),
        "timestamps": verify_all_updated_timestamps(),
        "dependencies": check_cross_references(),
        "git_status": check_uncommitted_changes()
    }
    
    if any(checks.values()):
        report_issues(checks)
        return False
    
    return True
```

### STEP 7: Git Commit

**Commit with descriptive message:**

```bash
# Auto-generated commit message
git add [all modified files]
git commit -m "ingest: [session-title] → [summary]

Auto-handled: [count] pieces
Flagged & approved: [count] pieces

- [Node1]: [what changed]
- [Node2]: [what changed]
- [Node3]: [created new]"

git push origin main
```

---

## Auto-Handle Rule Implementations

### Rule 1: Simple Append

```python
def is_simple_append(piece):
    return (
        piece.destination_count == 1 and
        not has_conflicts(piece) and
        piece.section_exists and
        piece.strategy == "APPEND"
    )
```

### Rule 2: Clear Correction

```python
def is_clear_correction(piece):
    return (
        piece.destination_count == 1 and
        piece.strategy == "REPLACE" and
        piece.supersedes is not None and
        not has_cross_dependencies(piece)
    )
```

### Rule 3: Duplicate Detection

```python
def is_duplicate(piece):
    node = load_node(piece.destination)
    return content_exists_identically(node, piece.content)
```

### Rule 4: Single-Destination Update

```python
def is_single_destination(piece):
    return (
        piece.destination_count == 1 and
        piece.section_exists and
        not has_conflicts(piece) and
        not affects_multiple_domains(piece)
    )
```

---

## Flag Rule Implementations

### Flag 1: Conflicts Detected

```python
def has_conflicts(piece):
    node = load_node(piece.destination)
    existing_content = get_section_content(node, piece.section)
    
    return contradicts(piece.content, existing_content)
```

### Flag 2: Multi-Destination Routing

```python
def is_multi_destination(piece):
    return piece.destination_count >= 3
```

### Flag 3: Cross-Domain Impact

```python
def is_cross_domain(piece):
    domains = get_affected_domains(piece)
    return len(domains) >= 2
```

### Flag 4: Cost/Pricing Change

```python
def is_financial_change(piece):
    financial_keywords = ["cost", "price", "paid", "free", "$", "charge"]
    return any(kw in piece.content.lower() for kw in financial_keywords)
```

### Flag 5: Architecture Pivot

```python
def is_architecture_pivot(piece):
    pivot_indicators = [
        "replaced",
        "deprecated",
        "adopted",
        "rejected",
        "migration",
        "refactor"
    ]
    return any(ind in piece.content.lower() for ind in pivot_indicators)
```

### Flag 6: Archival Decision

```python
def needs_archival_decision(piece):
    return (
        piece.supersedes is not None and
        has_historical_value(piece.supersedes) and
        piece.strategy == "REPLACE"
    )
```

---

## Learning System Implementation

**Track patterns:**

```python
class IngestionLearning:
    def __init__(self):
        self.approval_history = []
        self.pattern_rules = []
    
    def learn_pattern(self, piece, approved, modification=None):
        record = {
            'piece': piece,
            'approved': approved,
            'modification': modification,
            'timestamp': datetime.now()
        }
        self.approval_history.append(record)
        
        # After 5 approvals of similar pattern
        similar = self.find_similar_approvals(piece, count=5)
        if len(similar) >= 5:
            self.create_auto_handle_rule(piece, similar)
    
    def create_auto_handle_rule(self, piece, similar_cases):
        pattern = extract_pattern(similar_cases)
        rule = {
            'pattern': pattern,
            'confidence': calculate_confidence(similar_cases),
            'created': datetime.now()
        }
        self.pattern_rules.append(rule)
        
        # Log to file
        save_learned_rule(rule)
```

---

## Example Execution

**User input:**
```
Execute knowledge ingestion for 2026-05-03_Knowledge_Pipeline_Meta_Session.md using Option C
```

**Claude Code output:**
```
Loading session: 2026-05-03_Knowledge_Pipeline_Meta_Session.md
Extracting INGESTION MAP... ✓
Found 8 knowledge pieces

Classifying...
  - Auto-handle: 5 pieces (62%)
  - Flagged: 3 pieces (38%)

Processing auto-handle queue...
  ✓ Updated AI_Engineering.md (MCP ecosystem)
  ✓ Updated Data_Science.md (Knowledge Pipeline status)
  ✓ Skipped PowerShell_Aliases.md (duplicate)
  ✓ Updated KNOWLEDGE_INGESTION_PROTOCOL.md (example)
  ✓ Updated Custom_Agent_TTS.md (Kokoro cost note)

Auto-handle complete: 5/5 successful

Presenting flagged items for review...

====== INGESTION REVIEW REQUIRED ======

Session: 2026-05-03_Knowledge_Pipeline_Meta_Session
Flagged Items: 3

--- ITEM 1 of 3 ---
Type: MULTI_NODE
Priority: MEDIUM
Nodes: AI_Engineering.md, Data_Science.md, Creative_Systems.md
Update: 3-domain architecture created

Suggested Resolution:
  Add wiki-link to 01_DOMAINS/ in each domain node

Affected Nodes:
  - All 3 domain master dashboards

Your Decision:
  [1] Approve suggested resolution
  [2] Modify resolution
  [3] Skip this update

Choice: 1

✓ Approved

--- ITEM 2 of 3 ---
[next flag]

Choice: 1

✓ Approved

--- ITEM 3 of 3 ---
[final flag]

Choice: 1

✓ Approved

Executing approved changes...
  ✓ Updated AI_Engineering.md
  ✓ Updated Data_Science.md
  ✓ Updated Creative_Systems.md

Verifying integrity...
  ✓ No broken links
  ✓ Timestamps updated
  ✓ Dependencies checked

Committing changes...
  git add -A
  git commit -m "ingest: knowledge-pipeline-meta-session → validated automation

  Auto-handled: 5 pieces (62%)
  Flagged & approved: 3 pieces (38%)

  - AI_Engineering: Obsidian MCP operational, Kokoro note
  - Data_Science: Knowledge Pipeline operational, 01_DOMAINS added
  - Creative_Systems: Domain architecture link added"

  git push origin main

✓ Ingestion complete

SUMMARY:
  Total pieces: 8
  Auto-handled: 5 (62%)
  Flagged: 3 (38%)
  Approved: 3 (100%)
  Skipped: 0
  Rollbacks: 0

Review changes: git diff HEAD~1
```

---

## Error Handling

**If something fails:**

```python
try:
    execute_ingestion(session_file)
except ConflictUnresolvable as e:
    print(f"ERROR: Cannot auto-resolve conflict in {e.node}")
    print(f"Manual review required: {e.details}")
    exit_with_partial_commit()

except NodeNotFound as e:
    print(f"ERROR: Target node doesn't exist: {e.node}")
    print(f"Create node first or modify INGESTION MAP")
    exit_without_commit()

except IntegrityCheckFailed as e:
    print(f"ERROR: Post-ingestion integrity check failed")
    print(f"Issues: {e.failures}")
    print(f"Rolling back changes...")
    git_reset_hard()
    exit_clean()
```

---

## Performance Tracking

**Log to file after each ingestion:**

```json
{
  "session": "2026-05-03_Knowledge_Pipeline_Meta_Session.md",
  "timestamp": "2026-05-03T14:30:00Z",
  "stats": {
    "total_pieces": 8,
    "auto_handled": 5,
    "flagged": 3,
    "approved": 3,
    "modified": 0,
    "skipped": 0,
    "rollbacks": 0
  },
  "auto_handle_rate": 0.62,
  "flag_rate": 0.38,
  "approval_rate": 1.0,
  "git_commit": "a7f3c9d",
  "execution_time": "45s"
}
```

---

## Connected Files
- KNOWLEDGE_INGESTION_PROTOCOL_V2.md (protocol rules)
- SESSION_COMPILE_TEMPLATE_V2.md (source format)
- Past_Chat_Compilation_Protocol.md (workflow)
