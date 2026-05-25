"""
drive_cleanup_phases.py — Clean up empty phase folders on Drive
Deletes empty Phase_0X folders, keeps only folders with files.
Creates a top-level "BRAIN_OS Learning Path" shortcut folder.

Usage:
    python drive_cleanup_phases.py --dry-run
    python drive_cleanup_phases.py
"""

import argparse
import sys
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

TOKEN_FILE = Path(r"C:\Dev\Projects\soccer-content-generator\gdrive_token.json")


def get_service():
    creds = Credentials.from_authorized_user_file(str(TOKEN_FILE))
    return build("drive", "v3", credentials=creds)


def list_children(service, folder_id: str) -> list:
    """List all files/folders inside a folder."""
    results = []
    page_token = None
    while True:
        resp = service.files().list(
            q=f"'{folder_id}' in parents and trashed=false",
            fields="files(id,name,mimeType),nextPageToken",
            pageToken=page_token
        ).execute()
        results.extend(resp.get("files", []))
        page_token = resp.get("nextPageToken")
        if not page_token:
            break
    return results


def find_phase_folders(service) -> list:
    """Find all Phase_0X folders on Drive."""
    results = []
    page_token = None
    while True:
        resp = service.files().list(
            q="mimeType='application/vnd.google-apps.folder' and name contains 'Phase_' and trashed=false",
            fields="files(id,name,parents),nextPageToken",
            pageToken=page_token
        ).execute()
        results.extend(resp.get("files", []))
        page_token = resp.get("nextPageToken")
        if not page_token:
            break
    return results


def trash_folder(service, folder_id: str):
    """Move folder to trash."""
    service.files().update(
        fileId=folder_id,
        body={"trashed": True}
    ).execute()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    service = get_service()

    print("[cleanup] Scanning Phase folders on Drive...")
    phase_folders = find_phase_folders(service)
    print(f"[cleanup] Found {len(phase_folders)} Phase folders total")

    empty = []
    populated = []

    for folder in phase_folders:
        children = list_children(service, folder["id"])
        if children:
            populated.append((folder, children))
        else:
            empty.append(folder)

    print(f"\n  POPULATED ({len(populated)}):")
    for folder, children in populated:
        print(f"    ✅ {folder['name']} — {len(children)} files")

    print(f"\n  EMPTY ({len(empty)}) — will be deleted:")
    for folder in empty:
        print(f"    🗑  {folder['name']} (id: {folder['id']})")

    if args.dry_run:
        print("\n[cleanup] Dry run — nothing deleted.")
        return

    if not empty:
        print("\n[cleanup] No empty folders to delete.")
        return

    confirm = input(f"\nDelete {len(empty)} empty folders? [y/N] ").strip().lower()
    if confirm != "y":
        print("[cleanup] Aborted.")
        return

    for folder in empty:
        trash_folder(service, folder["id"])
        print(f"  🗑  Deleted: {folder['name']}")

    print(f"\n[cleanup] Done. {len(empty)} empty folders deleted.")
    print(f"[cleanup] {len(populated)} folders with content preserved.")


if __name__ == "__main__":
    main()
