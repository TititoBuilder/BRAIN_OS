---
tags: [system, flow-launcher, aliases, shortcuts, hotkeys]
status: active — 18 aliases configured 2026-04-29
version: Flow Launcher 2.1.1
install: C:\Users\titit\AppData\Local\FlowLauncher
settings: C:\Users\titit\AppData\Roaming\FlowLauncher\Settings\Settings.json
---

# Flow Launcher Aliases

All keyword aliases for the BDF, CA, Resolve MCP, and Read-Along projects,
plus system shortcuts for OBS, DaVinci, SyncThing, and BRAIN_OS.

---

## Status

| Mechanism | Status |
|---|---|
| `Settings.json` | ✅ Generated — 18 aliases written 2026-04-29 |
| Shell plugin (`>` prefix) | ✅ Works — type `> python bot_service.py` etc. |
| Custom keyword aliases | ✅ Active — restart Flow Launcher to apply |
| `start_bdf.ps1` launcher | ✅ Works — `.\start_bdf.ps1` from any terminal |

---

## All Aliases

### BDF Soccer Bot

| Keyword | Command | Notes |
|---|---|---|
| `bdf` | `code C:\Dev\Projects\soccer-content-generator\bdf.code-workspace` | Opens VS Code workspace |
| `bdf-start` | `pwsh -File C:\Dev\Projects\soccer-content-generator\start_bdf.ps1` | Opens 4 WT tabs |
| `bot` | `pwsh -Command "Set-Location 'C:\Dev\Projects\soccer-content-generator'; .\venv\Scripts\Activate.ps1; python bot_service.py"` | Bot service only |
| `relay` | `pwsh -Command "Set-Location 'C:\Dev\Projects\soccer-content-generator'; .\venv\Scripts\Activate.ps1; python obs_relay.py --match UCL --default-event HIGHLIGHT"` | OBS relay |
| `obs-mcp` | `pwsh -NoExit -Command "Set-Location 'C:\Dev\Projects\soccer-content-generator'; .\venv\Scripts\Activate.ps1; python obs_mcp.py"` | OBS WebSocket MCP (port 8001) |
| `dash` | `start http://localhost:5173` | Open dashboard in browser |
| `sync` | `pwsh -Command "Set-Location 'C:\Dev\Projects\soccer-content-generator'; .\venv\Scripts\Activate.ps1; python sync_brain.py"` | Weekly brain sync |

### Custom Agent

