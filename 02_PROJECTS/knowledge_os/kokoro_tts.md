---
knowledge_os_machine_key: kokoro_tts
knowledge_os_domain: Audio & Media
knowledge_os_status: Mastered
knowledge_os_score: 88
knowledge_os_priority: High
knowledge_os_evidence: ca-audio one-command pipeline operational; af_heart + am_adam anchor segments on RTX 5070 Ti
knowledge_os_last_touched: '2026-06-11'
---
# Kokoro TTS
## What It Is
Kokoro is the local, GPU-based text-to-speech engine, the pipeline workhorse of
the audio system. Unlike Edge TTS, which calls a cloud service for one-off
guides, Kokoro runs entirely on local hardware and is built for repeated,
automated chapter generation. It is the engine behind the book audio: feed it
chapter text and it returns narrated audio with no manual steps.
## How It Works
Kokoro runs on the RTX 5070 Ti through CUDA, using the nightly cu128 PyTorch
build. Its main voice is af_heart, a warm female voice, and it outputs WAV, a
lossless format. The whole pipeline fires from a single alias, ca-audio, with no
hand steps in between. After Kokoro narrates a chapter, anchor_generator.py
appends a closing segment in the voice am_adam, a deeper male voice that contrasts
with the main narration. chapter_combiner.py then concatenates the two pieces
with ffmpeg into one MP3, which syncs automatically to Google Drive. The result
is a complete, anchored chapter produced from one command.
## Why It Matters
Kokoro costs nothing to run per chapter. Because synthesis happens on local
hardware, the marginal cost of each additional chapter after the GPU run is
effectively zero. This is the key budget insight: when API logs showed charges,
those came from Claude Opus compiling the chapter text, not from Kokoro
synthesizing audio. The expensive step is text generation, never the audio
engine. That separation is what makes high-volume chapter production affordable.
## The Pattern
Use Kokoro for anything that runs in a pipeline, which is most book and chapter
audio. Reserve Edge TTS for one-off learning guides where a male voice or MP3 is
specifically needed. The one firm rule: never batch-process Kokoro without first
checking for existing audio, because regenerating files that already exist wastes
GPU time and risks overwriting good output. See [[tts_systems]] for the
side-by-side comparison and [[edge_tts]] for the one-off engine.
