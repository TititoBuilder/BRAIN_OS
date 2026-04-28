---
tags: [agent, orchestrator, bdf, live]
---
# AGENT: Video orchestrator

## Role
Controls the full BDF video pipeline from Resolve render to Twitter publish.
Only orchestrator allowed to activate video and export agents.

## Controls
- [[DaVinci_Resolve_MCP]]
- [[BDF_Memory_Agent]]

## Flow
Render complete → mcp_ingest → LanceDB write → mp4 to BDF_Share → publish ready

## Trigger
[[Trigger_Render_Complete]] or [[Trigger_Script_Ready]] via [[Master_Control]]

## Output
Processed mp4 + .meta.json sidecar in C:\BDF_Share

## Connected to
[[BDF_Video_Production_Flow]]
[[Resolve_Export_Log]]
[[DaVinci_Resolve_MCP]]
