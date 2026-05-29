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
## Read-Along App — Full Architecture
<!-- updated 2026-05-28: Full architecture docs created this session for Read-Along App -->
## Read-Along App — Full Architecture
- **Interface:** 4-tab unified interface
- **Tabs:** (to be detailed per implementation)
- **Audio agent:** RA_Whisper_Agent integration
- **Docs status:** Full architecture documented 2026-05-28
- **Session audio node:** read_along_app_session added to vault dropdown (2026-05-28)
- **Interface:** 4-tab unified interface
- **Tabs:** (1) Upload/Transcribe, (2) Read-Along Player, (3) Export, (4) Settings
- **Stack:** RA_Whisper_Agent for transcription, Kokoro TTS optional, OBS MCP for recording integration
- **Status:** Architecture fully documented this session
