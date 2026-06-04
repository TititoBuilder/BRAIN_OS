#!/usr/bin/env python3
"""
audio_stitcher.py — Knowledge OS Phase 2
=========================================
Reads audio_manifest.json exported from the Knowledge OS app.
Generates TTS transition narrations (Edge TTS, en-US-GuyNeural).
Stitches all tracks into one continuous MP3 session.

Location : C:\\BRAIN_OS\\09_TOOLS\\audio_stitcher.py
Venv     : C:\\Knowledge\\CA\\venv\\Scripts\\python.exe

Install deps (once):
    C:\\Knowledge\\CA\\venv\\Scripts\\pip install pydub edge-tts
    winget install Gyan.FFmpeg          # required by pydub

Usage:
    python audio_stitcher.py ^
        --manifest "C:\\path\\to\\audio_manifest.json" ^
        --audio-dir "C:\\path\\to\\wav_files" ^
        --output "C:\\BRAIN_OS\\audio_out\\session.mp3"

File naming: each audio file must be named by machine_key.
    e.g.  prompt_engineering.wav  /  rag_pipelines.mp3
    The manifest's `file_hint` field shows the expected Drive path per track.

Flags:
    --manifest    Path to audio_manifest.json  (required)
    --audio-dir   Directory of .wav/.mp3 files (required)
    --output      Output MP3 path              (default: stitched_session.mp3)
    --gap         Silence gap ms between tracks (default: 1500)
    --no-tts      Skip TTS -- use silence only  (default: off)
    --bitrate     MP3 bitrate                  (default: 192k)
    --voice       Edge TTS voice               (default: en-US-GuyNeural)
    --dry-run     Print plan only, no output
"""

import argparse
import asyncio
import json
import sys
import tempfile
from pathlib import Path


# --- Dependency checks --------------------------------------------------------

def _require(pkg, pip_name=None):
    import importlib
    try:
        return importlib.import_module(pkg)
    except ImportError:
        name = pip_name or pkg
        print(f"ERROR: '{name}' not installed.\n"
              f"  Run: C:\\Knowledge\\CA\\venv\\Scripts\\pip install {name}")
        sys.exit(1)


# --- TTS ----------------------------------------------------------------------

async def _tts_to_file(text: str, path: str, voice: str) -> bool:
    """Generate TTS and save to path. Returns True on success."""
    edge_tts = _require("edge_tts", "edge-tts")
    try:
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(path)
        return True
    except Exception as e:
        print(f"    TTS error: {e}")
        return False


# Kokoro voices are generated via gen_tts_staging.py (same pipeline as topics)
GEN_TTS = Path(r"C:\Users\titit\Projects\read-along-app\backend\gen_tts_staging.py")
GEN_TTS_PYTHON = Path(r"C:\Dev\Projects\soccer-content-generator\venv\Scripts\python.exe")

