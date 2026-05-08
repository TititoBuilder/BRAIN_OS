# OBSIDIAN QUICK REFERENCE — BRAIN_OS
> Created: May 2026 | Cristian's personal reference

---

## CORE CONCEPTS

### Semantic
"Relating to meaning." Projects are the semantic center = where raw session data becomes understood knowledge.

### Markdown (.md)
Plain text with formatting symbols:
  # Title           → big heading
  ## Section        → smaller heading
  **bold**          → bold
  - item            → bullet
  [[NoteName]]      → wiki-link (Obsidian only)
  ![[NoteName]]     → embed (paste content inline)

### YAML Metadata
The ID card of every note. Lives between --- at the top:
  ---
  tags: [system, protocol]
  created: 2026-05-03
  version: 2
  ---
Obsidian reads this to power search, graph colors, and filtering.
You edit it visually via the Properties panel (top of every note).

### Protocol vs Script
  Protocol = rules + decisions (plain English document, tells Claude Code WHAT to do)
  Script   = executable code (runs commands, tells the system HOW to do it)

---

## THE BRAIN_OS FLOW

  Session ends
       ↓
  YOU run session_close.py              ← your decision (C:\BRAIN_OS\09_TOOLS\)
       ↓
  10_CHATS gets the compiled .md file
       ↓
  YOU tell Claude Code: "run ingestion protocol"  ← your decision
       ↓
  KNOWLEDGE_INGESTION_PROTOCOL_V2 guides Claude Code
       ↓
  01_PROJECTS / 02_AGENTS / etc. automatically updated

Scripts:    session_close.py (recorder), ingestion execution (builder)
Protocol:   KNOWLEDGE_INGESTION_PROTOCOL_V2 (blueprint) → lives in 07_SYSTEM
Mode:       Option C — Hybrid Automated + Review Points

---

## KEYBOARD SHORTCUTS

  Ctrl+P            → Command Palette (access EVERY feature)
  Ctrl+O            → Quick open file (fuzzy search)
  Ctrl+Shift+F      → Search all notes full-text
  Ctrl+G            → Global graph view
  Ctrl+Alt+G        → Local graph (current note only)
  Ctrl+N            → New note
  Ctrl+E            → Toggle edit / preview mode
  Ctrl+B            → Toggle left sidebar
  Ctrl+Shift+B      → Toggle right sidebar
  Ctrl+\            → Split pane vertical
  Alt+← / Alt+→     → Navigate back / forward
  Ctrl+click link   → Open in new split pane
  Ctrl+hover link   → Preview note without opening

---

## TAGS — EVERYTHING YOU NEED TO KNOW

Tags are searchable labels. They give notes multiple identities beyond their folder location.

  Type #tagname anywhere in a note → auto-registered. No setup needed.

USES:
  tag:#protocol         → find every protocol doc
  tag:#active           → find all active projects
  tag:#broken           → find known broken things
  tag:#todo             → find action items
  tag:#option-c         → find all hybrid-mode configs
  tag:#system           → find vault infrastructure notes

TAGS vs FOLDERS:
  Folder = physical home    (one note = one folder only)
  Tag    = logical identity  (one note = unlimited tags)

  Example:
    session_2026-05-06.md lives in → 10_CHATS (folder)
    But is also findable via       → #bdf #lancedb #bug-fix (tags)

SEARCH SYNTAX:
  tag:#system                       → all system notes
  tag:#active path:01_PROJECTS      → active notes inside projects folder
  content:"LanceDB" tag:#bdf        → LanceDB mentions in BDF notes

---

## LINKS — THE POWER SYSTEM

  [[Note Name]]                 → link to a note
  [[Note Name|Display Text]]    → link with custom label
  [[Note Name#Heading]]         → link to a specific section
  ![[Note Name]]                → embed (show content inline)
  ![[image.png]]                → embed an image

Backlinks are automatic:
  If Note A links to Note B → Note B knows about it (visible in right sidebar)
  This is how the graph builds itself.

---

## GRAPH VIEW

  Ctrl+G            → Open global graph
  Ctrl+Alt+G        → Open local graph (current note)

Controls panel (inside graph, top-left):
  Filters   → show/hide notes by tag, folder, path
  Groups    → color-code nodes (your 12-color system lives here)
  Display   → adjust node size, link thickness
  Forces    → control node attraction/repulsion

Interactions:
  Scroll              → zoom in/out
  Click + drag        → pan
  Click node          → open note
  Hover node          → highlight connections
  Ctrl+click node     → open in new pane

Graph health check:
  Node with few connections = underdocumented or not linked properly
  Node with many connections = important hub in your knowledge system

---

## FILE EXPLORER TIPS

  Right-click file/folder   → rename, move, delete, create from template
  Drag and drop             → reorganize
  Pin files                 → stay at top of explorer
  Ctrl+click any [[link]]   → open note in split pane (side by side reading)

---

## PROPERTIES PANEL (right sidebar)

Shows for current note:
  Backlinks   → every note that links TO this note
  Outlinks    → every note this note links TO
  Tags        → all tags on this note
  Properties  → YAML fields (editable visually)

---

## CANVAS FILES (.canvas)

Infinite visual boards. Your Main_Canvas in 00_DASHBOARD is one.
  - Place notes as cards (linked to real .md files)
  - Add text cards, images, PDFs, web links
  - Draw arrows between cards with labels
  - Color-code cards and groups

---

## VAULT STRUCTURE (BRAIN_OS)

  00_DASHBOARD    → Main_Canvas (visual map of everything)
  01_PROJECTS     → Project knowledge nodes
  02_AGENTS       → Agent documentation
  03_APIS         → External connections map
  04_WORKFLOWS    → Process flows
  06_TEMPLATES    → Reusable note templates
  07_SYSTEM       → Infrastructure docs (protocols, shortcuts, registry)
  08_TEMPLATES    → Session compile templates
  08_TRIGGERS     → Automation trigger docs
  09_TOOLS        → Scripts (session_close.py lives here)
  10_CHATS        → Raw session compiles (knowledge entry point)

Knowledge flows: 10_CHATS → (ingestion) → 01_PROJECTS outward

---

## QUICK HEALTH CHECKS

  Are projects being updated?     Check: do project nodes link back to recent 10_CHATS notes?
  Is a tag working?               Search: tag:#tagname — should return results
  Is a link broken?               Broken links show as red/unresolved in graph
  Is a note isolated?             Graph: nodes with zero connections = orphaned notes

---
