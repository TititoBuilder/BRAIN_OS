"""
anchor_generator.py — AI Learning Anchor Generator
Generates a closing "Learning Anchor" segment for any audio chapter.
Voice: am_michael (Kokoro TTS)
Usage:
    python anchor_generator.py --source "converted/ch01_pipeline_architecture_TTS.txt"
    python anchor_generator.py --source "converted/ch01_pipeline_architecture_TTS.txt" --preview
"""

import argparse
import os
import sys
import json
import urllib.request
import urllib.error
from pathlib import Path
from dotenv import load_dotenv

# ── Config ─────────────────────────────────────────────────────────────────────
BRAIN_OS_ROOT   = Path(r"C:\BRAIN_OS")
PROJECT_ROOT    = Path(r"C:\Dev\Projects\soccer-content-generator")
BRAIN_AUDIO_PKG = Path(r"C:\Dev\shared\brain-audio")
ENV_FILE        = PROJECT_ROOT / ".env"
OUTPUT_SUFFIX   = "_anchor"
TTS_VOICE       = "am_michael"
TTS_PROFILE     = "default"
MAX_WORDS       = 400

ANCHOR_SYSTEM_PROMPT = """You are a master teacher speaking directly to a software developer named Cristian.
He just finished listening to a technical chapter about his own projects and systems.
Deliver a closing segment of 300-400 words maximum.

Rules:
- Open with exactly: "Let me bring this home for you..."
- Identify the 3 most important concepts from the chapter
- For each concept, use ONE powerful real-world analogy that makes it stick
- Close with a single sentence Cristian should remember forever — make it quotable
- Tone: warm, direct, confident — like a senior mentor talking to a developer he believes in
- Never use bullet points or headers — speak naturally as if talking to him
- Do NOT repeat the chapter content verbatim — distill and reframe it
- The goal: when Cristian finishes listening, the lesson is locked in"""


# ── Claude API call ─────────────────────────────────────────────────────────────
def generate_anchor_script(source_text: str, api_key: str) -> str:
    """Call Claude API to generate the learning anchor script."""
    
    # Truncate source if very long (keep first 8000 chars for context)
    if len(source_text) > 8000:
        source_text = source_text[:8000] + "\n\n[...content truncated for anchor generation...]"
    
    payload = {
        "model": "claude-sonnet-4-6",
        "max_tokens": 1000,
        "system": ANCHOR_SYSTEM_PROMPT,
        "messages": [
            {
                "role": "user",
                "content": f"Here is the chapter content:\n\n{source_text}\n\nGenerate the learning anchor closing segment now."
            }
        ]
    }

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["content"][0]["text"].strip()
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        print(f"[anchor] Claude API error {e.code}: {body}")
        sys.exit(1)
    except Exception as e:
        print(f"[anchor] Unexpected API error: {e}")
        sys.exit(1)


# ── TTS synthesis ───────────────────────────────────────────────────────────────
def synthesize_anchor(script: str, output_path: Path) -> bool:
    """Run TTS on the anchor script using tts_local.py with am_michael voice."""
    
    TTS_SCRIPT = Path(r"C:\Dev\Projects\soccer-content-generator\tts_local.py")
    TTS_VENV   = Path(r"C:\Knowledge\CA\venv\Scripts\python.exe")
    
    # Write script to temp file
    temp_txt = output_path.with_suffix(".txt")
    temp_txt.write_text(script, encoding="utf-8")
    
    try:
        import subprocess
        result = subprocess.run(
    [str(TTS_VENV), str(TTS_SCRIPT), str(temp_txt), "--voice", "am_adam"],
    capture_output=True, text=True, encoding="utf-8", errors="replace",
    env={**os.environ, "PYTHONIOENCODING": "utf-8"}
)
        # tts_local.py appends _am_adam_audio to the stem
        actual_output = output_path.parent / (output_path.stem + "_am_adam_audio.mp3")
        if result.returncode == 0 and actual_output.exists():
            actual_output.rename(output_path)  # rename to expected path
            return True
        else:
            print(f"[anchor] TTS returncode: {result.returncode}")
            print(f"[anchor] TTS stderr: {result.stderr}")
            print(f"[anchor] TTS stdout: {result.stdout[:500]}")   
            print(f"[anchor] Script saved as fallback: {temp_txt}")
            return False
    except Exception as e:
        print(f"[anchor] Subprocess error: {e}")
        return False


