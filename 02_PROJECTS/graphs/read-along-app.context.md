# read-along-app — dependency context
_updated: 2026-05-12T14:35:55.417413+00:00_
_nodes: 1_

## API
- **backend/backend.py** (11.9 KB) — external: `fastapi`, `fastapi.middleware.cors`, `fastapi.responses`, `fastapi.staticfiles`, `whisper`


<!-- auto-updated 2026-05-28 -->
**Last Sync:** 2026-05-28
- Full architecture documented: 4-tab unified interface
- See 02_PROJECTS/Read_Along_App.md for full spec


<!-- auto-updated 2026-05-28 -->
## Read-Along App — Full Architecture (2026-05-28)
- **Interface:** 4-tab unified interface
- **Tabs:** (1) Upload/Transcribe, (2) Read-Along Player, (3) Export, (4) Settings
- **Stack:** RA_Whisper_Agent for transcription, Kokoro TTS optional, OBS MCP for recording integration
- **Status:** Architecture fully documented this session
