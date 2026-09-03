---
tags: [system, triggers, knowledge-graph]
---
# Trigger Architecture — Master Index

Single source of truth for all 13 system triggers across BDF, BRAIN_OS, and CA. Each trigger fires exactly one type of signal; all activations and connections are documented in the linked trigger files.

## Trigger Types
| Type | Description |
|---|---|
| TIME | Fired by Google Calendar at a scheduled time |
| EVENT | Fired by a file/data change detected by a watcher or MCP |
| STATE | Fired when a monitored condition becomes true |
| MANUAL | Fired by an explicit human decision or script run |

---

<!-- TRIGGER_INDEX:START -->

## TIME — 3 triggers
| Trigger | Project | Schedule | Implemented by |
|---|---|---|---|
| [[Trigger_BDF_Queue_Check]] | soccer-content-generator | Daily 12:00pm PST | parked - watchdog.py --check bdf exists but BDF is not active |
| [[Trigger_BrainOS_Daily_Review]] | BRAIN_OS | Daily 9:00am PST | Google Calendar 9:00am - manual, no code |
| [[Trigger_Daily_Log_Update]] | BRAIN_OS | Daily 6:00pm PST | Google Calendar 6:00pm - manual, no code |

## EVENT — 5 triggers
| Trigger | Project | Source | Implemented by |
|---|---|---|---|
| [[Trigger_Clip_Detected]] | soccer-content-generator | New file in BDF_Share or master_edit/ready | parked - BDF not active |
| [[Trigger_Match_Scheduled]] | soccer-content-generator | ContentWindow enum in schedule_manager.py | parked - BDF not active |
| [[Trigger_Render_Complete]] | soccer-content-generator | New entry in export_log.jsonl | parked - BDF not active |
| [[Trigger_Script_Ready]] | soccer-content-generator | New file in the triggers folder | parked - BDF not active |
| [[Trigger_Telegram_Message]] | soccer-content-generator | Incoming Telegram message to bot_service.py | parked - BDF not active |

## STATE — 2 triggers
| Trigger | Project | Condition | Implemented by |
|---|---|---|---|
| [[Trigger_Drive_Change_Token]] | soccer-content-generator / BRAIN_OS | Drive token differs from manifest | 09_TOOLS/drive_sync.py --get-token, called by graph_maintainer.py |
| [[Trigger_Graph_TTL_Expired]] | BRAIN_OS | SESSION_ANCHOR_TTL_HOURS exceeded | 09_TOOLS/graph_maintainer.py:222 |

## MANUAL — 3 triggers
| Trigger | Project | How | Implemented by |
|---|---|---|---|
| [[Trigger_Book_Compile]] | CristianConstruction | book_compiler.py via the brainos-book function | brainos-book PowerShell function |
| [[Trigger_New_Idea]] | BRAIN_OS / CristianConstruction | User input, note or voice or task | none - describes a habit, not a mechanism |
| [[Trigger_Session_Close]] | BRAIN_OS | session_close.py manual run | 09_TOOLS/session_close.py |

## Coverage by Project
| Project | Triggers |
|---|---|
| BRAIN_OS | [[Trigger_BrainOS_Daily_Review]] [[Trigger_Daily_Log_Update]] [[Trigger_Drive_Change_Token]] [[Trigger_Graph_TTL_Expired]] [[Trigger_New_Idea]] [[Trigger_Session_Close]] |
| CristianConstruction | [[Trigger_Book_Compile]] [[Trigger_New_Idea]] |
| soccer-content-generator | [[Trigger_BDF_Queue_Check]] [[Trigger_Clip_Detected]] [[Trigger_Drive_Change_Token]] [[Trigger_Match_Scheduled]] [[Trigger_Render_Complete]] [[Trigger_Script_Ready]] [[Trigger_Telegram_Message]] |

<!-- TRIGGER_INDEX:END -->

## Related
[[Master_Control]] [[BDF_Agent_Pipeline]] [[CA_Orchestrator]] [[KNOWLEDGE_INGESTION_PROTOCOL_V2]]
