---
tags: [nav, readalong]
updated: 2026-05-05
---

# Read-Along App Navigation

## Launch Sequence
```powershell
# T1 — Backend
cd C:\Users\titit\Projects\read-along-app\backend
.\venv\Scripts\Activate.ps1
uvicorn backend:app --reload

# T2 — Claude Code
cd C:\Users\titit\Projects\read-along-app
claude
```

## Key Paths
| Item | Path |
|---|---|
| Code | `C:\Users\titit\Projects\read-along-app\` |
| Backend | `backend\backend.py` |
| Backend venv | `backend\venv\` (large — PyTorch + Whisper + CUDA) |
| Generated audio | `generated_audio\` (gitignored) |
| TTS dependency | `C:\Dev\Projects\soccer-content-generator\tts_local.py` |
| Workspace | `read-along.code-workspace` |

## Audio Pipeline
```
upload → Whisper base model → word timestamps JSON → React word sync
text file → tts_local.py (Kokoro via BDF venv subprocess) → WAV → same pipeline
```

## Status
Backend functional · Frontend scaffolded · Word-sync highlighting pending
