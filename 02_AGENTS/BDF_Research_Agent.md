---
tags: [agent, live]
---

# AGENT: BDF Research Agent

## Project
BDF Soccer Bot

## Function
Monitors match schedules and classifies the current content window so downstream agents know what type of content to produce and when.

## Input
- `ucl_schedule.json` — fixture list with kickoff times, key players, win probabilities, aggregate context
- System clock (UTC) — used to compute minutes-to-kickoff and classify the window

## Output
- `MatchWindow` dataclass: match_id, home/away, kickoff_utc, round_name, content_window, minutes_to_kickoff, key_players, content_angles, avatar_players, win_probability, aggregate_context, narrative
- `get_pre_match_brief()` — structured prompt brief fed directly into the Creative/Content agents
- `get_match_day_summary()` — human-readable match day overview string

## Trigger
Polled by bot_service.py and dashboard_api.py; any agent that needs schedule context calls `ScheduleManager().get_active_windows()` directly — no scheduled cron, query-on-demand.

## Tools and APIs
- `ucl_schedule.json` (local JSON, single source of truth for all fixture data)
- No external API calls — schedule data is pre-ingested

## Canonical file
C:\Dev\Projects\soccer-content-generator\src\data\ingestion\schedule_manager.py

## Connected to
- [[BDF_Creative_Agent]] — receives content_window + content_angles to select post type
- [[BDF_Automation_Agent]] — bot_service.py queries active windows on heartbeat
- [[BDF_Soccer_Bot]] project
- [[BDF_Content_Research_Flow]]
- [[Football_API]]
- [[NewsAPI]]
- [[LanceDB_Vector_Store]]

## Status
Live

## Content windows
| Window | Trigger | Content Strategy |
|---|---|---|
| PRE_MATCH_24H | 24h before kickoff | previews, predictions |
| PRE_MATCH_2H | 2h before kickoff | lineup hot takes, hype |
| LIVE_MATCH | During 90 mins | real-time reaction |
| POST_MATCH_2H | 0-2h after | hot takes, ratings |
| POST_MATCH_24H | Next day | analysis, clips, avatars |
| NO_MATCH | Any other time | standard scheduling |
