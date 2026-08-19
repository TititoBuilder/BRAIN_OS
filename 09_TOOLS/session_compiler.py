r"""
category: Session Management
session_compiler.py — Session-to-Audio Chapter Compiler
=========================================================
Takes one session archive from 08_SESSIONS\, distills it into a clean
reviewable chapter via the Claude API, converts that chapter into a spoken
narration script, synthesizes audio via the existing Kokoro TTS chain,
uploads the result to Google Drive, and adds an entry to drive_index.json
so the Read-Along app can serve it.

Pipeline:
    1. Read session archive .md from 08_SESSIONS\
    2. Claude call #1 — distill into a structured, reviewable chapter .md
       (written to 08_SESSIONS\distilled\ for review)
    3. Claude call #2 — convert the chapter into a natural spoken script
    4. tts_local.py (BDF project, CA_Book venv, Kokoro) — script -> .mp3
       (written to audio_staging\<machine_key>.mp3 — gitignored, never committed)
    5. Upload .mp3 to Google Drive (Knowledge_OS brainos_sessions folder)
    6. Update drive_index.json — index[machine_key] = "id:<drive_file_id>"

Usage:
    python C:\BRAIN_OS\09_TOOLS\session_compiler.py
        (compiles the most recent session archive)
    python C:\BRAIN_OS\09_TOOLS\session_compiler.py 2026-06-17_2222_bdf_ca_brain_os_resolve.md
    python C:\BRAIN_OS\09_TOOLS\session_compiler.py --dry-run
    python C:\BRAIN_OS\09_TOOLS\session_compiler.py --chapter-only
    python C:\BRAIN_OS\09_TOOLS\session_compiler.py --force --voice af_heart
"""

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

from dotenv import load_dotenv

from project_paths import project_script, project_venv_python

# ── Config ──────────────────────────────────────────────────────────────────
BRAIN_OS       = Path(r"C:\BRAIN_OS")
SESSIONS_DIR   = BRAIN_OS / "08_SESSIONS"
DISTILLED_DIR  = SESSIONS_DIR / "distilled"
AUDIO_STAGING  = BRAIN_OS / "audio_staging"
DRIVE_INDEX    = BRAIN_OS / "09_TOOLS" / "drive_index.json"
CONFIG_FILE    = BRAIN_OS / "BRAIN_OS_CONFIG.json"

BDF_ENV_FILE   = Path(r"C:\Dev\Projects\soccer-content-generator\.env")
BRAIN_ENV_FILE = BRAIN_OS / "03_APIS" / ".env"

MODEL             = "claude-sonnet-4-6"
CHAPTER_MAX_TOKENS   = 4096
NARRATION_MAX_TOKENS = 2200
DEFAULT_VOICE     = "af_heart"

# ── Prompts ───────────────────────────────────────────────────────────────────
CHAPTER_SYSTEM_PROMPT = """You are a knowledge distiller for BRAIN_OS, Cristian's personal
knowledge-graph vault. You receive a session archive — a dated log of commit-style
bullet points recording what was built, fixed, and decided across his projects
(BDF, CristianConstruction, BRAIN_OS, Read-Along App, Resolve MCP Server) during one
working session.

Distill it into a clean, reviewable chapter. Write as reference documentation, not
as a conversation recap or a re-listing of every bullet. Group related bullets into
a coherent narrative of what actually happened and why it mattered.

Never use phrases like "Claude said", "you mentioned", or "in this session". Only
include a section if it has real content — omit empty categories entirely. Be
concrete: include exact file names, tool names, and commands where present.
"""

CHAPTER_PROMPT = """Distill this BRAIN_OS session archive into a reviewable chapter.

Organize the output into these sections (only include sections with actual content):

## Summary
One or two sentences: what this session accomplished, at a glance.

## Systems Built
Tools, scripts, or integrations created or extended. Include file names and locations.

## Decisions Made
Choices made and the reasoning behind them.

## Problems Solved
Bugs fixed or blockers removed, with root cause and fix.

## Patterns & Principles Earned
Anything reusable that emerged — a rule of thumb, a corrected assumption, a
principle worth remembering.

## Open Threads
Anything left unresolved or deferred to a future session.

---

Session archive ({filename}):

{content}
"""

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


