r"""
category: Google Drive
drive_sync.py — BDF Drive Manifest Sync
========================================
Walks BDF/chapters/ and BDF/sessions/ on Google Drive,
writes bdf_drive_manifest.json to BRAIN_OS graphs directory.

Usage:
    python C:/BRAIN_OS/09_TOOLS/drive_sync.py
    python C:/BRAIN_OS/09_TOOLS/drive_sync.py --upload converted\ch17_clip_name_parser_af_heart_audio.mp3
    python C:/BRAIN_OS/09_TOOLS/drive_sync.py --upload SESSION_20260407_0827_audio.mp3
    python C:/BRAIN_OS/09_TOOLS/drive_sync.py --upload myfile.mp3 --folder sessions
    python C:/BRAIN_OS/09_TOOLS/drive_sync.py --get-token
    python C:/BRAIN_OS/09_TOOLS/drive_sync.py --normalize
    python C:/BRAIN_OS/09_TOOLS/drive_sync.py --normalize --dry-run

When to run:
    - After uploading new audio files to Drive
    - After regenerating a chapter's audio
    - When graph_maintainer reports "[manifest] not found"

Note: if the token was created with drive.readonly scope, delete
gdrive_token.json and re-run to re-authorize with write access.

Output:
    C:\BRAIN_OS\02_PROJECTS\graphs\bdf_drive_manifest.json
"""

import argparse
import json
import mimetypes
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# ── Google Auth ───────────────────────────────────────────────────────────────
try:
    from googleapiclient.http import MediaFileUpload

    from drive_service import get_service
except ImportError:
    print("[!] Missing Google auth libraries. Run:")
    print("    pip install google-api-python-client google-auth-oauthlib google-auth-httplib2")
    sys.exit(1)

# ── Paths ─────────────────────────────────────────────────────────────────────
# Ported from BDF 2026-09-01. The old root constant was derived from
# __file__.parent.parent, which named the BDF project there and would name
# C:\BRAIN_OS here, pointing the credential paths at files that do not exist.
# Credentials now come from drive_service, the one Drive auth implementation.
BRAIN_OS_DIR  = Path(r"C:\BRAIN_OS")
MANIFEST_PATH = BRAIN_OS_DIR / "02_PROJECTS" / "graphs" / "bdf_drive_manifest.json"

SCOPES = ["https://www.googleapis.com/auth/drive"]

def _load_drive_folders() -> dict:
    config_path = BRAIN_OS_DIR / "BRAIN_OS_CONFIG.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    return config["drive_folders"]


# ── Auth ──────────────────────────────────────────────────────────────────────

def _get_drive_service():
    """Authenticate via the shared drive_service module."""
    return get_service()


# ── Key extraction ────────────────────────────────────────────────────────────

def _chapter_key(filename: str) -> str | None:
    """
    ch01_pipeline_architecture_af_heart_audio.mp3
        → ch01_pipeline_architecture
    """
    m = re.match(r"(ch\d+_.+?)_af_heart_audio\.mp3$", filename)
    return m.group(1) if m else None


def _anchor_key(filename: str) -> str | None:
    """
    ch01_pipeline_architecture_anchor.mp3
        → ch01_pipeline_architecture_anchor
    """
    m = re.match(r"(ch\d+_.+_anchor)\.mp3$", filename)
    return m.group(1) if m else None


def _combined_key(filename: str) -> str | None:
    """
    ch01_pipeline_architecture_combined.mp3
        → ch01_pipeline_architecture_combined
    """
    m = re.match(r"(ch\d+_.+_combined)\.mp3$", filename)
    return m.group(1) if m else None


def _session_key(filename: str) -> str | None:
    """
    BDF_SESSION_20260331_1517_predator_setup_milestone_variations.mp3
        → 20260331_1517
    SESSION_20260407_0827_audio.mp3
        → 20260407_0827
    BDF_Session_Summary_March18_2026_af_heart_audio.mp3
        → BDF_Session_Summary_March18_2026
    _session_20260331_1354_combined_af_heart_audio.mp3
        → 20260331_1354
    """
    m = re.match(r"^BDF_SESSION_(\d{8}_\d{4})_", filename)
    if m:
        return m.group(1)
    m = re.match(r"SESSION_(\d{8}_\d{4})_audio\.mp3$", filename)
    if m:
        return m.group(1)
    m = re.match(r"(BDF_Session_[A-Za-z]+_[A-Za-z]+\d+_\d{4})_af_heart_audio\.mp3$", filename)
    if m:
        return m.group(1)
    m = re.match(r"_session_(\d{8}_\d{4})_combined_af_heart_audio\.mp3$", filename)
    return m.group(1) if m else None


