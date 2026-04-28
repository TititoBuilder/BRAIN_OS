---
tags: [agent, orchestrator, bdf, live]
---
# AGENT: Content orchestrator

## Role
Controls the full BDF content pipeline from research to publish.
Only orchestrator allowed to activate content agents.

## Controls
- [[BDF_Research_Agent]]
- [[BDF_Analysis_Agent]]
- [[BDF_Creative_Agent]]
- [[BDF_Automation_Agent]]

## Flow
Match trigger → Research → RAG analysis → Card generation → Queue → Telegram → Twitter

## Trigger
[[Trigger_Match_Scheduled]] via [[Master_Control]]

## Output
Published tweet with branded card

## Connected to
[[BDF_Content_Research_Flow]]
[[BDF_Social_Media_Flow]]
[[Content_Queue]]
