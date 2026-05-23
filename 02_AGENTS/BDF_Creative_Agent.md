---
tags: [agent, live]
---

# AGENT: BDF Creative Agent

## Project
BDF Soccer Bot

## Function
Generates branded 1200x675 cards via PIL compositing (card_composer) over AI-generated images (image_agent, media_agent).

## Input
- `topic` (str) — player or match subject
- `content_type` (str) — hot_take, match_recap, match_preview, tactical_analysis, etc.
- `headline`, `body`, `stat_line` — text content from Creative/Content generation pipeline
- Optional: `source_image` path (for template overlay), `subject_a`/`subject_b` (for matchup templates)

## Output
- Composed PNG card at `src/images/cards/card_{hash}.png` (1200×675, Twitter-spec)
- `ImageSearchResult` dataclass with path, source, topic_key, record metadata
- BDF-branded watermark + Brazil/France accent stripe on all cards

## Trigger
Called by the content generation pipeline after post text is ready — image compositing is the final step before Telegram approval queue.

## Tools and APIs
- [[OpenAI_DALL-E3]] — `dall-e-3` model; currently active
- [[OpenAI_gpt-image-1]] — `gpt-image-1` — PLACEHOLDER, not yet implemented. Return to this when resuming BDF image work.
- [[Unsplash_API]] — primary photo source (UNSPLASH_ACCESS_KEY)
- [[Pixabay_API]] — fallback photo source (PIXABAY_API_KEY)
- [[NewsImageAgent]] — real player photos scraped from BBC/ESPN feeds
- [[Pillow_PIL]] — local image compositing, resizing, text rendering (no API cost)

## Canonical file
C:\Dev\Projects\soccer-content-generator\src\image_agent.py (tier 0 AI generation)
C:\Dev\Projects\soccer-content-generator\src\media_agent.py (DALL-E 3 active; gpt-image-1 wired but not yet implemented)
C:\Dev\Projects\soccer-content-generator\src\card_composer.py (PIL compositing, 20 accent-colored templates)

## Connected to
- [[BDF_Automation_Agent]] — bot_service.py triggers image lookup via ClipWatcher/content pipeline
- [[BDF_Research_Agent]] — content_window determines which card template is selected
- [[BDF_Soccer_Bot]] project
- [[OpenAI_gpt-image-1]]
- [[Pixabay_API]]
- [[Anthropic_Claude]]
- [[BDF_Social_Media_Flow]]
- [[Content_Queue]]

## Status
Live — gpt-image-1 migration PLACEHOLDER, not yet implemented. Return to this when resuming BDF image work.

## Image tier fallback order
| Tier | Source | Notes |
|---|---|---|
| 0 | DALL-E 3 / gpt-image-1 (AI gen) | Fired before NewsImageAgent for fresh visuals |
| 0.5 | BDF Card Composer (PIL template) | 20 accent-colored templates, no API call |
| 1 | NewsImageAgent (BBC/ESPN photos) | Real player photos |
| 2 | Local avatar library | Pre-rendered player avatars |
| 3 | Unsplash (primary) | Creative Commons |
| 4 | Pixabay (fallback) | CC0 |

## Card template accent colors (20 types)
hot_take (red), match_recap (orange), match_preview (cyan), tactical_analysis (purple), and 16 more — all rendered at 1200×675 with BDF watermark and Brazil/France stripe.
