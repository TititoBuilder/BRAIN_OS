# Programming Terminology Reference
## BRAIN_OS Developer Handbook — Part 3

---

## CLI Tools & Aliases

### $PROFILE
The PowerShell startup script that runs automatically every time a terminal opens. It is a built-in variable that always resolves to an absolute path — `CurrentUserCurrentHost` by default. On this machine it lives at:
```
C:\Users\titit\OneDrive\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1
```
Because this path is inside OneDrive, the profile syncs across machines automatically. All custom functions and shortcuts defined here are available in every new terminal session.

**Four profile scopes exist:**
- `AllUsersAllHosts` — system-wide, every account, every terminal type
- `AllUsersCurrentHost` — system-wide, PowerShell only
- `CurrentUserAllHosts` — your account, every terminal type
- `CurrentUserCurrentHost` — your account, PowerShell only ← this is `$PROFILE`

---

### Set-Alias vs Function
`Set-Alias` creates a dumb shortcut — name A maps to name B, nothing else. It accepts exactly two positional parameters: the shortcut name and the target command. Attempting to pass flags breaks it immediately.

```powershell
# WRONG — breaks silently
Set-Alias cc claude --dangerously-skip-permissions

# RIGHT — use a function when flags are needed
function cc {
    claude --dangerously-skip-permissions @args
}
```

**Rule:** When a tool needs persistent flags, wrap it in a function, not an alias.

---

### Dot-Sourcing (`. $PROFILE`)
The dot operator before a script path tells PowerShell to execute the file in the **current scope** rather than a child scope. Without the dot, any functions defined in the script load into a temporary bubble and vanish when execution ends. With the dot, they stay loaded in your active session.

```powershell
$PROFILE          # does nothing — prints the path
. $PROFILE        # executes the file and keeps everything it defines
```

Use after editing `$PROFILE` to reload without restarting the terminal.

---

### @args (Argument Forwarding / Argument Passthrough)
`@args` is a PowerShell splatting operator that captures all arguments passed to a function and forwards them unchanged to the next command. This makes a function a transparent middleman — it doesn't need to know what arguments are coming, it just passes them through.

```powershell
function ca-book {
    Set-Location "C:\Dev\CristianConstruction"
    & "C:\Knowledge\CA\venv\Scripts\python.exe" "C:\Dev\CristianConstruction\book_compiler.py" @args
}
```

```
You type:     ca-book --no-audio
Function receives: @args = ["--no-audio"]
Python gets:  book_compiler.py --no-audio
```

**Computing term:** Argument forwarding or argument passthrough.

---

## Pipeline Concepts

### Session Atomic Unit
A single Claude session (from open to close) treated as the minimum unit of knowledge. Each session produces one summary, one audio file, one distilled `.md`. Nothing spans sessions — if it wasn't committed before close, it didn't happen.

---

### One-File-Per-Run Cost Rule
Every pipeline run writes exactly one output file. No accumulation, no batching across runs unless explicitly designed. This keeps cost per operation predictable and makes blast radius small when something fails.

---

### Compile Convention
The act of taking raw session files from `incoming\`, processing them into structured chapters, and writing to the compiled master document. Always triggered explicitly — never automatic. The `book_compiler.py` pattern: read `incoming\`, route by topic, deduplicate, write master, trigger TTS.

---

### Three-Outcome Routing
A content decision pattern where every item passes through exactly three possible paths: approve, reject, or hold. No ambiguous states. Applied to session distillation, content queue management, and image pipeline decisions.

---

### Bridge Document
A file that exists specifically to connect two systems or contexts. Not a primary document — a translation layer. Example: `_session_20260331_1517_combined_TTS.txt` bridges a Claude session (knowledge) to a TTS pipeline (audio).

---

### TTL (Time-To-Live)
A value that defines how long something is considered fresh before it must be refreshed or invalidated. In BRAIN_OS, the graph TTL (`SESSION_ANCHOR_TTL_HOURS=4` in `BRAIN_OS_CONFIG.json`) controls how long the dependency graph is trusted before `graph_maintainer.py` re-scans the project.

---

### Manifest
A file that lists the known state of a collection — typically filenames, checksums, or metadata. Used to detect additions, deletions, or changes without reading every file. The Drive sync manifest tracks which audio files have been uploaded, so `drive_sync.py` only uploads new ones.

---

### Parity Check
Comparing two collections to verify they match. A parity check between the local `converted\` folder and the Drive `sessions\` folder confirms every local audio file has a corresponding remote copy. A failed parity check means drift exists and sync is needed.

---

## Architecture Patterns

### Module Organization Pattern
Each major system function is isolated in its own Python module (`bot_service.py`, `dashboard_api.py`, `telegram_approver.py`). Each module can be imported and tested independently. Clear boundaries between concerns. No module reaches into another's internal state directly.

---

### Try-Except Wrapper Pattern
Critical file operations are wrapped in try-except blocks so partial failures don't crash entire automation chains. If one file fails during compilation, the process continues with remaining files. The failure is logged as a warning, not raised as a fatal error.

```python
except Exception as e:
    log.warning(f"Operation unavailable: {e}")
    return {"error": str(e)}
