# WORKFLOW: BDF Avatar Pipeline

## Project
BDF

## Flow
GPT-4o → Inkscape → Cartoon Animator 5 → Kling AI → Twitter

## Steps
1. [[BDF_Creative_Agent]] — GPT-4o generates reference image descriptions and style prompts for player avatar (consistent art style: semi-realistic cartoon, team kit, club colors)
2. **Inkscape** — vector tracing / manual refinement of AI-generated base image; exported as high-res PNG per pose
3. **Cartoon Animator 5** — rigging and posing; each player requires multiple poses (minimum 5 for a complete set):
   - Idle / portrait
   - Celebration
   - Dribbling
   - Shooting / striking
   - Reaction
4. [[BDF_Creative_Agent]] — `create_avatar_library.py` sends PNG pose to Kling AI `POST /v1/videos/image2video`; motion prompt pulled from `PLAYER_MOTION` dict (per-player animation personality); polls `GET /v1/videos/image2video/{task_id}` until complete
5. Output video downloaded to `output/videos/`; used in Twitter posts and Telegram previews

## Trigger
Manual — run `create_avatar_library.py` per player, per pose. No automatic trigger.

## Output
- 5-second MP4 animation per pose per player in `output/videos/`
- Static PNG stills in `output/avatars/`
- Used as visual assets in BDF social posts and Telegram approval previews

## Rules and constraints
- Kling AI cost: $0.14/clip (image-to-video, 5 sec); $0.28/clip (text-to-video) — tracked in cost_tracker.py
- Model: `kling-v1`; auth: HS256 JWT from KLING_ACCESS_KEY + KLING_SECRET_KEY
- **No real player footage** — avatars are fully AI-generated/illustrated; no DMCA exposure
- No player likeness guarantees — cartoon style avoids personality rights issues
- Cartoon Animator 5 must be licensed and installed locally

## Status
| Player | Poses done | Status |
|---|---|---|
| Endrick | 5 | Complete |
| De Bruyne | 2 | Partial — 3 poses remaining |
| Lamine Yamal | 0 | Pending |
| Haaland | 0 | Pending |
| Mbappé | 0 | Pending |
| Vinicius Jr. | 0 | Pending |
| Bellingham | 0 | Pending |
| Salah | 0 | Pending |
| Pedri | 0 | Pending |
| Gavi | 0 | Pending |
