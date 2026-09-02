"""
category: Google Drive
drive_service.py — Shared Google Drive authentication and upload for 09_TOOLS.

Single source for building an authenticated Drive service. Seven tools each
built their own; three omitted the refresh branch and broke roughly an hour
after the token was issued, surfacing as a Drive API rejection rather than an
auth failure.

The OAuth token lives with the BDF project because a Drive token is issued per
Google Cloud project and cannot be duplicated. See CLAUDE.md.

Import as a sibling:
    from drive_service import get_service

Self-test:
    python C:/BRAIN_OS/09_TOOLS/drive_service.py
"""

from pathlib import Path

DEFAULT_CREDS = Path(r"C:\Dev\Projects\soccer-content-generator\gdrive_credentials.json")
DEFAULT_TOKEN = Path(r"C:\Dev\Projects\soccer-content-generator\gdrive_token.json")
SCOPES = ["https://www.googleapis.com/auth/drive"]


class DriveAuthError(RuntimeError):
    """Token cannot be refreshed and the browser flow is not permitted."""


def _browser_flow(creds_path: Path, token_path: Path):
    """Run the OAuth consent flow and persist the new token."""
    from google_auth_oauthlib.flow import InstalledAppFlow

    flow = InstalledAppFlow.from_client_secrets_file(str(creds_path), SCOPES)
    creds = flow.run_local_server(port=0)
    token_path.write_text(creds.to_json(), encoding="utf-8")
    return creds


def get_service(creds_path: Path = DEFAULT_CREDS,
                token_path: Path = DEFAULT_TOKEN,
                allow_browser: bool = True):
    """Return an authenticated Drive v3 service.

    Refreshes an expired token when a refresh token is present and writes the
    refreshed credentials back. Falls back to the browser consent flow only
    when allow_browser is True, so long-running pipelines cannot block on a
    consent screen.
    """
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from google.auth.exceptions import RefreshError
    from googleapiclient.discovery import build

    creds = None
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

    if not creds or not creds.valid:
        stale = None
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                token_path.write_text(creds.to_json(), encoding="utf-8")
            except RefreshError as e:
                # A revoked refresh token cannot be renewed, but it can be
                # replaced. Raising here would strand every caller when the
                # recovery path is one consent screen away.
                stale = e
                creds = None
        if creds is None or not creds.valid:
            if not allow_browser:
                raise DriveAuthError(
                    f"Drive token at {token_path} cannot be refreshed and the "
                    f"browser flow is disabled"
                    + (f": {stale}" if stale else "")
                    + f".\n  Work already written to disk is safe. Reauthorize with:"
                    f"\n    python C:/BRAIN_OS/09_TOOLS/drive_service.py"
                ) from stale
            if stale:
                print(f"  Drive refresh failed ({stale}); re-authorizing.")
            creds = _browser_flow(creds_path, token_path)

    return build("drive", "v3", credentials=creds)


if __name__ == "__main__":
    svc = get_service()
    about = svc.about().get(fields="user(emailAddress)").execute()
    print("OK authenticated as", about["user"]["emailAddress"])
