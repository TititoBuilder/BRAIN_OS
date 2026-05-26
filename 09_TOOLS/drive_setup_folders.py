#!/usr/bin/env python3
"""
drive_setup_folders.py
Creates the Knowledge_OS domain folder tree on Google Drive
and moves session_01_knowledge_os.mp3 from root into Knowledge_OS/.
"""

import sys
from pathlib import Path

CREDS_FILE = Path(r"C:\Dev\Projects\soccer-content-generator\gdrive_credentials.json")
TOKEN_FILE  = Path(r"C:\Dev\Projects\soccer-content-generator\gdrive_token.json")
SCOPES      = ["https://www.googleapis.com/auth/drive"]

DOMAIN_FOLDERS = [
    "AI_ML",
    "Systems_Design",
    "Python",
    "Data_Engineering",
    "APIs_Protocols",
    "Cloud_DevOps",
    "Audio_Media",
    "Knowledge_Systems",
    "Security",
]

SESSION_FILE = "session_01_knowledge_os.mp3"


# ── Auth ──────────────────────────────────────────────────────────────────

def get_service():
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            TOKEN_FILE.write_text(creds.to_json())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)
            TOKEN_FILE.write_text(creds.to_json())

    return build("drive", "v3", credentials=creds)


# ── Helpers ───────────────────────────────────────────────────────────────

FOLDER_MIME = "application/vnd.google-apps.folder"


def find_folder(service, name: str, parent_id: str) -> str | None:
    """Return folder ID if it exists under parent, else None."""
    q = (
        f"name='{name}' and mimeType='{FOLDER_MIME}' "
        f"and '{parent_id}' in parents and trashed=false"
    )
    resp = service.files().list(q=q, fields="files(id)").execute()
    items = resp.get("files", [])
    return items[0]["id"] if items else None


def ensure_folder(service, name: str, parent_id: str) -> tuple[str, bool]:
    """Return (folder_id, created). Creates only if missing."""
    fid = find_folder(service, name, parent_id)
    if fid:
        return fid, False
    body = {"name": name, "mimeType": FOLDER_MIME, "parents": [parent_id]}
    f = service.files().create(body=body, fields="id").execute()
    return f["id"], True


def find_file_in_root(service, name: str) -> str | None:
    """Find a file by name in My Drive root."""
    q = f"name='{name}' and 'root' in parents and trashed=false"
    resp = service.files().list(q=q, fields="files(id, name)").execute()
    items = resp.get("files", [])
    return items[0]["id"] if items else None


def move_file(service, file_id: str, new_parent_id: str, old_parent_id: str = "root"):
    """Move file to new_parent, removing from old_parent."""
    service.files().update(
        fileId=file_id,
        addParents=new_parent_id,
        removeParents=old_parent_id,
        fields="id, parents",
    ).execute()


# ── Main ──────────────────────────────────────────────────────────────────

def main():
    print()
    print("=" * 60)
    print("  KNOWLEDGE_OS — Drive folder setup")
    print("=" * 60)

    service = get_service()

    # ── 1. Knowledge_OS root ─────────────────────────────────────
    ko_id, created = ensure_folder(service, "Knowledge_OS", "root")
    tag = "[CREATED]" if created else "[EXISTS] "
    print(f"\n  {tag}  Knowledge_OS/")

    # ── 2. Domain folders + subfolders ───────────────────────────
    created_count = 0
    exists_count  = 0

    for domain in DOMAIN_FOLDERS:
        d_id, d_new = ensure_folder(service, domain, ko_id)
        tag = "[CREATED]" if d_new else "[EXISTS] "
        print(f"  {tag}  Knowledge_OS/{domain}/")
        if d_new:
            created_count += 1
        else:
            exists_count  += 1

        for sub in ("sessions", "raw_audio"):
            _, s_new = ensure_folder(service, sub, d_id)
            s_tag = "[CREATED]" if s_new else "[EXISTS] "
            print(f"  {s_tag}    Knowledge_OS/{domain}/{sub}/")
            if s_new:
                created_count += 1
            else:
                exists_count  += 1

    # ── 3. Move session_01_knowledge_os.mp3 ──────────────────────
    print()
    print(f"  Locating {SESSION_FILE} in Drive root...")
    file_id = find_file_in_root(service, SESSION_FILE)
    if file_id:
        move_file(service, file_id, ko_id)
        print(f"  [MOVED]   {SESSION_FILE}")
        print(f"         -> Knowledge_OS/{SESSION_FILE}")
    else:
        print(f"  [SKIP]    {SESSION_FILE} not found in Drive root (may already be moved)")

    # ── Summary ──────────────────────────────────────────────────
    total = 1 + len(DOMAIN_FOLDERS) * 3  # root + 9*(domain+sessions+raw_audio)
    print()
    print("=" * 60)
    print(f"  Folders created : {created_count}")
    print(f"  Already existed : {exists_count  + (0 if created else 1)}")
    print(f"  Total expected  : {total}")
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()
