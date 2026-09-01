r"""
category: Google Drive
get_drive_ids.py — Print name and Drive ID for every file in a folder.

Output is one "name | id" line per file, for capturing IDs into
drive_index.json. Pass the folder ID with --folder; it is not hardcoded.

Usage:
    python get_drive_ids.py --folder 1AbC...
    python get_drive_ids.py --folder 1AbC... --include-folders
"""
import argparse

from drive_service import get_service


def list_folder(service, folder_id: str, include_folders: bool) -> list[dict]:
    """Return every file in folder_id, paging until the results are exhausted."""
    q = f"'{folder_id}' in parents and trashed=false"
    if not include_folders:
        q += " and mimeType != 'application/vnd.google-apps.folder'"

    files, page_token = [], None
    while True:
        resp = service.files().list(
            q=q,
            fields="files(id,name),nextPageToken",
            pageSize=100,
            pageToken=page_token,
        ).execute()
        files.extend(resp.get("files", []))
        page_token = resp.get("nextPageToken")
        if not page_token:
            break
    return files


def main() -> None:
    ap = argparse.ArgumentParser(description="List Drive file names and IDs for one folder")
    ap.add_argument("--folder", required=True, help="Drive folder ID")
    ap.add_argument("--include-folders", action="store_true", help="include subfolders in the output")
    args = ap.parse_args()

    files = list_folder(get_service(), args.folder, args.include_folders)
    for f in sorted(files, key=lambda x: x["name"]):
        print(f["name"] + " | " + f["id"])
    print(f"\n{len(files)} items")


if __name__ == "__main__":
    main()
