# HARNESS — BRAIN_OS

Status: DRAFT. Describes what IS as of 2026-08-26, from Phase 2 discovery.
No fixes applied. Items marked UNVERIFIED were not confirmed by a command.
Destination when accepted: C:\BRAIN_OS\HARNESS.md

---

## 1. Context Assembler

Auto-loaded by Claude Code:
- `C:\Users\titit\.claude\CLAUDE.md` — 0.2 KB, global, every session on this
  machine. Contains only the `/graphify` skill trigger.
- `C:\BRAIN_OS\CLAUDE.md` — 8.8 KB, updated 8/19/2026. The operating contract.

Manually loaded (by Cristian, not by the harness):
- `07_SYSTEM\Cristian_Principles.md`
- `02_PROJECTS\graphs\brain-os.context.md` — 2.7 KB, August

Generated context layer (`graphify` output, `02_PROJECTS\graphs\`):
- `brain-os.context.md`, `brain-os.graphify.json`, `brain-os.json` (11.9 KB)
- Same triad exists for: ca-book, read-along-app, soccer-content-generator
- Does NOT exist for: custom-agent, resolve-mcp-server, obs-mcp-server

Orchestrator: `09_TOOLS\session_start.py`
- Loads project context, health check, Telegram notification
- Project registry covers: bdf, brainos, ca, construction, resolve
- Auto-detects project from cwd when `--project` omitted

Second CLAUDE.md: `03_APIS\CLAUDE.md`, 5.2 KB, 6/17/2026 — two months stale.
Relationship to root CLAUDE.md UNVERIFIED.

## 2. Tool Layer

`%APPDATA%\Claude\claude_desktop_config.json` — 2.6 KB, 8/21/2026, live:
- `davinci-resolve` → resolve-mcp-server\server.py
- `davinci-resolve-api` → resolve-mcp-server\server_api.py
- `context7` → npx @upstash/context7-mcp
- `obsidian` → npx obsidian-mcp, pointed at C:\BRAIN_OS

Second install: `AppData\Local\Packages\Claude_pzs8sxrjxfjjc\...` (MSIX),
0.1 KB, 4/17/2026, no servers. Abandoned.

Skill layer: `~\.claude\skills\graphify\SKILL.md`, invoked via `/graphify`.

Tool schemas are read once at harness startup and cached. Adding or changing
a server requires a full Claude Desktop restart.

## 3. Loop

Not owned. Anthropic's, via Claude Code and Claude Desktop.
Raw transcripts at `C:\Users\titit\.claude\projects\*\*.jsonl` — one JSON
object per turn. This is the only readable record of loop execution.

## 4. Policy Gate

Written in `CLAUDE.md`, enforced by nothing:
- trace before changing
- read-only verification before destructive actions
- no "for now" patches — root fixes only
- check `Tools_Registry.md` before adopting a tool
- atomic commits (both sides of a contract in one push)
- git add by explicit filename, never -A
- FLAGS.txt has exactly one writer, at session close only

No spend ceiling of any kind.

Whether `session_start.py` enforces anything — exits non-zero, blocks on a
failed health check — is UNVERIFIED. First 40 lines are imports and paths.

## 5. State Persistence

- `08_SESSIONS\*.md` — authoritative local session record
- `FLAGS.txt` — study/gap ledger
- `02_PROJECTS\LESSON_QUEUE.md`
- `02_PROJECTS\graphs\projects.manifest.json`, `artifacts.manifest.json`
- `05_MEMORY\`
- `audio_staging\lancedb.json`, `audio_staging\lancedb_vector_store.json`
- git remote: TititoBuilder/BRAIN_OS

---

## GAPS

1. `session_start.py` hardcodes
   `ENV_FILE = C:\Dev\Projects\soccer-content-generator\.env`.
   BRAIN_OS's orchestrator loads credentials from BDF's project. Applies to
   every project in the registry, not just bdf. Same hardcoded-path pattern
   fixed elsewhere in August; survived here. → DESIGN, high

2. `.context.md` coverage is 4 projects, and the set does not match the
   harness target set. custom-agent, resolve-mcp-server, obs-mcp-server have
   none — so the "load CLAUDE.md + .context.md, no exceptions" clause is
   unsatisfiable for 3 of 5 targets. → RISK

3. Policy gate is documentation, not enforcement. Every rule depends on
   Cristian remembering it mid-session. → DESIGN

4. No spend ceiling. BDF has one (~$0.01/post, Schnell vs 1.1 Pro).
   BRAIN_OS has no equivalent. → DESIGN, cross-pollination candidate

5. Two CLAUDE.md files in the vault; `03_APIS\` copy two months stale.
   Precedence undocumented. → DESIGN

6. Global `.claude\CLAUDE.md` is 200 bytes. Highest-leverage file on the
   machine — loaded into every session, every project — carries one line.
   → DESIGN

7. Second Claude Desktop install (MSIX) with empty config. Editing the wrong
   file silently does nothing. → RISK

8. `audio_staging\lancedb.json` matches
   `read-along-app\backend\transcripts\lancedb.json` at identical line
   numbers (1544, 1658, 1982, 2546, 2696, 2930, 2978). Duplicated state
   across two projects, no declared owner. → DESIGN

9. `C:\AI\` — Datasets + Models, created 3/22/2026 9:30:16 AM, zero
   references anywhere on disk. Dead. → RISK, delete candidate

---

## OPEN QUESTIONS

- Does `session_start.py` block, or only report?
- What does `03_APIS\CLAUDE.md` contain that the root one doesn't?
- Which of the two `audio_staging` lancedb files is authoritative?
- Is `C:\BDF\lancedb` read by anything, or orphaned?
