"""
download_brainos_chapters.py — Download BRAIN OS guide WAVs from Drive
"""
import os, sys, json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(r"C:\Dev\Projects\soccer-content-generator\.env"))

OUTPUT_DIR = Path(r"C:\Dev\Projects\soccer-content-generator\converted\brainos_chapters")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FILES = {
    "programming_terminology_reference": "13CTY6mW-BXS-nhQJx87HddNO0pzYxsHC",
    "claudeguide_skills_system":         "1dX6oEA4F8qi2Kl6Z69-h4NDpgJSRF9Nh",
    "claudeguide_prompting_architecture":"12R2Lr0xTLrFXhvVe4Py0fn6SXWXOPytl",
    "claudeguide_mcp_setup":             "19JV8MtSTys-E8vUPT9hPLBHYsjw8cxwx",
    "claudeguide_claude_md_standards":   "1oVo0jvRUeGFsJ8BBuzExd28dpu-cgIS2",
    "resolve_mcp_guide":                 "1AmenAuvjrwk_1gavyd05FwV9cVUa7oO1",
    "guide_venv":                        "1yZYAQuJM4--biE76271zQQD5-8KP9-Ex",
    "guide_obsidian_claude":             "1m7R2AMTev6hrCRq0dlVGfoXb_TJnR8Ql",
    "guide_mcp_ecosystem":               "1lPc0LOkZZfUN_2CAtCz-uU-khB4zunmM",
    "guide_lancedb":                     "1ivJFo4lBTKfwAhsaQZcJohLelaSARfOe",
    "guide_brain_os":                    "1i9TS3rx15rC5XUe3Eus9ctt1R_VU0MdR",
}

def get_service():
    sys.path.insert(0, str(Path(r"C:\Dev\Projects\soccer-content-generator")))
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    TOKEN = Path(r"C:\Dev\Projects\soccer-content-generator\gdrive_token.json")
    creds = Credentials.from_authorized_user_file(str(TOKEN))
    return build("drive", "v3", credentials=creds)

def download_file(service, file_id: str, dest: Path):
    from googleapiclient.http import MediaIoBaseDownload
    import io
    req = service.files().get_media(fileId=file_id)
    buf = io.BytesIO()
    dl = MediaIoBaseDownload(buf, req)
    done = False
    while not done:
        _, done = dl.next_chunk()
    dest.write_bytes(buf.getvalue())

def main():
    service = get_service()
    for name, file_id in FILES.items():
        # Output as mp3 filename matching learning_path_builder expectations
        dest = OUTPUT_DIR / f"{name}_audio.mp3"
        if dest.exists():
            print(f"  ✓ exists: {dest.name}")
            continue
        print(f"  ↓ {name}...", end=" ", flush=True)
        try:
            download_file(service, file_id, dest)
            size_mb = dest.stat().st_size / 1024 / 1024
            print(f"✅ {size_mb:.1f} MB")
        except Exception as e:
            print(f"❌ {e}")

if __name__ == "__main__":
    main()
