---
tags: [agent, orchestrator, bdf, live]
---
# AGENT: Data orchestrator

## Role
Controls all knowledge ingestion and vector store maintenance.
Owns LanceDB integrity and book compilation pipeline.

## Controls
- [[BDF_Memory_Agent]]
- [[BDF_Analysis_Agent]]

## Flow
Source data → book_compiler → Claude Opus → Kokoro TTS → Google Drive
AND: export_log → mcp_ingest → LanceDB embed → index update

## Critical rules
ONE file per book_compiler run — never batch (cost $1.50-2.50 per run)
LANCE_DB_PATH must be set before any lancedb.connect() call

## Connected to
[[BDF_Knowledge_Build_Flow]]
[[LanceDB_Vector_Store]]
[[BDF_Book_System]]
[[CA_Knowledge_Book]]
[[GoogleDrive_API]]
