---
knowledge_os_machine_key: obsidian_workflows
knowledge_os_domain: Knowledge Systems
knowledge_os_status: Mastered
knowledge_os_score: 82
knowledge_os_priority: High
knowledge_os_evidence: BRAIN_OS 00–10 structure, session pipeline operational
knowledge_os_last_touched: '2026-05-24'
---
# Obsidian Workflows

## What It Is
Obsidian is the vault layer of BRAIN_OS — the knowledge OS implemented as a
structured directory of markdown files at C colon backslash BRAIN underscore OS.
The vault follows a zero-through-ten folder taxonomy: meta, domains, projects,
APIs, workflows, canvas, templates, system, sessions, tools, and chats. Every
folder has a declared purpose and nothing lives outside its designated section.

## How It Works
The session pipeline runs at every session close. The active chat is compiled
into a structured session file. session_close.py archives it to the sessions
folder, triggers the knowledge ingestion protocol, and fires a Telegram
confirmation. The ingestion protocol classifies each piece of knowledge as
auto-handle or flagged, applies changes to vault nodes, verifies internal link
integrity, and commits the changes to Git. The morning watchdog at seven fifteen
daily scans for orphaned nodes — files that exist in the vault but are not
linked from any other file. The Obsidian MCP integration, running via
obsidian-mcp, provides eleven tools that let Claude Code read, write, search,
and move vault notes without the Obsidian application open. The vault is fully
Git-backed, which means every update is auditable and Obsidian sync sees a
clean committed state.

## Why It Matters
The vault compensates for the context limitation of AI assistants. No session
exists only in a chat window — every session produces at least one archived
artifact and at least one vault update. The result is that every new session
can start from a documented, searchable record of prior decisions rather than
from memory alone. Writing directly to vault files outside a Git commit risks
corrupting Obsidian sync, which is why all writes go through MCP tools or
Claude Code edits that are immediately committed.

## The Pattern
Every session is atomic: it initializes, does work, and closes with a documented
artifact. Obsidian is the memory layer, not a scratchpad. Anything worth keeping
in a future conversation must be committed to the vault before the session closes.

