---
tags: [system, claude, cost, infra, live]
parent: "[[Tools_Registry]]"
updated: 2026-04-30
---

# Claude Code — Cost Control & Permission Standard

## The problem (discovered 2026-04-30)
- `Bash(*)` + `Read(*)` wildcards = unbounded context window on every agentic step
- Each tool call resends entire conversation history + all readable files
- One long session with Opus = $5–15 in a single day
- April 2026 spike: ~$25 in 2 days from unconstrained soccer bot sessions

---

## Model cost hierarchy
| Model | Input $/M | Output $/M | Use for |
|---|---|---|---|
| Claude Opus 4.5 | $15.00 | $75.00 | Never — use Sonnet |
| Claude Sonnet 4.6 | $3.00 | $15.00 | Default for everything |
| Claude Haiku 4.5 | $0.80 | $4.00 | Simple classification tasks |

**Rule: always default to `claude-sonnet-4-6`. Opus only for hard architecture decisions and only manually.**

---

## Permission standard — project settings.json

```json
{
  "permissions": {
    "allow": [
      "Read(C:\\Dev\\Projects\\{project}\\src\\**)",
      "Read(C:\\Dev\\Projects\\{project}\\tests\\**)",
      "Write(C:\\Dev\\Projects\\{project}\\src\\**)",
      "Edit(C:\\Dev\\Projects\\{project}\\src\\**)",
      "Bash(python *)",
      "Bash(pip install *)",
      "Bash(pytest *)",
      "Bash(git status)",
      "Bash(git diff *)",
      "Bash(git add *)",
      "Bash(git commit *)"
    ],
    "deny": [
      "Bash(rm *)",
      "Bash(curl *)",
      "Bash(wget *)"
    ]
  }
}
```

**Never use:** `Bash(*)`, `Read(*)`, `Write(*)`, `Edit(*)` — these are god-mode and cause runaway costs.

---

## .claudeignore standard
Add to every project root:

```
__pycache__/
*.pyc
.venv/
venv/
node_modules/
*.log
*.lock
dist/
build/
data/raw/
```

---

## Model switch completed 2026-04-30
| Project | Files changed | Old model | New model |
|---|---|---|---|
| soccer-content-generator | book_compiler.py, mcp_book_compiler.py, story_generator.py, COST_ANALYSIS.md | claude-opus-4-5 | claude-sonnet-4-6 |
| resolve-mcp-server | none found | — | — |

---

## Cost monitoring
- Script: `C:\BRAIN_OS\03_APIS\claude_monitor.py`
- Input: CSV from console.anthropic.com → Cost → Export
- Alerts: Telegram via Boticris bot
- Schedule: 1st of every month (calendar event set)
- See: [[Tools_Registry]]
