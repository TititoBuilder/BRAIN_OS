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

## TIME — 3 triggers
| Trigger | Project | Schedule |
|---|---|---|
| [[Trigger_BrainOS_Daily_Review]] | BRAIN_OS | Daily 9:00am PST |
| [[Trigger_BDF_Queue_Check]] | BDF | Daily 12:00pm PST |
| [[Trigger_Daily_Log_Update]] | BRAIN_OS | Daily 6:00pm PST |

## EVENT — 5 triggers
| Trigger | Project | Source |
|---|---|---|
| [[Trigger_Match_Scheduled]] | BDF | ContentWindow enum in schedule_manager.py |
| [[Trigger_Render_Complete]] | BDF | New entry in export_log.jsonl |
| [[Trigger_Script_Ready]] | BDF | New file in triggers\ folder |
| [[Trigger_Clip_Detected]] | BDF | New file in BDF_Share\ or master_edit\ready\ |
| [[Trigger_Telegram_Message]] | BDF | Incoming Telegram message to bot_service.py |

## STATE — 2 triggers
| Trigger | Project | Condition |
|---|---|---|
| [[Trigger_Graph_TTL_Expired]] | BRAIN_OS | SESSION_ANCHOR_TTL_HOURS exceeded |
| [[Trigger_Drive_Change_Token]] | BDF/BRAIN_OS | Drive token differs from manifest |

## MANUAL — 3 triggers
| Trigger | Project | How |
|---|---|---|
| [[Trigger_New_Idea]] | CA/BRAIN_OS | User input — note, voice, or task |
| [[Trigger_Session_Close]] | BRAIN_OS | session_close.py manual run |
| [[Trigger_Book_Compile]] | CA | book_compiler.py via brainos-book PowerShell function |

---

## Coverage by Project
| Project | Triggers |
|---|---|
| BDF (soccer-content-generator) | [[Trigger_Match_Scheduled]] [[Trigger_Render_Complete]] [[Trigger_Script_Ready]] [[Trigger_Clip_Detected]] [[Trigger_Telegram_Message]] [[Trigger_BDF_Queue_Check]] [[Trigger_Drive_Change_Token]] |
| BRAIN_OS | [[Trigger_Session_Close]] [[Trigger_Graph_TTL_Expired]] [[Trigger_Drive_Change_Token]] [[Trigger_BrainOS_Daily_Review]] [[Trigger_Daily_Log_Update]] [[Trigger_New_Idea]] |
| CA (CristianConstruction) | [[Trigger_Book_Compile]] [[Trigger_New_Idea]] |

## Related
[[Master_Control]] [[BDF_Agent_Pipeline]] [[CA_Orchestrator]] [[KNOWLEDGE_INGESTION_PROTOCOL_V2]]
