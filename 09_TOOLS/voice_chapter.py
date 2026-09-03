"""
category: Audio Generation
voice_chapter.py — Narrate a distilled chapter, synthesize it, upload it.

Back half of the old session_compiler.py. Takes a chapter written by
distill_session.py and derives the machine_key from its filename, so the
two tools exchange a file rather than shared state. Re-runnable without
paying for distillation again.

Usage:
    python C:/BRAIN_OS/09_TOOLS/voice_chapter.py session_20260830_2050.md
    python C:/BRAIN_OS/09_TOOLS/voice_chapter.py <chapter> --dry-run
    python C:/BRAIN_OS/09_TOOLS/voice_chapter.py <chapter> --voice af_heart
    python C:/BRAIN_OS/09_TOOLS/voice_chapter.py <chapter> --force
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import date
from pathlib import Path

from claude_client import load_api_key, call_claude
from drive_service import get_service
from project_paths import project_script, project_venv_python

# ── Config ──────────────────────────────────────────────────────────────────
BRAIN_OS      = Path(r"C:\BRAIN_OS")
SESSIONS_DIR  = BRAIN_OS / "08_SESSIONS"
DISTILLED_DIR = SESSIONS_DIR / "distilled"
AUDIO_STAGING = BRAIN_OS / "audio_staging"
DRIVE_INDEX   = BRAIN_OS / "09_TOOLS" / "drive_index.json"
CONFIG_FILE   = BRAIN_OS / "BRAIN_OS_CONFIG.json"

NARRATION_MAX_TOKENS = 2200
DEFAULT_VOICE = "af_heart"

NARRATION_PROMPT = """Convert this distilled session chapter into a natural spoken
narration script. The listener is Cristian, hearing a recap of his own work while
driving or at the gym.

Rules:
- Write in second person: "You built..." "You fixed..." "You decided..."
- Convert markdown headers into natural spoken transitions
- Convert bullet lists into flowing sentences
- Skip the frontmatter-style "## Summary" label itself, but open with its content
- Tone: clear, direct, conversational — like a colleague recapping your own session
- Length: aim for 4-7 minutes of speech (roughly 550-900 words) — cover every
  section that has content, but synthesize rather than reading verbatim
- Start with: "Here's what you got done in this session..."

Output only the spoken script — no headers, no markdown, no preamble.

Chapter:

{content}
"""



def narrate_chapter(api_key: str, chapter_body: str) -> str:
    body = chapter_body
    if len(body) > 12000:
        body = body[:12000] + "\n\n[...truncated for narration...]"
    prompt = NARRATION_PROMPT.format(content=body)
    return call_claude(api_key, "", prompt, NARRATION_MAX_TOKENS)



# ── TTS ─────────────────────────────────────────────────────────────────────────
def synthesize(script: str, machine_key: str, voice: str) -> Path | None:
    """Run tts_local.py (BDF, CA_Book venv, Kokoro) on the narration script.
    Returns the final .mp3 path in audio_staging\\, or None on failure."""
    AUDIO_STAGING.mkdir(parents=True, exist_ok=True)
    tts_script = project_script("BDF", "tts_local.py")
    tts_venv = project_venv_python("CA_Book")

    temp_txt = AUDIO_STAGING / f"{machine_key}_TTS.txt"
    temp_txt.write_text(script, encoding="utf-8", newline="\n")

    print(f"  Synthesizing with voice: {voice} (Kokoro, CA_Book venv)...")
    result = subprocess.run(
        [str(tts_venv), str(tts_script), str(temp_txt), "--voice", voice],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        env={**os.environ, "PYTHONIOENCODING": "utf-8"},
    )

    # tts_local.py appends _<voice>_audio to the stem
    produced = AUDIO_STAGING / f"{machine_key}_{voice}_audio.mp3"
    final_path = AUDIO_STAGING / f"{machine_key}.mp3"

    if result.returncode == 0 and produced.exists():
        produced.rename(final_path)
        temp_txt.unlink()  # clean up — no stray .txt left behind
        return final_path

    print(f"  TTS failed (exit {result.returncode})")
    print(f"  stderr: {result.stderr[-500:]}")
    print(f"  Narration script preserved for inspection: {temp_txt}")
    return None


# ── Google Drive ────────────────────────────────────────────────────────────────
def load_drive_config() -> tuple[Path, Path, str]:
    if not CONFIG_FILE.exists():
        sys.exit(f"ERROR: {CONFIG_FILE} not found")
    cfg = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    drive = cfg.get("drive", {})
    folder_id = cfg.get("drive_folders", {}).get("brainos_sessions")
    creds_path = Path(drive.get("credentials_path", ""))
    token_path = Path(drive.get("token_path", ""))
    if not creds_path or not token_path or not folder_id:
        sys.exit("ERROR: BRAIN_OS_CONFIG.json missing drive.credentials_path, "
                  "drive.token_path, or drive_folders.brainos_sessions")
    return creds_path, token_path, folder_id


def get_drive_service(creds_path: Path, token_path: Path):
    """Authenticate without a browser fallback: a TTS run must not block
    on a consent screen. See drive_service.DriveAuthError for recovery."""
    return get_service(creds_path, token_path, allow_browser=False)


def upload_to_drive(service, local_path: Path, folder_id: str) -> str:
    from googleapiclient.http import MediaFileUpload

    media = MediaFileUpload(str(local_path), mimetype="audio/mpeg", resumable=True,
                             chunksize=8 * 1024 * 1024)
    request = service.files().create(
        body={"name": local_path.name, "parents": [folder_id]},
        media_body=media,
        fields="id, name, webViewLink",
    )

    size_mb = local_path.stat().st_size / (1024 * 1024)
    print(f"  Uploading {local_path.name} ({size_mb:.1f} MB) to Drive...")

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            pct = int(status.progress() * 100)
            print(f"    {pct}%", end="\r", flush=True)

    print(f"  Upload complete. Drive ID: {response['id']}")
    return response["id"]


# ── drive_index.json ────────────────────────────────────────────────────────────
def update_drive_index(machine_key: str, file_id: str, force: bool) -> None:
    data = json.loads(DRIVE_INDEX.read_text(encoding="utf-8"))
    index = data.setdefault("index", {})

    if machine_key in index and not force:
        existing = index[machine_key]
        answer = input(
            f"  drive_index.json already has '{machine_key}' -> {existing}. "
            f"Overwrite with new upload? [y/N] "
        ).strip().lower()
        if answer != "y":
            print("  Skipped index update — existing entry left unchanged.")
            return

    index[machine_key] = f"id:{file_id}"
    data["generated"] = date.today().isoformat()
    DRIVE_INDEX.write_text(
        json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8", newline="\n"
    )
    print(f"  drive_index.json updated: '{machine_key}' -> id:{file_id}")




# ── Main ────────────────────────────────────────────────────────────────────
def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Narrate, synthesize and upload a distilled chapter")
    parser.add_argument("chapter", help="Chapter filename in 08_SESSIONS/distilled")
    parser.add_argument("--voice", default=DEFAULT_VOICE, help=f"Kokoro voice (default: {DEFAULT_VOICE})")
    parser.add_argument("--dry-run", action="store_true", help="Narrate only; print it, write nothing")
    parser.add_argument("--force", action="store_true", help="Skip confirmations")
    args = parser.parse_args()

    print("=" * 60)
    print("  VOICE CHAPTER")
    print("=" * 60)

    chapter_path = Path(args.chapter)
    if not chapter_path.is_absolute():
        chapter_path = DISTILLED_DIR / chapter_path
    if not chapter_path.exists():
        sys.exit(f"ERROR: chapter not found: {chapter_path}")

    machine_key = chapter_path.stem
    chapter_doc = chapter_path.read_text(encoding="utf-8")
    body = chapter_doc.split("\n", 1)[1].lstrip() if chapter_doc.startswith("#") else chapter_doc

    print(f"\nChapter    : {chapter_path.name}")
    print(f"Machine key: {machine_key}")

    api_key = load_api_key()

    print("\n-- Generating narration script (Claude) --")
    script = narrate_chapter(api_key, body)
    print(f"  Narration: {len(script.split())} words")

    if args.dry_run:
        print("\n" + "-" * 60)
        print(script)
        print("-" * 60)
        print("\n[dry-run] Stopping before TTS, upload and index write.")
        return

    if not args.force:
        answer = input(f"\n  Proceed to TTS + Drive upload for '{machine_key}'? [y/N] ").strip().lower()
        if answer != "y":
            print("  Aborted \u2014 chapter is untouched, audio not generated.")
            return

    print("\n-- Synthesizing audio (Kokoro / tts_local.py) --")
    mp3_path = synthesize(script, machine_key, args.voice)
    if not mp3_path:
        sys.exit(1)
    print(f"  Audio ready: {mp3_path}  ({mp3_path.stat().st_size / (1024*1024):.1f} MB)")

    print("\n-- Uploading to Google Drive --")
    creds_path, token_path, folder_id = load_drive_config()
    service = get_drive_service(creds_path, token_path)
    file_id = upload_to_drive(service, mp3_path, folder_id)

    print("\n-- Updating drive_index.json --")
    update_drive_index(machine_key, file_id, args.force)

    print("\n" + "=" * 60)
    print("  DONE")
    print(f"  Audio    : {mp3_path.name} (local, gitignored \u2014 never commit)")
    print(f"  Drive ID : {file_id}")
    print(f"  Index key: {machine_key}")
    print("=" * 60)


if __name__ == "__main__":
    main()
