---
tags: [api, live]
---

# API: Kling AI

## Purpose
Image-to-video generation for animated player highlight clips in the BDF avatar library.

## Used by projects
- BDF

## Limits and rules
- Rate limits: not documented; task-based async (poll until done)
- Cost: $0.14/clip (image-to-video, 5 sec); $0.28/clip (text-to-video) — tracked in cost_tracker.py
- Legal constraints: generated clips only (no real footage); no player likeness guarantees

## Credentials
- `KLING_ACCESS_KEY`
- `KLING_SECRET_KEY`

## Connected agents
- [[BDF_Creative_Agent]]

## Inputs
- Base URL: `https://api.klingai.com`
- Auth: HS256 JWT — `header.payload.signature` sent as Bearer token; generated from KLING_ACCESS_KEY + KLING_SECRET_KEY
- Submit endpoint: `POST /v1/videos/image2video`
- Poll endpoint: `GET /v1/videos/image2video/{task_id}`
- Model: `kling-v1`
- Params: source image (player avatar PNG), duration=5, cfg_scale=0.5, motion prompt from `PLAYER_MOTION` dict
- 10 players total in avatar library; Endrick and De Bruyne complete; 8 players pending

## Outputs
- `task_id` returned on submit; poll until `status=succeed`
- Video URL in response → downloaded to `output/videos/`
- Per-player animation personality defined in `PLAYER_MOTION` dict (e.g. explosive dribble, clinical finish)

## Connected to
- [[BDF_Avatar_Pipeline]]
- [[BDF_Creative_Agent]]
