---
tags: [workflow, live]
---

# WORKFLOW: BDF Content Research Flow

## Project
BDF

## Flow
ScheduleManager → API clients → LanceDB RAG → Claude → content_queue.json

## Steps
1. [[BDF_Research_Agent]] — `ScheduleManager` evaluates active `ContentWindow` enum value to determine topic priority and content type
2. [[BDF_Research_Agent]] — API clients fetch live data: football-data.org (standings, fixtures), TheSportsDB (squad/event data), NewsAPI (recent articles)
3. [[BDF_Analysis_Agent]] — `RagPipeline.retrieve()` rewrites query into 3 semantic variants → multi-retrieve from LanceDB → deduplicate → filter (threshold 0.82) → CrossEncoder rerank → top 8 docs returned
4. [[BDF_Creative_Agent]] — Claude (`claude-sonnet-4-20250514`) receives enriched context (RAG docs + API data + knowledge enricher facts) and generates caption + hashtags
5. [[BDF_Automation_Agent]] — output written to `content_queue.json` with status=`pending`; Telegram approval flow begins

## Trigger
`ContentWindow` enum value set by `ScheduleManager`:
- `pre_match_24h` — preview content, tactical analysis
- `pre_match_2h` — hot takes, lineup reactions
- `live` — real-time match updates
- `post_match` — recaps, player ratings, highlight commentary
- `transfer_window` — rumor + market value content
- `offseason` — historical/rankings content

## Output
New post entry in `src/queue/content_queue.json` with status=`pending`, including: topic, content_type, generated caption, hashtags, platform targets, and associated image path.

## Rules and constraints
- Football API: 10 req/min (football-data.org), 100 calls/day self-imposed cap across all football clients
- NewsAPI: free tier; $0.000 cost
- RAG relevance threshold: cosine distance < 0.82; CrossEncoder reranker falls back silently if GPU unavailable
- Claude cost: ~$0.006–$0.008 per post (tracked in cost_tracker.py)
- Knowledge enricher TF-IDF threshold: 0.6801 cosine distance

## Scripts Reference

<!-- Source: 20260315_session_compile_story_kling (ingested 2026-05-05) -->

| Script | Location | Purpose | Output |
|---|---|---|---|
| `story_generator.py` | project root | AI-written 3-scene soccer animation scripts (claude-sonnet-4-6, ~$0.015/story) | `output/stories/story_{players}_{timestamp}.txt` |

**Editorial note:** Despite the script existing and producing usable output (6 scripts generated in the March 15 session), the working decision is that **Cristian writes stories manually** for stronger creative control. `story_generator.py` is kept available for batch ideation and as a fallback, not as the primary content path. See [[BDF_Agent_Pipeline]] for full script architecture (cast, scenarios, run modes).

---

## Connected to
- [[Football_API]]
- [[NewsAPI]]
- [[LanceDB_Vector_Store]]
- [[Anthropic_Claude]]
- [[Content_Queue]]