```

---

### Token-Aware API Design
Different AI tasks use different `max_tokens` parameters based on expected response length. Chapter detection uses 80 tokens (short structured response). Chapter compilation uses 4000 tokens (detailed prose). Sizing tokens to the task reduces cost without sacrificing quality.

---

### Blast Radius Principle
When something fails, how much breaks? A well-designed system minimizes blast radius. A failure in one module should not cascade. The Try-Except Wrapper Pattern directly reduces blast radius. Shared packages (like `brain-audio`) increase blast radius if broken — they must be tested before publishing changes.

---

### Low Coupling / High Cohesion
**Cohesion:** Everything inside one module is closely related. `tts_local.py` only does TTS — nothing else.
**Coupling:** Modules depend on each other as little as possible. `book_compiler.py` calls `ca_audio.py` via subprocess rather than importing it directly — so each can change independently.

---

### Lazy vs Eager Connection
**Eager:** A server attempts its target connection at startup. If the target isn't available, the server fails to start. (Example: `obs-mcp-server` connects to OBS at launch.)
**Lazy:** A server only attempts connection when a tool is actually invoked. `Connected` status alone does not confirm tools work. (Example: `resolve-mcp-server` only bridges to port 9000 when a tool is called.)

---

### Shared Core Pattern
A package or module used by multiple projects, maintained in one place. Changes propagate to all consumers simultaneously. `brain-audio` is the Shared Core for all TTS operations across BDF, CA, and read-along-app. The risk: a breaking change breaks all three — keep the interface stable.

---

## Programming Terms

### timedelta
A Python `datetime` object representing a duration — a difference between two points in time. Used to calculate "N hours/days ago" by subtracting from `datetime.now()`.

```python
from datetime import datetime, timedelta
cutoff = datetime.now() - timedelta(hours=24)   # 24 hours ago
week_ago = datetime.now() - timedelta(days=7)   # 7 days ago
```

---

### strftime (String Format Time)
A method on Python `datetime` objects that converts a datetime into a formatted string. The format is specified using codes: `%Y` = four-digit year, `%m` = month, `%d` = day, `%H` = hour, `%M` = minute, `%S` = second.

```python
datetime.now().strftime("%Y-%m-%d %H:%M:%S")   # "2026-05-16 14:30:00"
datetime.now().strftime("%Y-%m-%d")             # "2026-05-16"
```

Used to generate filenames, git commit timestamps, and time filters for external tools like git `--since`.

---

### git log --since
A git flag that filters commit history by time, returning all commits after a given timestamp. Replaces counting-based flags like `-1` (last 1 commit) with time-based windows.

```bash
git log --since="2026-05-16 08:00:00" --pretty=%s
# returns all commit subjects from 8am today onward
```

Combined with Python's `timedelta` + `strftime`, this enables dynamic session-aware git reporting.

---

### Subprocess
A Python module that runs external commands (shell commands, other scripts, executables) from within a Python script. The calling script can capture output, check return codes, and pass arguments.

```python
import subprocess
result = subprocess.check_output(
    ["git", "log", "--since=2026-05-16", "--pretty=%s"],
    text=True
)
```

Used throughout BRAIN_OS pipeline to chain tools: `book_compiler.py` calls `ca_audio.py` via subprocess, `sync_brain.py` calls git via subprocess.

---

### Positional Parameter
An argument identified by its position in a command, not by a flag name. `Set-Alias name target` — `name` is the first positional parameter, `target` is the second. Extra arguments beyond the expected count cause `PositionalParameterNotFound` errors.

---

### venv (Virtual Environment)
An isolated Python installation scoped to a single project. Each venv has its own copy of Python and its own installed packages, completely separate from the system Python and other venvs. Prevents package version conflicts between projects.

```
C:\Knowledge\CA\venv\          ← CA Book venv
C:\Dev\Projects\soccer-content-generator\venv\   ← BDF venv
C:\Dev\Projects\custom-agent\venv\               ← Custom Agent venv
```

Activate with: `.\venv\Scripts\Activate.ps1`
Call directly without activating: `.\venv\Scripts\python.exe script.py`

---

*Last updated: 2026-05-16 — Session: $PROFILE cleanup, git lookback extension, BDF distilled review*
