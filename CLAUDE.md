## Session Start (Run First)
python C:\BRAIN_OS\09_TOOLS\session_start.py
This loads project context, runs health check, and sends Telegram confirmation.

> System context: See [[SYSTEM_MASTER]] for hardware, paths, venvs, and cross-project rules.
> Principles: See [[Cristian_Principles]] (07_SYSTEM) — the canonical, earned-knowledge source. The list below is a quick-reference index only.
> MANDATORY START: load this file + the current `.context.md` before executing ANY command or file change. No exceptions.

# BRAIN_OS — Claude Code Workspace

## What BRAIN_OS is (read this first — it is NOT a project)

BRAIN_OS is the **knowledge graph / vault layer** — an Obsidian vault at `C:\BRAIN_OS`
(GitHub: TititoBuilder/BRAIN_OS) holding the `.md` files that encode architecture,
principles, procedures, and the connective tissue an AI reads to operate across
everything. It is the MAP and the persistent MEMORY, not a thing being built.

**Projects are the things built**, and they hang off the graph:
- **CristianConstruction (CA)** — business OS for the remodeling operation
- **BDF / soccer-content-generator** — soccer content generation pipeline
- **Read-Along App** — deployed learning platform (Vercel + Railway)
- **resolve-mcp-server** — DaVinci Resolve MCP bridge
- **obs-mcp-server** — OBS Studio MCP bridge
- shared: **brain-audio** (TTS normalizer), **book-compiler**