| Keyword | Command |
|---|---|
| `ca` | `code C:\Dev\CristianConstruction\` |
| `ca-api` | `pwsh -Command "Set-Location 'C:\Dev\CristianConstruction'; uvicorn main:app --reload"` |

### Resolve MCP

| Keyword | Command |
|---|---|
| `mcp` | `code C:\Users\titit\Projects\resolve-mcp-server\` |
| `bridge` | `pwsh -Command "python C:\Users\titit\Projects\resolve-mcp-server\resolve_bridge.py"` |

### Read-Along App

| Keyword | Command |
|---|---|
| `read` | `code C:\Users\titit\Projects\read-along-app\` |
| `read-api` | `pwsh -Command "python C:\Users\titit\Projects\read-along-app\backend\backend.py"` |

### System

| Keyword | Command |
|---|---|
| `brain` | `code C:\BRAIN_OS\` |
| `obs` | `start "" "C:\Program Files\obs-studio\bin\64bit\obs64.exe"` |
| `davinci` | `start DaVinci Resolve` |
| `st` | `start "" "C:\Dev\Tools\syncthing\syncthing-windows-amd64-v2.0.15\syncthing.exe"` |
| `predator` | `start PredatorSense` |

---

## Shell Plugin — Works Today (No Setup Required)

The Shell plugin is triggered by `>` in Flow Launcher.
Use these while waiting for Settings.json to exist:

```
> python C:\Dev\Projects\soccer-content-generator\bot_service.py
> python C:\Dev\Projects\soccer-content-generator\sync_brain.py
> pwsh -File C:\Dev\Projects\soccer-content-generator\start_bdf.ps1
> code C:\BRAIN_OS\
> code C:\Dev\Projects\soccer-content-generator\
> start http://localhost:5173
```

---

## Setup: Adding Keyword Aliases

### Step 1 — Generate Settings.json

Run Flow Launcher from the Start Menu or:
```
C:\Users\titit\AppData\Local\FlowLauncher\Flow.Launcher.exe
```
This creates:
```
C:\Users\titit\AppData\Roaming\FlowLauncher\Settings\Settings.json
```

### Step 2 — Add CustomShortcuts to Settings.json

Open Settings.json and merge in this block (add inside the root `{}` object):

```json
"CustomShortcuts": [
  { "Key": "bdf",       "Value": "code C:\\Dev\\Projects\\soccer-content-generator\\bdf.code-workspace" },
  { "Key": "bdf-start", "Value": "pwsh -File C:\\Dev\\Projects\\soccer-content-generator\\start_bdf.ps1" },
  { "Key": "bot",       "Value": "pwsh -NoExit -Command \"Set-Location 'C:\\Dev\\Projects\\soccer-content-generator'; .\\venv\\Scripts\\Activate.ps1; python bot_service.py\"" },
  { "Key": "relay",     "Value": "pwsh -NoExit -Command \"Set-Location 'C:\\Dev\\Projects\\soccer-content-generator'; .\\venv\\Scripts\\Activate.ps1; python obs_relay.py --match UCL --default-event HIGHLIGHT\"" },
  { "Key": "dash",      "Value": "http://localhost:5173" },
  { "Key": "sync",      "Value": "pwsh -Command \"Set-Location 'C:\\Dev\\Projects\\soccer-content-generator'; .\\venv\\Scripts\\Activate.ps1; python sync_brain.py\"" },
  { "Key": "ca",        "Value": "code C:\\Dev\\CristianConstruction\\" },
  { "Key": "ca-api",    "Value": "pwsh -NoExit -Command \"Set-Location 'C:\\Dev\\CristianConstruction'; uvicorn main:app --reload\"" },
  { "Key": "mcp",       "Value": "code C:\\Users\\titit\\Projects\\resolve-mcp-server\\" },
  { "Key": "bridge",    "Value": "pwsh -Command \"python C:\\Users\\titit\\Projects\\resolve-mcp-server\\resolve_bridge.py\"" },
  { "Key": "read",      "Value": "code C:\\Users\\titit\\Projects\\read-along-app\\" },
  { "Key": "read-api",  "Value": "pwsh -Command \"python C:\\Users\\titit\\Projects\\read-along-app\\backend\\backend.py\"" },
  { "Key": "brain",     "Value": "code C:\\BRAIN_OS\\" },
  { "Key": "obs",       "Value": "C:\\Program Files\\obs-studio\\bin\\64bit\\obs64.exe" },
  { "Key": "davinci",   "Value": "DaVinci Resolve" },
  { "Key": "st",        "Value": "C:\\Dev\\Tools\\syncthing\\syncthing-windows-amd64-v2.0.15\\syncthing.exe" },
  { "Key": "predator",  "Value": "PredatorSense" }
]
```

### Step 3 — Restart Flow Launcher

Right-click the Flow Launcher tray icon → Restart.

---

## Alternative: Flow Launcher UI (no JSON editing)

1. Open Flow Launcher settings → **Plugin** tab → **Shell**
2. For each alias, the Shell plugin doesn't support saved aliases natively.
3. Install the **Custom Shortcuts** community plugin instead:
   - In Flow Launcher, type `pm install Custom Shortcuts`
   - Then configure via Settings → Plugins → Custom Shortcuts

---

## `start_bdf.ps1` — 4-Tab Launcher

File: `C:\Dev\Projects\soccer-content-generator\start_bdf.ps1`

```powershell
# Run from any terminal:
.\start_bdf.ps1                              # prompts for match
.\start_bdf.ps1 -Match UCL_Atletico_Arsenal  # fully automated
.\start_bdf.ps1 -Match skip                  # skips relay tab
```

Tabs opened:
| Tab | Color | Command |
|---|---|---|
| Bot Service | 🟢 Dark green | `python bot_service.py` |
| Dashboard API | 🔵 Dark blue | `python dashboard_api.py` |
| Frontend | 🟣 Purple | `npm run dev` |
| OBS Relay | 🟠 Orange | `python obs_relay.py --match ... --default-event HIGHLIGHT` |

---

## Connected to
- [[Tools_Registry]]
- [[Active_Environments]]
- [[BDF_Canvas]]
