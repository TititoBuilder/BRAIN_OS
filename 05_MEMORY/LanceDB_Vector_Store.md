---
tags: [memory, live]
---

# MEMORY: LanceDB Vector Store

## Purpose
Local vector database storing soccer knowledge documents with semantic embeddings. Supports RAG retrieval for BDF caption generation and content enrichment.

## Type
Vector store — persistent, file-based (LanceDB on-disk format)

## Location
**Canonical path:** `C:/Dev/Projects/soccer-content-generator/lance_db_soccer`
**Env var:** `LANCE_DB_PATH` — all code must read this; hardcoded fallbacks standardized to canonical path on 2026-04-27
**Table name:** `soccer_knowledge`
**Schema:** `id` (str), `content` (str), `vector` (float[]), `metadata` (JSON str)
**Embedding model:** `all-MiniLM-L6-v2` (sentence-transformers, loaded once at VectorStore init)

> **STALE PATH — DO NOT USE:** `F:/lance_db_soccer` — this was a WD external drive mount. Drive may be disconnected. Path is empty. Any code or note referencing F:/ is outdated.

## Files that read or write this store (from 2026-04-27 bug audit)
| File | Role |
|---|---|
| `src/vector_store.py` | VectorStore class — all add/search/delete/clear ops |
| `src/rag_pipeline.py` | `RagPipeline.retrieve()` — multi-query search + rerank |
| `mcp_ingest.py` | Writes new clip documents after export enrichment |
| `bot_service.py` | Reads doc count in `_count_docs()` helper |
| `rebuild_lancedb.py` | Drops and recreates table from source data |
| `scripts/cleanup_lancedb_duplicates.py` | Deduplicates by `id` field using pandas |

## Connected agents
- [[BDF_Analysis_Agent]]
- [[BDF_Memory_Agent]]

## Rules
- **LANCE_DB_PATH env var is authoritative** — never hardcode a path in application code
- All fallbacks standardized to `r"C:/Dev/Projects/soccer-content-generator/lance_db_soccer"` on 2026-04-27
- `rebuild_lancedb.py` bug fixed 2026-04-27: `shutil.rmtree('./lance_db')` replaced with env-var-resolved path — previously would have wiped a different directory than lancedb.connect targeted
- Run `scripts/cleanup_lancedb_duplicates.py` when WD drive was recently reconnected (may have synced duplicates)
- Separate LanceDB store exists at `C:\BDF\lancedb` for Resolve MCP / mcp_ingest clip metadata — different purpose, different table (`mcp_clips`)

## Status
Active. Populated with soccer knowledge documents. Doc count visible at startup via `VectorStore.__init__` log line.
