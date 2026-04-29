---
tags: [tools, windows, powertoys, utilities, system]
status: active
dependencies: [Windows 11]
parent: "[[09_TOOLS_INDEX]]"
children:
  - "[[PowerToys_Node]]"
  - "[[SyncThing_Node]]"
  - "[[obs_control.ahk]]"
---

# Windows Tools Node

System-level utilities and productivity tools installed on the Predator desktop.
Documented 2026-04-28.

---

## PowerToys
Microsoft open-source utility suite. Installed at:
`C:\Users\titit\AppData\Local\PowerToys\`

### Active Modules

| Module | Description |
|---|---|
| **Always on Top** | Pin any window to always stay above others (Win+Ctrl+T) |
| **Awake** | Keep PC awake without changing power settings — useful during renders |
| **Color Picker** | System-wide color sampler; copies HEX/RGB/HSL (Win+Shift+C) |
| **Command Palette** | Unified app + command launcher (replaces PowerToys Run with richer UI) |
| **Crop & Lock** | Create a cropped, locked thumbnail of any window |
| **FancyZones** | Custom window snap layout manager — configured for multi-monitor/ultrawide |
| **File Locksmith** | Right-click to see which processes are locking a file |
| **Find My Mouse** | Spotlight shake to locate cursor (Ctrl×2) |
| **Image Resizer** | Right-click bulk image resize |
| **Keyboard Manager** | Remap keys and shortcuts globally |
| **Light Switch** | Quick dark/light mode toggle |
| **Mouse Highlighter** | Highlight clicks for screen recording/demos |
| **Mouse Jump** | Jump mouse between monitors instantly |
| **Mouse Pointer Crosshairs** | Crosshair overlay for precise positioning |
| **Mouse Without Borders** | Share keyboard & mouse across multiple PCs on LAN |
| **PowerAccent** | Type accented characters by holding a letter key |
| **PowerOCR (Text Extractor)** | Screenshot OCR — extract text from any screen area (Win+Shift+T) |
| **Preview Handlers** | Explorer preview pane for SVG, PDF, Markdown, code, Gcode, QOI |
| **Shortcut Guide** | Overlay showing Win key shortcuts (hold Win) |
| **Workspaces** | Save and restore app/window layout snapshots |
| **ZoomIt** | Screen zoom and annotation tool (useful for recordings) |

### FancyZones Layout Notes
- Custom zone layout active — ultrawide/multi-zone split
- Layout persists across monitor connects/disconnects
- Used alongside Resolve + Claude Code + browser for the BDF pipeline

---

## AutoHotkey
Version: **2.0.24**

| Setting | Value |
|---|---|
| Script | `C:\Users\titit\obs_control.ahk` |
| Hotkeys | F8 = Start/Stop Recording · F9 = Start/Stop Replay Buffer · F10 = Save Replay Buffer |
| Auto-start | Shortcut in Windows Startup folder — runs on every boot |

### Purpose
Controls OBS Studio via hotkeys as a workaround for obsws-python's incompatibility with OBS v5 WebSocket. See [[OBS_Node]] → Known Issues.

### Child scripts
- [[obs_control.ahk]] — OBS hotkey controller (F8/F9/F10)

---

## Flow Launcher
**Not confirmed installed** — not found at standard paths.
May not be present or may use PowerToys Command Palette instead.

---

## SyncThing
Peer-to-peer file sync tool.
- **Status**: Listed in system inventory; exact install path not confirmed
- **Use case**: Sync project files and library exports between machines
- **Config**: Check `http://localhost:8384` for web UI when running