# ── Session location ──────────────────────────────────────────────────────────
def find_session(name: str | None) -> Path:
    if name:
        p = Path(name)
        if not p.is_absolute():
            p = SESSIONS_DIR / name
        if not p.exists():
            sys.exit(f"ERROR: session archive not found: {p}")
        return p
    files = sorted(
        (f for f in SESSIONS_DIR.glob("*.md") if f.name != "ingestion_flags.md"),
        key=lambda f: f.stat().st_mtime,
        reverse=True,
    )
    if not files:
        sys.exit(f"ERROR: no session archives found in {SESSIONS_DIR}")
    return files[0]


def session_machine_key(path: Path) -> str:
    """Filename is the machine key source — timestamp is all that's needed."""
    m = re.search(r"(\d{4}-\d{2}-\d{2})_(\d{4})", path.stem)
    if m:
        date_part = m.group(1).replace("-", "")
        return f"session_{date_part}_{m.group(2)}"
    return f"session_{re.sub(r'[^a-z0-9]+', '_', path.stem.lower()).strip('_')}"


def chapter_output_path(machine_key: str) -> Path:
    return DISTILLED_DIR / f"{machine_key}.md"


# ── Claude API ──────────────────────────────────────────────────────────────────
def load_api_key() -> str:
    load_dotenv(BDF_ENV_FILE)
    key = os.getenv("ANTHROPIC_API_KEY")
    if not key:
        load_dotenv(BRAIN_ENV_FILE)
        key = os.getenv("ANTHROPIC_API_KEY")
    if not key:
        sys.exit(f"ERROR: ANTHROPIC_API_KEY not found in {BDF_ENV_FILE} or {BRAIN_ENV_FILE}")
    return key


def call_claude(api_key: str, system: str, prompt: str, max_tokens: int) -> str:
    payload = {
        "model": MODEL,
        "max_tokens": max_tokens,
        "system": system,
        "messages": [{"role": "user", "content": prompt}],
    }
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["content"][0]["text"].strip()
    except urllib.error.HTTPError as e:
        sys.exit(f"ERROR: Claude API {e.code}: {e.read().decode()[:500]}")
    except Exception as e:
        sys.exit(f"ERROR: unexpected API error: {e}")


def distill_chapter(api_key: str, session_path: Path) -> str:
    content = session_path.read_text(encoding="utf-8", errors="replace")
    prompt = CHAPTER_PROMPT.format(filename=session_path.name, content=content)
    return call_claude(api_key, CHAPTER_SYSTEM_PROMPT, prompt, CHAPTER_MAX_TOKENS)


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
    try:
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request
        from google.auth.exceptions import RefreshError
        from googleapiclient.discovery import build
    except ImportError:
        sys.exit("ERROR: Google libraries not installed. "
                  "Run: pip install google-api-python-client google-auth-oauthlib")

    scopes = ["https://www.googleapis.com/auth/drive"]
    if not token_path.exists():
        sys.exit(f"ERROR: Drive token not found: {token_path}")

    creds = Credentials.from_authorized_user_file(str(token_path), scopes)
    if creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
        except RefreshError as e:
            sys.exit(
                f"ERROR: Drive refresh token is expired/revoked: {e}\n"
                f"  This is a credential problem, not a script bug -- the chapter and audio\n"
                f"  files below were already produced successfully and are safe on disk.\n"
                f"  Re-authenticate interactively (e.g. via drive_browser.py's OAuth flow,\n"
                f"  which calls flow.run_local_server) to get a fresh token at:\n"
                f"    {token_path}"
            )
        token_path.write_text(creds.to_json(), encoding="utf-8", newline="\n")

    return build("drive", "v3", credentials=creds)


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


