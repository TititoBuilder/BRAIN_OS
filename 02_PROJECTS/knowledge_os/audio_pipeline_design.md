---
knowledge_os_machine_key: audio_pipeline_design
knowledge_os_domain: Audio & Media
knowledge_os_status: Practiced
knowledge_os_score: 72
knowledge_os_priority: High
knowledge_os_evidence: book_compiler.py â†’ ca_audio.py â†’ Drive
knowledge_os_last_touched: '2026-05-08'
---
# Audio Pipeline Design

## What It Is
The audio pipeline is the signature architecture of this system: a closed loop
that turns written knowledge into narrated audio and feeds listening progress
back into the knowledge base. It connects four stores — the Obsidian vault,
local GPU synthesis, Google Drive, and the Read-Along app — into one cycle:
build, listen, update score, repeat.

## How It Works
The flow runs in stages. Source text begins as markdown in the vault. Kokoro
TTS, running locally on the RTX 5070 Ti, synthesizes that text into audio using
the af_heart voice. anchor_generator.py appends a closing learning segment, and
audio_stitcher.py combines the pieces into a single session file via ffmpeg.
The stitched audio uploads to Google Drive, which is the canonical home for all
audio — binaries never go into Git. Separately, Whisper runs locally on the GPU
at roughly forty-two times real time, transcribing each audio file into a JSON
manifest with word-level timestamps. Those manifests are committed to the
Read-Along app's repository. The deployed app streams audio from Drive and reads
the timestamp manifests from the repo, enabling karaoke-style highlighting as
each word is spoken.

## Why It Matters
The design follows the federated hybrid model: the local machine is the heavy
compute compiler, the cloud server is a lightweight coordinator. Synthesis and
transcription happen locally at zero marginal cost and zero latency, while the
deployed app only ever streams finished audio and reads small JSON files. There
is no reason to run TTS or Whisper in the cloud. The loop closes because
listening progress and review scores flow back through obsidian_sync.py into
the vault, so what gets studied informs what gets built next.

## The Pattern
Master locally, deliver remotely. Generate and stitch in high quality on the
GPU, transcribe locally, then hand off only finished MP3s to Drive and small
manifests to the app. Heavy compute stays on the machine that owns the hardware;
the cloud only coordinates.
