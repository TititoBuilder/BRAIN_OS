# BRAIN_OS Programming Terminology Reference

> Aggregated from 15 BDF session distillations (2026-03-31 through 2026-05-14).
> Sections extracted: Key Commands, Patterns Discovered, Principles Earned.
> Deduplicated; near-identical entries merged into their canonical form.

---

## CLI Tools & Aliases

### PowerShell Profile Functions
Location: `C:\Users\titit\OneDrive\Documents\WindowsPowerShell\`
Both `Microsoft.VSCode_profile.ps1` and `Microsoft.PowerShell_profile.ps1` must be kept identical so aliases load in all terminal contexts.

| Alias | Purpose |
|---|---|
| `bdf-log` | Move current session log to `C:\Knowledge\BDF\Session_Resumes\processed\` |
| `bdf-compile` | Run book_compiler.py against BDF incoming dir (one file at a time) |
| `bdf-book` | Full BDF compile run with venv activation |
| `ca-log` | Same as bdf-log but for CristianConstruction project |
| `ca-compile` | Compile run for CA book |
| `ca-book` | Full CA book compile with venv |
| `ca-audio` | Generate TTS audio for CA book |
| `brainos-book` | Compile run targeting BrainOS book |
| `dev` | File watcher for active development session |

**Verify all aliases are loaded:**
```powershell
Get-Command bdf-log, bdf-compile, bdf-book, ca-log, ca-compile, ca-book, ca-audio, dev
```

**Find and open the active profile:**
```powershell
code $PROFILE
$PROFILE | Format-List -Force *
```

### Book Compiler CLI (`book_compiler.py`)
Plugin-architecture compiler — one file per run is non-negotiable (see Principles Earned).

```bash
python book_compiler.py                 # process one file from incoming/
python book_compiler.py --status        # health report: word counts, file stats, no API calls
python book_compiler.py --no-audio      # skip TTS generation
python book_compiler.py --no-stitch     # skip master stitching step
python book_compiler.py --book brainos  # target BrainOS book config
python book_compiler.py --book bdf      # target BDF book config
python book_compiler.py --book ca       # target CA book config
```

### TTS Pipeline CLI
```bash
python converter.py source.py --engine tts          # convert source to TTS-clean text
python converter.py soccer_bot.py --engine both     # produce both TTS and NotebookLM outputs
python tts_local.py converted/source_TTS.txt        # generate audio from prepared text
python tts_local.py converted/file_TTS.txt --voice am_adam  # specify voice
python tts_local.py --batch converted/              # batch-process all TTS-ready files
ffplay converted\file_audio.mp3                     # play result immediately
```

### SyncThing CLI
```bash
syncthing                    # start (keep terminal open — closing kills sync silently)
# Web interface: http://127.0.0.1:8384
```

### OBS Relay CLI
```bash
python obs_relay.py --match UCL_Arsenal_PSG --default-event GOAL
python obs_relay.py --match UCL_Barcelona_Newcastle
```

### BDF Pipeline Startup
```bash
# Unified startup (Predator)
.\start.bat

# Manual (4 terminals on processing machine)
python bot_service.py                          # Terminal 1 — headless engine
uvicorn dashboard_api:app --reload             # Terminal 2 — FastAPI on :8000
cd dashboard && npm run dev                    # Terminal 3 — React on :5173 or :3000
python -m streamlit run enhanced_dashboard.py  # Terminal 4 — Mission Control on :8501

