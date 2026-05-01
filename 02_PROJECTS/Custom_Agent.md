---
tags: [project, audio, tts, standalone, ca-book]
project: custom-agent
status: active
updated: 2026-05-01
parent: "[[Project_Directory]]"
---

# Custom Agent — CA Book Audio Synthesizer

Standalone chapter-by-chapter audio synthesizer for the CA Book project.
Lives at `C:\Dev\Projects\custom-agent`.
Serves the CA knowledge base at `C:\Knowledge\CA\` — has **no connection
to the BDF pipeline**.

---

## Purpose

Converts CA Book markdown chapters into clean spoken-word WAV files using
local TTS. Designed to make the CA Book listenable — one audio file per
chapter, processed on demand via CLI.

---

## ca_audio.py

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
python ca_audio.py ch01_origin
python ca_audio.py ch01_origin ch02_system ch03_next
```

Chapters are processed sequentially in argument order.

---

## Environment and Dependencies

**External API dependency:** Telegram only (alerts — no content dependency).

**Python dependencies:**
- `kokoro` — local TTS engine
- `numpy` — audio array concatenation
- `soundfile` — WAV file output
- `python-dotenv` — env var loading
- `requests` — Telegram HTTP calls

**Required env vars** (see `.env.template` in project root):

| Variable | Purpose |
|---|---|
| `TELEGRAM_BOT_TOKEN` | Boticris bot token |
| `TELEGRAM_CHAT_ID` | Target chat for alerts |

No Anthropic API key required. No OpenAI key. Fully local TTS.

---

## Telegram Alert Pattern

Follows the `sync_brain.py` standard exactly:

- **On start** — fires immediately when script is invoked
- **On clean finish** — fires after last WAV is written
- **On crash** — fires on any uncaught exception with truncated traceback

Added during standardization pass 2026-04-30.

---

## Standardization Status (2026-04-30)

| Item | Status |
|---|---|
| `CLAUDE.md` | ✅ Created (auto-generated from filesystem) |
| `.claude/settings.json` | ✅ Scoped to `C:\Dev\Projects\custom-agent\**` |
| `.gitignore` | ✅ Standard Python entries |
| `.env.template` | ✅ Created during cross-project sweep |
| Git repo | ✅ Initialized, branch `main`, commit `edc7d10` |
| GitHub remote | ✅ `https://github.com/TititoBuilder/custom-agent` (private) |
| Claude model audit | ✅ Zero `claude-opus` references found |
| Telegram alerts | ✅ Added to `ca_audio.py` |

---

## CA Book — Knowledge Base Context

The CA Book is a separate knowledge domain from BDF. It lives at
`C:\Knowledge\CA\` and is **not** managed by the soccer-content-generator
pipeline, the BDF queue, or any BDF script.

```
C:\Knowledge\CA\
  CA_Book\
    chapters\    ← markdown source files (input)
    audio\       ← synthesized WAV output
```

This project has no cross-dependency with any other project in the stack.
It is invoked manually when new chapters need audio output.

---

## Open Questions

- How many chapters currently exist in `chapters\`?
- Is the CA Book still being actively written, or is it in archive/playback phase?
- Is there a planned listener interface (app, player, read-along-app integration)?

---

## Connected to

- [[Project_Directory]]
- [[Tools_Registry]]
- [[Session_Protocol]]
