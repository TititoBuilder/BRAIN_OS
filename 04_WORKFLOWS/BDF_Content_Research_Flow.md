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

## Connected to
- [[Football_API]]
- [[NewsAPI]]
- [[LanceDB_Vector_Store]]
- [[Anthropic_Claude]]
- [[Content_Queue]]
