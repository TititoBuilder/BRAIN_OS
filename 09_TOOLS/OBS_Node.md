---
tags: [tools, obs, recording, streaming, capture]
status: active
dependencies: [RTX 5070 Ti, NVENC]
parent: "[[09_TOOLS_INDEX]]"
children: []
---

# OBS Node

OBS Studio — screen capture and recording for the BDF content pipeline.
Profile: `Untitled` (default). Settings read 2026-04-28.

---

## Video Settings

| Setting | Value |
|---|---|
| Base Resolution | 1920×1080 |
| Output Resolution | 1920×1080 |
| FPS | 60 |
| Color Format | NV12 |
| Color Space | BT.709 |
| Color Range | Full |
| Scale Filter | Bicubic |
| SDR White Level | 300 |
| HDR Nominal Peak | 1000 |

---

## Audio Settings

| Setting | Value |
|---|---|
| Sample Rate | 48000 Hz |
| Channel Setup | Stereo |
| Monitoring Device | Default |
| Audio Track 1 Bitrate | 160 kbps |

---

## Output Settings (Advanced Mode)

### Recording
| Setting | Value |
|---|---|
| Encoder | NVENC H.264 (`obs_nvenc_h264_tex`) |
| Rate Control | CBR |
| Format | MP4 |
| Output Path | `C:/Media/Recordings` |
| File Split | By size — 4096 MB per file |
| Audio Encoder | ffmpeg_aac |
| No spaces in filename | true |

### Replay Buffer
| Setting | Value |
|---|---|
| Enabled | Yes (Advanced Output) |
| Buffer Duration | 15 seconds |
| Buffer Size Limit | 512 MB |
| Start Hotkey | `F7` |
| Save Hotkey | `F8` |

### Stream (placeholder)
| Setting | Value |
|---|---|
| Reconnect | Yes — retry delay 2s, max 25 retries |
| Low Latency | Disabled |
| Delay | Disabled |

---

## Scenes

| Scene | Notes |
|---|---|
| **Scene** | Default scene — active for BDF capture sessions |

### Transitions
- Cut (default)
- Fade

---

## Sources

| Source Name | Type | Notes |
|---|---|---|
| `Paramount_RealMadrid_BayernCapture` | Window Capture | Chrome — UCL on Paramount+ / CBS Sports |
| `Desktop Audio` | WASAPI Output | System audio |
| `Mic/Aux` | WASAPI Input | Microphone |

### Filters on `Paramount_RealMadrid_BayernCapture`
- `Remove Browser Bar` — crop filter to strip the Chrome address bar from the capture

---

## File Naming
Format: `%CCYY-%MM-%DD %hh-%mm-%ss`
Example: `2026-04-28 14-32-00.mp4`

---

## Setup Notes
- OBS used to capture live football streams (Paramount+, CBS) for BDF highlight pipeline
- Recordings land in `C:/Media/Recordings/` — separate from Resolve render output (`C:\BDF\renders\`)
- NVENC encoder leverages RTX 5070 Ti for zero-CPU-cost recording at 60fps
- Replay buffer (F7/F8) used to grab spontaneous highlight moments without pre-recording
- Profile named `Untitled` — no multi-profile setup yet
