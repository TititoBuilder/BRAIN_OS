---
tags: [system, infra, live]
---
# Active environments

## BDF Soccer Bot
- Path: C:\Dev\Projects\soccer-content-generator\
- Venv: C:\Dev\Projects\soccer-content-generator\venv\
- Activate: venv\Scripts\Activate.ps1
- Python: 3.12
- Key packages: lancedb, sentence-transformers, tweepy, 
  anthropic, python-telegram-bot, kokoro, torch (CUDA 12.8)
- .env location: project root
- LANCE_DB_PATH: C:/Dev/Projects/soccer-content-generator/lance_db_soccer
- Launch: python bot_service.py (T1)

## Custom Agent (CA)
- Path: C:\Dev\CristianConstruction\
- Python: 3.12.10
- TTS: PyTorch 2.11+cu128, Kokoro, patched coqui-tts 0.27.5
- Dashboard: localhost:3000
- API: localhost:8000
- Aliases: ca-book, ca-compile, ca-audio

## Read-Along App
- Path: C:\Users\titit\Projects\read-along-app\
- Venv: backend venv
- Backend: FastAPI + Whisper + PyTorch CUDA
- Frontend: NOT YET BUILT (Vite scaffold pending)
- Local git only — no GitHub remote

## Resolve MCP Server
- Path: C:\Users\titit\Projects\resolve-mcp-server\
- Venv: active (seen in terminal)
- Transport: TCP PORT=9000
- AdditionalDirectories: soccer-content-generator/src

## BRAIN_OS
- Path: C:\BRAIN_OS\
- No venv — markdown only
- GitHub: TititoBuilder/BRAIN_OS

## Shared
- CUDA: 12.8 on RTX 5070 Ti
- All heavy ML runs on Predator GPU
- Never run large models on CPU