def _brainos_key(filename: str) -> str | None:
    """
    Key for BRAIN_OS Handbook audio files — full stem, no suffix stripping.
    guide_brain_os.wav        → guide_brain_os
    claudeguide_mcp_setup.wav → claudeguide_mcp_setup
    Returns None for non-audio files (not expected in these folders).
    """
    p = Path(filename)
    if p.suffix.lower() in {".wav", ".mp3"}:
        return p.stem
    return None


# ── Drive listing ─────────────────────────────────────────────────────────────

def _list_folder(service, folder_id: str) -> list[dict]:
    """Return all non-trashed files in a Drive folder tree, recursing into subfolders."""
    results = []
    page_token = None

    while True:
        resp = service.files().list(
            q=f"'{folder_id}' in parents and trashed = false",
            fields="nextPageToken, files(id, name, mimeType, modifiedTime, size)",
            pageToken=page_token,
            pageSize=100,
        ).execute()
        for item in resp.get("files", []):
            if item["mimeType"] == "application/vnd.google-apps.folder":
                results.extend(_list_folder(service, item["id"]))
            else:
                results.append(item)
        page_token = resp.get("nextPageToken")
        if not page_token:
            break

    return results


# ── Manifest build ────────────────────────────────────────────────────────────

def build_manifest(service, drive_folders: dict) -> dict:
    """Scan Drive folders and return a structured manifest dict."""
    manifest: dict = {
        "last_synced":      datetime.now(timezone.utc).isoformat(),
        "chapters":         {},
        "sessions":         {},
        "bdf_anchors":      {},
        "bdf_combined":     {},
        "brainos_chapters": {},
        "brainos_sessions": {},
    }

    print("  Scanning BDF chapters/...")
    for file in _list_folder(service, drive_folders["bdf_chapters"]):
        entry = {
            "drive_id":      file["id"],
            "filename":      file["name"],
            "modified_time": file["modifiedTime"],
            "size_bytes":    int(file.get("size", 0)),
        }
        key = _chapter_key(file["name"])
        if key:
            manifest["chapters"][key] = entry
            continue
        key = _anchor_key(file["name"])
        if key:
            manifest["bdf_anchors"][key] = entry
            continue
        key = _combined_key(file["name"])
        if key:
            manifest["bdf_combined"][key] = entry
            continue
        print(f"  [?] Unrecognized chapter filename: {file['name']}")

    print("  Scanning BDF sessions/...")
    for file in _list_folder(service, drive_folders["bdf_sessions"]):
        key = _session_key(file["name"])
        if key:
            manifest["sessions"][key] = {
                "drive_id":      file["id"],
                "filename":      file["name"],
                "modified_time": file["modifiedTime"],
                "size_bytes":    int(file.get("size", 0)),
            }
        else:
            print(f"  [?] Unrecognized session filename: {file['name']}")

    print("  Scanning BRAIN_OS chapters/...")
    for file in _list_folder(service, drive_folders["brainos_chapters"]):
        key = _brainos_key(file["name"])
        if key:
            manifest["brainos_chapters"][key] = {
                "drive_id":      file["id"],
                "filename":      file["name"],
                "modified_time": file["modifiedTime"],
                "size_bytes":    int(file.get("size", 0)),
            }
        else:
            print(f"  [?] Unrecognized BRAIN_OS chapter filename: {file['name']}")

    print("  Scanning BRAIN_OS sessions/...")
    for file in _list_folder(service, drive_folders["brainos_sessions"]):
        key = _brainos_key(file["name"])
        if key:
            manifest["brainos_sessions"][key] = {
                "drive_id":      file["id"],
                "filename":      file["name"],
                "modified_time": file["modifiedTime"],
                "size_bytes":    int(file.get("size", 0)),
            }
        else:
            print(f"  [?] Unrecognized BRAIN_OS session filename: {file['name']}")

    return manifest


# ── Upload ────────────────────────────────────────────────────────────────────

def _detect_upload_folder(filename: str) -> str:
    """Return 'sessions', 'chapters', or 'tools' based on filename pattern."""
    if re.match(r"_session_.+_combined_af_heart_audio\.mp3$", filename):
        return "sessions"
    if re.match(r"SESSION_.+_audio\.mp3$", filename):
        return "sessions"
    if filename.lower().endswith(".wav"):
        return "tools"
    return "chapters"


