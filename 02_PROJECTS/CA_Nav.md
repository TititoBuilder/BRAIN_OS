---
tags: [nav, ca, custom-agent]
updated: 2026-05-05
---

# Custom Agent Navigation

## Two Separate Projects — Do Not Confuse
| Name | Path | Purpose |
|---|---|---|
| CA TTS (ca_audio.py) | `C:\Dev\Projects\custom-agent\` | Converts CA Book chapters to WAV |
| CA Business OS | `C:\Dev\CristianConstruction\` | 9-agent FastAPI system |

## CA Audio Launch
```powershell
ca-audio          # alias: activates CA venv + runs ca_audio.py
# OR manually:
cd C:\Dev\Projects\custom-agent
.\venv\Scripts\Activate.ps1
python ca_audio.py
```

## CA Book Aliases
```powershell
ca-log "file.txt"      # Downloads → C:\Knowledge\CA\Session_Resumes\processed\
ca-compile "file.txt"  # Downloads → C:\Knowledge\CA\CA_Book\incoming\
ca-book                # activates C:\Knowledge\CA\venv → runs CA book_compiler.py
```

## Key Paths
| Item | Path |
|---|---|
| ca_audio.py | `C:\Dev\Projects\custom-agent\ca_audio.py` |
| CA venv (audio) | `C:\Dev\Projects\custom-agent\venv\` |
| CA Book compiler | `C:\Knowledge\CA\CA_Book\book_compiler.py` |
| CA Book venv | `C:\Knowledge\CA\venv\` (anthropic + python-dotenv) |
| CA chapters | `C:\Knowledge\CA\CA_Book\chapters\` (.md × 10) |
| Session resumes | `C:\Knowledge\CA\Session_Resumes\` |

## TTS Notes
- Engine: Kokoro local (RTX 5070 Ti / CUDA)
- Voice: af_heart (American English, warm female)
- Zero API cost — fully local
- 3 manual patches required in coqui-tts for Blackwell GPU compatibility
