---
tags: [trigger, time, brain_os]
type: TIME
project: BRAIN_OS
fires_when: "Daily 7:30am PST"
implemented_by: Task Scheduler BRAINOS_Morning_Watchdog -> watchdog.py --check morning
---
# TRIGGER: Morning watchdog
## What fires it
Windows Task Scheduler — every day 7:30am PST
Task: `\BRAINOS_Morning_Watchdog`
Action: `C:\Users\titit\AppData\Local\Programs\Python\Python312\python.exe C:\BRAIN_OS\09_TOOLS\watchdog.py --check morning`
Checks: audio parity via graph_maintainer, vault orphan count, Queue.md In Progress count, uncommitted files
Reports: Telegram, or a clean-run message when nothing is wrong
## Activates
Nothing automatically. The report is read by a human.
## Distinct from Trigger_BrainOS_Daily_Review
That is a 9:00am Calendar event for judgment work — scan the graph view,
review active projects, flag stale nodes. This is a script checking four
measurable conditions. Same rough purpose, different mechanisms, different
failure modes: this one can be disabled, refuse to start on battery, or run
under an interpreter without psutil. All three have happened.
## Project
[[BRAIN_OS]]
## Connected to
[[Trigger_Architecture]]
[[Trigger_BrainOS_Daily_Review]]
[[Trigger_Graph_TTL_Expired]]


<!-- auto-updated 2026-09-04 -->
<!-- Node added 2026-09-04: morning watchdog trigger, distinct from the 9am review. Annotated with implemented_by per trigger annotation pass. -->
