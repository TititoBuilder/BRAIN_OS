#!/usr/bin/env python3
"""
drive_browser.py -- Knowledge OS Drive Organizer
=================================================
Audits Google Drive audio folders and reorganizes them
to match Knowledge OS machine_key naming convention.

Location : C:\\BRAIN_OS\\09_TOOLS\\drive_browser.py
Venv     : C:\\Knowledge\\CA\\venv\\Scripts\\python.exe
Creds    : C:\\Dev\\Projects\\soccer-content-generator\\gdrive_credentials.json
Token    : C:\\Dev\\Projects\\soccer-content-generator\\gdrive_token.json

Usage:
    # Audit only — see all files
    python drive_browser.py --audit

    # Show rename plan — no changes made
    python drive_browser.py --plan

    # Execute full reorganization
    python drive_browser.py --execute

    # Create Knowledge_OS folder structure on Drive
    python drive_browser.py --setup-folders
"""

import argparse
import json
import sys
from pathlib import Path

CREDS_FILE = Path(r"C:\Dev\Projects\soccer-content-generator\gdrive_credentials.json")
TOKEN_FILE  = Path(r"C:\Dev\Projects\soccer-content-generator\gdrive_token.json")
SCOPES      = ["https://www.googleapis.com/auth/drive"]

AUDIO_FOLDERS = ["BRAIN_OS_Handbook", "CA_Book_Audio", "BDF KNOWLEDGE BOOK", "Tools"]

# Knowledge OS domain → Drive subfolder name
DOMAIN_FOLDERS = {
    "AI/ML":              "AI_ML",
    "Systems Design":     "Systems_Design",
    "Python":             "Python",
    "Data Engineering":   "Data_Engineering",
    "APIs & Protocols":   "APIs_Protocols",
    "Cloud & DevOps":     "Cloud_DevOps",
    "Audio & Media":      "Audio_Media",
    "Knowledge Systems":  "Knowledge_Systems",
    "Security":           "Security",
}

# Known filename → machine_key mapping
# Add more as you discover files
FILE_MAP = {
    # BRAIN_OS_Handbook
    "ch01": "pkm_fundamentals",
    "ch02": "obsidian_workflows",
    "ch03": "knowledge_graph_design",
    "ch04": "graph_databases",
    "chapter_01": "pkm_fundamentals",
    "chapter_02": "obsidian_workflows",
    "chapter_03": "knowledge_graph_design",
    "chapter_04": "graph_databases",
    # CA_Book_Audio
    "ch05": "python_asyncio",
    "ch06": "rest_api_design",
    "ch07": "agent_orchestration",
    "ch08": "federated_systems",
    "ch09": "etl_pipelines",
    "chapter_05": "python_asyncio",
    "chapter_06": "rest_api_design",
    "chapter_07": "agent_orchestration",
    # BDF KNOWLEDGE BOOK
    "bdf_ch01": "llm_fundamentals",
    "bdf_ch02": "rag_pipelines",
    "bdf_ch03": "vector_embeddings",
    "bdf_ch04": "retrieval_systems",
    "bdf_ch05": "llm_data_pipelines",
    # Tools/Claudeguide
    "claude_code_workflow":      "model_context_protocol",
    "claude_md_standards":       "prompt_engineering",
    "mcp_setup":                 "model_context_protocol",
    "prompting_architecture":    "prompt_engineering",
    "skills_system":             "function_calling",
    # BrainOS audio files found locally
    "final_resume_from_tools_to_voice": "audio_pipeline_design",
    "master":                           "pkm_fundamentals",
    "programming_terminology_reference":"llm_fundamentals",
    "resolve_mcp_guide":                "model_context_protocol",
}


# ─── Auth ─────────────────────────────────────────────────────────────────

