---
tags: [tools, book, reference, stack, documentation]
status: active
dependencies: []
parent: "[[09_TOOLS_INDEX]]"
children:
  - "[[VSCode_Node]]"
  - "[[Windows_Tools_Node]]"
  - "[[Predator_Node]]"
  - "[[OBS_Node]]"
---

# Tools Book Node

Master book entry for all tools, software, and hardware in the BRAIN_OS stack.
This is the single source of truth for what is installed, why, and how it fits together.

---

## Purpose

Document every tool in the development and content-production environment so that:
- Onboarding a new machine is reproducible
- AI agents (Claude Code, MCP) have full context on available tooling
- Version changes and config drifts are tracked over time

---

## Current Stack

### Editor
| Tool | Version | Role |
|---|---|---|
| VS Code | Latest | Primary code editor |
| GitLens | 17.12.2 | Git blame, history, worktrees |
| Git Graph | 1.30.0 | Visual commit graph |
| Claude Code | 2.1.121 | AI agent in-editor |
| GitHub Copilot Chat | 0.45.1 | Inline AI assist |
| Pylance | 2026.2.1 | Python type-checking & IntelliSense |
| Python (ms-python) | 2026.4.0 | Python runtime integration |
| Debugpy | 2026.4.0 | Python debugger |
| Python Envs | 1.28.0 | Virtualenv manager |
| PowerShell | 2025.4.0 | PS scripting support |
| Run on Save | 1.0.3 | File-event automation |
| Error Lens | 3.28.0 | Inline diagnostics |
| Material Icon Theme | 5.34.0 | Icon theme |
| Todo Tree | 0.0.226 | TODO tag tracker |
| Obsidian MD | 1.3.0 | Wikilink-aware Markdown |

### System Utilities
| Tool | Role |
|---|---|
| PowerToys (21 modules) | Window management, productivity, FancyZones |
| SyncThing | Peer-to-peer file sync |

### Content Production
| Tool | Role |
|---|---|
| OBS Studio | 60fps NVENC screen capture + replay buffer |
| DaVinci Resolve Free | Video editing & render queue for BDF pipeline |

### Hardware
| Component | Spec |
|---|---|
| GPU | RTX 5070 Ti |
| CUDA | 12.8 |
| Display | 165Hz, 1920×1080 |
| Platform | Acer Predator, Windows 11 Home |

---

## Setup Notes

### VS Code
- Install extensions from `.vscode/extensions.json` or install each ID manually
- Python virtualenvs managed per project via Python Envs extension
- `runonsave` config lives in workspace `settings.json` per repo

### PowerToys
- Install from Microsoft Store or GitHub releases
- FancyZones layout: export/import via PowerToys Settings → FancyZones → Layout backup
- Awake module prevents sleep during Resolve render queue runs

### OBS
- Profile `Untitled` — settings at `C:\Users\titit\AppData\Roaming\obs-studio\basic\profiles\Untitled\`
- Recordings to `C:/Media/Recordings/` — ensure drive has space before long sessions
- Replay buffer: always start with F7 before watching live matches
- NVENC requires RTX GPU — encoder: `obs_nvenc_h264_tex`

### DaVinci Resolve (BDF pipeline)
- Resolve Free — limited to one render job at a time (see CLAUDE.md for full constraints)
- Bridge started via Resolve Py3 console
- Render presets: 5 active platforms (YouTube 1080p, TikTok, Instagram, Twitter, Facebook)

### Predator
- Turbo mode via Predator Sense — required for sustained NVENC + Python compute
- CUDA 12.8 required for `mcp_ingest.py` LanceDB vector ops

---

## Version History

| Date | Change |
|---|---|
| 2026-04-28 | Initial documentation — all nodes created from live system scan |
