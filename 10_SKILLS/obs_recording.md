---
tags: [skills, obs, recording, capture, predator, confirmed]
status: confirmed
machine: Predator (CRISTIAN)
parent: "[[10_SKILLS_INDEX]]"
confirmed: 2026-04-29
supersedes: "[[OBS_Skill]] personal config section"
---

# OBS Recording — Confirmed Settings (Predator)

Locked-in settings for BDF highlight capture on Predator (hostname: CRISTIAN).
These were verified in active match-day use on 2026-04-29.
`obs_relay.py` reads from `C:\Media\Recordings` and routes clips to `C:\BDF_Share`.

---

## Machine

| Setting | Value |
|---|---|
| Machine | Predator (hostname: **CRISTIAN**) |
| OBS Version | 32.1.2 |
| GPU | RTX 5070 Ti (NVENC) |

---

## Video Settings

| Setting | Value |
|---|---|
| Base Resolution | 1920×1080 |
| Output Resolution | 1920×1080 |
| FPS | 60 |
| Color Format | **NV12** |
| Color Space | **Rec. 709** |
| Color Range | **Full** |

---

## Output Settings (Advanced Mode)

### Recording

| Setting | Value |
|---|---|
| Recording Path | `C:\Media\Recordings` |
| Format | **MKV** |
| Encoder | **NVENC H.264** (`obs_nvenc_h264_tex`) |
| Rate Control | **CQP** |
| CQ Level | **18** |
| Audio Encoder | ffmpeg_aac |

> CQP 18 = near-lossless quality. Used instead of CBR so file size scales
> with scene complexity rather than burning constant bitrate on static frames.

### Replay Buffer

| Setting | Value |
|---|---|
| Enabled | Yes |
| Duration | **20 seconds** |
| Trigger | F10 (Save Replay) |

---

## Hotkeys

| Hotkey | Action |
|---|---|
| `F8` | Start / Stop Recording |
| `F9` | Start / Stop Replay Buffer |
| `F10` | Save Replay |

---

## Browser Source

| Setting | Value |
|---|---|
| Hardware Acceleration | **DISABLED** |

> Must be disabled — GPU contention with NVENC causes dropped frames when
> hardware acceleration is on during active recording.

---

## Pipeline Integration

```
OBS F8/F10
  → C:\Media\Recordings  (MKV files)
  → obs_relay.py         (renames with match context, copies to BDF_Share)
  → C:\BDF_Share         (clip_watcher.py intake)
  → content_queue.json   (status=pending)
  → dashboard localhost:5173
```

`obs_relay.py` auto-detects Predator via hostname `CRISTIAN` and writes
directly to `C:\BDF_Share` (same machine). On HP it uses SyncThing instead.

---

## What Changed (vs OBS_Skill.md / OBS_Node.md)

| Field | Old | Confirmed |
|---|---|---|
| Recording path | `C:\BDF_OBS_Clips\RawFootage` | `C:\Media\Recordings` |
| Rate Control | CBR | CQP |
| CQ Level | — | 18 |
| Replay Buffer | 60s | 20s |
| Browser HW Accel | unspecified | DISABLED |
