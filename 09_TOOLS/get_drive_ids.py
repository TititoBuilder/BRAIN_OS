r"""
category: Google Drive
get_drive_ids.py — list file names and Drive IDs for one hardcoded folder.

Prints "name | id" per file, for capturing IDs to paste into drive_index.json.
Authenticates through drive_service.py. The folder ID in the query is
hardcoded; edit it before running against a different folder.
"""
from drive_service import get_service

service = get_service()

results = service.files().list(
    q="'1jCp3ONYmJoRslpJRFmB4r' in parents and trashed=false",
    fields="files(id,name)",
    pageSize=50
).execute()

for f in results.get("files", []):
    print(f["name"] + " | " + f["id"])