# HP machine (2 terminals)
python obs_relay.py --match <COMPETITION_TEAMS>
syncthing
```

> **Never run `bot_service.py` and `enhanced_terminal_ui.py` simultaneously** — both load SoccerBot and will conflict.

---

## Pipeline Concepts

### Three-Outcome File Routing
Every file entering the book compiler routes to exactly one outcome — no ambiguous states:

| Outcome | Location | Trigger |
|---|---|---|
| **Merged** | `incoming\_processed\` | Content integrates cleanly into a known chapter |
| **Quarantined** | `incoming\_review\` | Unknown chapter tag or low confidence score |
| **Rejected** | `incoming\_rejected\` | Fails BDF relevance filter (non-project content) |

### Confidence-Scored Auto-Routing
1-10 scale applied before chapter detection:
- **8-10**: Auto-route to chapter
- **7**: Flag for operator review
- **6 and below**: Quarantine to `incoming\_review\`

### BDF Filename Convention (Caption Quality Driver)
Structured filenames are directly required for high-confidence AI caption generation:
```
COMPETITION_HomeTeam_AwayTeam_EVENTTYPE_YYYY-MM-DD_HH-MM-SS.mp4
```
Example: `UCL_Arsenal_PSG_GOAL_2026-03-27_21-47-33.mp4`

Generic OBS filenames produce low-confidence fallback captions that lack match context. Filename structure is not aesthetic — it is a data contract.

### File Stability Validation (Video Files)
OBS writes clips asynchronously. Naive timestamp checks transfer corrupted files. Required pattern:
```python
size_before = os.path.getsize(clip_path)
time.sleep(5)
size_after = os.path.getsize(clip_path)
if size_before != size_after:
    # File still growing — retry later
```
Skip all 0-byte files unconditionally.

### One-File-Per-Run Rule
Never batch multiple compile files. Chapter overlap causes exponential cost compounding:
- Each subsequent merge reads all previous merged content as input tokens
- Evidence: normal single-file runs = $1.50-2.50; batched runs = $7-8
- Run `bdf-compile` → wait for completion → run again for the next file

### Dual Twitter API Architecture
Twitter's free tier does not support media uploads through v2:
- **v2 (tweepy.Client)** — post tweets
- **v1.1 (tweepy.API)** — upload media (images, chunked video)

### Competition Detection Cascade
Three-tier fallback for export tagging:
1. Explicit CLI argument
2. Keyword detection in clip filename
3. Bridge query of active project/timeline name in DaVinci Resolve

### Single-Input Dual-Output (TTS/NotebookLM)
Every source file produces two optimized formats:
- `filename_TTS.txt` — plain text optimized for TTS narration
- `filename_NotebookLM.md` — structured markdown with metadata headers for active synthesis

### Chunking as Universal Pattern
Sentence-level chunking at ~400 characters with 0.3s silence padding between chunks. The same problem solved for Kokoro TTS context windows is identical to Claude API prompt chunking in the soccer bot. Recognize this pattern when facing it again.

### Hybrid Approval Model
Automation handles all preparation (content generation, formatting, scheduling). Human judgment is preserved only at the consequence moment (external publish). Telegram serves as the mobile approval interface — no desktop dependency.

### Event-Driven vs Scheduled Processing
The book compiler performs zero work when `incoming\` is empty. This is intentional — event-driven design scales to zero cost when idle. Scheduled polling wastes resources on empty runs.

### Silent Failures as a Debugging Class
The most expensive bugs produce no errors: path typos in watch directories, enum type mismatches, missing attribute declarations, 0-byte file transfers. These run silently and accomplish nothing. Path validation must fail loudly at startup.

### Cross-Project Handoff Message Pattern
When work spans separate Claude projects, the handoff must be self-contained:
```
Hi Claude. I am continuing work on [Project Name] at [working directory].

WHAT WAS BUILT IN THE SEPARATE SESSION ([date]):
[Numbered deliverables with technical specs]

IMMEDIATE PENDING ITEMS (do before anything else):
[Specific fixes, commits, configuration changes]