def upload_file(service, local_path: Path, folder_key: str, drive_folders: dict) -> None:
    """Upload a local file to the given BDF Drive folder, updating in-place if it already exists."""
    if not local_path.exists():
        sys.exit(f"[!] File not found: {local_path}")

    mime_type, _ = mimetypes.guess_type(str(local_path))
    if mime_type is None:
        mime_type = "application/octet-stream"

    folder_id = drive_folders[folder_key]
    media = MediaFileUpload(str(local_path), mimetype=mime_type, resumable=True, chunksize=50 * 1024 * 1024)

    print(f"\nUploading {local_path.name} → {folder_key}/ ...")

    existing = service.files().list(
        q=f"name = '{local_path.name}' and '{folder_id}' in parents and trashed = false",
        fields="files(id, name)",
        pageSize=1,
    ).execute().get("files", [])

    if existing:
        existing_id = existing[0]["id"]
        result = service.files().update(
            fileId=existing_id,
            media_body=media,
            fields="id, name",
        ).execute()
        print(f"  [updated] {result['name']} — id: {result['id']}")
    else:
        file_metadata = {"name": local_path.name, "parents": [folder_id]}
        result = service.files().create(
            body=file_metadata,
            media_body=media,
            fields="id, name",
        ).execute()
        print(f"  [upload] {result['name']} — id: {result['id']}")


# ── Normalize ─────────────────────────────────────────────────────────────────

_TIMESTAMP_KEY_RE = re.compile(r"^\d{8}_\d{4}$")

_SECTION_FOLDER: dict[str, str] = {
    "chapters":         "bdf_chapters",
    "sessions":         "bdf_sessions",
    "bdf_anchors":      "bdf_chapters",
    "bdf_combined":     "bdf_chapters",
    "brainos_chapters": "brainos_chapters",
    "brainos_sessions": "brainos_sessions",
}


def _canonical_filename(section: str, key: str) -> str | None:
    """
    Return the expected filename for a manifest entry, or None if the entry is
    not normalizable (named sessions, unknown sections).

    chapters:         ch01_pipeline_architecture → ch01_pipeline_architecture_af_heart_audio.mp3
    sessions:         20260426_2043              → _session_20260426_2043_combined_af_heart_audio.mp3
    sessions (named): BDF_Session_Summary_*      → None  (skip)
    brainos_chapters: claudeguide_mcp_setup      → claudeguide_mcp_setup.wav
    brainos_sessions: (empty)                    → None
    """
    if section == "chapters":
        return f"{key}_af_heart_audio.mp3"
    if section == "sessions":
        if _TIMESTAMP_KEY_RE.match(key):
            return f"_session_{key}_combined_af_heart_audio.mp3"
        return None
    if section in ("bdf_anchors", "bdf_combined"):
        return f"{key}.mp3"
    if section == "brainos_chapters":
        return f"{key}.wav"
    return None


def _drive_file_exists(service, folder_id: str, filename: str) -> bool:
    """Return True if filename already exists (non-trashed) in folder_id on Drive."""
    resp = service.files().list(
        q=f"name = '{filename}' and '{folder_id}' in parents and trashed = false",
        fields="files(id)",
        pageSize=1,
    ).execute()
    return bool(resp.get("files"))