def get_drive_service():
    try:
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
    except ImportError:
        print("ERROR: Google libraries not installed.")
        print("  Run: C:\\Knowledge\\CA\\venv\\Scripts\\pip install google-api-python-client google-auth-oauthlib")
        sys.exit(1)

    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDS_FILE.exists():
                print(f"ERROR: Credentials not found at {CREDS_FILE}")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)
        TOKEN_FILE.write_text(creds.to_json())

    return build("drive", "v3", credentials=creds)


# ─── Drive helpers ────────────────────────────────────────────────────────

def list_folder(service, folder_id: str, prefix: str = "") -> list[dict]:
    """Recursively list all files in a folder and its subfolders.
    Each returned file dict gains a 'folder_path' key, e.g.
    'BRAIN_OS_Handbook/chapters/ch01.wav'.
    """
    files = []
    page_token = None
    while True:
        resp = service.files().list(
            q=f"'{folder_id}' in parents and trashed=false",
            fields="nextPageToken, files(id, name, mimeType, size, parents)",
            pageToken=page_token,
            pageSize=100
        ).execute()
        for item in resp.get("files", []):
            if item["mimeType"] == "application/vnd.google-apps.folder":
                sub_prefix = f"{prefix}/{item['name']}" if prefix else item["name"]
                files.extend(list_folder(service, item["id"], prefix=sub_prefix))
            else:
                item["folder_path"] = f"{prefix}/{item['name']}" if prefix else item["name"]
                files.append(item)
        page_token = resp.get("nextPageToken")
        if not page_token:
            break
    return files


def find_folder(service, name: str, parent_id: str = None) -> dict | None:
    """Find a folder by name, optionally under a parent."""
    q = f"name='{name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    if parent_id:
        q += f" and '{parent_id}' in parents"
    resp = service.files().list(q=q, fields="files(id, name, parents)").execute()
    files = resp.get("files", [])
    return files[0] if files else None


def create_folder(service, name: str, parent_id: str = None) -> str:
    """Create a folder, return its ID."""
    meta = {
        "name": name,
        "mimeType": "application/vnd.google-apps.folder"
    }
    if parent_id:
        meta["parents"] = [parent_id]
    f = service.files().create(body=meta, fields="id").execute()
    print(f"  [CREATED] folder: {name}")
    return f["id"]


def move_and_rename(service, file_id: str, new_name: str, new_parent_id: str, old_parent_id: str):
    """Move a file to a new folder and rename it."""
    service.files().update(
        fileId=file_id,
        addParents=new_parent_id,
        removeParents=old_parent_id,
        body={"name": new_name},
        fields="id, name, parents"
    ).execute()


def normalize(name: str) -> str:
    """Normalize a filename for machine_key matching."""
    stem = Path(name).stem.lower()
    import re
    return re.sub(r"[^a-z0-9]+", "_", stem).strip("_")


# ─── Audit ────────────────────────────────────────────────────────────────

def audit(service):
    print()
    print("=" * 66)
    print("  DRIVE AUDIT — Knowledge OS")
    print("=" * 66)

    total = 0
    results = []

    for folder_name in AUDIO_FOLDERS:
        folder = find_folder(service, folder_name)
        if not folder:
            print(f"\n  [MISS] Folder not found: {folder_name}")
            continue

        files = list_folder(service, folder["id"], prefix=folder_name)

        print(f"\n  [{folder_name}]  ({len(files)} files)")
        for f in sorted(files, key=lambda x: x["folder_path"]):
            norm   = normalize(f["name"])
            mapped = FILE_MAP.get(norm, "-- no mapping --")
            size   = int(f.get("size", 0)) // (1024*1024)
            marker = "[OK]" if mapped != "-- no mapping --" else "[?] "
            path   = f["folder_path"]
            print(f"    {marker}  {path:<55}  {size:>4}MB  -> {mapped}")
            total += 1
            actual_parent = f.get("parents", [folder["id"]])[0]
            results.append({"file": f, "folder": folder_name, "folder_id": actual_parent, "norm": norm, "mapped": mapped})

    print()
    print(f"  Total files : {total}")
    mapped_count = sum(1 for r in results if r["mapped"] != "-- no mapping --")
    print(f"  Mapped      : {mapped_count}/{total}")
    print(f"  Unmapped    : {total - mapped_count}  (update FILE_MAP in script)")
    print("=" * 66)
    print()
    return results