WHAT COMES NEXT:
[Next objective and why it belongs in this project context]
```

### Pre-Routing Beats Post-Detection
Determine chapter routing during the compile session response (routing map step), not via auto-detection after file creation. The auto-detector is a safety net — the routing map is the primary mechanism.

### Cost Accumulation in Batch Processing
When multiple files touch the same chapter, each successive merge reads all previous merges as input. Token costs compound exponentially. Always run one file per book-compile execution.

---

## Architecture Patterns

### Two-Machine Split Architecture
- **HP Laptop**: OBS recording to `D:\BDF_RawFootage`, DaVinci Resolve editing, exports to `C:\Media\Exports\`
- **Predator (canonical machine)**: AI processing, LanceDB at `C:\lance_db_soccer`, publishing pipeline

WD Elements external drive stays on Predator permanently — moving it between machines risks LanceDB corruption.

### SyncThing over OneDrive
OneDrive introduced silent 0-byte failures and unpredictable multi-minute delays for large video files. SyncThing provides direct LAN sync completing 50MB transfers in under 10 seconds. Configured as "BDF-Clips" folder share with `C:\BDF_Share` as the local path on both machines.

SyncThing paths:
- HP: `C:\Dev\Tools\syncthing\syncthing-windows-amd64-v2.0.15\syncthing.exe`
- Predator: `C:\Users\titit\AppData\Local\Microsoft\WinGet\Links\syncthing.exe`

### Three-Layer Application Architecture
- **Layer 1**: Python Backend — core processing engine (bot_service.py or enhanced_terminal_ui.py, not both)
- **Layer 2**: FastAPI Server — HTTP bridge on localhost:8000
- **Layer 3**: React Dashboard — visual surface on localhost:5173 via axios

### Plugin Architecture (Book Compiler)
Per-file pipeline: `RelevancePlugin -> MarkdownStripPlugin -> DistillPlugin -> TTSPlugin`
Pipeline halts when `ctx.stopped = True`. Each plugin receives and returns a `Context` dataclass. New capabilities are added as plugins without touching existing flow.

### Two-Process Socket Architecture (DaVinci Resolve)
Resolve Free tier blocks external `bmd.scriptapp` access. Workaround: TCP socket on `127.0.0.1:9000` bridges external MCP server to Resolve's embedded Python console. Each tool call opens a fresh connection — no persistent pool, no leaked resources.

Bridge reload command (must include encoding parameter):
```python
exec(open(r"C:\Users\titit\Projects\resolve-mcp-server\resolve_bridge.py", encoding="utf-8").read())
```

### Background Daemon Thread for Telegram Polling
Telegram's callback expiry window is 60 seconds absolute. Background daemon thread polls every 5 seconds with its own isolated asyncio event loop. Daemon threads cannot share the main thread's event loop.
```python
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
```

### Three-Phase Session Structure
1. **Initialization** — context loading, objectives, success criteria
2. **Active Work** — iterative implementation with inline documentation
3. **Compilation** — summary, artifact inventory, decisions captured, handoff bridge for next session

### Session as Atomic Unit
Every work session is self-contained, documented, and integrated. Sessions are defined by logical work units, not calendar time. Each produces tangible artifacts and a handoff bridge so any future AI session can continue without memory assumptions.

### Knowledge-Code Separation
Absolute separation:
- Code (executable systems): `C:\Dev\Projects\`
- Knowledge (documents, references): `C:\Knowledge\`
- Large data (LanceDB, media): `C:\lance_db_soccer\`, `C:\BDF_Share\`

Knowledge documents describe systems but never contain executable systems.

### Dual Learning Engine
- **Engine One (Kokoro TTS)**: Passive audio consumption during movement — listen while walking, commuting
- **Engine Two (NotebookLM)**: Active synthesis and reflection at a desk
Most tools fail by trying to serve both modes with one interface.

### PowerShell Profile Synchronization
Both `Microsoft.VSCode_profile.ps1` and `Microsoft.PowerShell_profile.ps1` must be identical. VS Code terminals load the VSCode profile; standalone PowerShell loads the PowerShell profile. Divergence means aliases work in one context but silently fail in the other.

### Windows Encoding Boundary Pattern
Every file operation must be explicit about encoding on Windows:
```python
open(path, encoding="utf-8")                               # always
subprocess.run(..., encoding="utf-8", errors="replace")    # all subprocess pipes
# Set PYTHONIOENCODING="utf-8" in subprocess env
```
Python's `open()` defaults to the system encoding (cp1252 on Windows), which is a footgun in pipelines that generate output across different terminal types.

### Protocol vs Script Distinction
- **Protocol**: Plain English document containing rules and intent — tells Claude Code what to do and why
- **Script**: Executable code performing specific actions

BRAIN_OS requires both. Scripts without protocols lack intent; protocols without scripts are just documentation.

### Exception Visibility Principle
Every `except` block must do one of: re-raise, log, store in accessible state, or return error status. Bare `except: pass` is forbidden — it creates debugging nightmares where failures occur silently.

### Thread-Safe Queue Pattern (asyncio-threading)
One thread = one event loop = one Bot instance. Background threads draining shared queues must run in their own event loop, never the main thread's.

### Layer Hierarchy for DaVinci Resolve Compositing
- V1: Background (match promotional / game screenshot)
- V2-V3: Content elements and secondary graphics
- V4+: Primary titles and overlay elements

Higher tracks render in front. Document this explicitly to avoid layer conflicts in complex edits.

### Unknown Tag Resolution Workflow
When the compiler encounters an unrecognized chapter tag:
1. Content saved to `incoming\_review\` with tag name embedded in filename
2. Terminal prints the exact Python dict entry needed for the `CHAPTERS` registry
3. Operator adds chapter definition, reruns compiler

### Date Injection System
`src/date_injector.py` with `inject_into_prompt()` prepends temporal context to every Claude prompt. Without this, Claude generates content with no concept of current date — incorrect match timing, season references, countdown values.

---

## Key Commands (aggregated)

### Book Compiler
```bash
python book_compiler.py --status                # health check, no API cost
python book_compiler.py                         # process next file in incoming/
python book_compiler.py --book brainos --no-audio  # BrainOS book, skip TTS
python book_compiler.py --book bdf --no-stitch  # BDF book, skip master rebuild
```

### BDF Full Pipeline Startup (Predator)
```powershell
python bot_service.py                           # headless engine (Terminal 1)
uvicorn dashboard_api:app --reload              # FastAPI :8000 (Terminal 2)
cd dashboard && npm run dev                     # React :5173 (Terminal 3)
python -m streamlit run enhanced_dashboard.py   # Streamlit :8501 (Terminal 4, optional)
```

### SyncThing
```powershell
# Start on HP
Start-Process "C:\Dev\Tools\syncthing\syncthing-windows-amd64-v2.0.15\syncthing.exe"