# ── Main ────────────────────────────────────────────────────────────────────────
def _process_one(source_path: Path, output_path: Path, api_key: str, preview: bool) -> bool:
    """Process a single source file into an anchor. Returns True on success."""
    print(f"[anchor] Source: {source_path.name}")
    source_text = source_path.read_text(encoding="utf-8", errors="ignore")
    print(f"[anchor] Source words: {len(source_text.split()):,}")

    print("[anchor] Generating anchor script via Claude API...")
    script = generate_anchor_script(source_text, api_key)
    print(f"[anchor] Anchor script: {len(script.split())} words")

    if preview:
        print("\n" + "-" * 60)
        print("LEARNING ANCHOR PREVIEW")
        print("-" * 60)
        print(script)
        print("-" * 60)
        print("\n[anchor] Preview mode — TTS not run.")
        return True

    print(f"[anchor] Synthesizing with voice: {TTS_VOICE}")
    print(f"[anchor] Output: {output_path}")
    success = synthesize_anchor(script, output_path)
    if success:
        size_mb = output_path.stat().st_size / (1024 * 1024)
        print(f"[anchor] Done. {output_path.name} ({size_mb:.1f} MB)")
    else:
        print("[anchor] TTS failed — check fallback .txt file above.")
    return success


def main():
    parser = argparse.ArgumentParser(
        description="Generate a Learning Anchor closing segment for an audio chapter."
    )
    parser.add_argument(
        "--source",
        default=None,
        help="Path to the source .txt chapter file (required unless --batch)"
    )
    parser.add_argument(
        "--batch",
        action="store_true",
        help="Process all ch*_TTS.txt files in converted/"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-generate even if anchor .mp3 already exists (batch mode only)"
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Print generated script without running TTS"
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output path for anchor .mp3 (default: same dir as source with _anchor suffix)"
    )
    args = parser.parse_args()

    if not args.batch and not args.source:
        parser.error("--source is required unless --batch is specified")

    # ── Load env ────────────────────────────────────────────────────────────────
    load_dotenv(ENV_FILE)
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        load_dotenv(BRAIN_OS_ROOT / "03_APIS" / ".env")
        api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("[anchor] ERROR: ANTHROPIC_API_KEY not found in .env")
        print(f"  Add it to: {ENV_FILE}")
        sys.exit(1)

    # ── Batch mode ──────────────────────────────────────────────────────────────
    if args.batch:
        converted_dir = PROJECT_ROOT / "converted"
        source_files  = sorted(converted_dir.glob("ch*_TTS.txt"))
        if not source_files:
            print(f"[anchor] No ch*_TTS.txt files found in {converted_dir}")
            sys.exit(1)

        total   = len(source_files)
        done    = 0
        skipped = 0
        failed  = 0

        print(f"[anchor] Batch mode — {total} chapter(s) found")
        print(f"[anchor] Output dir: {converted_dir}\n")

        for i, source_path in enumerate(source_files, 1):
            stem        = source_path.stem.replace("_TTS", "")
            output_path = source_path.parent / f"{stem}{OUTPUT_SUFFIX}.mp3"

            if not args.force and output_path.exists():
                print(f"  {i:02d}/{total} SKIP  {source_path.name} (anchor exists)")
                skipped += 1
                continue

            print(f"  {i:02d}/{total} {source_path.name}")
            ok = _process_one(source_path, output_path, api_key, args.preview)
            if ok:
                done += 1
            else:
                failed += 1
            print()

        print("=" * 55)
        print(f"  BATCH COMPLETE  done={done}  skipped={skipped}  failed={failed}")
        print("=" * 55)
        return

    # ── Single file mode ────────────────────────────────────────────────────────
    source_path = Path(args.source)
    if not source_path.exists():
        source_path = PROJECT_ROOT / args.source
    if not source_path.exists():
        print(f"[anchor] ERROR: Source file not found: {args.source}")
        sys.exit(1)

    if args.output:
        output_path = Path(args.output)
    else:
        stem        = source_path.stem.replace("_TTS", "")
        output_path = source_path.parent / f"{stem}{OUTPUT_SUFFIX}.mp3"

    _process_one(source_path, output_path, api_key, args.preview)


if __name__ == "__main__":
    main()
