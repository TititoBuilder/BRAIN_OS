---
tags: [skills, obs, recording, capture, streaming]
status: in-progress
parent: "[[10_SKILLS_INDEX]]"
children: []
proof: recording configured, replay buffer F8/F9/F10 armed
blocking: OBS MCP v5 WebSocket incompatibility
---

# OBS Skill

OBS Studio — screen capture and recording for the BDF highlight pipeline.
Recording and replay buffer are operational; MCP automation is blocked pending a v5-compatible library.

---

## Status
**In-progress** — core recording configured and working. MCP control layer blocked.

---

## Personal Config

| Setting | Value |
|---|---|
| Encoder | NVENC H.264 (`obs_nvenc_h264_tex`) |
| Format | MKV |
| Output Path | `C:\BDF_OBS_Clips\RawFootage` |
| Replay Buffer | 60 seconds |
| Resolution | 1920 × 1080 |
| FPS | 60 |
| Color Space | BT.709 / Full range |

### Hotkeys
| Hotkey | Action |
|---|---|
| `F8` | Start / Stop Recording |
| `F9` | Start / Stop Replay Buffer |
| `F10` | Save Replay Buffer |

---

## Blocking Issue

**OBS MCP — obsws-python v5 WebSocket incompatibility**
- `obsws-python` targets the old v4 WebSocket API and fails to authenticate against OBS v5 (port 4455, auth enabled).
- MCP server at `C:\Users\titit\Projects\obs-mcp-server\server_api.py` is currently offline.

### Active Workaround
AutoHotkey script `obs_control.ahk` sends F8/F9/F10 hotkeys to control OBS without WebSocket.
- Script: `C:\Users\titit\obs_control.ahk`
- Auto-starts on boot via Windows Startup folder
- See [[Windows_Tools_Node]] → AutoHotkey

### Resolution Path
- Monitor `obsws-python` for v5 support, **or**
- Rebuild MCP server using `simpleobsws` (native OBS v5 WebSocket library)

---

## Proof of Work
- 2026-04-28: Recording path, format, encoder, replay buffer, hotkeys all configured
- MCP blocker documented in [[OBS_Node]] → Known Issues
- AHK workaround deployed and verified