def normalize_manifest(service, drive_folders: dict, dry_run: bool = False) -> None:
    """
    Scan the manifest for ALTERNATE entries (filename != canonical form) and
    rename them on Drive to match the canonical naming convention.

    Safety: collision check runs before every rename.  --dry-run prints the
    plan without touching Drive or the manifest file.
    """
    if not MANIFEST_PATH.exists():
        print("[!] Manifest not found — run: python C:/BRAIN_OS/09_TOOLS/drive_sync.py")
        return

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    print("=" * 60)
    prefix = "--normalize  [DRY RUN — no changes applied]" if dry_run else "--normalize"
    print(prefix)
    print("=" * 60)

    total_found = 0
    total_renamed = 0
    total_skipped = 0

    for section, folder_key in _SECTION_FOLDER.items():
        entries: dict = manifest.get(section, {})
        if not entries:
            continue

        folder_id = drive_folders.get(folder_key)
        if not folder_id:
            print(f"\n  [!] No Drive folder configured for section '{section}' — skipping")
            continue

        alternates = []
        for key, entry in entries.items():
            expected = _canonical_filename(section, key)
            if expected is None or entry["filename"] == expected:
                continue
            alternates.append((key, entry, expected))

        if not alternates:
            continue

        print(f"\n  [{section.upper()}] {len(alternates)} ALTERNATE(s)")

        for key, entry, expected in alternates:
            total_found += 1
            drive_id       = entry["drive_id"]
            current_name   = entry["filename"]

            print(f"\n    key:      {key}")
            print(f"    id:       {drive_id}")
            print(f"    current:  {current_name}")
            print(f"    expected: {expected}")

            if dry_run:
                print(f"    action:   [dry-run] would rename on Drive and update manifest")
                continue

            if _drive_file_exists(service, folder_id, expected):
                print(f"    action:   [SKIP] collision — '{expected}' already exists on Drive")
                total_skipped += 1
                continue

            try:
                service.files().update(
                    fileId=drive_id,
                    body={"name": expected},
                    fields="id, name",
                ).execute()
            except Exception as exc:
                print(f"    action:   [ERROR] Drive rename failed: {exc}")
                total_skipped += 1
                continue

            manifest[section][key]["filename"] = expected
            total_renamed += 1
            print(f"    action:   [renamed]")

    print()
    if total_found == 0:
        print("[normalize] No ALTERNATE entries found — manifest is already canonical.")
        return

    if dry_run:
        print(f"[normalize] {total_found} ALTERNATE(s) found — dry-run complete, nothing changed.")
        return

    print(f"[normalize] {total_found} found / {total_renamed} renamed / {total_skipped} skipped")

    if total_renamed > 0:
        manifest["last_synced"] = datetime.now(timezone.utc).isoformat()
        MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[manifest] updated → {MANIFEST_PATH}")


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    # Ported from BDF 2026-09-01. It prints non-ASCII (arrows, box drawing)
    # and Windows' default console codepage cannot encode them, so a print
    # raised UnicodeEncodeError under system Python while working under
    # BDF's venv. The interpreter was masking a defect in this file.
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

    drive_folders = _load_drive_folders()

    parser = argparse.ArgumentParser(description="BDF Drive Manifest Sync")
    parser.add_argument(
        "--upload",
        metavar="FILE",
        help="Upload a local file to Drive (folder auto-detected), then sync the manifest",
    )
    parser.add_argument(
        "--folder",
        choices=list(drive_folders.keys()),
        help="Override destination folder (default: auto-detected from filename)",
    )
    parser.add_argument(
        "--get-token",
        action="store_true",
        help="Print the current Drive startPageToken to stdout and exit",
    )
    parser.add_argument(
        "--normalize",
        action="store_true",
        help="Rename ALTERNATE-format Drive files to the canonical convention and update the manifest",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview --normalize changes without renaming anything on Drive",
    )
    args = parser.parse_args()

    service = _get_drive_service()

    if args.get_token:
        print(service.changes().getStartPageToken().execute().get("startPageToken", ""))
        return

    if args.normalize:
        normalize_manifest(service, drive_folders, dry_run=args.dry_run)
        return

    if args.dry_run and not args.normalize:
        print("[!] --dry-run only applies with --normalize")
        return

    print("=" * 60)
    print("BDF Drive Manifest Sync")
    print("=" * 60)

    print("\nConnecting to Google Drive... OK")

    if args.upload:
        local_path = Path(args.upload)
        folder_key = args.folder or _detect_upload_folder(local_path.name)
        upload_file(service, local_path, folder_key, drive_folders)

    print("\nScanning BDF audio library...")
    manifest = build_manifest(service, drive_folders)

    ch_count      = len(manifest["chapters"])
    s_count       = len(manifest["sessions"])
    anchor_count  = len(manifest["bdf_anchors"])
    combined_count = len(manifest["bdf_combined"])
    bch_count     = len(manifest["brainos_chapters"])
    bs_count      = len(manifest["brainos_sessions"])

    start_page_token = service.changes().getStartPageToken().execute().get("startPageToken", "")
    manifest["start_page_token"] = start_page_token

    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\n[manifest] written → {MANIFEST_PATH}")
    print(f"  bdf_chapters:     {ch_count}")
    print(f"  bdf_anchors:      {anchor_count}")
    print(f"  bdf_combined:     {combined_count}")
    print(f"  bdf_sessions:     {s_count}")
    print(f"  brainos_chapters: {bch_count}")
    print(f"  brainos_sessions: {bs_count}")
    print(f"  synced:           {manifest['last_synced'][:19].replace('T', ' ')} UTC")


if __name__ == "__main__":
    main()
