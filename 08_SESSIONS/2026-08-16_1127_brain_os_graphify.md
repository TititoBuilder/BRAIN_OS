# 2026-08-16 — Graphify session recovery (BRAIN_OS)

Recovered from Claude Code transcript `51d43329-532e-47b7-83db-58ae785a3c62.jsonl`
(485 KB, `C:\Users\titit\.claude\projects\C--BRAIN-OS\`). That session was never
written to `08_SESSIONS\`. This file is the write-up it should have had.

---

## 0. Why it was hard to find

`conversation_search` indexes standalone claude.ai chats only. Claude Code
sessions are invisible to it. The 4-Bucket session (2026-07-08) failed four
search angles looking for this exact work and concluded it was lost.

Recovery path that worked: grep the raw `.jsonl` transcripts, rank by hit
density, read the top file.

    Get-ChildItem "C:\Users\titit\.claude\projects\*\*.jsonl" | ForEach-Object {
        $hits = (Select-String -Path $_.FullName -Pattern "graphif").Count
        if ($hits -gt 0) { [PSCustomObject]@{ Hits=$hits; Project=$_.Directory.Name; File=$_.Name } }
    } | Sort-Object Hits -Descending

Result: 43 hits in one file, then a cliff to 10 / 5 / 5 / 2 and a tail of 1s.
The tail is ambient context carrying the word into unrelated sessions. The
density cliff is the signal.

RULE CONFIRMED: any session where real work happens locally must be written to
`08_SESSIONS\` or it is effectively lost to retrieval. `.jsonl` files are Claude
Code internal storage, not an archive format — they are a file that happens not
to have been deleted yet.

---

## 1. THE NAME COLLISION (read this before typing graphify)

Two unrelated tools. `07_SYSTEM\Tools_Registry.md` documents this at line 315.
Both the 4-Bucket session and the recovery session got it wrong at least once.

| | homemade | third-party |
|---|---|---|
| Name | `graphify.py` — always with `.py`, always explicit path | `graphifyy` (PyPI) / `graphify` (CLI) |
| Location | `C:\BRAIN_OS\09_TOOLS\graphify.py` | `C:\Users\titit\.local\bin\graphify.exe` |
| Called by | `graph_maintainer.py` | `/graphify .` Claude Code skill |
| Builds | BRAIN_OS audio/dependency graph | code-architecture knowledge graph |
| Input | `02_PROJECTS/graphs/projects.manifest.json` | a project directory |
| Output | `.context.md` files | `graph.html`, `GRAPH_REPORT.md`, `graph.json` |

RULE: never write bare `graphify` for the homemade one in any doc or commit
message. Write `graphify.py`.

---

## 2. WORK DONE IN THE RECOVERED SESSION

### 2.1 `graphify.py` — cross-project mode spliced in

Source: `09_TOOLS/graphify_cross_project_extension.py` (copy from, unmodified).
Target: `09_TOOLS/graphify.py`. Three edits, +113 lines total.

- **Lines 276–369** — five functions under a new `# Cross-project system map`
  header, immediately above `# Entry point`:
  `_scan_editable`, `_scan_deploys`, `_scan_drive`,
  `build_cross_project_graph`, `write_cross_project_context_md`
- **Line 383** — `parser.add_argument("--cross-project", action="store_true", ...)`
- **Lines 386–399** — dispatch block directly after `args = parser.parse_args()`,
  returning **before** the single-project logic

Constraints held: `build_graph` and `write_context_md` untouched; existing path
runs identically when the flag is absent; no `--force` branch on the
cross-project path (deliberately excluded); all imports already present.
Verified with `ast.parse`.

The three `_scan_*` helpers inspect editable installs, deploy targets, and
Google Drive usage across projects. This is the machinery that surfaces
cross-project coupling — almost certainly how the Drive credential sprawl was
found, i.e. a scanner built for that class of defect, not an incidental notice.

### 2.2 `projects.manifest.json` — CA_Book added

    { "name": "CA_Book", "root": "C:/Knowledge/CA/CA_Book", "venv": "C:/Knowledge/CA/venv" }

Positioned after `CristianConstruction`, before `Resolve MCP Server`. Verified
7 projects. `detect`, `shared_packages`, `output` untouched.

NOTE: `root` and `venv` are hardcoded absolute paths. This is exactly why the
`CA_Book → cc-audiobook` rename must touch this file.

### 2.3 Corruption repairs

- `09_TOOLS/session_start.py` — UTF-8 BOM (U+FEFF) prepended before the opening
  `"""`. Removed. Line-50 change (`context_md` → `brain-os.context.md`) preserved.
  Rewritten UTF-8 no-BOM, LF.
- `07_SYSTEM/Tools_Registry.md` — the entire `## graphifyy` block was pasted
  twice, and contained literal null bytes (`^@9_TOOLS` should read `09_TOOLS`)
  plus stray `\r`. Duplicate deleted, nulls and CRs stripped. Verified heading
  count = 1.

Both traced to a prior editing session. Encoding damage is silent until
something reads the file.

### 2.4 `session_close.py` — Navigation.md auto-refresh

Block inserted in `main()` after the archive-saved print (line 234): runs
`09_TOOLS/vault_index.py`, `git add`s `00_DASHBOARD/Navigation.md`, then commits
**only if** `git diff --cached --quiet` returns 1. Scoped to that one path.
Catches `CalledProcessError` and `TimeoutExpired` as warnings — a nav failure
cannot break session close.

---

## 3. QUEUE CHANGES MADE IN THAT SESSION

### 3.1 TOKEN FRAGILITY — prior diagnosis overturned (2026-06-22)

The open item previously blamed **Cloudflare 403/1010** for Railway push
failures. That is likely WRONG. Investigation points to Railway **token type**
(Team vs Project token), not bot-blocking.

- Local refresh works (`token_sync.py`, soccer-content-generator)
- Duplicate `RAILWAY_TOKEN` line removed from `.env` (was lines 27–28)
- NEXT: regenerate `RAILWAY_TOKEN` in the Railway dashboard as a **Project**
  token scoped to read-along-app; swap into `.env` as a single line
- Failure is **intermittent** — one clean run does not prove the fix. Verify
  across several real `token_sync.py` runs.
- Manual clipboard fallback still works meanwhile

### 3.2 `CA_Book\venv` — PARKED, not deleted (found 2026-06-22)

`C:\Knowledge\CA\CA_Book\venv` exists (36 pkgs, anthropic+google stack, **no**
`brain_audio`) but everything runs through the parent `C:\Knowledge\CA\venv`.
All `$PROFILE` book functions point at the parent; CA_Book code imports neither
`brain_audio` nor `anthropic` directly. Nothing references the child venv.

Stale by all evidence — parked deliberately, not deleted. Revisit, confirm, then
delete. Harmless meanwhile.

---

## 4. STATE OF THE THIRD-PARTY TOOL (verified 2026-08-16)

- `uv tool list` → **graphifyy v0.8.44**, exposing `graphify` and `graphify-mcp`
- `Get-Command graphify` → `C:\Users\titit\.local\bin\graphify.exe`.
  PATH holding; the manual profile edits from June survived.
- **`graphify-mcp` has never been wired up.** No match in
  `C:\Users\titit\.claude.json`; `C:\BRAIN_OS\.mcp.json` does not exist.
- Pilot numbers (95% extracted / 5% inferred / 0% ambiguous, 0.91 mean inferred
  confidence, read-along-app, 2026-06-19) were recorded **without a version** —
  not a valid baseline for v0.8.44.

`Tools_Registry.md` amended at line 328 with all four points.

---

## 5. OPEN ITEMS AFTER THIS SESSION

- [ ] **Reword the rename queue item.** `CA_Book → cc-audiobook` lists "graphify
      config paths" as step 3 of the atomic four. Ambiguous now that the
      collision is documented. It means **`graphify.py`** — specifically the
      `projects.manifest.json` entry. `graphifyy` has never run against
      `C:\Knowledge`, so it holds no stored path there.
- [ ] **Evaluate `graphify-mcp`.** Different integration path from `/graphify .`
      — queryable mid-session vs. run-to-produce-`graph.html`. Compare against
      the existing `obs-mcp-server` / `resolve-mcp-server` pattern.
- [ ] **Record a v0.8.44 baseline.** Re-run the read-along-app pilot so the
      confidence numbers are attached to a known version.
- [ ] **Run `graphify.py --cross-project`.** Spliced in and parsing, but the
      session ended before it was ever run. Verify `.gitignore` first.
- [ ] **`graphifyy` never run on** soccer-content-generator,
      CristianConstruction, or BRAIN_OS itself. On BDF, scope to a subfolder
      first — read-along-app alone was 167 files / ~839k words and the report
      flagged that as expensive for semantic extraction. BDF is larger.
- [ ] **Consolidate Google Drive credentials.** `gdrive_credentials.json` /
      `gdrive_token.json` shared by 4–6 scripts, copies in
      `C:\Knowledge\CA\CA_Book\`. Found independently by both this session and
      the 4-Bucket session. Flagged in `00_INDEX\Operations.md`.

---

## 6. THE ONE-LINE VERSION

A session that produced real code was never written up, so a later session
concluded it was lost — and the recovery turned up two facts nobody was looking
for: a second binary that ships and has never been wired up, and pilot metrics
with no version attached to them.

A tool you cannot name precisely is a tool you will eventually misuse.
