---
tags: [tools, obs, recording, streaming, capture]
status: active
dependencies: [RTX 5070 Ti, NVENC]
parent: "[[09_TOOLS_INDEX]]"
children: []
version: 32.1.2
confirmed: 2026-04-29
machine: Predator (CRISTIAN)
---

# OBS Node

OBS Studio — screen capture and recording for the BDF content pipeline.
Profile: `Untitled` (default). Settings confirmed 2026-04-29. Version: **32.1.2**.
Machine: **Predator** (hostname: CRISTIAN). See [[obs_recording]] for canonical confirmed config.

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
| Rate Control | **CQP** |
| CQ Level | **18** |
| Format | MKV |
| Output Path | `C:\Media\Recordings` |
| Audio Encoder | ffmpeg_aac |
| No spaces in filename | true |
| Process Priority | **High** |

### Replay Buffer
| Setting | Value |
|---|---|
| Enabled | Yes (Advanced Output) |
| Buffer Duration | **20 seconds** |
| Buffer Size Limit | 512 MB |

### Hotkeys
| Hotkey | Action |
|---|---|
| `F8` | Start / Stop Recording |
| `F9` | Start / Stop Replay Buffer |
| `F10` | Save Replay Buffer |

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

## WebSocket
| Setting | Value |
|---|---|
| Port | 4455 |
| Authentication | Enabled |

---

## Known Issues
- **obsws-python incompatible with OBS v5 WebSocket protocol** — the Python library targets the old v4 API and fails to authenticate against v5.
  - **Workaround**: OBS is controlled via AutoHotkey (`obs_control.ahk`) using hotkeys instead of WebSocket commands. See [[Windows_Tools_Node]] → AutoHotkey.

---

## Browser Source

| Setting | Value |
|---|---|
| Hardware Acceleration | **DISABLED** |

> Must be disabled — GPU contention with NVENC causes dropped frames when on.

---

## WD Elements / LanceDB Path

| Note | Value |
|---|---|
| WD Elements mount | Always `D:` on Predator |
| Why not `F:` | Recovery partition blocks `F:` assignment |
| LanceDB path | `D:/lance_db_soccer` |

---

## Setup Notes
- OBS used to capture live football streams (Paramount+, CBS) for BDF highlight pipeline
- Recordings land in `C:\Media\Recordings` — separate from Resolve render output (`C:\BDF\renders\`)
- NVENC encoder leverages RTX 5070 Ti for zero-CPU-cost recording at 60fps
- Replay buffer (F9/F10) used to grab spontaneous highlight moments without pre-recording
- Profile named `Untitled` — no multi-profile setup yet
- CQP 18 chosen over CBR: file size scales with scene complexity, better quality on action shots