# ─── Setup folders ────────────────────────────────────────────────────────

def setup_folders(service) -> dict[str, str]:
    """Create Knowledge_OS/domain/ folder structure on Drive. Returns domain->id map."""
    print("\n  Setting up Knowledge_OS folder structure...")

    root = find_folder(service, "Knowledge_OS")
    if not root:
        root_id = create_folder(service, "Knowledge_OS")
    else:
        root_id = root["id"]
        print(f"  [OK] Knowledge_OS already exists")

    domain_ids = {}
    for domain, fname in DOMAIN_FOLDERS.items():
        existing = find_folder(service, fname, parent_id=root_id)
        if existing:
            domain_ids[domain] = existing["id"]
            print(f"  [OK] {fname} already exists")
        else:
            domain_ids[domain] = create_folder(service, fname, parent_id=root_id)

    print(f"  [OK] Structure ready\n")
    return domain_ids


# ─── Plan ─────────────────────────────────────────────────────────────────

def show_plan(service):
    results = audit(service)
    mapped  = [r for r in results if r["mapped"] != "-- no mapping --"]

    print("=" * 66)
    print("  REORGANIZATION PLAN")
    print("  Files will be renamed to machine_key and moved to")
    print("  Knowledge_OS/{domain}/ on Drive")
    print("=" * 66)

    # Load topic domain map from local obsidian_sync.json if available
    sync_path = Path(r"C:\BRAIN_OS\09_TOOLS\obsidian_sync.json")
    key_to_domain = {}
    if sync_path.exists():
        with open(sync_path) as f:
            data = json.load(f)
        topics = data if isinstance(data, list) else data.get("topics", [])
        key_to_domain = {t["machine_key"]: t["domain"] for t in topics}

    print()
    for r in mapped:
        ext    = Path(r["file"]["name"]).suffix
        new_name = f"{r['mapped']}{ext}"
        domain = key_to_domain.get(r["mapped"], "Unknown")
        folder = DOMAIN_FOLDERS.get(domain, "Unknown")
        print(f"  {r['file']['name']}")
        print(f"    -> Knowledge_OS/{folder}/{new_name}")
        print()

    unmapped = [r for r in results if r["mapped"] == "-- no mapping --"]
    if unmapped:
        print(f"  UNMAPPED ({len(unmapped)} files — add to FILE_MAP):")
        for r in unmapped:
            print(f"    {r['file']['name']}  [{r['norm']}]")
    print()


# ─── Execute ──────────────────────────────────────────────────────────────

def execute(service):
    print("\n  Loading plan...")
    results = audit(service)
    mapped  = [r for r in results if r["mapped"] != "-- no mapping --"]

    sync_path = Path(r"C:\BRAIN_OS\09_TOOLS\obsidian_sync.json")
    key_to_domain = {}
    if sync_path.exists():
        with open(sync_path) as f:
            data = json.load(f)
        topics = data if isinstance(data, list) else data.get("topics", [])
        key_to_domain = {t["machine_key"]: t["domain"] for t in topics}

    domain_ids = setup_folders(service)

    print("=" * 66)
    print("  EXECUTING REORGANIZATION")
    print("=" * 66)
    print()

    moved = 0
    for r in mapped:
        ext      = Path(r["file"]["name"]).suffix
        new_name = f"{r['mapped']}{ext}"
        domain   = key_to_domain.get(r["mapped"], "")
        dest_id  = domain_ids.get(domain)

        if not dest_id:
            print(f"  [SKIP] No domain folder for: {r['mapped']} (domain: {domain})")
            continue

        move_and_rename(service, r["file"]["id"], new_name, dest_id, r["folder_id"])
        print(f"  [MOVED] {r['file']['name']}")
        print(f"          -> Knowledge_OS/{DOMAIN_FOLDERS.get(domain,'?')}/{new_name}")
        moved += 1

    print()
    print("=" * 66)
    print(f"  Moved   : {moved}")
    print(f"  Skipped : {len(mapped) - moved}")
    print("=" * 66)
    print()


