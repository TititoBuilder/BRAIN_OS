# BRAIN_OS Dashboard — Build Spec (v1)

A local, live, read-only dashboard for the BRAIN_OS vault. Four panels:
queue, system map, tools, venvs. Built as a FastAPI backend + Vite/React
frontend. Models the proven pattern from BDF's `dashboard_api.py` (FastAPI +
CORS + uvicorn) and CristianConstruction's `dashboard/src/Dashboard.jsx`
(api.js fetch helper + useEffect/useState), but written CLEAN — do NOT
replicate BDF's 2000-line accreted structure with duplicate app/route
definitions. One definition each, ~150 lines for the API.

## Location
Everything lives under `C:\BRAIN_OS\00_DASHBOARD\dashboard\`.

## Declared finish
One command launches both servers; opening localhost shows four live panels
reflecting current vault files. Read-only. No write-back, no file browser.

---

## Backend — `brain_dashboard_api.py`

FastAPI app, single `app = FastAPI()`, single CORS middleware block allowing
`http://localhost:5173`. Launches via `uvicorn.run(app, host="127.0.0.1", port=8000)`
under `if __name__ == "__main__":`. All file reads use `encoding="utf-8"`.
Use pathlib. Absolute base path: `BRAIN_OS = Path(r"C:\BRAIN_OS")`.

Four GET endpoints, each returning JSON:

### GET /api/queue
Parse `BRAIN_OS / "00_DASHBOARD" / "Queue.md"`.
- Track current section from `## ` headers (e.g. "In Progress", "Next Sessions").
- A line `lstrip().startswith("- [ ]")` is an OPEN item; `- [x]` is DONE.
- Item text = everything after the `]` marker, stripped.
- Return:
```
{
  "sections": [
    {"name": "In Progress", "items": [
        {"text": "...", "done": false}, ...
    ]}, ...
  ],
  "open_count": <int>,
  "done_count": <int>
}
```

### GET /api/system-map
Read `BRAIN_OS / "07_SYSTEM" / "system_map.json"` and return its parsed
contents directly (it already has the right shape: project/nodes with
venv, shared_packages, deploys, uses_drive). If the file is missing, return
`{"error": "system_map.json not found"}` with 200 (frontend handles gracefully).

### GET /api/tools
List `*.py` files in `BRAIN_OS / "09_TOOLS"`. For each, read the first
docstring line (the first non-empty line inside the opening `"""`), or first
`# comment` line, as a one-line description. Return:
```
{"tools": [{"name": "graphify.py", "desc": "..."}, ...], "count": <int>}
```
Sort alphabetically. Skip `__pycache__` and non-.py.

### GET /api/venvs
Derive from the system_map data (same source as /api/system-map). For each
project that has a venv, return its venv path and whether brain_audio is in
shared_packages. Return:
```
{"venvs": [{"project": "BDF", "venv": "...", "brain_audio": true}, ...]}
```

### GET /api/health
Return `{"status": "ok"}` — used by the frontend to show the live indicator.

---

## Frontend — Vite + React

Standard Vite React scaffold in the `dashboard/` folder (`npm create vite`
layout: package.json, vite.config.js, index.html, src/). Mirror CC's pattern:
- `src/api.js`: a small helper with `const BASE = 'http://localhost:8000'`
  and an `api` object exposing `queue()`, `systemMap()`, `tools()`, `venvs()`,
  `health()` — each `fetch(BASE + path).then(r => r.json())`.
- `src/App.jsx`: top bar (title "BRAIN_OS dashboard" + live indicator from
  /api/health), a row of 4 metric cards (open queue items, projects mapped,
  tools count, venvs tracked), then a 2-column grid of 4 panels.
- Four panel components (can be in App.jsx or separate files):
  - QueuePanel: sections with checkboxes (done = checked + muted, open =
    unchecked). Show open items first/prominently.
  - SystemMapPanel: a table — project | venv | brain_audio | deploys | drive.
  - ToolsPanel: list of tool name (mono font) + description.
  - VenvsPanel: list of venv + brain_audio indicator.
- Fetch all on mount with useEffect/useState. Handle loading + error states
  (show "loading…" then data, or a friendly error if API is down).

Styling: clean, minimal, readable. Plain CSS is fine (App.css). Dark text on
light, simple borders, generous spacing. No heavy framework needed.

---

## Launcher — `launch_dashboard.ps1`

In `00_DASHBOARD\dashboard\`. Starts both servers:
1. Start the API in a background job/window using the BRAIN_OS-appropriate
   Python. NOTE: pick the Python that has fastapi+uvicorn installed. BDF's
   venv has fastapi (`C:\Dev\Projects\soccer-content-generator\venv`). EITHER
   reuse that venv OR document that the user must `pip install fastapi uvicorn`
   into the chosen interpreter. Flag this clearly in the script comments.
2. Start the frontend: `cd` into dashboard, `npm run dev`.
3. Print the URL (http://localhost:5173) to open.

Use clear Write-Host status lines. Do NOT hardcode assumptions about which
venv — detect or document.

---

## Constraints (BRAIN_OS rules)
- All Python file writes: `encoding="utf-8"`, no BOM.
- Clean, single-definition code. No duplicate app/route blocks.
- Do not commit `node_modules` (gitignore already covers it; verify a
  `.gitignore` exists in the dashboard folder or rely on the vault one).
- Read-only: no endpoint writes to any vault file in v1.
- Verify the API parses and the frontend builds; do not start servers or
  git commit — the user does that.
