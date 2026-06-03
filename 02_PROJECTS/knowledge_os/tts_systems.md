---
knowledge_os_machine_key: tts_systems
knowledge_os_domain: Audio & Media
knowledge_os_status: Mastered
knowledge_os_score: 88
knowledge_os_priority: High
knowledge_os_evidence: Kokoro af_heart + Edge TTS en-US-GuyNeural operational
knowledge_os_last_touched: '2026-05-24'
---
# TTS Systems

## What It Is
TTS stands for Text-to-Speech. On this system it means two distinct engines that
turn written chapter text into narrated audio: Kokoro, which runs locally on the
GPU, and Edge TTS, which calls a free Microsoft cloud service. They serve
different purposes and are not interchangeable.

## How It Works
Kokoro runs on the RTX 5070 Ti via CUDA with the nightly cu128 PyTorch build.
It uses the voice af_heart, a warm female voice, and outputs WAV files. The
alias ca-audio triggers the full pipeline in one command with no manual steps.
Edge TTS uses Microsoft's en-US-GuyNeural voice, a natural-sounding American
male, at minus five percent speed for better comprehension. It outputs MP3 and
takes three manual steps: generate the script, run the command, upload the file.
After Kokoro generates a chapter, anchor_generator.py appends a closing segment
in the voice am_adam, a deeper male voice for contrast. chapter_combiner.py then
concatenates the two files via ffmpeg into a single MP3, which syncs
automatically to Google Drive.

## Why It Matters
Both engines are completely free. The costs that appeared in API logs — charges
of thirty-seven cents up to eight dollars — came from Claude Opus compiling the
chapter text, not from any TTS engine. This distinction matters for budget
tracking: the expensive step is text generation, not audio synthesis. Kokoro
produces audio on local hardware, so it scales to zero marginal cost per chapter
after the GPU run.

## The Pattern
Use Kokoro for anything that runs in a pipeline. Use Edge TTS for one-off
learning guides where a male voice or MP3 format is specifically needed. Never
batch-process Kokoro without checking for existing audio first — regenerating
files that already exist wastes GPU time and risks overwriting good output.

