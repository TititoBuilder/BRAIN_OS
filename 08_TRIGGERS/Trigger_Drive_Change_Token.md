---
tags: [trigger, state, bdf, brain_os]
type: STATE
project: soccer-content-generator / BRAIN_OS
fires_when: Drive token differs from manifest
implemented_by: 09_TOOLS/drive_sync.py --get-token, called by graph_maintainer.py
---
# TRIGGER: Drive change token
## What fires it
`drive_sync.py --get-token` detects token differs from manifest
File: `C:\BRAIN_OS\09_TOOLS\drive_sync.py`
## Activates
[[BDF_Agent_Pipeline]]
## Project
[[soccer-content-generator]]
## CLAUDE.md
`C:\Dev\Projects\soccer-content-generator\CLAUDE.md`
## Connected to
[[Trigger_Architecture]]
[[Trigger_Graph_TTL_Expired]]
[[BDF_Operations_Status]]
[[Master_Control]]
