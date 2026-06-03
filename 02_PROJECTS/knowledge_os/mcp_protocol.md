---
knowledge_os_machine_key: mcp_protocol
knowledge_os_domain: APIs & Protocols
knowledge_os_status: Mastered
knowledge_os_score: 88
knowledge_os_priority: High
knowledge_os_evidence: resolve-mcp-server lazy TCP, 6 MCP servers
knowledge_os_last_touched: '2026-05-24'
---
# MCP Protocol

## What It Is
MCP stands for Model Context Protocol. It is a standard that lets Claude Code
connect to external systems — Obsidian, GitHub, DaVinci Resolve, Google Drive,
Gmail, and Google Calendar — through a unified interface. Instead of bespoke
integrations for each service, every connected system exposes tools under the
naming pattern mcp, double underscore, server name, double underscore, tool name.

## How It Works
Two transport types exist. Stdio spawns the MCP server as a subprocess with no
open port — Obsidian MCP uses this, launched via npx obsidian-mcp pointing at
the vault path. TCP maintains a persistent connection on a fixed port — the
DaVinci Resolve MCP server uses TCP on port nine thousand because Resolve Free
cannot be subprocessed. A bridge script runs inside Resolve's embedded Python
console and listens for TCP messages. Each tool call opens a fresh socket,
executes, and closes with no persistent pool and no leaked connections. Claude
Code reads MCP server configuration from settings.json at startup. Servers
registered under mcpServers appear in the tool list once connected, namespaced
as described. A critical naming distinction applies here: the Obsidian package
is obsidian-mcp, not obs-mcp. The prefix obs belongs to OBS Studio, the
streaming software. Using the wrong package name causes silent failure with no
useful error message at connection time.

## Why It Matters
MCP replaced separate bespoke integration scripts for every external system.
Context7 MCP fetches live library documentation inside Claude Code without a
web search. The Resolve MCP enables scripted DaVinci Resolve control across a
process boundary that would otherwise be closed. Obsidian MCP allows reading
and writing vault notes without the Obsidian application being open. Six servers
run simultaneously in the current setup.

## The Pattern
Stdio for tools that can run as subprocesses. TCP for tools that must bridge to
an already-running application that owns its own process. Always verify the
exact package name — the wrong name produces no error at registration time,
only silent unavailability when the tool is called.

