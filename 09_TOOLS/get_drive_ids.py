from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

token = Path(r'C:\Dev\Projects\soccer-content-generator\gdrive_token.json')
creds = Credentials.from_authorized_user_file(str(token))
service = build('drive', 'v3', credentials=creds)

results = service.files().list(
    q="'1jCp3ONYmJoRslpJRFmB4r' in parents and trashed=false",
    fields="files(id,name)",
    pageSize=50
).execute()

for f in results.get("files", []):
    print(f["name"] + " | " + f["id"])