# ── Main ────────────────────────────────────────────────────────────────────────
def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Compile a session archive into a reviewable audio chapter")
    parser.add_argument("session_file", nargs="?", help="Filename in 08_SESSIONS\\ (default: most recent)")
    parser.add_argument("--voice", default=DEFAULT_VOICE, help=f"Kokoro voice (default: {DEFAULT_VOICE})")
    parser.add_argument("--dry-run", action="store_true", help="Distill + narrate only; print output, write nothing")
    parser.add_argument("--chapter-only", action="store_true", help="Write the distilled chapter, stop before audio")
    parser.add_argument("--force", action="store_true", help="Skip overwrite/collision confirmations")
    args = parser.parse_args()

    print("=" * 60)
    print("  SESSION COMPILER")
    print("=" * 60)

    # ── Step 1: locate + verify session ──────────────────────────────────────
    session_path = find_session(args.session_file)
    machine_key = session_machine_key(session_path)
    print(f"\nSession    : {session_path.name}")
    print(f"Machine key: {machine_key}")

    api_key = load_api_key()

    # ── Step 2: distill chapter ──────────────────────────────────────────────
    print("\n-- Distilling chapter (Claude) --")
    chapter_body = distill_chapter(api_key, session_path)
    chapter_doc = f"# Session Chapter — {session_path.name}\n\n{chapter_body}\n"

    if args.dry_run:
        print("\n" + "-" * 60)
        print("DRY RUN — distilled chapter:")
        print("-" * 60)
        print(chapter_doc)

    out_chapter = chapter_output_path(machine_key)
    if not args.dry_run:
        DISTILLED_DIR.mkdir(parents=True, exist_ok=True)
        if out_chapter.exists() and not args.force:
            answer = input(f"  {out_chapter.name} exists. Overwrite? [y/N] ").strip().lower()
            if answer != "y":
                print("  Aborted — nothing written.")
                return
        out_chapter.write_text(chapter_doc, encoding="utf-8", newline="\n")
        print(f"  Chapter written -> {out_chapter}")

    if args.chapter_only:
        print("\n[chapter-only] Stopping before audio generation.")
        return

    # ── Step 3: narration script ──────────────────────────────────────────────
    print("\n-- Generating narration script (Claude) --")
    script = narrate_chapter(api_key, chapter_body)
    print(f"  Narration: {len(script.split())} words")

    if args.dry_run:
        print("\n" + "-" * 60)
        print("DRY RUN — narration script:")
        print("-" * 60)
        print(script)
        print("-" * 60)
        print("\n[dry-run] Stopping before TTS/upload/index write.")
        return

    if not args.force:
        answer = input(f"\n  Proceed to TTS + Drive upload for '{machine_key}'? [y/N] ").strip().lower()
        if answer != "y":
            print("  Aborted — chapter is saved, audio not generated.")
            return

    # ── Step 4: TTS ───────────────────────────────────────────────────────────
    print("\n-- Synthesizing audio (Kokoro / tts_local.py) --")
    mp3_path = synthesize(script, machine_key, args.voice)
    if not mp3_path:
        sys.exit(1)
    print(f"  Audio ready: {mp3_path}  ({mp3_path.stat().st_size / (1024*1024):.1f} MB)")

    # ── Step 5: upload ────────────────────────────────────────────────────────
    print("\n-- Uploading to Google Drive --")
    creds_path, token_path, folder_id = load_drive_config()
    service = get_drive_service(creds_path, token_path)
    file_id = upload_to_drive(service, mp3_path, folder_id)

    # ── Step 6: index update ──────────────────────────────────────────────────
    print("\n-- Updating drive_index.json --")
    update_drive_index(machine_key, file_id, args.force)

    print("\n" + "=" * 60)
    print("  DONE")
    print(f"  Chapter : {out_chapter}")
    print(f"  Audio   : {mp3_path.name} (local, gitignored — never commit)")
    print(f"  Drive ID: {file_id}")
    print(f"  Index key: {machine_key}")
    print("=" * 60)
    print("\nNext step (manual — not run automatically):")
    print(f"  cd C:\\BRAIN_OS")
    print(f"  git add 09_TOOLS/drive_index.json 08_SESSIONS/distilled/{machine_key}.md")
    print(f"  git commit -m \"feat: add {machine_key} session chapter audio\"")
    print(f"  git push")


if __name__ == "__main__":
    main()
