---
tags: [agent, live]
---

# AGENT: BDF Analysis Agent

## Project
BDF Soccer Bot

## Function
Multi-query RAG retrieval over the LanceDB soccer knowledge corpus — rewrites the query into 3 semantic variants, retrieves, deduplicates, filters by relevance score, and reranks with a local CrossEncoder before returning the top 8 documents.

## Input
- `topic` (str) — player name, team, match context
- `content_type` (str) — "skill", "goal", "analysis", etc.
- LanceDB vector store at `F:/lance_db_soccer` (env var `LANCE_DB_PATH`)

## Output
- `list[dict]` — up to 8 ranked documents with relevance scores
- `get_stats()` — pipeline telemetry: total_calls, avg_docs_retrieved, avg_docs_after_filter, filter_pass_rate_pct

## Trigger
Called by SoccerBot and the content generation pipeline whenever factual context is needed for caption or post generation.

## Tools and APIs
- [[LanceDB]] — local vector store at `F:/lance_db_soccer`; env var `LANCE_DB_PATH`; fallback `./lance_db`
- [[Anthropic_Claude]] — `claude-haiku-4-5-20251001` for query rewriting (3 semantic variants per call)
- `cross-encoder/ms-marco-MiniLM-L-6-v2` — local CrossEncoder reranker (HuggingFace sentence-transformers, GPU, zero API cost)

## Canonical file
C:\Dev\Projects\soccer-content-generator\src\rag_pipeline.py

## Connected to
- [[BDF_Automation_Agent]] — SoccerBot passes VectorStore instance into RagPipeline at init
- [[BDF_Memory_Agent]] — mcp_ingest.py writes clip records that populate LanceDB
- [[BDF_Soccer_Bot]] project

## Status
Live

## Pipeline steps
1. `_rewrite_query` — Claude Haiku generates 3 variants: stats/form, competition context, narrative angle
2. `_multi_retrieve` — queries vector store with each variant
3. `_deduplicate` — removes duplicate docs by ID
4. `_filter_by_score` — drops docs below relevance threshold (0.82)
5. `_rerank` — CrossEncoder scores each (query, doc) pair, sorts descending
6. Returns top `MAX_FINAL_DOCS` (8)
