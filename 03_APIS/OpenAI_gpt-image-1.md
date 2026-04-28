---
tags: [api, critical]
---

# API: OpenAI gpt-image-1

## Purpose
AI image generation for branded BDF post visuals — replaces DALL-E 3 (deprecated May 12 2026).

## Used by projects
- BDF

## Limits and rules
- Rate limits: standard OpenAI tier limits
- Cost: tracked in cost_tracker.py; gpt-image-1 priced per image
- Legal constraints: DALL-E 3 (`dall-e-3`) fully deprecated May 12 2026 — migration to gpt-image-1 in progress
- No broadcast footage or copyrighted kit imagery in prompts

## Credentials
`OPENAI_API_KEY`

## Connected agents
- [[BDF_Creative_Agent]]

## Inputs
- Endpoint: `https://api.openai.com/v1/images/generations`
- Model progression:
  - `dall-e-3` — still wired in media_agent.py:358, :633 and generate_avatar.py:128 (deprecated)
  - `gpt-image-1` — wired in media_agent.py:430 and create_avatar_library.py:405 (active)
- image_agent.py: `AIImageAgent` wrapper fires as tier 0 before `NewsImageAgent`
- Typical params: prompt (generated from subject + content_type), size, quality

## Outputs
- Image URL or base64 data returned in API response
- Saved locally then passed to card_composer.py for PIL compositing
- Player avatar PNGs written to `output/avatars/` by create_avatar_library.py

## Connected to
- [[BDF_Creative_Agent]]
- [[BDF_Avatar_Pipeline]]
