---
tags: [tools, hardware, predator, gpu, display, system]
status: active
dependencies: []
parent: "[[09_TOOLS_INDEX]]"
children: []
---

# Predator Node

Acer Predator desktop — primary workstation for the BDF pipeline, AI dev, and content production.
Documented 2026-04-28.

---

## Hardware Specs

| Component | Spec |
|---|---|
| GPU | NVIDIA GeForce RTX 5070 Ti |
| CUDA | 12.8 |
| Display | 165Hz monitor |
| OS | Windows 11 Home |

---

## Power & Performance Profiles

### Turbo Mode
- Activated via Predator Sense app
- Maximizes CPU + GPU clocks, disables power limits
- Used during DaVinci Resolve renders and AI inference workloads
- Fans ramp to max — audible but necessary for sustained GPU load

### Power Profiles

| Profile | Use Case |
|---|---|
| **Turbo** | Render queue, GPU compute, heavy AI tasks |
| **Performance** | Normal dev work with full CPU headroom |
| **Balanced** | Everyday use, reduced fan noise |
| **Eco** | Battery preservation / low-load tasks |

Profiles switched via Predator Sense or keyboard shortcut.

---

## Display

- **Refresh rate**: 165Hz
- **Resolution**: 1920×1080 (confirmed via OBS base canvas)
- **FreeSync / G-Sync**: enabled via NVIDIA Control Panel

---

## GPU & CUDA

| Item | Value |
|---|---|
| GPU | RTX 5070 Ti |
| CUDA Version | 12.8 |
| NVENC | Available — used by OBS and DaVinci Resolve render queue |
| Driver API | Used by `resolve_bridge.py` for hardware-accelerated export |

---

## FancyZones Layout (via PowerToys)

Custom snap zones configured for the BDF workflow:
- Zone 1: DaVinci Resolve (primary — wide)
- Zone 2: Terminal / Claude Code (right panel)
- Zone 3: Browser / reference (floating or secondary)

Layout saved via PowerToys Workspaces.

---

## Setup Notes
- Resolve Free Tier runs in the main desktop session — bridge (`resolve_bridge.py`) must be pasted into Resolve Py3 console
- NVENC used for both OBS recording and Resolve render presets
- CUDA 12.8 required for LanceDB + ML enrichment pipeline in `mcp_ingest.py`
