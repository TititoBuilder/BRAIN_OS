---
tags: [skills, obs, recording, capture, streaming]
status: active
parent: "[[10_SKILLS_INDEX]]"
children: []
proof: recording confirmed operational 2026-04-29 — CQP 18, 20s replay, C:\Media\Recordings
blocking: none
confirmed: 2026-04-29
mcp: obs_mcp.py — simpleobsws 1.4.x — port 8001 — resolved 2026-04-29
---

# OBS Skill

OBS Studio — screen capture and recording for the BDF highlight pipeline.
Recording, replay buffer, and WebSocket MCP control are all operational.

---

## Status
**Active** — fully operational. Recording + MCP control layer live.

---

## Personal Config (Predator — confirmed 2026-04-29)

| Setting | Value |
|---|---|
| Machine | Predator (hostname: CRISTIAN) |
| Encoder | NVENC H.264 (`obs_nvenc_h264_tex`) |
| Rate Control | **CQP** |
| CQ Level | **18** |
| Format | MKV |
| Output Path | `C:\Media\Recordings` |
| Replay Buffer | **20 seconds** |
| Resolution | 1920 × 1080 |
| FPS | 60 |
| Color Format | NV12 |
| Color Space | Rec. 709 |
| Color Range | Full |
| Browser HW Accel | **DISABLED** |
| Process Priority | **High** |

### Hotkeys
| Hotkey | Action |
|---|---|
| `F8` | Start / Stop Recording |
| `F9` | Start / Stop Replay Buffer |
| `F10` | Save Replay |

---

## MCP Control Layer

**obs_mcp.py** — `C:\Dev\Projects\soccer-content-generator\obs_mcp.py`
- Library: `simpleobsws` 1.4.x (native OBS WebSocket v5 protocol)
- Port: 8001 (standalone FastAPI)
- WebSocket target: `ws://localhost:4455`, password via `OBS_WS_PASSWORD` in `.env`
- Run: `python obs_mcp.py`
- Import: `from obs_mcp import OBSController`

| Endpoint | Action |
|---|---|
| `GET  /obs/status` | recording state, replay buffer state, current scene |
| `POST /obs/save_replay` | SaveReplayBuffer (F10 equivalent) |
| `POST /obs/start_replay_buffer` | StartReplayBuffer |
| `POST /obs/stop_replay_buffer` | StopReplayBuffer |
| `POST /obs/start_recording` | StartRecord |
| `POST /obs/stop_recording` | StopRecord |
| `POST /obs/set_scene` | SetCurrentProgramScene |

OBS offline → returns `{"status": "obs_offline"}`, never crashes.
Auto-reconnects on each call if connection dropped.

### Previous Blocker (resolved 2026-04-29)
`obsws-python` targeted v4 WebSocket API — incompatible with OBS v5 (port 4455).
Replaced with `simpleobsws`. AHK hotkey workaround (`obs_control.ahk`) still boots on startup as fallback.

---

## WD Elements / LanceDB

| Note | Value |
|---|---|
| WD Elements mount | Always `D:` on Predator |
| Why not `F:` | Recovery partition blocks `F:` assignment |
| LanceDB path | `D:/lance_db_soccer` |

---

## Proof of Work
- 2026-04-29: `obs_mcp.py` built with `simpleobsws` — v5 WebSocket blocker resolved
- 2026-04-29: Settings confirmed in active match-day use — CQP 18, 20s buffer, `C:\Media\Recordings`
- 2026-04-28: Recording path, format, encoder, replay buffer, hotkeys configured
- AHK workaround (`obs_control.ahk`) remains as boot-time fallback