def _kokoro_to_file(text: str, path: str) -> bool:
    """Generate af_heart (Kokoro) audio via gen_tts_staging.py."""
    import subprocess, tempfile, os
    tmp_md = Path(tempfile.gettempdir()) / f"_trans_{os.getpid()}_{abs(hash(text))%99999}.md"
    tmp_md.write_text(text + "\n", encoding="utf-8")
    try:
        r = subprocess.run([str(GEN_TTS_PYTHON), str(GEN_TTS), str(tmp_md), str(path)],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        return r.returncode == 0 and Path(path).exists()
    finally:
        tmp_md.unlink(missing_ok=True)

def generate_tts(text: str, path: str, voice: str) -> bool:
    # Kokoro voice names start with af_ / am_; route those to the topic pipeline
    if voice.startswith("af_") or voice.startswith("am_"):
        return _kokoro_to_file(text, path)
    return asyncio.run(_tts_to_file(text, path, voice))


# --- Audio helpers ------------------------------------------------------------

EXTENSIONS = [".wav", ".mp3", ".m4a", ".ogg"]


def find_audio(machine_key: str, audio_dir: Path):
    """Return AudioSegment if a file named machine_key exists, else None."""
    AudioSegment = _require("pydub").AudioSegment
    for ext in EXTENSIONS:
        p = audio_dir / f"{machine_key}{ext}"
        if p.exists():
            try:
                seg = AudioSegment.from_file(str(p))
                dur = len(seg) / 1000
                print(f"    [OK] {p.name}  ({dur:.0f}s)")
                return seg
            except Exception as e:
                print(f"    [FAIL] Load failed for {p.name}: {e}")
    print(f"    [FAIL] Not found: {machine_key}{{.wav/.mp3}} in {audio_dir}")
    return None


# --- Core stitcher ------------------------------------------------------------

def stitch(
    manifest_path: Path,
    audio_dir: Path,
    output_path: Path,
    gap_ms: int = 1500,
    no_tts: bool = False,
    bitrate: str = "192k",
    voice: str = "en-US-GuyNeural",
    dry_run: bool = False,
):
    # Lazy import after dep check
    _require("pydub", "pydub")
    from pydub import AudioSegment

    # Load manifest
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    tracks = manifest.get("tracks", [])
    if not tracks:
        print("ERROR: Manifest contains no tracks.")
        sys.exit(1)

    phase     = manifest.get("phase", "Learning Phase")
    total_h   = manifest.get("total_duration_human", "")
    n_tracks  = len(tracks)

    print()
    print("=" * 62)
    print("  Knowledge OS -- Audio Stitcher")
    print(f"  Phase    : {phase}")
    print(f"  Tracks   : {n_tracks}  |  Est. {total_h}")
    print(f"  Audio Dir: {audio_dir}")
    print(f"  Output   : {output_path}")
    print(f"  TTS      : {'OFF (silence only)' if no_tts else voice}")
    print(f"  Gap      : {gap_ms}ms")
    if dry_run:
        print("  MODE     : DRY RUN -- no files written")
    print("=" * 62)
    print()

    if dry_run:
        for i, t in enumerate(tracks, 1):
            status = "[SKIP] (No Audio)" if t.get("audio_status") == "No Audio" else "[QUEUE]"
            print(f"  [{i:02d}] {status}  {t.get('topic','?')}  [{t.get('machine_key')}]")
            if not no_tts and i < n_tracks:
                print(f"       -> TTS: \"{t.get('transition', '')}\"")
        print()
        return

    silence    = AudioSegment.silent(duration=gap_ms)
    long_pause = AudioSegment.silent(duration=gap_ms * 2)
    final      = AudioSegment.empty()
    loaded     = 0
    skipped    = []

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)

        # Intro narration
        if not no_tts:
            intro_text = (
                f"Welcome to your {phase}. "
                f"This session has {n_tracks} topics"
                + (f", totalling {total_h}." if total_h else ".")
                + " Beginning now."
            )
            print("[00] Intro narration...")
            intro_p = str(tmp / "intro.mp3")
            if generate_tts(intro_text, intro_p, voice):
                intro_seg = AudioSegment.from_file(intro_p)
                final += intro_seg + long_pause
                print(f"    [OK] Intro ({len(intro_seg)/1000:.0f}s)\n")

        # Tracks
        for i, track in enumerate(tracks):
            key        = track.get("machine_key", f"track_{i}")
            topic      = track.get("topic", key)
            transition = track.get("transition", f"Next: {topic}.")
            audio_st   = track.get("audio_status", "No Audio")
            is_last    = (i == n_tracks - 1)

            print(f"[{i+1:02d}/{n_tracks}] {topic}")

            if audio_st == "No Audio":
                print(f"    [SKIP] Skipped - marked 'No Audio' in manifest\n")
                skipped.append(topic)
                continue

            seg = find_audio(key, audio_dir)
            if seg is None:
                skipped.append(topic)
                print()
                continue

            final  += seg
            loaded += 1

            # Transition narration between tracks
            if not is_last:
                if not no_tts:
                    trans_p = str(tmp / f"trans_{i:02d}.mp3")
                    print(f"    -> TTS transition: \"{transition}\"")
                    ok = generate_tts(transition, trans_p, voice)
                    if ok:
                        trans_seg = AudioSegment.from_file(trans_p)
                        final += silence + trans_seg + silence
                    else:
                        final += long_pause
                else:
                    final += long_pause
            print()

        # Outro
        if not no_tts and loaded > 0:
            outro_text = (
                f"Session complete. You covered {loaded} topic"
                f"{'s' if loaded != 1 else ''}. "
                "Update your scores and build evidence in Knowledge OS. "
                "Good work."
            )
            print("[--] Outro narration...")
            outro_p = str(tmp / "outro.mp3")
            if generate_tts(outro_text, outro_p, voice):
                outro_seg = AudioSegment.from_file(outro_p)
                final += long_pause + outro_seg
                print(f"    [OK] Outro ({len(outro_seg)/1000:.0f}s)\n")

        # Export
        if len(final) == 0:
            print("ERROR: Nothing to export. Check --audio-dir and file names.")
            sys.exit(1)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        print(f"Exporting MP3 ({bitrate})...")
        final.export(str(output_path), format="mp3", bitrate=bitrate)

        dur_min  = len(final) / 60000
        size_mb  = output_path.stat().st_size / (1024 * 1024)

        print()
        print("=" * 62)
        print("  [OK]  STITCHED SUCCESSFULLY")
        print(f"  Duration  : {dur_min:.1f} min  ({dur_min/60:.1f} hr)")
        print(f"  File size : {size_mb:.1f} MB")
        print(f"  Loaded    : {loaded}/{n_tracks} tracks")
        if skipped:
            names = ', '.join(skipped[:4]) + ('...' if len(skipped) > 4 else '')
            print(f"  Skipped   : {len(skipped)}  ({names})")
        print(f"  Output    : {output_path}")
        print("=" * 62)
        print()


