---
tags: [workflow, live]
---

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

## Connected to
- [[OpenAI_gpt-image-1]]
- [[KlingAI]]
- [[BDF_Creative_Agent]]
- [[Twitter_API_v2]]

---

<!-- PATCH APPLIED 2026-05-05 — sources: 20260315 (Session 3 style_transfer), 20260318 -->

## Image Model: gpt-image-1 (Current Standard)

**Migration status:** DALL-E 3 → gpt-image-1
**Deadline:** May 12, 2026 (DALL-E 3 deprecation)
**Model chosen:** `gpt-image-1` (not 1.5 — cost efficiency)

### Core Technique: Style Transfer via images.edit()
```python
response = client.images.edit(
    model="gpt-image-1",
    image=open("reference_screenshot.png", "rb"),
    prompt="Convert to BDF cartoon style, clean flat 2D, chibi T-pose, white background..."
)
```

### Quality Tiers
| Tier | Cost | Use Case |
|---|---|---|
| `low` | ~$0.011 | Drafts, iteration |
| `medium` | ~$0.042 | Volume library (create_avatar_library.py) |
| `high` | ~$0.167 | Accuracy-critical: PSG5, hero characters |

### Migration Checklist
- [ ] Audit all `dall-e-3` model references in codebase
- [ ] Swap `images.generate()` → `images.edit()` where style transfer needed
- [ ] Update `ai_image_agent.py` with new endpoint
- [ ] Wire `test_style_transfer.py` logic into production agent
- [ ] **DEADLINE: May 12, 2026**

---

## Age Scale System (5 Tiers)

Manual control system — prompt includes age tier for physical accuracy.

| Tier | Age Range | Physical Characteristics |
|---|---|---|
| Youth | 16-19 | Smaller build, younger facial features, less defined muscle |
| Young Pro | 20-24 | Athletic peak, lean, energetic proportions |
| Prime | 25-29 | Full build, established look, peak physical presence |
| Veteran | 30-34 | Slight bulk, experienced features, authority in posture |
| Late Career | 35-40 | Character lines, mature build, distinguished presence |

**Implementation:** Include tier label in prompt:
```
"...age tier: Prime (25-29), Athletic peak build..."
```

---

## Avatar Pipeline Split (Two Tracks)

| Track | Style | Purpose | Quality |
|---|---|---|---|
| CA5 Rigging | Chibi T-pose, flat 2D | Cartoon Animator 5 animation | HIGH |
| Static Posts | Realistic caricature | Social media images | MEDIUM |

---

## CA5 + Inkscape Rigging Pipeline

Full workflow for animated characters:

1. **Generate** — chibi T-pose character sheet via gpt-image-1 (HIGH quality)
2. **Import** — bring PNG into Inkscape (free Illustrator replacement)
3. **Separate** — manually separate into layers: `body`, `arms`, `head`, `legs`
4. **Export** — each layer as individual PNG with transparent background
5. **Import to CA5** — load all layer PNGs into Cartoon Animator 5
6. **Map bones** — assign CA5 bone rig to layer anchor points
7. **Animate** — use CA5 motion library or custom keyframes

**First player for rigging:** Vitinha or Haaland (established avatars, good quality)
**Inkscape:** Free, confirmed working — `C:\Program Files\Inkscape\`

---

## Character Sheet Format

**Single-character T-pose** (not multi-view) — confirmed superior for CA5:
- Multi-view prompts produce inconsistent proportions across views
- Single T-pose → cleaner layer separation in Inkscape
- Back/side views generated separately as needed

---

## Scripts Reference

| Script | Location | Purpose | Quality |
|---|---|---|---|
| `generate_psg5.py` | project root | 5 PSG players with age scale | HIGH ($0.167/image) |
| `create_avatar_library.py` | project root | 25-player bulk library | MEDIUM ($0.042/image) |
| `test_style_transfer.py` | project root | Style transfer tests from screenshots | varies |
| `test_character_sheet.py` | project root | CA5 character sheet generation tests | varies |

---

## Known DALL-E Limitations (Why We Migrated)

- Adds incorrect sponsor logos (Emirates on Mbappe)
- Poor likeness accuracy for Black players
- No reference image input (can't style-match)
- Deprecated May 12, 2026

---

## Cost Reference (This Pipeline)

| Operation | Script | Quality | Cost |
|---|---|---|---|
| Single avatar | manual | medium | $0.042 |
| Single avatar | manual | high | $0.167 |
| 25-player library | create_avatar_library.py | medium | $1.05 |
| PSG5 set | generate_psg5.py | high | $0.835 |
| Vitinha final (confirmed) | generate_psg5.py | high | $0.167 |
