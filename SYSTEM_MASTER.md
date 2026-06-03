# SYSTEM_MASTER.md
> System-level infrastructure knowledge extracted from BDF_Book and BrainOS_Book distilled files.
> Applies across ALL projects. Last updated: 2026-05-24.

---

## Hardware & Runtime

| Item              | Detail                                                                                             |
| ----------------- | -------------------------------------------------------------------------------------------------- |
| Machine           | Acer Predator Helios — canonical/sole active dev machine as of April 2026                          |
| GPU               | NVIDIA GeForce RTX 5070 Ti Laptop GPU                                                              |
| CUDA              | sm_120 (Blackwell) — requires PyTorch nightly cu128                                                |
| AI Venv           | `C:\Knowledge\CA\venv` — canonical for all AI/TTS/PyTorch work                                     |
| PyTorch           | nightly cu128 installed, CUDA verified True                                                        |
| CPU fallback      | Never install CPU-only torch — always use nightly cu128                                            |
| Python Version    | 3.12.10                                                                                            |
| System Python     | `C:\Users\titit\AppData\Local\Programs\Python\Python312` — no AI packages, never use for inference |
| Secondary Machine | HP Laptop — OBS recording and streaming only (not for development)                                 |
| Retired Machine   | Dell workstation — permanently retired due to hardware failure (April 2026)                        |

---

## Canonical Paths

