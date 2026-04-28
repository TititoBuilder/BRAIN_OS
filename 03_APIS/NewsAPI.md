---
tags: [api, live]
---

# API: NewsAPI

## Purpose
Fetches recent soccer news articles and og:image previews for BDF content enrichment and image sourcing.

## Used by projects
- BDF

## Limits and rules
- Rate limits: free tier (developer plan)
- Cost: $0 (logged as $0.000 in cost_tracker.py)
- Legal constraints: articles are source-credited; images scraped from og:image only (no full article reproduction)

## Credentials
`NEWS_API_KEY`

## Connected agents
- [[BDF_Research_Agent]]
- [[BDF_Creative_Agent]]

## Inputs
- Endpoint: `https://newsapi.org/v2/everything`
- Params: `q` (subject + content_type keywords), `language=en`, `sortBy=publishedAt`, `pageSize=5`
- Called from: news_api_client.py, api_data_fetcher.py, match_data_fetcher.py

## Outputs
- Article list: title, description, url, urlToImage, publishedAt
- `news_image_agent.py` scrapes `og:image` from article URLs as the image tier 2 fallback
- Article snippets fed into knowledge enrichment context for caption generation

## Connected to
- [[BDF_Research_Agent]]
- [[BDF_Content_Research_Flow]]
