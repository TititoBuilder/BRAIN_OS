# Steganographic Audio Fingerprinting

**Status:** Complete  
**Commit:** `48e9684`  
**Module:** `C:\Dev\shared\brain-audio\brain_audio\fingerprint.py`

---

## What It Does
Embeds an inaudible 18,500 Hz sine wave into any WAV file at generation 
time. A local-SNR FFT detector can verify the file originated from the 
brain-audio pipeline — surviving re-saves and format conversion.

---

## Architecture

### Embed
1. Load WAV → numpy array (time domain)
2. Build time axis: `t = linspace(0, duration, num_samples)`
3. Generate tone: `A * sin(2π * f * t)` where f=18500, A=0.0008
4. Superposition: `audio + tone`
5. Clamp to `[-1.0, 1.0]` → write back

### Detect
1. Load WAV → numpy array
2. FFT → frequency domain (`np.fft.rfft`)
3. Find target bin closest to 18,500 Hz
4. Slice 10 neighbor bins each side (skip ±1 guard band → spectral leakage)
5. `noise_floor = mean(neighbors)`
6. `snr_ratio = signal_strength / noise_floor`
7. `detected = snr_ratio > 3.0`

---

## Key Constants
| Constant | Value | Reason |
|---|---|---|
| `FINGERPRINT_HZ` | 18,500 | Inaudible to most adults |
| `FINGERPRINT_AMPLITUDE` | 0.0008 | ~0.08% of max signal |
| `SNR_THRESHOLD` | 3.0 | Eliminates false positives |
| `GUARD_BAND` | ±1 bin | Avoids spectral leakage shoulders |
| `NEIGHBOR_WINDOW` | 10 bins each side | Stable local noise floor estimate |

---

## Test Results

<!-- auto-updated 2026-05-28 -->
## Steganographic Fingerprint Module
- **Method:** Local-SNR FFT detection
- **Status:** Implemented 2026-05-28
- **Integration:** Auto-fingerprints every TTS output via brain-audio
- **Verification:** Fingerprint integrity checked after master WAV stitch in book-compiler
- **Artifact:** test_audio.wav excluded via .gitignore


<!-- auto-ingested 2026-05-28 -->
## Steganographic Fingerprint Module — 2026-05-28
- Implemented steganographic fingerprint embedding using **local-SNR FFT detection**
- Module integrated into brain-audio package
- `test_audio.wav` artifact added to .gitignore
- Auto-fingerprinting wired into every TTS output via book-compiler pipeline
- Fingerprint integrity verified after master WAV stitch step


<!-- auto-updated 2026-05-28 -->
## Fingerprinting Integration — 2026-05-28
- **feat:** Verify fingerprint integrity after master WAV stitch
- **feat:** Auto-fingerprint every TTS output via brain-audio module
- Both features merged into book-compiler this session
- Fingerprint check runs post-stitch to catch corruption before delivery


<!-- auto-updated 2026-05-28 -->
## Integration Status — Updated 2026-05-28
- book-compiler now verifies fingerprint integrity after master WAV stitch
- Auto-fingerprint applied to every TTS output via brain-audio module
- Ingested from 2026-05-25 session; confirmed active as of 2026-05-28
