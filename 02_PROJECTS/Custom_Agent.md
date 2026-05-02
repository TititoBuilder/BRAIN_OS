---
tags: [project, audio, tts, standalone, ca-book]
project: custom-agent
status: active
updated: 2026-05-01
parent: "[[Project_Directory]]"
---

# Custom Agent — CA Book Audio Synthesizer

> ⚠️ **DISAMBIGUATION — TWO PROJECTS SHARE THE NAME "CUSTOM AGENT"**
>
> This node documents the **TTS companion** at `C:\Dev\Projects\custom-agent\`.
> It synthesizes audio for the CA Book and has no business logic.
>
> The **Custom Agent business OS** — 9-agent FastAPI app for Custom Agent
> Remodel & Skilltrade — lives at `C:\Dev\CristianConstruction\`.
> See [[CristianConstruction]] for that project.

Standalone chapter-by-chapter audio synthesizer for the CA Book project.
Serves the CA knowledge base at `C:\Knowledge\CA\` — **no connection
to the BDF pipeline and no connection to read-along-app**.

---

## Purpose

Converts CA Book markdown chapters into clean spoken-word WAV files using
local TTS. Designed to make the CA Book listenable — one audio file per
chapter, processed on demand via CLI or via the `ca-audio` PowerShell alias.

---

## ca_[audio.py](http://audio.py)

**The only active Python file in the project.**

| Property | Value |
|---|---|
| Input | `C:\Knowledge\CA\CA_Book\chapters\` (markdown files) |
| Output | `C:\Knowledge\CA\CA_Book\audio\` (WAV files) |
| TTS engine | Kokoro (local, not OpenAI or ElevenLabs) |
| Voice | `af_heart` — American English, warm female |
| Sample rate | 24000 Hz |
| Audio format | WAV via `soundfile` |
| Array handling | `numpy` for chunk concatenation |

**Processing pipeline:**

```
CLI args (chapter keys)
  → read markdown from chapters/
  → strip_markdown()        ← custom function, removes all MD formatting
  → Kokoro TTS synthesis    ← local model, af_heart voice
  → numpy array concat
  → soundfile WAV write     → audio/
  → Telegram alert (start / finish / crash)
```

**CLI usage:**

```powershell
python ca_[audio.py](http://audio.py) ch01_origin
python ca_[audio.py](http://audio.py) ch01_origin ch02_system ch03_next
```

Preferred invocation via alias:

```powershell
ca-audio ch01_origin
```

Use `ca-audio` only when manually regenerating stale audio outside a
normal `ca-book` run. Standard pipeline uses `ca-book` which calls the
compiler and syncs to Drive automatically.

---

## CA Book — Knowledge Base Context

```
C:\Knowledge\CA\
  CA_Book\
    chapters\    ← 10 .md source files (all compiled as of 4/15/2026)
    audio\       ← 10 .wav output files (all generated)
    incoming\    ← drop new content, run ca-book
    _processed\, _review\, _rejected\
    CA_Master_Book.txt   ← stitched full book (119KB)
    cost_log.txt
    book_[compiler.py](http://compiler.py)     ← CA compiler (lives here, NOT in code root)
```

CA Book chapter state (as of 2026-04-15): all 10 chapters healthy.

---

## Environment and Dependencies

**External API dependency:** Telegram only.

**Python dependencies:**
- `kokoro` — local TTS engine
- `numpy` — audio array concatenation
- `soundfile` — WAV file output
- `python-dotenv` — env var loading
- `requests` — Telegram HTTP calls

**Venv:** `C:\Dev\Projects\custom-agent\venv\` — TTS-only, patched coqui-tts.
Not shared with any other project.

**Required env vars** (see `.env.template`):

| Variable | Purpose |
|---|---|
| `TELEGRAM_BOT_TOKEN` | Boticris bot token |
| `TELEGRAM_CHAT_ID` | Target chat for alerts |

No Anthropic API key. No OpenAI key. Fully local TTS.

---

## Telegram Alert Pattern

Fires on: script start · clean finish · uncaught exception (truncated traceback).
Added during standardization pass 2026-04-30. Pattern sourced from `sync_[brain.py](http://brain.py)`.

---

## Standardization Status (2026-04-30)

| Item | Status |
|---|---|
| `[CLAUDE.md](http://CLAUDE.md)` | ✅ Created |
| `.claude/settings.json` | ✅ Scoped to `C:\Dev\Projects\custom-agent\**` |
| `.gitignore` | ✅ Standard Python entries |
| `.env.template` | ✅ Created |
| Git + GitHub | ✅ `TititoBuilder/custom-agent` (private), commit `edc7d10` |
| Model audit | ✅ Zero `claude-opus` references |
| Telegram alerts | ✅ Added to `ca_[audio.py](http://audio.py)` |

---

## TTS Environment — Fragile, Document Carefully

The TTS venv at `C:\Dev\Projects\custom-agent\venv\` requires specific versions
and **3 manual source patches** to coqui-tts. If the venv is ever rebuilt,
these patches must be reapplied or TTS will not run on the RTX 5070 Ti (sm_120 Blackwell).

**Required versions:**

| Package | Version |
|---|---|
| PyTorch | `2.11.0+cu128` (required for sm_120 Blackwell) |
| coqui-tts | `0.27.5` (patched — see below) |
| Kokoro | `0.9.4` |

**Patch 1 — `TTS\tts\layers\tortoise\autoregressive.py`**

Remove:
```python
from transformers.pytorch_utils import isin_mps_friendly as isin
```
Add local def:
```python
def isin(elements, test_elements):
    return torch.isin(elements, test_elements)
```

**Patch 2 — `TTS\__init__.py`**

Remove:
```python
from transformers.utils.import_utils import (
    is_torch_greater_or_equal, is_torchcodec_available)
```
Add local defs using `packaging.version` and `importlib.util`.

**Patch 3 — `TTS\tts\layers\tortoise\autoregressive.py`** (same file as Patch 1)

Correct parameter name from `element` → `elements` to match keyword argument in caller.

**TTS launch rule:** Always open a **fresh terminal** before TTS work.
The BDF venv auto-activates at startup — if it's already active, deactivate first.

```powershell
& "C:\Dev\Projects\custom-agent\venv\Scripts\Activate.ps1"
cd C:\Dev\Projects\custom-agent
python ca_audio.py ch01_origin
```

Patch documentation also lives in: `C:\Dev\Projects\custom-agent\TTS_PATCH_NOTES.md`

> ⚠️ **read-along-app connection: DENIED.** read-along-app is a standalone
> Whisper transcription tool with no dependency on CA Book WAV files.

---

## Open Items (updated)

- `ca_audio.py` line 4: `SyntaxWarning: invalid escape sequence '\K'`
  - Cause: raw string `r"C:\Knowledge\..."` missing the `r` prefix in docstring/comment
  - Fix: one-line change in VS Code — add `r` prefix or double the backslash
  - Priority: low (warning only, does not break execution)

---

## Connected to

- [[CristianConstruction]]
- [[Project_Directory]]
- [[Tools_Registry]]
- [[Session_Protocol]]
