---
tags: [trigger, time, bdf]
type: TIME
project: soccer-content-generator
fires_when: "Daily 12:00pm PST"
implemented_by: parked - watchdog.py --check bdf exists but BDF is not active
---
# TRIGGER: BDF queue check
## What fires it
Google Calendar — every day 12:00pm PST
Event: BDF Queue Check
Checklist: Check content_queue.json, review Telegram approvals, verify bot_service.py running
## Activates
[[Content_Orchestrator]] manual
## Project
[[soccer-content-generator]]
## CLAUDE.md
`C:\Dev\Projects\soccer-content-generator\CLAUDE.md`
## Connected to
[[Trigger_Architecture]]
[[Trigger_BrainOS_Daily_Review]]
[[Trigger_Daily_Log_Update]]
[[Trigger_Telegram_Message]]
[[BDF_Agent_Pipeline]]
