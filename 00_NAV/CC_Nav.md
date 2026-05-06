---
tags: [nav, construction]
updated: 2026-05-05
commit: 9ce37d4
---

# CristianConstruction Navigation

## Launch Sequence
```powershell
# T1 — FastAPI backend
cd C:\Dev\CristianConstruction
.\venv\Scripts\Activate.ps1
uvicorn src.api.main:app --reload

# T2 — React dashboard
cd C:\Dev\CristianConstruction\dashboard
npm run dev

# T3 — Claude Code
cd C:\Dev\CristianConstruction
claude

# T4 — Landing page hot-reload
dev   # alias: watches cc_landing.html → auto-deploys to Vercel
```
**URLs:** API `http://localhost:8000` · Dashboard `http://localhost:3000`
**Vercel:** `https://cc-landing-v2-eta.vercel.app`

## Key Paths
| Item | Path |
|---|---|
| Code | `C:\Dev\CristianConstruction\` |
| Venv | `C:\Dev\CristianConstruction\venv\` |
| Workspace | `custom-agent.code-workspace` |
| Data (NEVER DELETE) | `data\jobs.csv` · `clients.csv` · `schedule.csv` · `reviews.csv` · `referrals.csv` |
| Landing page | `cc_landing.html` |
| Deploy script | `C:\Dev\deploy-landing.ps1` |

## 9 Agents
`lead_agent` · `quote_agent` · `review_agent` · `social_agent` · `finance_agent`
`schedule_agent` · `proposal_agent` · `reputation_agent` · `referral_agent`
Routing: `sms_handler.py` + `telegram_handler.py`

## GitHub
Remote: `TititoBuilder/cristian-construction`
HEAD: `9ce37d4` — feat: centralize Telegram integration with 8-command handler