# --- CLI ----------------------------------------------------------------------

def main():
    p = argparse.ArgumentParser(
        description="Knowledge OS Audio Stitcher -- Phase 2",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples
--------
  # Basic run
  python audio_stitcher.py ^
      --manifest audio_manifest.json ^
      --audio-dir "C:\\Audio\\BRAIN_OS"

  # Custom output + no TTS (silence gaps only)
  python audio_stitcher.py ^
      --manifest audio_manifest.json ^
      --audio-dir "C:\\Audio" ^
      --output "C:\\BRAIN_OS\\audio_out\\phase1.mp3" ^
      --no-tts

  # Dry run -- see what would be processed
  python audio_stitcher.py ^
      --manifest audio_manifest.json ^
      --audio-dir "C:\\Audio" ^
      --dry-run

File naming convention
----------------------
  Audio files must be named by machine_key (from the manifest).
  Supported: .wav  .mp3  .m4a  .ogg
  Example:   prompt_engineering.wav
             rag_pipelines.mp3
  The manifest's `file_hint` field shows the expected Drive path per track.
        """
    )
    p.add_argument("--manifest",  required=True,            help="Path to audio_manifest.json")
    p.add_argument("--audio-dir", required=True,            help="Directory containing audio files named by machine_key")
    p.add_argument("--output",    default="stitched_session.mp3", help="Output MP3 path (default: stitched_session.mp3)")
    p.add_argument("--gap",       type=int, default=1500,   help="Silence gap in ms (default: 1500)")
    p.add_argument("--no-tts",    action="store_true",      help="Use silence instead of TTS transitions")
    p.add_argument("--bitrate",   default="192k",           help="MP3 export bitrate (default: 192k)")
    p.add_argument("--voice",     default="en-US-GuyNeural",help="Edge TTS voice (default: en-US-GuyNeural)")
    p.add_argument("--dry-run",   action="store_true",      help="Print plan only, no files written")

    args = p.parse_args()

    stitch(
        manifest_path = Path(args.manifest),
        audio_dir     = Path(args.audio_dir),
        output_path   = Path(args.output),
        gap_ms        = args.gap,
        no_tts        = args.no_tts,
        bitrate       = args.bitrate,
        voice         = args.voice,
        dry_run       = args.dry_run,
    )


if __name__ == "__main__":
    main()