| Path | Purpose |
|---|---|
| `C:\Dev\Projects\soccer-content-generator\` | Core BDF pipeline — canonical single source of truth |
| `C:\Knowledge\BDF\` | BDF knowledge documents (absolute separation from code) |
| `C:\Knowledge\BDF\BDF_Book\` | BDF book root |
| `C:\Knowledge\BDF\BDF_Book\incoming\` | Session file drop zone |
| `C:\Knowledge\BDF\BDF_Book\incoming\_processed\` | Successfully merged files archive |
| `C:\Knowledge\BDF\BDF_Book\incoming\_review\` | Quarantined files (unknown tags or low confidence) |
| `C:\Knowledge\BDF\BDF_Book\incoming\_rejected\` | Non-BDF content (preserved but excluded) |
| `C:\Knowledge\BDF\BDF_Book\chapters\` | Compiler-managed chapter files |
| `C:\Knowledge\BDF\BDF_Book\audio\` | TTS output files |
| `C:\Knowledge\BDF\BDF_Book\BDF_Master_Book.txt` | Auto-generated master book (never edit directly) |
| `C:\Knowledge\BDF\Session_Resumes\processed\` | Session resume archive (canonical target) |
| `C:\lance_db_soccer\` | LanceDB vector database (canonical as of May 2026; previously `F:\`) |
| `F:\` | WD Elements external drive — permanently on Predator, never moved |
| `C:\BRAIN_OS\` | BRAIN_OS Obsidian vault (knowledge system) |
| `C:\BDF_Share\` | SyncThing sync folder (local path on both HP and Predator) |
| `C:\Dev\CristianConstruction\` | Custom Agent / Cristian Construction project root |
| `C:\Users\titit\Projects\resolve-mcp-server\` | DaVinci Resolve MCP server project |
| `C:\Users\titit\Projects\resolve-mcp-server\resolve_bridge.py` | Bridge script (must reload with `encoding="utf-8"`) |
| `D:\BDF_RawFootage\` | OBS recording directory (HP laptop) |
| `D:\DaVinci_Archive\` | DaVinci Resolve archive (Installers, Live_ProjectLib, BACKUP, Fusion_AutoSaves) |
| `D:\BDF\documentation\session-logs\` | Session logs (monthly subdirectories) |
| `C:\Dev\Projects\soccer-content-generator\gdrive_credentials.json` | Google Drive credentials |
| `C:\Program Files\Blackmagic Design\DaVinci Resolve\Resolve.exe` | DaVinci Resolve installation |
| `C:\Users\titit\AppData\Roaming\Blackmagic Design\DaVinci Resolve\` | Resolve project database |
| `C:\Users\titit\Downloads\` | Chrome downloads (create manually if missing — OneDrive can delete it) |

**PowerShell Profiles** (must be kept identical):
- `C:\Users\titit\OneDrive\Documents\WindowsPowerShell\Microsoft.VSCode_profile.ps1`
- `C:\Users\titit\OneDrive\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1`

**VS Code Workspaces**:
- `bdf.code-workspace` — includes soccer-content-generator and resolve-mcp-server
- `custom-agent.code-workspace`
- `read-along-app.code-workspace`
- `resolve-mcp-server.code-workspace`

---

## Python Environments & Venvs

### BDF Soccer Content Generator
- **Path**: `C:\Dev\Projects\soccer-content-generator\venv\`
- **Purpose**: Core BDF pipeline (bot service, clip watcher, SoccerBot, TTS compilation)
- **Key packages**: mcp, anthropic, tweepy, uvicorn, fastapi, pillow, lancedb, kokoro, ffmpeg

### Custom Agent / Cristian Construction
- **Path**: `C:\Dev\CristianConstruction\venv\`
- **Purpose**: Custom Agent work — isolated from soccer venv to prevent conflicts (created May 2026)
- **Key packages**: fastapi, uvicorn, anthropic (minimal, clean)

### Resolve MCP Server
- **Path**: `C:\Users\titit\Projects\resolve-mcp-server\venv\`
- **Purpose**: DaVinci Resolve MCP server automation
- **Key packages**: mcp, pyautogui, pywinauto

### AI / TTS / PyTorch (Canonical)
- **Path**: `C:\Knowledge\CA\venv`
- **Purpose**: All AI inference, TTS (Kokoro), PyTorch workloads
- **PyTorch**: nightly cu128 — sm_120 Blackwell (RTX 5070 Ti)

### Verification
```powershell
where.exe python        # Use where.exe, NOT where, in PowerShell
& "C:\path\to\venv\Scripts\Activate.ps1"
where.exe python        # Verify correct location after activation
```

---

## PowerShell Aliases

All aliases defined in both profile files (must be kept identical):

| Alias | Purpose |
|---|---|
| `bdf-log` | Move current session to `C:\Knowledge\BDF\Session_Resumes\processed\` |
| `bdf-compile` | Move compile file from Downloads to `BDF_Book/incoming/` |
| `bdf-book` | Full BDF compile with venv activation |
| `ca-log` | Move session to CristianConstruction archive |
| `ca-compile` | Move compile file from Downloads to `CA_Book/incoming/` |
| `ca-book` | Full CA compile with venv |
| `ca-audio` | Generate TTS audio for CA book |
| `dev` | File watcher for active development |
| `map-bdf` | Run `scripts/graph_maintainer.py` from soccer-content-generator — hash check, audio parity (HEALTHY/STALE/MISSING/ORPHANED vs Drive), dependency mapping, graphify update |
| `mcp-log` | Move session file from Downloads → `C:\Knowledge\MCP\Session_Resumes\processed\` |
| `mcp-compile` | Move compile file from Downloads → `C:\Knowledge\MCP\MCP_Book\incoming\` |
| `mcp-book` | Activate BDF venv, run `mcp_book_compiler.py` from soccer-content-generator |
| `bdf-tts` | `C:\Knowledge\CA\venv` python → `tts_local.py` in BDF project |
| `brainos-book` | `C:\Knowledge\CA\venv` python → `book_compiler.py --book brainos` from shared compiler |
| `cc` | Run `claude --dangerously-skip-permissions` (unrestricted Claude Code shell) |

**Verify aliases**:
```powershell
Get-Command bdf-log, bdf-compile, bdf-book, ca-log, ca-compile, ca-book, ca-audio, dev
code $PROFILE
$PROFILE | Format-List -Force *   # Show all four profile locations
```

---

## Cross-Project Rules (Never Do This)

### BDF_Master_Book.txt — never edit directly
Always regenerated by compiler from chapter files. Direct edits vanish on next compilation run. All modifications must flow through the chapter structure.

### Never batch multiple compile files
Running multiple files simultaneously causes exponential token cost ($7-8 batched vs $1.50-2.50 single). Each successive merge reads all previous merges as input tokens. Rule: one `bdf-compile` → wait for completion → `bdf-book` → repeat.

### Never run bot_service.py and enhanced_terminal_ui.py simultaneously
Both load SoccerBot and will conflict. Use `bot_service.py` as headless engine.

### Never move the WD Elements external drive between machines
LanceDB vector store corruption risk. Keep permanently on Predator.

### Never use OneDrive for video or large file transfers
Silent 0-byte failures and multi-minute delays. Use SyncThing (50MB < 10 seconds) or local copy.

### Never use relative paths in automation
Break when run from unexpected directories. Always use absolute paths in PowerShell functions and scripts.

### Never run Anthropic API calls with Surfshark VPN active
McAfee + VPN both intercept SSL → `WinError 10054` connection resets. Pause VPN before any Anthropic API calls or SyncThing local discovery.

### Never use bare `except: pass` blocks
Creates silent debugging nightmares. Every `except` block must: re-raise, log, store in accessible state, or return an error status.

### Never skip encoding parameter when reloading the Resolve bridge
`UnicodeDecodeError: 'charmap' codec can't decode` without it. Reload command must be:
```python
exec(open(r"C:\path\to\resolve_bridge.py", encoding="utf-8").read())
```

