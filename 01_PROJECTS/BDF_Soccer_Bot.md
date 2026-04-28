# PROJECT: BDF Soccer Bot

## Status
Active

## Brain Architecture coverage
- Input Layer: yes
- AI Agents: yes
- Workflows: yes
- Knowledge Graph: yes
- Output Layer: yes
- Infrastructure: yes

## Root path
C:\Dev\Projects\soccer-content-generator\

## GitHub
TititoBuilder/soccer-content-generator

## Inputs
- DaVinci Resolve render outputs (MP4) landing in `C:\BDF\renders\staging\`
- `C:\BDF\renders\export_log.jsonl` — append-only log written by export_pipeline.py
- Football fixture data via Football-Data.org API
- Soccer news via NewsAPI
- Telegram approval messages (human-in-the-loop content gating)

## Active agents
- [[ClipNameParser]] — parses subject / content_type / competition / date from filename stems
- [[KnowledgeEnricher]] — TF-IDF cosine retrieval against soccer knowledge corpus (threshold 0.6801)
- [[SubjectMemory]] — tracks per-subject clip history, frequency, and recency across sessions
- [[PatternDetector]] — tracks subject/content_type frequency for editorial pattern signals
- [[SoccerBot]] — RAG bot with TopicRouter, MatchDataFetcher, VectorStore, CostTracker
- [[ContentAgent]] — generates captions and post copy via Claude Haiku
- [[QualityAgent]] — scores generated content before queuing
- [[MediaAgent]] — handles platform-specific media formatting

## Connected APIs
- [[Anthropic_Claude]] — caption generation (claude-haiku-4-5-20251001), enrichment, RAG (claude-sonnet-4-6)
- [[OpenAI]] — fallback LLM layer
- [[Twitter_X]] — clip/caption publishing via tweepy
- [[Telegram]] — human approval gate via python-telegram-bot; hybrid deferred: terminal -> phone -> sync publish
- [[Football_Data_org]] — live fixture schedule, match results, standings
- [[NewsAPI]] — soccer news context for enrichment
- [[Google_Drive]] — book/TTS output archival via google-api-python-client
- [[YouTube]] — video upload target via google-api-python-client

## Outputs
- Twitter/X posts (clip + caption, platform-optimized)
- Telegram approval queue + published confirmations
- LanceDB vector records at `C:/lance_db_soccer` table `mcp_clips`
- Content queue at `src/queue/content_queue.json`
- Routed MP4 library at `C:\BDF\library\{category}\{Subject}\{content_type}\`
- BDF Share drop at `C:\BDF_Share\` (ingest copies verified clips here)
- Dashboard at `http://localhost:8000` (FastAPI) — /api/fixtures, /api/queue, /api/stats, /api/players, /api/health
- Compiled knowledge books (book_compiler.py / mcp_book_compiler.py) — TTS + Drive upload

## Workflows
- [[ExportPipeline]] — 4-step one-pass: detect MP4s in staging -> write export_log entry -> run mcp_ingest -> route to library (`export_pipeline.py`)
- [[McpIngest]] — reads new export_log entries, enriches via KnowledgeEnricher, generates captions via Claude, writes LanceDB + Share + queue (`mcp_ingest.py`)
- [[TelegramApprover]] — deferred send to Telegram, human approves on phone, sync-publishes to Twitter (`telegram_approver.py`)
- [[DashboardApi]] — FastAPI server exposing fixture and queue state to local Vite dashboard (`dashboard_api.py`)
- [[BookCompiler]] — routes tagged `.txt`/`.md` chapters into compiled knowledge books, uploads via Google Drive (`book_compiler.py`, `mcp_book_compiler.py`)
- [[ResolveExport]] — DaVinci Resolve batch render via MCP bridge (resolve-mcp-server), one job per platform per clip range
