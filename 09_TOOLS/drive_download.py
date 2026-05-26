#!/usr/bin/env python3
"""
drive_download.py — Download specific Drive files by folder_path, rename to machine_key.
Usage: python drive_download.py
"""

import sys
from pathlib import Path

CREDS_FILE = Path(r"C:\Dev\Projects\soccer-content-generator\gdrive_credentials.json")
TOKEN_FILE  = Path(r"C:\Dev\Projects\soccer-content-generator\gdrive_token.json")
SCOPES      = ["https://www.googleapis.com/auth/drive"]
OUTPUT_DIR  = Path(r"C:\BRAIN_OS\audio_staging")

DOWNLOADS = [
    (
        "BDF KNOWLEDGE BOOK/BDF/chapters/Phase_03_BDF_Pipeline/ch04_lancedb_rag_af_heart_audio.mp3",
        "rag_pipelines.mp3",
    ),
    (
        "BDF KNOWLEDGE BOOK/BDF/chapters/Phase_03_BDF_Pipeline/ch01_pipeline_architecture_af_heart_audio.mp3",
        "etl_pipelines.mp3",
    ),
    (
        "CA_Book_Audio/chapters/ch04_agents.wav",
        "agent_orchestration.wav",
    ),
    (
        "CA_Book_Audio/chapters/ch07_deployment.wav",
        "monolith_vs_microservices.wav",
    ),
    (
        "CA_Book_Audio/chapters/ch11_architecture.wav",
        "federated_systems.wav",
    ),
    (
        "BRAIN_OS_Handbook/chapters/Phase_02_Architecture/mcp_registry_audio.mp3",
        "mcp_protocol.mp3",
    ),
    (
        "BRAIN_OS_Handbook/chapters/Phase_05_Programming_Fundamentals/resolve_mcp_guide.wav",
        "model_context_protocol.wav",
    ),
]


def get_drive_service():
    try:
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
    except ImportError:
        print("ERROR: Google libraries not installed.")
        sys.exit(1)

    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            TOKEN_FILE.write_text(creds.to_json())
        else:
            if not CREDS_FILE.exists():
                print(f"ERROR: Credentials not found at {CREDS_FILE}")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)
            TOKEN_FILE.write_text(creds.to_json())

    return build("drive", "v3", credentials=creds)


def find_item_by_path(service, folder_path: str):
    """Walk folder_path components top-down, return the final file dict or None."""
    parts = folder_path.split("/")
    parent_id = "root"
    item = None

    for i, part in enumerate(parts):
        is_last = (i == len(parts) - 1)
        escaped = part.replace("'", "\\'")

        if is_last:
            q = f"name='{escaped}' and '{parent_id}' in parents and trashed=false"
        else:
            q = (
                f"name='{escaped}' and mimeType='application/vnd.google-apps.folder' "
                f"and '{parent_id}' in parents and trashed=false"
            )

        resp = service.files().list(
            q=q,
            fields="files(id, name, mimeType, size)",
            pageSize=10,
        ).execute()

        items = resp.get("files", [])
        if not items:
            return None, f"not found at step [{part}]"

        item = items[0]
        parent_id = item["id"]

    return item, None


def download_file(service, file_id: str, dest_path: Path, label: str):
    from googleapiclient.http import MediaIoBaseDownload

    request = service.files().get_media(fileId=file_id)

    with open(dest_path, "wb") as fh:
        dl = MediaIoBaseDownload(fh, request, chunksize=8 * 1024 * 1024)
        done = False
        while not done:
            status, done = dl.next_chunk()
            if status:
                pct = int(status.progress() * 100)
                filled = pct // 5
                bar = "#" * filled + "." * (20 - filled)
                print(f"  [{bar}] {pct:3d}%  {label}", end="\r", flush=True)

    size_mb = dest_path.stat().st_size / (1024 * 1024)
    print(f"  [{'#'*20}] 100%  {label}  -- {size_mb:.1f} MB          ")
    return size_mb


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print()
    print("=" * 64)
    print("  DRIVE DOWNLOAD — Knowledge OS audio staging")
    print(f"  Output : {OUTPUT_DIR}")
    print("=" * 64)

    service = get_drive_service()

    ok = 0
    total_mb = 0.0

    for idx, (folder_path, dest_name) in enumerate(DOWNLOADS, 1):
        src_name = folder_path.split("/")[-1]
        dest_path = OUTPUT_DIR / dest_name

        print(f"\n  [{idx}/{len(DOWNLOADS)}] {src_name}")
        print(f"         -> {dest_name}")

        item, err = find_item_by_path(service, folder_path)
        if err:
            print(f"  [ERROR] {err}")
            continue

        mb = download_file(service, item["id"], dest_path, dest_name)
        total_mb += mb
        ok += 1

    print()
    print("=" * 64)
    print(f"  Downloaded : {ok}/{len(DOWNLOADS)} files")
    print(f"  Total size : {total_mb:.1f} MB")
    print(f"  Location   : {OUTPUT_DIR}")
    print("=" * 64)
    print()


if __name__ == "__main__":
    main()