### Never use Unicode symbols in pipeline print statements
Crashes on cp1252 terminals or pipes. Use ASCII only: `[OK]`, `[FAIL]`, `->`, etc.

### Never commit LanceDB vector store to Git
Stores rebuild locally per machine. Keep `lance_db` folder in `.gitignore`.

### Never use file timestamps alone for video stability validation
OBS writes clips asynchronously. Pattern: wait 5 seconds, compare file sizes before and after, skip 0-byte files unconditionally.

### Never assume the Downloads folder exists
OneDrive sync conflicts or accidental deletion can remove it. Create with:
```powershell
New-Item -ItemType Directory -Path "$HOME\Downloads"
```

### Never let PowerShell profiles diverge
VS Code loads `Microsoft.VSCode_profile.ps1`; standalone PowerShell loads `Microsoft.PowerShell_profile.ps1`. Divergence causes aliases to work in one context and silently fail in the other. Keep both files identical.

### Never assume implicit attributes in multi-stage pipelines
Silent failures when attributes aren't explicitly declared at each stage. Always declare every attribute in `__init__()`. Use `getattr(obj, "attr", None)` defensively only at system boundaries.

### Never use string values where enums are expected
Passes without immediate error; crashes deep in call stack with `'str' has no attribute value`. Use `ContentType.MATCH_RECAP`, not `"match_recap"`.

### Never run bulk TTS without checking existing audio first
Regenerating audio that already exists wastes GPU time and risks overwriting good files. Always use the skip-existing pattern:
```powershell
Where-Object { -not (Test-Path ($_.FullName -replace '_TTS\.txt$', '_af_heart_audio.mp3')) }
```

---

## Architecture Decisions

