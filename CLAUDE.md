# BRAIN_OS — Claude Code Workspace

## Project Overview

BRAIN_OS is a structured Obsidian vault and knowledge-management layer for the BDF automation system, holding API references, agent documentation, session archives, workflow templates, and system tooling. It functions as the persistent memory and audit trail for all AI-assisted development work across connected projects.

## Stack

| Item | Detail |
|---|---|
| Language | Python 3.12+ |
| Vault | Obsidian (markdown + .canvas files) |
| Cost monitoring | `claude_monitor.py` → Anthropic Admin API CSV export |
| Notifications | `urllib.request` → Telegram Bot API |
| Env management | `python-dotenv` |

## Key Paths

| Path | Purpose |
|---|---|
| `03_APIS/claude_monitor.py` | Claude API cost monitor + Telegram budget alerts |
| `03_APIS/.env` | Local secrets (see Active .env Vars below) |
| `06_TEMPLATES/` | Reusable node templates for projects, agents, workflows, APIs |
| `07_SYSTEM/Tools_Registry.md` | Full tool registry and session log |
| `09_TOOLS/session_{date}.md` | Archived session summaries (written by session_close.py) |

## Model Standard

All Claude API calls in this project must use **`claude-sonnet-4-6`**. Never use `claude-opus-*` — Opus drove 87.9% of the prior API bill and is what `claude_monitor.py` exists to catch.

## Permission Rule

Never use `Bash(*)` or `Read(*)` wildcards in `.claude/settings.json`. Scope every tool permission to a specific path or command. BRAIN_OS is an Obsidian vault — wildcard writes can corrupt vault metadata (`.obsidian/`).

## Notification Standard

All alerts route through the existing Telegram bot:
- Token: `TELEGRAM_BOT_TOKEN` in `.env`
- Chat ID: `TELEGRAM_CHAT_ID` in `.env`
- Delivery: `urllib.request` POST to `api.telegram.org`
- Do not introduce any other notification service (no Gmail SMTP, ntfy, Slack).

## MCP Integrations

**Context7**: before writing any code that calls a library, run `resolve-library-id` then `query-docs`. Never rely on training data for `anthropic`, `python-dotenv`, `rich`, or any other dependency.

**Obsidian**: all decisions and session outputs must be documented in `C:\BRAIN_OS` before the session closes (via `session_close.py` in soccer-content-generator).

## Session Close Checklist

- [ ] Merge any open worktrees to main
- [ ] Run session_close.py from this terminal:
      Win+X → Terminal →
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
