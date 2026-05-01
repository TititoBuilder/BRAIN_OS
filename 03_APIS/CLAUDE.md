## Session close checklist

- [ ] Merge any open worktrees to main
- [ ] Run session_close.py from the touched project
- [ ] Confirm Telegram confirmation received
- [ ] Confirm BRAIN_OS commit appears in git log

---

# BRAIN_OS / 03_APIS — Claude Code Workspace

## Project Overview

`03_APIS` is the API documentation and monitoring hub for the BDF system: it
holds markdown reference sheets for every external API in use (Anthropic,
Twitter, Telegram, Football-Data, etc.) and `claude_monitor.py`, a script that
pulls live usage data from the Anthropic Admin API and fires Telegram alerts
when daily or monthly spend exceeds configured budgets.

---

## Stack

| Item | Detail |
|---|---|
| Language | Python 3.12+ |
| AI cost monitoring | `anthropic` SDK (Admin API, usage endpoint) |
| Terminal output | `rich` (graceful fallback to `print` if absent) |
| Env | `python-dotenv` |
| Alerts | `urllib.request` → Telegram Bot API |
| Docs format | Markdown (one `.md` per API) |

---

## Model Standard

`claude_monitor.py` does not generate AI content — it queries the Anthropic
Admin API for billing data only. Any future scripting that calls Claude in
this directory must use **`claude-sonnet-4-6`**. Never use `claude-opus-*`
models — Opus drove 87.9% of the API bill in prior audits and is what this
monitor exists to catch.

---

## Permission Rule

**Never use `Bash(*)` or `Read(*)` wildcards.** Scope every tool call to a
specific file path. This directory is part of the BRAIN_OS Obsidian vault —
wildcard writes can corrupt vault metadata.

---

## MCP integrations

- **Context7**: use `resolve-library-id` then `query-docs` for any library before writing code that calls it — never rely on training data for anthropic, python-dotenv, or rich.
- **Obsidian**: all decisions and builds get documented in `C:\BRAIN_OS` before the session closes (via `session_close.py` in soccer-content-generator).
- **Telegram**: all alerts use `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID` via `urllib.request` POST to `api.telegram.org`. No other notification service.

---

## Tools in Use

Full registry: `C:\BRAIN_OS\07_SYSTEM\Tools_Registry.md`

Key tools active in this directory:
- **claude_monitor.py** — Anthropic Admin API cost monitor + Telegram alerter
- **Telegram bot** — alert delivery (same bot token as BDF pipeline)
- **Context7 MCP** — live docs for `anthropic`, `python-dotenv`, `rich`

---

## Notification Standard

All alerts from `claude_monitor.py` route through the existing Telegram bot.
- Token: `TELEGRAM_BOT_TOKEN` in `.env`
- Chat ID: `TELEGRAM_CHAT_ID` in `.env`
- Fires when: daily spend > `DAILY_BUDGET_USD` OR monthly projection > `MONTHLY_BUDGET_USD`
- Do not introduce any other notification service (no Gmail SMTP, ntfy, Slack).

---

## Session Close Procedure

At the end of every working session, run from the soccer-content-generator root:

```
cd C:\Dev\Projects\soccer-content-generator
venv\Scripts\python session_close.py
```

This archives the session summary to `C:\BRAIN_OS\09_TOOLS\session_{date}.md`,
commits BRAIN_OS, and sends a Telegram confirmation.

---

## Do Not Run

| Script / Action | Reason |
|---|---|
| `claude_monitor.py` in a loop / cron without reading output | It makes live Admin API calls that count toward rate limits; always review output before scheduling |
| Any script that writes to `C:\BRAIN_OS\` outside a git worktree | BRAIN_OS is an Obsidian vault — always commit changes via git so Obsidian sync stays clean |

---

## Active .env Vars

The `.env` file lives in `C:\BRAIN_OS\03_APIS\.env`. Keys only — never print
or log values.

```
ANTHROPIC_ADMIN_KEY
DAILY_BUDGET_USD
MONTHLY_BUDGET_USD
TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID
```

---

## Directory Contents

| File | Purpose |
|---|---|
| `claude_monitor.py` | Live Claude API cost monitor + Telegram budget alerts |
| `Anthropic_Claude.md` | Anthropic API reference (models, pricing, limits) |
| `Football_API.md` | API-Football / RapidAPI reference |
| `GoogleDrive_API.md` | Google Drive API reference |
| `KlingAI.md` | Kling AI video generation API reference |
| `NewsAPI.md` | NewsAPI.org reference |
| `OpenAI_gpt-image-1.md` | OpenAI image generation API reference |
| `Pixabay_API.md` | Pixabay stock image API reference |
| `Telegram_Bot.md` | Telegram Bot API reference (our bot setup, commands) |
| `Twitter_API_v2.md` | Twitter / X API v2 reference (OAuth 2.0, endpoints) |

---

## Running claude_monitor.py

```
cd C:\BRAIN_OS\03_APIS
python claude_monitor.py
```

Requires `ANTHROPIC_ADMIN_KEY` (Admin API key — different from the standard
`ANTHROPIC_API_KEY` used by the BDF pipeline). The Admin key is obtained from
`console.anthropic.com → API Keys (Admin)`.

Output: terminal table grouped by model + Telegram alert if over budget.
Schedule: run manually at start of month after reviewing the console CSV.
