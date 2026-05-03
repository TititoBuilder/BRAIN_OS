---
tags: [project, audio, tts, standalone, ca-book, kokoro]
project: custom-agent
status: active
updated: 2026-05-02
parent: "[[Project_Directory]]"
---

# Custom Agent TTS — CA Book Audio Synthesizer

> ⚠️ **DISAMBIGUATION — TWO PROJECTS SHARE "CUSTOM AGENT"**
>
> This note covers the **TTS audio synthesizer** at `C:\Dev\Projects\custom-agent\`.
> The **9-agent FastAPI business OS** lives at `C:\Dev\CristianConstruction\`.
> See [[CristianConstruction]] for that project.

Standalone chapter-by-chapter audio synthesizer for the CA Book knowledge base. Converts Markdown chapters into WAV files using local Kokoro TTS — no cloud API calls, no Anthropic key, no OpenAI.

Root: `C:\Dev\Projects\custom-agent\`
GitHub: `TititoBuilder/custom-agent` (private)

---

## Business Value

Makes the CA knowledge base (`C:\Knowledge\CA\`) listenable. One WAV per chapter, synthesized on demand via CLI or the `ca-audio` PowerShell alias. All 10 CA Book chapters have corresponding audio as of 2026-04-15.

---

## Architecture

```
CLI args (chapter keys)
  → read markdown from C:\Knowledge\CA\CA_Book\chapters\
  → strip_markdown()        ← strips all MD formatting
  → Kokoro TTS synthesis    ← local model, af_heart voice
  → numpy array concat
  → soundfile WAV write     → C:\Knowledge\CA\CA_Book\audio\
  → Telegram alert (start / finish / crash)
```

---

## Key File: ca_audio.py

**The only active Python file in the project.**

| Property | Value |
|---|---|
| Input | `C:\Knowledge\CA\CA_Book\chapters\` (`.md` files) |
| Output | `C:\Knowledge\CA\CA_Book\audio\` (`.wav` files) |
| TTS engine | Kokoro (local — not OpenAI or ElevenLabs) |
| Voice | `af_heart` — American English, warm female |
| Sample rate | 24000 Hz |
| Audio format | WAV via `soundfile` |

---

## CLI Usage

```powershell
# Standard — via PowerShell alias
ca-audio ch01_origin

# Direct
cd C:\Dev\Projects\custom-agent
& .\venv\Scripts\Activate.ps1
python ca_audio.py ch01_origin

# Multiple chapters
python ca_audio.py ch01_origin ch02_system ch03_next
```

Use `ca-audio` only when manually regenerating stale audio outside a normal `ca-book` run. The standard `ca-book` pipeline calls the compiler and syncs audio to Drive automatically.

**TTS launch rule:** Always open a **fresh terminal** before TTS work. The BDF venv auto-activates at shell startup — deactivate it first if already active.

---

## Stack

| Package | Version |
|---|---|
| `kokoro` | `0.9.4` |
| `numpy` | audio array concatenation |
| `soundfile` | WAV file output |
| `python-dotenv` | env var loading |
| `requests` | Telegram HTTP |
| PyTorch | `2.11.0+cu128` (sm_120 Blackwell required) |
| coqui-tts | `0.27.5` (patched — see below) |

**Venv:** `C:\Dev\Projects\custom-agent\venv\` — TTS-only, not shared with any other project.

---

## TTS Venv — Fragile, 3 Manual Patches Required

The RTX 5070 Ti (sm_120 Blackwell architecture) requires specific PyTorch builds and 3 source-level patches to coqui-tts. **If the venv is ever rebuilt, these patches must be reapplied or TTS will not run.**

Full patch notes: `C:\Dev\Projects\custom-agent\TTS_PATCH_NOTES.md`

### Patch 1 — `TTS\tts\layers\tortoise\autoregressive.py`
Remove:
```python
from transformers.pytorch_utils import isin_mps_friendly as isin
```
Add local def:
```python
def isin(elements, test_elements):
    return torch.isin(elements, test_elements)
```

### Patch 2 — `TTS\__init__.py`
Remove:
```python
from transformers.utils.import_utils import (
    is_torch_greater_or_equal, is_torchcodec_available)
```
Add local defs using `packaging.version` and `importlib.util`.

### Patch 3 — `TTS\tts\layers\tortoise\autoregressive.py` (same file as Patch 1)
Correct parameter name from `element` → `elements` to match keyword argument in caller.

---

## Cost (Corrected 2026-05-03)
Kokoro TTS is 100% FREE - runs locally on RTX 5070 Ti via CUDA with zero API costs.

**Cost Confusion Clarified:**
The charges visible in cost logs ($0.37, $7.15, $8.56) were from Claude Opus
compilation of book chapters, NOT from Kokoro audio generation. The confusion
arose because both operations run in the same `bdf-book` command:
- Step 1: Claude Opus compiles chapter (COSTS $0.15-0.30)
- Step 2: Kokoro generates audio (FREE)
- Step 3: Google Drive sync (FREE)

Kokoro is invisible in cost logs because it costs nothing.

**Previous note:** Previously documented as having costs, corrected May 3, 2026
after full timeline analysis from March 25 creation to present.

---

## Environment Variables

```
TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID
```

No `ANTHROPIC_API_KEY`. Fully local TTS — no cloud inference.

---

## CA Book Structure

```
C:\Knowledge\CA\
  CA_Book\
    chapters\    ← 10 .md source files (all compiled as of 2026-04-15)
    audio\       ← 10 .wav output files (all generated)
    incoming\    ← drop new content, run ca-book
    _processed\
    _review\
    _rejected\
    CA_Master_Book.txt   ← stitched full book (119 KB)
    cost_log.txt
    book_compiler.py     ← CA compiler (lives here, not in code root)
```

---

## Open Items

- `ca_audio.py` line 4: `SyntaxWarning: invalid escape sequence '\K'` — fix: add `r` prefix to raw-string path in docstring. Low priority (warning only, does not break execution).

---

## Standardization Status (2026-04-30)

| Item | Status |
|---|---|
| `CLAUDE.md` | ✅ Created |
| `.claude/settings.json` | ✅ Scoped to `C:\Dev\Projects\custom-agent\**` |
| `.gitignore` | ✅ Standard Python entries |
| `.env.template` | ✅ Created |
| Git + GitHub | ✅ `TititoBuilder/custom-agent` (private), initial commit `edc7d10` |
| Telegram alerts | ✅ Added to `ca_audio.py` |
| Model audit | ✅ Zero `claude-opus` references |

---

## Connected to

- [[CristianConstruction]]
- [[Read_Along_App]]
- [[BDF_Canvas]]
- [[Project_Directory]]
- [[Tools_Registry]]