# Start on Predator
Start-Process "C:\Users\titit\AppData\Local\Microsoft\WinGet\Links\syncthing.exe"
```

### OBS + Capture Setup
```powershell
New-Item -ItemType Directory -Path "D:\BDF_RawFootage" -Force
```
```bash
python obs_relay.py --match UCL_Arsenal_PSG --default-event GOAL
```

### VPN Management (required before bot/sync sessions)
```powershell
Stop-Service -Name "Surfshark Service" -Force
Start-Service -Name "Surfshark Service"
```

### Network Profile (required for SyncThing local discovery)
```powershell
Set-NetConnectionProfile -Name "SpectrumSetup-ED3B" -NetworkCategory Private
```

### Git Sync (after downloading files from Claude chat)
```bash
git add filename.py
git commit -m "feat: description"
git push
```

### Git Commit with Conventional Format
```bash
git commit -m "docs: reconcile LanceDB paths, remove ghost files, archive 01 PROJECTS"
# Types: feat: fix: docs: chore: refactor: — lowercase, no period
```

### FFmpeg Video Conversion
```bash
# Single file
ffmpeg -i "input.mkv" -c:v libx264 -c:a aac "output.mp4"
```
```powershell
# Bulk MKV to MP4
New-Item -ItemType Directory -Force -Path "D:\BreakingDownFutbol\Converted"
Get-ChildItem "D:\BreakingDownFutbol\RawFootage\*.mkv" | ForEach-Object {
    $output = "D:\BreakingDownFutbol\Converted\" + $_.BaseName + ".mp4"
    ffmpeg -i $_.FullName -c:v libx264 -c:a aac $output
}
```

### Gallery Image Resize (PIL — 16:9 for Twitter)
```python
from PIL import Image
from pathlib import Path

