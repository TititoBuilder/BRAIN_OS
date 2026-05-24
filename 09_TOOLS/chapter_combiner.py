"""
chapter_combiner.py — Merge original chapter audio + learning anchor into one MP3
Uses ffmpeg to concatenate: [original_audio] + [anchor_audio] = [combined_audio]

Usage:
    python chapter_combiner.py --dry-run
    python chapter_combiner.py --skip-existing
    python chapter_combiner.py --chapter ch01_pipeline_architecture
"""

import argparse
import subprocess
import sys
from pathlib import Path

CONVERTED_DIR = Path(r"C:\Dev\Projects\soccer-content-generator\converted")
OUTPUT_DIR    = CONVERTED_DIR / "combined"


def get_pairs() -> list[tuple[Path, Path, Path]]:
    """Return list of (original_mp3, anchor_mp3, output_mp3) tuples."""
    pairs = []
    for anchor in sorted(CONVERTED_DIR.glob("ch*_anchor.mp3")):
        stem = anchor.stem.replace("_anchor", "")
        # Find original — named ch01_pipeline_architecture_af_heart_audio.mp3
        originals = list(CONVERTED_DIR.glob(f"{stem}_af_heart_audio.mp3"))
        if not originals:
            # Try without voice suffix
            originals = list(CONVERTED_DIR.glob(f"{stem}.mp3"))
        if originals:
            original = originals[0]
            output = OUTPUT_DIR / f"{stem}_combined.mp3"
            pairs.append((original, anchor, output))
        else:
            print(f"  [!] No original found for {anchor.name}")
    return pairs


def combine(original: Path, anchor: Path, output: Path) -> bool:
    """Concatenate original + anchor using ffmpeg."""
    # Write concat list to temp file
    list_file = output.parent / "_concat_list.txt"
    list_file.write_text(
        f"file '{original}'\nfile '{anchor}'\n",
        encoding="utf-8"
    )
    result = subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0",
         "-i", str(list_file), "-c", "copy", str(output)],
        capture_output=True, text=True
    )
    list_file.unlink(missing_ok=True)
    return result.returncode == 0 and output.exists()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run",       action="store_true")
    parser.add_argument("--skip-existing", action="store_true")
    parser.add_argument("--chapter",       help="Process single chapter stem")
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    pairs = get_pairs()

    if args.chapter:
        pairs = [(o, a, out) for o, a, out in pairs if args.chapter in o.stem]

    if args.skip_existing:
        pairs = [(o, a, out) for o, a, out in pairs if not out.exists()]

    print(f"[combiner] {len(pairs)} chapters to combine")
    print(f"[combiner] Output: {OUTPUT_DIR}\n")

    if args.dry_run:
        for orig, anchor, out in pairs:
            exists = "✓" if out.exists() else "·"
            print(f"  [{exists}] {out.name}")
            print(f"       + {orig.name}")
            print(f"       + {anchor.name}")
        return

    success, failed = [], []
    for orig, anchor, out in pairs:
        print(f"  {orig.stem[:40]}...", end=" ", flush=True)
        if combine(orig, anchor, out):
            size_mb = out.stat().st_size / 1024 / 1024
            print(f"✅ {size_mb:.1f} MB")
            success.append(out.name)
        else:
            print("❌")
            failed.append(out.name)

    print(f"\n{'='*50}")
    print(f"  Done: {len(success)}/{len(pairs)}")
    if failed:
        for f in failed:
            print(f"  ❌ {f}")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
