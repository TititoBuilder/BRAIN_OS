---
knowledge_os_machine_key: audio_formats
knowledge_os_domain: Creative Systems
---
# Audio Formats

## What It Is
An audio format is how sound gets stored as a file. The two that matter for
most work are WAV and MP3. WAV is uncompressed: every sample is stored exactly,
giving perfect quality and large files. MP3 is compressed: it throws away data
the human ear barely notices, giving much smaller files at a small quality
cost.

## How It Works
Sound is captured by sampling: measuring the wave thousands of times per second.
The sample rate is how often, commonly 44,100 times per second, which by the
Nyquist rule captures every frequency a human can hear. WAV keeps all those
samples. MP3 runs them through a compression model that drops inaudible detail,
shrinking the file roughly ten to one.

## Why It Matters
The choice is a tradeoff between quality and size, and it depends on the stage.
Master and edit in WAV so no quality is lost while you work. Distribute in MP3
so files are small enough to stream and store cheaply. Your audio pipeline
follows exactly this: generate and stitch in high quality, then deliver as MP3
to the app and to Google Drive.

## The Pattern
Lossless for working, lossy for delivery. Keep the perfect copy upstream;
compress only at the final hand-off.
