"""
anchor_batch.py — Batch Learning Anchor Generator
Runs anchor_generator.py on every _TTS.txt file in converted/ folder.

Usage:
    python anchor_batch.py
    python anchor_batch.py --dry-run          # list files, don't process
    python anchor_batch.py --skip-existing    # skip if _anchor.mp3 already exists
    python anchor_batch.py --limit 5          # process only first N files
"""

import argparse
import subprocess
import sys
import time
from pathlib import Path

# ── Config ─────────────────────────────────────────────────────────────────────
CONVERTED_DIR   = Path(r"C:\Dev\Projects\soccer-content-generator\converted")
ANCHOR_SCRIPT   = Path(r"C:\BRAIN_OS\09_TOOLS\anchor_generator.py")
PYTHON_EXE      = Path(r"C:\Knowledge\CA\venv\Scripts\python.exe")
DELAY_SECONDS   = 3  # pause between files to avoid API rate limits


def get_tts_files(converted_dir: Path) -> list[Path]:
    """Get all _TTS.txt files sorted alphabetically."""
    return sorted(converted_dir.glob("ch*_TTS.txt"))


def anchor_exists(tts_file: Path) -> bool:
    """Check if anchor MP3 already exists for this chapter."""
    stem = tts_file.stem.replace("_TTS", "")
    return (tts_file.parent / f"{stem}_anchor.mp3").exists()


def main():
    parser = argparse.ArgumentParser(description="Batch anchor generator")
    parser.add_argument("--dry-run",       action="store_true", help="List files only")
    parser.add_argument("--skip-existing", action="store_true", help="Skip if anchor exists")
    parser.add_argument("--limit",         type=int, default=None, help="Max files to process")
    args = parser.parse_args()

    files = get_tts_files(CONVERTED_DIR)
    if not files:
        print(f"[batch] No _TTS.txt files found in {CONVERTED_DIR}")
        sys.exit(1)

    if args.skip_existing:
        files = [f for f in files if not anchor_exists(f)]

    if args.limit:
        files = files[:args.limit]

    print(f"[batch] Found {len(files)} files to process")
    print(f"[batch] Converted dir: {CONVERTED_DIR}")
    print()

    if args.dry_run:
        for i, f in enumerate(files, 1):
            exists = "✓ exists" if anchor_exists(f) else "· missing"
            print(f"  {i:02d}. {f.name}  [{exists}]")
        print(f"\n[batch] Dry run complete — {len(files)} files listed, nothing processed.")
        return

    success = []
    failed  = []

    for i, tts_file in enumerate(files, 1):
        print(f"[batch] {i}/{len(files)} — {tts_file.name}")

        result = subprocess.run(
            [str(PYTHON_EXE), str(ANCHOR_SCRIPT), "--source", str(tts_file)],
            capture_output=True, text=True,
            encoding="utf-8", errors="replace",
            env={"PYTHONIOENCODING": "utf-8", **__import__("os").environ}
        )

        if result.returncode == 0 and "Done." in result.stdout:
            # Extract size from output
            for line in result.stdout.splitlines():
                if "Done." in line:
                    print(f"  ✅ {line.strip()}")
            success.append(tts_file.name)
        else:
            print(f"  ❌ Failed")
            # Show last 3 lines of output for context
            lines = (result.stdout + result.stderr).strip().splitlines()
            for line in lines[-3:]:
                print(f"     {line}")
            failed.append(tts_file.name)

        if i < len(files):
            time.sleep(DELAY_SECONDS)

    # ── Summary ──────────────────────────────────────────────────────────────
    print()
    print("=" * 55)
    print(f"  BATCH COMPLETE")
    print(f"  Success: {len(success)}/{len(files)}")
    print(f"  Failed:  {len(failed)}")
    if failed:
        print(f"\n  Failed files:")
        for f in failed:
            print(f"    - {f}")
    print("=" * 55)


if __name__ == "__main__":
    main()
