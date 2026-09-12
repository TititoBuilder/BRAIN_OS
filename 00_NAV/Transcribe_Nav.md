---
tags: [nav, whisper, transcription]
updated: 2026-09-09
---

# One-Off Audio Transcription Navigation

Ad-hoc "transcribe this recording now" workflow. Not part of any repo, not part of the BDF pipeline. For the app-level Whisper service see [[RA_Whisper_Agent]]; for benchmark numbers see [[whisper_gpu_analysis]].

## Copy-Paste Fast Path

```powershell
# 1. Point at the canonical GPU venv (MUST be re-set in every new window)
$py = "C:\Dev\Projects\soccer-content-generator\venv\Scripts\python.exe"
& $py -c "import sys; print(sys.executable)"   # must echo the venv path back

# 2. Write the scratch script
New-Item -ItemType Directory -Path C:\Temp -Force | Out-Null
Set-Content -Path C:\Temp\transcribe.py -Encoding UTF8 -Value @'
import sys, time, whisper
from pathlib import Path
audio = Path(sys.argv[1])
model = whisper.load_model("large-v3", device="cuda")
t0 = time.perf_counter()
result = model.transcribe(str(audio), fp16=True, verbose=False)
lines = [f"[{s['start']:7.1f}s] {s['text'].strip()}" for s in result["segments"]]
out = audio.with_suffix(".transcript.txt")
out.write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines))
print(f"\nDone in {(time.perf_counter()-t0)/60:.1f} min -> {out}")
'@

# 3. Run
& $py C:\Temp\transcribe.py "<full path to audio>"
```

## What This Software Is

| | |
|---|---|
| **Package** | `openai-whisper` (NOT `faster-whisper` — that one is not installed) |
| **What it is** | OpenAI's speech-to-text model. Runs fully offline, local weights, no API calls, $0 per run |
| **What it does** | Audio in → timestamped text segments out. Auto-detects language |
| **Where it runs from** | `C:\Dev\Projects\soccer-content-generator\venv` — the canonical shared GPU venv |
| **Torch** | `2.12.0.dev20260324+cu128` (nightly — required for Blackwell sm_120) |
| **GPU** | RTX 5070 Ti Laptop, 12GB. `cuda avail: True` confirmed 2026-09-09 |
| **Model used** | `large-v3` — ~2.88GB weights, fits 12GB comfortably |
| **Weights cache** | `%USERPROFILE%\.cache\whisper` — downloads once, NOT into the venv |
| **Decoder dependency** | System `ffmpeg` at `%LOCALAPPDATA%\Microsoft\WinGet\Links\ffmpeg.exe` |
| **Measured speed** | 23,430 frames (~4 min audio) in 25–41s. See [[whisper_gpu_analysis]] for the 42x batch average |

## HARD RULE

The `soccer-content-generator` venv is **canonical shared GPU infrastructure**. Read-only.
Never relocate it, never `pip install` into it, never activate-and-forget. Call `python.exe` by
full path so no shell state changes and nothing can accidentally land inside it.

## Bumps Hit — And The Fix

**1. Placeholder run literally**
`$py = "<VENV_ROOT>\Scripts\python.exe"` → *"The module '<VENV_ROOT>' could not be loaded."*
PowerShell read the angle-bracket text as a command name. Substitute the real path before running.

**2. `$py` silently reverted to system Python** ← the expensive one
New PowerShell window = variables gone. `& $py` with `$py` empty falls through to PATH and hits
`C:\Users\titit\AppData\Local\Programs\Python\Python312\python.exe`, which has no torch and no
whisper. Symptom is a confusing unrelated error. **Always re-set `$py` and verify with
`sys.executable` first.**

**3. `C:\Temp` did not exist / downloaded script never landed**
Don't rely on moving a file in. Write the script inline with a here-string. `New-Item -Force`
creates the folder and stays silent if it already exists.

**4. `@'...'@` vs `@"..."@`**
Single-quoted here-string = literal, nothing expanded. Double-quoted = PowerShell expands `$vars`
inside first. **Writing source code to disk always wants the single-quoted form**, or `$` in the
code gets eaten. Closing delimiter must sit at column zero on its own line.

**5. `faster_whisper MISSING`**
Only `openai-whisper` is present. That backend shells out to system `ffmpeg` to decode `.m4a`.
Check with `Get-Command ffmpeg` before blaming the model. If missing: `winget install Gyan.FFmpeg`
then open a new shell — **never pip-install into the venv to work around it.**

**6. Forcing `language="en"` corrupted accented English**
On the 2026-09-09 dealer call, hardcoding `en` produced garbage across the CarFax and financing
section ("any call you, what it early want to do"). Removing the flag fixed the same audio on the
same model. **Constraining the decoder narrows its search — let it autodetect unless there is a
concrete reason not to.**

**7. First run looks frozen**
~2.88GB of weights download before anything prints. Normal. Cached afterward.

## Verify-Before-Running Snippet

```powershell
& $py -c @"
import torch
print('torch', torch.__version__, '| cuda avail:', torch.cuda.is_available())
print('device:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'NONE')
for m in ('faster_whisper','whisper'):
    try:
        __import__(m); print(m, 'OK')
    except ImportError:
        print(m, 'MISSING')
"@
```

## Output

Transcript lands as `<audio name>.transcript.txt` beside the source audio, and prints to console.

---
**→** [[SYSTEM_MASTER]] · [[whisper_gpu_analysis]] · [[RA_Whisper_Agent]] · [[systems_operations]]
