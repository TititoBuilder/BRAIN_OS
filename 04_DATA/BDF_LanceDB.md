---
tags: [bdf, pipeline, live]
updated: 2026-05-01
parent: "[[BDF_Soccer_Bot]]"
---

# BDF LanceDB Vector Store

This document describes what data lives in the BDF vector store, what tables exist, how the pipeline queries it, and why LanceDB was chosen over alternatives.

---

## Physical Location

The live vector store is on the WD Elements external drive, which always mounts as `D:` on the Predator machine. The canonical path is `D:\lance_db_soccer`. Some older code and the `.env` template reference `C:\lance_db_soccer` or `C:/lance_db_soccer` — this is wrong and will silently fail to find any data on a fresh session if the drive is not mounted. The environment variable `LANCE_DB_PATH` must point to `D:\lance_db_soccer`. The health check in `dashboard_api.py` reads this env var at runtime.

---

## Tables

### soccer_knowledge

The primary knowledge table. It is populated by `lancedb_integrator.py` using structured data from CSV files and by `mcp_ingest.py` for DaVinci export clips. The table stores three categories of document:

**Player profiles** — Created from `player_profiles.csv` combined with optional `personal_life.csv` and `tactical_data.csv`. Each document is a rich natural-language description of a player: name, age, club, position, nationality, market value with a contextual tier label (world-class superstar / top-tier player / promising talent / developing player), key strengths, career highlights, international caps and goals, and personal-life context when available. Schema fields include `id`, `name`, `stage_name`, `club`, `position`, `nationality`, `age`, `market_value`, `content_type` (= `"player_profile"`), `searchable_text`, `vector`, and `metadata`.

**Club profiles** — Created from `clubs.csv`. Each document covers club name, country, league, stadium with capacity, founding year, nickname, and a market-value-based prestige label. Schema fields mirror player profiles with `content_type` = `"club_profile"`, replacing the player-specific attributes with `country`, `league`, `stadium`.

**Competition records** — Created from `competitions.csv`. Each document covers competition name, type, country, founding year, and a prestige level that produces a qualitative descriptor. Schema field `content_type` = `"competition"`.

### mcp_clips

Populated by `mcp_ingest.py` for every DaVinci Resolve export processed. This table stores clip metadata alongside AI-generated captions. See `CLAUDE.md` for the full field list and a note on the mandatory pre-build diagnostic. The `mcp_clips` table is separate from `soccer_knowledge` — it stores operational pipeline records (exports, captions, queue entries) while `soccer_knowledge` stores editorial knowledge (players, clubs, competitions).

---

## Embedding Model and Distance Metric

The embedding model used by `lancedb_integrator.py` is `all-MiniLM-L6-v2` from the `sentence-transformers` library. This model produces 384-dimensional float vectors. LanceDB stores these as `vector` columns and performs approximate nearest-neighbour search using L2 (Euclidean) distance by default. The `dashboard_api.py` health check confirms the `soccer_knowledge` table is accessible by counting rows via `tbl.count_rows()`.

---

## How the Pipeline Queries LanceDB

`src/vector_store.py` is the primary query interface. It wraps LanceDB with a `VectorStore` class that exposes a `get_stats()` method (row count, table list) and semantic search. At dashboard startup, `initialize_vector_store()` in `dashboard_api.py` calls `VectorStore().get_stats()["total_documents"]` and caches the count to display in the health panel.

The `/status` hub route performs a live count on every call: `db.open_table("soccer_knowledge").count_rows()`. The `/api/health` route opens the table directly and counts rows via `to_pandas()`.

The caption enrichment path in `mcp_ingest.py` (when active) queries `soccer_knowledge` semantically before calling the Anthropic API: it embeds the clip subject and competition as a query vector, retrieves the top-k matching knowledge documents, and injects that context into the caption prompt so that captions can reference factual information ("Guler's third UCL goal this season") rather than generating plausible-sounding but unverified claims.

---

## Why LanceDB

LanceDB was chosen because it runs entirely in-process with no separate server, installs as a Python package, stores data as files on disk, supports columnar Lance format with efficient vector indexing, and has a clean Python API for both writes and searches. For a solo pipeline on a single machine, the zero-server model eliminates a category of operational risk (daemon management, port conflicts, restart sequences) and means the full pipeline can be launched with a single `python` command from the venv.

An alternative considered was ChromaDB, but LanceDB's native Lance file format offers better performance for large metadata scans alongside the vector search, which matters for the clip metadata queries in `mcp_clips`.

---

## Connected to

- [[BDF_Canvas]]
- [[Tools_Registry]]
- [[LanceDB_Vector_Store]]
