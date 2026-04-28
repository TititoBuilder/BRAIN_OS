---
tags: [agent, live]
---

# AGENT: CA Kokoro TTS

## Project
Custom Agent (CristianConstruction)

## Function
Offline text-to-speech synthesizer that reads CA Book chapter markdown files, strips all formatting, generates natural-sounding WAV audio using the Kokoro `af_heart` voice (American English, warm female), and saves the result to the audio library.

## Input
- Chapter markdown files at `C:\Knowledge\CA\CA_Book\chapters\chXX_name.md`
- One or more chapter keys passed as CLI positional arguments (e.g. `ch01_origin ch02_system`)

## Output
- WAV audio files at `C:\Knowledge\CA\CA_Book\audio\chXX_name.wav`
- Sample rate: 24000 Hz
- Console: word count, estimated duration (~130 words/min), actual duration after synthesis

## Trigger
Manual CLI: `python ca_audio.py ch01_origin [ch02_system ...]`; no background service, no scheduled task — runs on demand per chapter.

## Tools and APIs
- [[Kokoro_TTS]] — local `KPipeline(lang_code="a")`, voice `af_heart`; yields audio chunks in segments; no API cost, fully offline
- `numpy` — concatenates audio chunks into single array before write
- `soundfile` — writes final WAV to disk

## Canonical file
C:\Dev\Projects\custom-agent\ca_audio.py

## Connected to
- [[CABookAudio]] workflow — manual step in book production pipeline
- [[Custom_Agent]] project

## Status
Live

## Markdown stripping
Removes: code fences, inline code, headers, bold/italic, horizontal rules, links (keeps label), image tags, HTML tags. Collapses 3+ blank lines into single paragraph break. This ensures Kokoro reads clean prose without speaking markdown syntax.
