---
tags: [system, powershell, aliases, reference]
status: live
updated: 2026-05-01
parent: "[[Project_Directory]]"
---

# PowerShell Aliases

All active aliases for BDF, CA, and landing page workflows.
Defined in `$PROFILE` — two profile files, both must be maintained.

---

## Profile File Locations

> ⚠️ **CRITICAL — Windows has 4 profile locations.**
> VS Code terminal loads `CurrentUserCurrentHost` only.
> Always use `code $PROFILE` to open the exact file the current terminal loads.
> Run as TWO SEPARATE commands — never on the same line.

```powershell
code $PROFILE   # opens the correct profile for current terminal
. $PROFILE      # reloads profile after editing
```

| Context | Profile Path |
|---|---|
| VS Code terminal | `C:\Users\titit\OneDrive\Documents\WindowsPowerShell\Microsoft.VSCode_profile.ps1` |
| Regular PowerShell | `C:\Users\titit\OneDrive\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1` |

Both files must be maintained — aliases added to one do not appear in the other.

---

## BDF Aliases

| Alias | What it does |
|---|---|
| `bdf-log "filename.txt"` | Moves file from Downloads to `BDF\Session_Resumes\processed\` |
| `bdf-compile "filename.txt"` | Moves file from Downloads to `BDF_Book\incoming\` |
| `bdf-book` | Activates BDF venv → runs `book_[compiler.py](http://compiler.py)` → compiles all files in `incoming\`, generates audio, syncs to Drive |

---

## CA Aliases

| Alias | What it does |
|---|---|
| `ca-log "filename.txt"` | Moves file from Downloads to `CA\Session_Resumes\processed\` |
| `ca-compile "filename.txt"` | Moves file from Downloads to `CA_Book\incoming\` |
| `ca-book` | Activates BDF venv (shared) → runs CA `book_[compiler.py](http://compiler.py)` → auto-syncs chapter .wav + `CA_Master_Book.txt` to Google Drive `CA_Book_Audio/` |
| `ca-audio chXX_name` | Activates TTS venv → runs `ca_[audio.py](http://audio.py)` for one chapter → outputs .wav to `C:\Knowledge\CA\CA_Book\audio\` |

> ⚠️ `ca-book` uses the **BDF venv**, not the TTS venv. The TTS venv
> (`C:\Dev\Projects\custom-agent\venv\`) is only invoked by `ca-audio`.

> ⚠️ CA compiler stops at the first `#chXX` tag. **One file per chapter.**
> Never batch multiple chapters into one compile file.

---

## Landing Page Alias

| Alias | What it does |
|---|---|
| `dev` | File watcher — auto-deploys `cc_landing.html` to Vercel on save |

---

## Key Rules

1. `bdf-book` cost: $1–2.50 per normal run. Batching causes overlap = $7–8. Never batch.
2. `ca-book` auto-syncs Drive — no extra steps needed after a successful run.
3. For bulk CA re-sync after major expansions: run `ca_bulk_[upload.py](http://upload.py)` (lives in Downloads, uses BDF venv).

---

## Known Issues

**Duplicate function definitions (fix pending):**
- `ca-log`, `ca-compile`, and `ca-book` have duplicate definitions in the profile
- Symptom: second definition silently overrides first — may cause unexpected behavior
- Fix: open `code $PROFILE`, find and remove the duplicate blocks

**ca-book points to wrong venv path (fix pending):**
- Current profile activates incorrect venv for `ca-book`
- ca-book must use the BDF venv at `C:\Dev\Projects\soccer-content-generator\venv\`
- Verify by checking the `Set-Location` and `Activate.ps1` lines inside the `ca-book` function
- Fix: correct the path to `C:\Dev\Projects\soccer-content-generator\venv\Scripts\Activate.ps1`

---

## Connected to

- [[Compile_Session_Workflow]]
- [[Project_Directory]]
- [[Tools_Registry]]