# ─── Upload ───────────────────────────────────────────────────────────────

def upload_file(service, local_path: Path, domain: str = None):
    """Upload a file to Knowledge_OS/{domain}/sessions/ or Knowledge_OS/ if no domain."""
    from googleapiclient.http import MediaFileUpload

    if not local_path.exists():
        print(f"ERROR: File not found: {local_path}")
        return

    file_size = local_path.stat().st_size

    # ── Resolve destination folder ────────────────────────────────
    ko = find_folder(service, "Knowledge_OS")
    if not ko:
        print("  [NEW] Knowledge_OS/")
        ko_id = create_folder(service, "Knowledge_OS")
    else:
        ko_id = ko["id"]

    if domain:
        dest_label = f"Knowledge_OS/{domain}/sessions/"
        d_folder = find_folder(service, domain, parent_id=ko_id)
        if not d_folder:
            print(f"  [NEW] Knowledge_OS/{domain}/")
            d_id = create_folder(service, domain, parent_id=ko_id)
        else:
            d_id = d_folder["id"]

        s_folder = find_folder(service, "sessions", parent_id=d_id)
        if not s_folder:
            print(f"  [NEW] Knowledge_OS/{domain}/sessions/")
            folder_id = create_folder(service, "sessions", parent_id=d_id)
        else:
            folder_id = s_folder["id"]
    else:
        dest_label = "Knowledge_OS/"
        folder_id = ko_id

    # ── Upload ────────────────────────────────────────────────────
    ext = local_path.suffix.lower()
    mime_map = {".mp3": "audio/mpeg", ".wav": "audio/wav", ".m4a": "audio/mp4", ".ogg": "audio/ogg"}
    mime_type = mime_map.get(ext, "application/octet-stream")

    media = MediaFileUpload(
        str(local_path),
        mimetype=mime_type,
        resumable=True,
        chunksize=8 * 1024 * 1024,
    )

    request = service.files().create(
        body={"name": local_path.name, "parents": [folder_id]},
        media_body=media,
        fields="id, name, webViewLink",
    )

    print(f"\n  File   : {local_path.name}")
    print(f"  Size   : {file_size / (1024*1024):.1f} MB")
    print(f"  Dest   : {dest_label}")
    print()

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            pct = int(status.progress() * 100)
            filled = pct // 5
            bar = "#" * filled + "." * (20 - filled)
            print(f"  [{bar}] {pct:3d}%", end="\r", flush=True)

    print(f"  [{'#'*20}] 100%  -- upload complete          ")
    print()
    print(f"  Drive ID  : {response['id']}")
    print(f"  Drive link: {response.get('webViewLink', 'N/A')}")
    print()
    return response


# ─── CLI ──────────────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(description="Knowledge OS Drive Organizer")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--audit",         action="store_true", help="List all files in audio folders")
    g.add_argument("--plan",          action="store_true", help="Show rename/move plan (no changes)")
    g.add_argument("--execute",       action="store_true", help="Execute full reorganization")
    g.add_argument("--setup-folders", action="store_true", help="Create Knowledge_OS folder structure only")
    g.add_argument("--upload",        metavar="FILE",      help="Upload a local file to Drive")
    p.add_argument("--domain",        metavar="DOMAIN",    default=None,
                   help="Domain subfolder for --upload, e.g. AI_ML  ->  Knowledge_OS/AI_ML/sessions/")
    args = p.parse_args()

    service = get_drive_service()

    if args.audit:
        audit(service)
    elif args.plan:
        show_plan(service)
    elif args.execute:
        execute(service)
    elif args.setup_folders:
        setup_folders(service)
    elif args.upload:
        upload_file(service, Path(args.upload), args.domain)


if __name__ == "__main__":
    main()
