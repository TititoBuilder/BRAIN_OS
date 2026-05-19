"""
drive_sync.py — sync local BRAIN_OS folders to Google Drive.

Folder IDs are read at runtime from BRAIN_OS_CONFIG.json so that
changing a folder ID never requires editing this script.
"""

import argparse
import json
from pathlib import Path


def _load_drive_folders() -> dict:
    config_path = Path(r"C:\BRAIN_OS\BRAIN_OS_CONFIG.json")
    config = json.loads(config_path.read_text(encoding="utf-8"))
    return config["drive_folders"]


def main() -> None:
    drive_folders = _load_drive_folders()

    parser = argparse.ArgumentParser(description="Sync files to Google Drive.")
    parser.add_argument(
        "--folder",
        choices=list(drive_folders.keys()),
        required=True,
        help="Which Drive folder to sync to.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print actions without uploading.",
    )
    args = parser.parse_args()

    folder_id = drive_folders[args.folder]
    print(f"Target folder: {args.folder} ({folder_id})")

    if args.dry_run:
        print("[dry-run] No files uploaded.")
        return

    # TODO: implement upload logic using Google Drive API
    raise NotImplementedError("Upload logic not yet implemented.")


if __name__ == "__main__":
    main()
