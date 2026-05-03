---
tags: [audio, tts, comparison, kokoro, edge-tts]
created: 2026-05-03
updated: 2026-05-03
parent: [[07_SYSTEM]]
---

# Audio Systems Comparison - Kokoro vs Edge TTS

Side-by-side comparison of the two audio generation systems in BRAIN_OS.

---

## Quick Comparison

| Property | Kokoro TTS | Edge TTS |
|---|---|---|
| **Cost** | FREE (local GPU) | FREE (Microsoft service) |
| **Automation** | HIGH — 1 command | LOW — 3 manual steps |
| **Format** | WAV | MP3 |
| **Voice** | af_heart (female, warm) | en-US-GuyNeural (male, American) |
| **Engine** | Local RTX 5070 Ti via CUDA | Microsoft cloud service |
| **Rate control** | Default | -5% (slower for comprehension) |
| **Use case** | Chapter audio (CA Book) | Learning guides |
| **Pipeline** | `ca-audio ch01` → WAV → Drive (auto) | Generate script → run → upload (manual) |
| **Integration** | BDF pipeline (`ca-book` command) | Standalone scripts |

---

## When to Use Which

### Use Kokoro when:
- Generating audio for CA Book chapters
- Batch processing multiple chapters
- Automated pipeline execution
- Repeatable, consistent output needed

### Use Edge TTS when:
- Creating one-off learning guides
- Need male voice / slower pacing
- MP3 format required
- Standalone script without BDF pipeline

---

## Cost Clarification (2026-05-03)

**Both systems are 100% FREE.**

Historical confusion: charges visible in cost logs ($0.37, $7.15, $8.56) came from
Claude Opus compiling book chapters — NOT from Kokoro or Edge TTS audio generation.

- Step 1: Claude Opus compiles chapter → **COSTS $0.15-0.30**
- Step 2: Kokoro/Edge TTS generates audio → **FREE**
- Step 3: Google Drive sync → **FREE**

---

## Decision Framework

```
Need audio for CA Book chapter?
  → YES → Kokoro (ca-audio)
  → NO
      Need learning guide / tutorial?
        → YES → Edge TTS
        → NO → Re-evaluate
```

---

## Connected to
- [[Edge_TTS_Learning_System]]
- [[Custom_Agent_TTS]]
