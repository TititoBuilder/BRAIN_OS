# AGENT: BDF Memory Agent

## Project
BDF Soccer Bot / Resolve MCP Server

## Function
Ingest pipeline that reads new entries from `export_log.jsonl` since the last watermark, enriches each with TF-IDF knowledge facts + subject history + pattern signals, generates platform captions via Claude Haiku, writes a structured record to LanceDB `mcp_clips`, and copies verified MP4s to `C:\BDF_Share\`.

## Input
- `C:\BDF\renders\export_log.jsonl` — append-only JSONL; one entry per export run (clip_name, subject, competition, platforms, verified files, output_dir, timestamp)
- `mcp_ingest_state.json` — watermark file (last_processed_timestamp); stored next to mcp_ingest.py; never replaces full file on write (merge-update pattern)
- `--dry-run` flag — processes only the most recent entry, no writes

## Output
- LanceDB record at `C:\BDF\lancedb` table `mcp_clips` — fields: clip_name, subject, content_type, description, timestamp, platforms (JSON), agent_context, captions (JSON)
- Platform captions via Claude Haiku: YouTube `{title, description, hashtags}`, TikTok `<=150 chars`, Instagram `<=150 chars + emojis`, Twitter `<=270 chars`
- Updated `mcp_ingest_state.json` watermark after each successful batch

## Trigger
CLI: `venv/Scripts/python mcp_ingest.py` (process all new entries) or `venv/Scripts/python mcp_ingest.py --dry-run` (test on last entry). Also called as a subprocess by `export_pipeline.py` in the soccer-content-generator project.

## Tools and APIs
- [[Anthropic_Claude]] — `claude-haiku-4-5-20251001`; prompt caching enabled on system message (header: `anthropic-beta: prompt-caching-2024-07-31`); generates per-platform captions
- [[LanceDB]] — local at `C:\BDF\lancedb`; table `mcp_clips`; gracefully silent if not installed
- [[KnowledgeEnricher]] — TF-IDF cosine retrieval from soccer knowledge corpus; threshold 0.6801; query = `"{subject} {content_type} {competition}"` (competition field from log entry)
- [[SubjectMemory]] — `src/agent/memory.py`; reads export_log for subject history; case-insensitive match on first `_`-separated token
- [[PatternDetector]] — `src/agent/pattern_detector.py`; recency-weighted export frequency + saturation detection (threshold: count >= 5 per content_type)

## Canonical file
C:\Users\titit\Projects\resolve-mcp-server\mcp_ingest.py

## Connected to
- [[TagAndExport]] workflow — post_export_cleanup writes the log entry that this agent consumes
- [[BDF_Analysis_Agent]] — writes to the same LanceDB that RagPipeline reads from
- [[Resolve_MCP]] project + [[BDF_Soccer_Bot]] project

## Status
Live

## Pipeline steps per entry
1. Parse clip_name → subject, content_type, description
2. Map render preset names to social platform names (YouTube - 1080p → YouTube, etc.)
3. KnowledgeEnricher: TF-IDF retrieval, build agent_context string
4. SubjectMemory: last_session() → recent clip history for this subject
5. PatternDetector: export_frequency_by_subject() → saturation signals
6. generate_captions_direct(): Claude Haiku with knowledge context → per-platform JSON
7. _write_mcp_clip(): LanceDB upsert (silent no-op if LanceDB not installed)
8. _save_state(): merge-update watermark with new last_processed_timestamp