### Two-machine architecture with SyncThing
- **HP Laptop**: OBS recording to `D:\BDF_RawFootage`, DaVinci Resolve editing/exports
- **Predator (canonical)**: AI processing, LanceDB at `C:\lance_db_soccer`, publishing pipeline
- **Sync method**: SyncThing LAN direct (`C:\BDF_Share\` on both); replaces OneDrive (multi-minute, silent 0-byte failures)
- **VPN rule**: Pause on both machines before match sessions — VPN breaks SyncThing local discovery

### Three-outcome file routing
Every incoming file has one deterministic fate:
- **Merged**: integrates cleanly into known chapter
- **Quarantined**: unknown tag or confidence < 7 → `incoming\_review\`
- **Rejected**: fails BDF relevance filter → `incoming\_rejected\` (preserved but excluded)

### Confidence-scored auto-routing thresholds
- 8–10: auto-route to chapter
- 7: flag for operator review
- ≤ 6: quarantine to `incoming\_review\`

### One-file-per-compilation rule
Never batch. Each successive merge reads all previous merges as input tokens — exponential cost growth. Process one file → wait → repeat.

### Three-layer application architecture
- **Layer 1**: Python backend (core processing engine)
- **Layer 2**: FastAPI server (HTTP bridge on `localhost:8000`)
- **Layer 3**: React dashboard (visual surface on `localhost:5173` via axios)

### Dual Twitter API approach
- v2 (`tweepy.Client`): post tweets
- v1.1 (`tweepy.API`): upload media (free tier does not support v2 media uploads)

### Local TTS over cloud
Kokoro-82M on RTX 5070 Ti: zero per-audio API costs, consistent voice, no latency. Sentence-level chunking at ~400 characters with 0.3s silence between chunks.

### Two-process socket architecture for DaVinci Resolve
Resolve Free blocks all external API access. TCP socket on `127.0.0.1:9000` bridges external MCP server to Resolve's embedded Python console. Each tool call opens a fresh socket connection (no persistent pool, no leaked resources).

### Windows encoding boundary pattern
- Every `open()`: explicit `encoding="utf-8"`
- Every subprocess: `PYTHONIOENCODING="utf-8"` env var
- Every subprocess pipe: `encoding="utf-8", errors="replace"`
- Python defaults to cp1252 on Windows — footgun in cross-terminal pipelines

### Hybrid approval model
Automation handles all preparation (generation, formatting, scheduling). Human judgment preserved only at the consequence moment (external publish). Telegram = mobile approval interface, no desktop dependency.

### Session as atomic unit
Every session: self-contained, documented, integrated. Produces tangible artifacts + handoff bridge. Three phases: (1) initialization, (2) active work, (3) compilation. Compensates for AI context limitations by building persistent knowledge.

### Knowledge–code separation
- Code (executable): `C:\Dev\Projects\`
- Knowledge (documents): `C:\Knowledge\`
- Large data: `C:\lance_db_soccer\`, `F:\`
Knowledge documents describe systems but never contain executable systems.

### Background daemon thread for async Telegram callbacks
Callback expiry window is 60 seconds absolute. Background daemon thread polls every 5 seconds with isolated asyncio event loop. One thread = one event loop = one Bot instance (threads cannot share main thread's event loop).

### Single-input dual-output format strategy
Every source file produces:
- `filename_TTS.txt` — plain text for Kokoro narration
- `filename_NotebookLM.md` — structured markdown for active synthesis
Chunking is universal: same pattern applies to TTS context windows and Claude API prompts.

### Local beats cloud when quality matches
System capabilities immune to pricing changes, API deprecations, service discontinuations. Applies to AI inference (Kokoro > cloud TTS) and file sync (SyncThing > OneDrive).

### One canonical authority pattern
When two versions of critical files exist, declare one canonical and explicitly mark the other deprecated. Document the deprecation — don't just ignore the dead copy.

### Include distinguishing information in filenames
Filename collisions are silent failures (wrong output, no error). Always include variant info in output filenames (e.g., voice name in TTS output: `f"{stem}_{engine.voice}_audio.mp3"`).

### Protocol vs script distinction
- **Protocol**: plain-English document containing rules and decisions (tells Claude Code what to do and why)
- **Script**: executable code performing specific actions
Both are required. Scripts without protocols lack intent; protocols without scripts are just documentation.

### Categorical vs incremental upgrades
Some hardware upgrades are qualitative (possible vs impossible), not quantitative (faster). Dell→Predator was a threshold crossing: "AI inference impractical" → "AI inference in seconds". Retire superseded environments completely.

### Event-driven over scheduled processing
Book compiler does zero work when `incoming\` is empty. Scales to zero cost when idle. Scheduled polling wastes resources on empty runs.

### Every project gets a remote at creation
Create the GitHub remote immediately when a local repo is initialized — not later. Retroactive remote setup requires force-push choreography and risks losing history. Rule: `git remote add origin` is part of project creation, not a follow-up task.

### Filenames are machine keys, not metadata stores
Filenames must be stable, ASCII-safe identifiers used by automation to locate files. Metadata (title, description, voice, date, variant) belongs inside the file or in a manifest — never encoded in the filename, where it silently breaks automation whenever details change.

### What/How/Where/Safety framework for data transformation tools
Before writing any data transformation tool, answer four questions:
- **What** gets transformed? (input format, data type)
- **How** is it transformed? (algorithm, model, rules)
- **Where** do inputs come from and outputs go? (paths, destinations)
- **Safety**: what fails silently if you don't handle it? (encoding, permissions, empty input, existing files)
Addressing all four before coding prevents the most common data pipeline bugs.

### DaVinci Resolve compositing layer hierarchy
- V1: Background
- V2–V3: Content elements and secondary graphics
- V4+: Primary titles and overlays
Higher tracks render in front. Explicit hierarchy prevents layer conflicts.

### Competition detection cascade (export tagging)
1. Explicit CLI argument
2. Keyword detection in clip filename
3. Bridge query of active project/timeline name in Resolve
Ensures correct tagging even when not explicitly specified.

---

## Orphans

Files with no logical home in the current vault structure. Linked here to keep them reachable in the graph.

- [[project_regrouping_narration_script]] — early project state narration (pre-BRAIN_OS, historical reference only)
