---
tags: [project, shared-package, tts, normalization, live]
project: brain-audio
status: live
updated: 2026-05-09
parent: "[[Project_Directory]]"
---

# brain-audio — Shared TTS Text Normalizer

Shared Python package that strips Markdown syntax and expands domain-specific
abbreviations so raw text reads naturally when narrated by a TTS engine.
Installed editably into multiple project venvs — one source, all consumers
stay in sync automatically.

---

## What It Does

Takes raw text (Markdown, plain prose, mixed content) and applies an ordered
chain of regex substitutions defined in a JSON profile. Outputs a clean string
ready for Kokoro / Piper or any other TTS engine.

```python
from brain_audio import normalize

result = normalize("## Match Report\n**xG: 2.3**", profile="soccer")
# → "Section: Match Report\nExpected Goals: 2.3"
```

---

## Location

| Item | Path |
|---|---|
| Package root | `C:\Dev\shared\brain-audio\` |
| Core logic | `brain_audio/converter.py` |
| Profiles | `brain_audio/profiles/` |
| Developer docs | `CLAUDE.md` at package root |

---

## Profiles

| Profile | Purpose |
|---|---|
| `default` | Markdown cleanup (headings, bold, code fences, dividers) + common abbreviations (`e.g.`, `vs.`, `%`) |
| `soccer` | BDF football domain — xG, xA, UCL, EPL, match time formats |
| `construction` | ROI, dollar amounts, `x` multipliers, imperial units |

Profiles are plain JSON files — add a new one by dropping a `.json` file in
`brain_audio/profiles/`. No code changes required.

---

## Profile Rule Format

```json
{
  "replacements": [
    {"pattern": "\\bxG\\b", "replacement": "Expected Goals"},
    {"pattern": "^#{1,6}\\s+(.+)$", "replacement": "Section: \\1", "flags": ["MULTILINE"]}
  ]
}
```

Supported flags: `IGNORECASE` (default), `MULTILINE`, `DOTALL`. Rules apply in order.
Old flat-dict format still works for backward compat (always IGNORECASE).

---

## Dependent Projects

| Project | Profile used |
|---|---|
| [[soccer-content-generator]] | `soccer` |
| [[CA-book]] | `default` |
| [[read-along-app]] | `default` |

---

## Install

```powershell
# Run inside the target project venv
& "<venv>\Scripts\python.exe" -m pip install -e C:\Dev\shared\brain-audio
```

Editable install — changes to `converter.py` or any profile JSON are live
immediately across all venvs without reinstalling.

---

## Session Usage
- `graph_maintainer.py` checks brain_audio is importable at session start
- If missing from a venv: `pip install -e C:\Dev\shared\brain-audio`
- Version check: `from brain_audio import __version__`

---

## Connected to

- [[Project_Directory]]
- [[soccer-content-generator]]
- [[CA-book]]
- [[read-along-app]]
- [[Tools_Registry]]


<!-- auto-updated 2026-05-28 -->
**Last Updated:** 2026-05-28
- Steganographic fingerprint module live (local-SNR FFT detection)
- test_audio.wav artifact ignored in tracking
- Integrated into book-compiler TTS pipeline (auto-fingerprint + post-stitch verification)


<!-- auto-updated 2026-05-28 -->
- **2026-05-28**: Steganographic fingerprint module added (local-SNR FFT detection); auto-fingerprint on every TTS output; integrity check after master WAV stitch; test_audio.wav excluded from tracking
