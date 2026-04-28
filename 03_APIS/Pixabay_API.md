---
tags: [api, live]
---

# API: Pixabay API

## Purpose
Free stock photo source for BDF post backgrounds when AI generation and news images are unavailable.

## Used by projects
- BDF

## Limits and rules
- Rate limits: 100 requests/60 seconds
- Cost: $0 (free, CC0 license)
- Legal constraints:
  - License: `pixabay_cc0` — images are free for commercial use, no attribution required
  - 24-hour local cache required per API terms of service
  - `safesearch=true` enforced on all queries

## Credentials
`PIXABAY_API_KEY`

## Connected agents
- [[BDF_Creative_Agent]]

## Inputs
- Endpoint: `https://pixabay.com/api/`
- Params: `q` (subject keywords), `image_type=photo`, `category=sports`, `safesearch=true`, `per_page=3`
- Tier position: fallback after Unsplash in image sourcing tier order (tier 3 or later)

## Outputs
- `largeImageURL` (1280px wide) — downloaded and passed to card_composer.py as background layer
- Results cached locally for 24 hours to respect API terms