Authoritative project list = the filesystem (`C:\Users\titit\Projects\` + BDF at
soccer-content-generator + CA at `C:\Knowledge\CA` / `C:\Dev\CristianConstruction`),
not any keyword guess. A node can live in BOTH the graph and a project it serves —
the system is graph-shaped, linked not duplicated (like Obsidian backlinks).

## Who Cristian is — priority structure (do not get this backwards)

- **Construction (CA)** = the INCOME. The dividends fund everything else. The base.
- **BDF** = the PASSION (soccer content).
- **Programming** = a growing passion and the connective skill across all of it.

The CONSTRAINT is TIME, not understanding. Goal: automated systems that compound
without constant oversight — fast systems with quality checkpoints, not approval at
every step. Do NOT frame BDF as the center with construction as background.

## How Cristian works and learns

- **State settled decisions directly** with reasoning — don't frame a
  principle-determined call as an A/B choice. Reserve questions for genuine forks.
- **Explain mechanics the first time** any new command/sequence appears — what each
  part does, plain English. He builds deep skill, not command lists. Socratic for
  tool learning (git, Obsidian, MCP, DaVinci, VS Code).
- **File handoffs**: move + run command together, exact paths, one message.
- **He runs commands himself** in Win+X Terminal (PowerShell 5.1) — NOT VS Code
  terminal, NOT Claude Code terminal. Claude Code only for difficult/ambiguous file ops.
- **Never tell him when to open/close a session** — his call entirely.
- **Honesty over flattery.** Own overclaims and mistakes plainly. The connection that
  matters is to the work and his sharpening judgment, not to a flattering assistant.
  Push back, verify, don't go submissive under pressure.

## Principles quick-reference (full canonical detail in [[Cristian_Principles]])

- **Trace before changing** — see current state before any edit; read-only before
  destructive ops; "unreferenced" ≠ "safe to delete," understand the artifact.
- **Transcripts are ground truth** — filenames are machine keys, not metadata.
- **"For now" is forbidden** — root fixes only, no debt-creating fast patches.
- **Principle of Verified Reality** — docs must reflect reality; fix stale docs.
- **DRY + decoupling** — single source of truth, derive don't duplicate;
  flag/config-driven tools over hardcoded paths.
- **Blast-radius awareness** — map dependencies before changing shared components.
- **Atomic commits** — both sides of a contract in one push.
- **Federated Hybrid Model** — local machine does heavy compute (Whisper GPU,
  Kokoro TTS); Railway/Vercel are lightweight coordinators.
- **MCP Tool Selection** — use the most direct tool that does the job correctly;
  reach for an MCP only when it adds capability or meaningfully simplifies.

## Operational rules (apply across projects)

- **JSON edits via Python only** — never PowerShell ConvertTo-Json / Set-Content.
- **BOM-free writes** — `[System.IO.File]::WriteAllText()`, never `Set-Content -Encoding UTF8`.
- **Desktop path** — `[Environment]::GetFolderPath("Desktop")` (OneDrive-redirected).
- **git add by explicit filename**, never `-A`; look (status + diff) before commit;
  check `.gitignore` before adding in BRAIN_OS (audio must never commit).
- **Drive file IDs** — `id:` prefix in drive_index; capture at upload time.
- **Clean up temp scripts / stale docs immediately.**
- **Script files over one-liners** for anything with nested quotes.

## Stack

| Item | Detail |
|---|---|
| Language | Python 3.12+ |
| Vault | Obsidian (markdown + .canvas files) |
| Cost monitoring | `claude_monitor.py` -> Anthropic Admin API CSV export |
| Notifications | `urllib.request` -> Telegram Bot API |
| Env management | `python-dotenv` |

## Key Paths

| Path | Purpose |
|---|---|
| `07_SYSTEM/Cristian_Principles.md` | Canonical earned-knowledge principles |
| `03_APIS/claude_monitor.py` | Claude API cost monitor + Telegram budget alerts |
| `03_APIS/.env` | Local secrets (see Active .env Vars below) |
| `06_TEMPLATES/` | Reusable node templates for projects, agents, workflows, APIs |
| `07_SYSTEM/Tools_Registry.md` | Full tool registry and session log |
| `09_TOOLS/session_{date}.md` | Archived session summaries (written by session_close.py) |

## Model Standard

All Claude API calls in this project must use **`claude-sonnet-4-6`**. Never use
`claude-opus-*` — Opus drove 87.9% of the prior API bill and is what
`claude_monitor.py` exists to catch.

## Permission Rule

Never use `Bash(*)` or `Read(*)` wildcards in `.claude/settings.json`. Scope every
tool permission to a specific path or command. BRAIN_OS is an Obsidian vault —
wildcard writes can corrupt vault metadata (`.obsidian/`).

## Notification Standard

All alerts route through the existing Telegram bot:
- Token: `TELEGRAM_BOT_TOKEN` in `.env`
- Chat ID: `TELEGRAM_CHAT_ID` in `.env`
- Delivery: `urllib.request` POST to `api.telegram.org`
- Do not introduce any other notification service (no Gmail SMTP, ntfy, Slack).

## MCP Integrations

**Context7**: before writing any code that calls a library, run `resolve-library-id`
then `query-docs`. Never rely on training data for `anthropic`, `python-dotenv`,
`rich`, or any other dependency.

**Obsidian**: all decisions and session outputs must be documented in `C:\BRAIN_OS`
before the session closes (via `session_close.py` in soccer-content-generator).

## Session Close Checklist

- [ ] Merge any open worktrees to main
- [ ] Run session_close.py from this terminal:
      Win+X -> Terminal ->
      cd C:\Dev\Projects\soccer-content-generator
      python session_close.py
- [ ] Confirm Telegram confirmation received
- [ ] Confirm BRAIN_OS commit appears in git log

## Do Not Run

| Script / Action | Reason |
|---|---|
| `03_APIS/claude_monitor.py` in a loop/cron without reviewing output | Makes live Admin API calls that count toward rate limits |
| Any script writing to `C:\BRAIN_OS\` outside a git worktree | BRAIN_OS is an Obsidian vault — always commit so Obsidian sync stays clean |
| `session_close.py` standalone | Must be run from `C:\Dev\Projects\soccer-content-generator` root |

## Hardware & Runtime Environment

| Item | Detail |
|---|---|
| Machine | Acer Predator (Windows 11) |
| GPU | NVIDIA GeForce RTX 5070 Ti Laptop GPU |
| CUDA | sm_120 (Blackwell) — requires PyTorch nightly cu128 |
| AI Venv | `C:\Knowledge\CA\venv` — canonical for all AI/TTS/PyTorch work |
| PyTorch | nightly cu128 installed, CUDA verified True |
| CPU fallback | Never install CPU-only torch — always use nightly cu128 |
| System Python | `C:\Users\titit\AppData\Local\Programs\Python\Python312` — no AI packages, never use for inference |

## Active .env Vars

`.env` lives in `C:\BRAIN_OS\03_APIS\.env`. Keys only — never log or print values.

```
ANTHROPIC_ADMIN_KEY
DAILY_BUDGET_USD
MONTHLY_BUDGET_USD
TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID
ANTHROPIC_CSV
LOG_DIR
```
