# API: Anthropic Claude

## Purpose
LLM backbone for caption generation, content analysis, RAG query rewriting, and conversational agents across all projects.

## Used by projects
- BDF, CA, ReadAlong, Resolve

## Limits and rules
- Rate limits: tier-dependent; prompt caching enabled in mcp_ingest.py (`anthropic-beta: prompt-caching-2024-07-31`)
- Cost: ~$0.006–$0.008 per post (tracked in cost_tracker.py); claude-opus-4 billed at $15/$75 per million tokens (in/out)
- Legal constraints: none project-specific

## Credentials
`ANTHROPIC_API_KEY`

## Connected agents
- [[BDF_Memory_Agent]]
- [[BDF_Research_Agent]]
- [[BDF_Analysis_Agent]]
- [[BDF_Creative_Agent]]
- [[CA_Orchestrator]]
- [[Resolve_Editing_Agent]]

## Inputs
- System prompt + user message dict (all projects use messages=[{"role":"user","content":...}])
- Prompt cache blocks: `{"type":"text","text":...,"cache_control":{"type":"ephemeral"}}` (mcp_ingest.py)
- Models by context:
  - `claude-haiku-4-5-20251001` — mcp_ingest.py, rag_pipeline.py (fast/cheap caption + query rewrite)
  - `claude-sonnet-4-6` — CristianConstruction claude_client.py (all 9 CA agents)
  - `claude-sonnet-4-20250514` — soccer_bot.py (content generation)
  - `claude-opus-4` — book_compiler.py, mcp_book_compiler.py (long-form creative)

## Outputs
- `resp.content[0].text` — caption text, JSON query variants, story segments
- Token usage logged per call in cost_tracker.py
- Streaming not used; all calls are synchronous `client.messages.create()`