for p in Path('src/images/gallery').glob('*.png'):
    img = Image.open(p)
    img = img.resize((1200, 675), Image.LANCZOS)
    img.save(p)
```

### Vector Store Rebuild (LanceDB)
```powershell
Remove-Item -Path "lance_db" -Recurse -Force
python src\enhanced_terminal_ui.py
python src\soccer_knowledge_ingester.py
```

### Resolve Bridge Reload (must include encoding)
```python
exec(open(r"C:\Users\titit\Projects\resolve-mcp-server\resolve_bridge.py", encoding="utf-8").read())
```

### Find Non-ASCII Characters in Pipeline Scripts
```powershell
Select-String -Path "*.py" -Pattern "print.*[✓✗⚠->—•]"
```

### Archive Before Patching
```powershell
Copy-Item resolve_bridge.py archive\resolve_bridge_vX_Y_DATE.py
```

### API Connection Diagnostics
```powershell
Test-NetConnection api.anthropic.com -Port 443
```

### PowerShell Profile Management
```powershell
code $PROFILE                       # open active profile in VS Code
$PROFILE | Format-List -Force *     # show all four profile locations
Get-Command bdf-log, bdf-compile, bdf-book, ca-log, ca-compile, ca-book, ca-audio, dev
```

### VS Code Workspace Switching
```
Ctrl+Shift+P -> "open recent" -> select workspace with briefcase icon
```

### Create Dedicated Venv
```powershell
python -m venv C:\Dev\CristianConstruction\venv
```

### Recreate Missing Downloads Folder
```powershell
New-Item -ItemType Directory -Path "$HOME\Downloads"
```

### Tailwind CSS v4 Setup (no config files needed)
```bash
npm install tailwindcss @tailwindcss/vite
npm install axios recharts lucide-react
# Add: @import "tailwindcss"; to index.css
# Add: @tailwindcss/vite plugin to vite.config.js
```

### Session Log Naming Convention
```
session-YYYY-MM-DD-[keyword].md
session-YYYY-MM-DD-[keyword]-01.md    # multiple sessions same day
```

### Register Unknown Chapter Tag (book compiler)
```python
# Add to CHAPTERS dictionary in book_compiler.py:
'new_tag': 'Chapter_Name.md'
```

### Obsidian Shortcuts
| Shortcut | Action |
|---|---|
| `Ctrl+P` | Command Palette |
| `Ctrl+O` | Quick open file |
| `Ctrl+Shift+F` | Full text search |
| `Ctrl+G` | Global graph view |
| `Ctrl+Alt+G` | Local graph view |

### VS Code Shortcuts
| Shortcut | Action |
|---|---|
| `Ctrl+Shift+P` | Command Palette |
| `Ctrl+P` | Quick open file |
| `Ctrl+Shift+F` | Search across project |
| `Ctrl+`` ` `` | Toggle terminal |
| `F12` | Go to definition |
| `Ctrl+D` | Select next occurrence |
| `F2` | Rename symbol project-wide |

---

## Principles Earned (aggregated)

### System Design

**Local Beats Cloud When Quality Matches**
System capabilities immune to pricing changes, API deprecations, and service discontinuations. Apply to all AI inference that can run on available hardware.

**Prefer Tools That Work Immediately**
Choose tools requiring no infrastructure setup over those needing compilation or complex dependencies. ChromaDB was rejected for C++ build requirements; LanceDB selected for pip-only installation.

**Event-Driven Over Scheduled**
Only perform work when something happens (file lands in `incoming\`). Scheduled execution wastes resources on empty runs. Event-driven scales to zero cost when idle.

**Elimination of Network Dependencies**
Direct file paths always trump network shares. SMB shares require static IPs, matching network profiles, firewall exceptions, and VPN coordination. Local paths (`C:\BDF_Share`) work regardless of network configuration.

**Separation of Concerns is Absolute**
Code in `C:\Dev\Projects\`, knowledge in `C:\Knowledge\`, large data on dedicated paths. Never mix contexts.

**Socket Protocol Simplicity**
One request, one response, dispose connection. Failed connections are automatically cleaned up, unlike persistent connection pools that can leak resources.

**Background Threading Requires Isolated Event Loops**
Daemon threads cannot share the main thread's asyncio event loop. Each background thread must create its own with `asyncio.new_event_loop()` and `asyncio.set_event_loop()`.

**External Services Have Hard Time Limits**
Telegram's 60-second callback expiry is absolute. Design polling systems to operate well within service time constraints, not at the margin.

**Free Tier API Methods Lie**
`hasattr()` returns True for methods that crash when called on Resolve Free tier. The only reliable test is calling the method in a `try/except` block during initialization or runtime.

**Connection Stability Over Speed**
CGNAT networks (T-Mobile MiFi) periodically reset long-running TCP connections. Retry logic is mandatory for AI API operations on such connections. Home WiFi on cable/fiber provides the stable environment for extended operations.

---

### Code Quality

**Explicit Encoding Everywhere**
Python's `open()` defaults to system encoding (cp1252 on Windows). Every file operation must specify `encoding="utf-8"` regardless of "works on my machine" scenarios.

**Unicode Is Pretty But Fragile**
ASCII output works universally across terminals, pipes, and CI systems. Replace Unicode symbols with ASCII equivalents (`-> not ->`, `[OK] not ✓`). The debugging time saved by avoiding encoding crashes outweighs aesthetic preferences.

**Explicit Beats Implicit in Multi-Stage Pipelines**
Every attribute must be explicitly declared at each pipeline stage. Python's dynamic typing allows silent failures when attributes are assumed to exist. Never rely on `getattr()` for attributes that weren't set in `__init__()`.

**Type System Assumptions Can Fail Silently**
String vs Enum confusion (`"match_recap"` vs `ContentType.MATCH_RECAP`) fails deep in call stacks with no obvious error message. Always use proper type constructors.

**Path Validation is Non-Negotiable**
Watchers monitoring nonexistent directories run without errors but never detect files. Validate all watch paths at startup and fail loudly if they don't exist.

**File Operations Need Generous Safety Margins**
Async file writing (OBS, external processes) requires stability checks with size comparison, not just timestamp delays. 5-second waits with before/after size comparison prevent corrupted transfers.

**Exception Visibility Principle**
Every `except` block must re-raise, log, store, or return an error status. Bare `except: pass` is forbidden.

**Never Edit Compiled Artifacts**
`BDF_Master_Book.txt` is always regenerated by the compiler from chapter files. Direct edits vanish on next compilation. All modifications flow through proper chapter structure.

**Output Tokens Dominate API Cost**
Output tokens are priced at 5x input tokens. A verbose chapter costs significantly more than concise output from lengthy source material. Be deliberate about output length in Haiku/Sonnet calls.

**Test End-to-End Flows Early**
Individual components may work in isolation but fail when integrated. Do not rely on unit-level success as evidence of pipeline correctness.

---

### Documentation & Knowledge

**Document Decisions at Decision Time**
The moment a choice is made is when reasoning is clearest. Waiting until session end leads to lost context and incomplete knowledge transfer.

**Assume Amnesia**
Write documentation assuming the reader (including future AI, including future you) knows nothing about previous sessions. Creates robust, self-contained records.

**Paths Are Sacred**
Always use full, explicit paths. Relative references break when context changes. "The downloads folder" is ambiguous. `C:\Users\titit\Downloads\` is not.

**The Book Is Truth**
Session logs can contain experiments and dead ends. The BDF Knowledge Book should only contain validated, current information. If it's in the Book, it should be trustworthy.

**Storage vs Synthesis Distinction**
Session transcripts are ingredients; chapters are meals. Synthesis creates refined knowledge that becomes more valuable over time. Raw transcripts become harder to search.

**Cross-AI Compatibility in Documentation**
Write documentation that works with any AI assistant: no assumptions about memory, explicit paths and commands, self-contained explanations, standard formats (Markdown, JSON) that any AI can parse.

**Commit Messages Must Have Intent**
Use conventional commit format with type prefix (`feat:`, `fix:`, `docs:`, `chore:`, `refactor:`) followed by lowercase descriptions without periods.

**Name Files Descriptively**
Date-based filenames cause collisions during archive processing. Use descriptive names like `20260404_animated_brand_compile.txt` instead of generic date patterns.

**Historical Content Tagging**
Dell-era content (pre-March 2026) gets tagged with historical context notes so current AI understands it is reference material, not current instructions.

**Knowledge Flow Requires Human Memory**
BRAIN_OS has reliable code but depends on humans remembering two manual steps: run `session_close.py` after sessions, then trigger the Knowledge Ingestion Protocol. The code works; the risk is forgetting.

---

### Workflow & Process

**One Canonical Authority**
When two versions of critical files exist, declare one canonical and explicitly mark the other dead. Don't just ignore the duplicate — document the deprecation.

**Preserve Everything, Filter Intelligently**
The compiler preserves all content but routes it appropriately. Even "rejected" content remains recoverable. This prevents data loss while maintaining knowledge base quality.

**Automation with Human Oversight Points**
Fully automate what can be automated (compilation, audio generation, cloud sync). Create clear human decision points for ambiguous cases (unknown tags, low-confidence routing, external publish).

**One File, One Run**
Never batch multiple compile files into one book-compiler execution. The marginal time savings are destroyed by exponential cost increases from chapter overlap.

**Explicit Routing Over Auto-Detection**
Pre-tagged files with routing maps eliminate costly auto-detection errors. The compiler's auto-detector is a safety net, not the primary mechanism.

**Separate Books Get Separate Files**
Cross-project sessions require separate compile outputs per target book. Contamination prevention at file creation beats detection at compile time.

**Verify Before Fixing**
Encoding bugs visible only in PowerShell display are not actual bugs. Signal interrupts during Claude Code are environment artifacts. Always verify a problem exists in the execution context that matters before attempting a fix.

**Always Audit Before Installing**
Check what extensions, tools, or configurations already exist before adding new ones. Redundant installs create conflicts and debugging overhead.

**Canonical Paths Are Sacred**
Once a canonical path is established (e.g., `C:\lance_db_soccer`), all references across all files must be updated systematically. Stale paths create invisible failure modes.

**Archive Early, Review Later**
Moving processed materials to archive prevents clutter while preserving optionality. Nothing is lost; decisions about permanent deletion are deferred until there is time to make them properly.

**VPN Breaks Local Network Features**
Surfshark VPN prevents SyncThing local discovery and blocks Telegram HTTPS callbacks. Always pause VPN during development sessions requiring local network sync or Telegram bot operations.

**Absolute Paths in Automation**
Relative paths in PowerShell functions break when run from unexpected working directories. Always use absolute paths in profile functions and automation scripts.

**Mobile-First Design is Non-Negotiable for Social Media**
Twitter content must assume mobile viewing: 1200x675 image dimensions, 96-120pt minimum font sizes, 4.5:1 contrast ratios, hooks placed within the first 3-5 seconds.

**Include Distinguishing Information in Filenames**
Filename collisions are silent failures producing wrong output with no error. Always include variant information (voice name, date, project) when multiple outputs are possible.

**lance_db Must Stay in .gitignore**
Vector stores rebuild locally per machine and are not shared between environments. Never commit the `lance_db` folder to GitHub.

**Never Run bot_service.py and enhanced_terminal_ui.py Simultaneously**
Both load SoccerBot and will conflict. Use `bot_service.py` as the headless engine for the dashboard workflow.

**Categorical vs Incremental Upgrades**
Some hardware upgrades are qualitative (possible vs impossible) rather than quantitative (faster). Recognize threshold crossings and retire superseded environments completely rather than maintaining parallel setups.

---

*Generated: 2026-05-16 | Source: 15 session distillations from `C:\Knowledge\BDF\BDF_Book\distilled\`*
