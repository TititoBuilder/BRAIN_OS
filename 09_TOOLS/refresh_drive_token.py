"""
refresh_drive_token.py — Drive Token Refresh + Railway Push
============================================================
Refreshes the local Google Drive OAuth token, then pushes the fresh
base64-encoded token to Railway as GOOGLE_TOKEN_JSON.

Solves the token-fragility problem: local token and Railway env var are
refreshed in one operation instead of two separate manual steps.

Required .env vars (add to C:\\Dev\\Projects\\soccer-content-generator\\.env):
    RAILWAY_TOKEN           Personal API token (Railway dashboard -> Account -> API Tokens)
    RAILWAY_PROJECT_ID      Project ID (from Railway dashboard URL)
    RAILWAY_ENVIRONMENT_ID  Environment ID (production — visible in Railway dashboard)
    RAILWAY_SERVICE_ID      Service ID for the read-along-app backend

Usage:
    python C:\\BRAIN_OS\\09_TOOLS\\refresh_drive_token.py
    python C:\\BRAIN_OS\\09_TOOLS\\refresh_drive_token.py --dry-run
"""

import argparse
import base64
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path
from dotenv import load_dotenv

# ── Config ─────────────────────────────────────────────────────────────────────
BRAIN_OS_ROOT = Path(r"C:\BRAIN_OS")
ENV_FILE      = Path(r"C:\Dev\Projects\soccer-content-generator\.env")
CONFIG_FILE   = BRAIN_OS_ROOT / "BRAIN_OS_CONFIG.json"

DRIVE_SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

RAILWAY_GQL   = "https://backboard.railway.app/graphql/v2"
VARIABLE_NAME = "GOOGLE_TOKEN_JSON"


# ── Config loader ───────────────────────────────────────────────────────────────
def load_paths() -> tuple[Path, Path]:
    """Return (credentials_path, token_path) from BRAIN_OS_CONFIG.json."""
    if not CONFIG_FILE.exists():
        print(f"[refresh] ERROR: {CONFIG_FILE} not found")
        sys.exit(1)
    cfg = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    drive = cfg.get("drive", {})
    creds_path = Path(drive.get("credentials_path", ""))
    token_path = Path(drive.get("token_path", ""))
    if not creds_path or not token_path:
        print("[refresh] ERROR: BRAIN_OS_CONFIG.json missing drive.credentials_path or drive.token_path")
        sys.exit(1)
    return creds_path, token_path


# ── Google token refresh ────────────────────────────────────────────────────────
def refresh_token(creds_path: Path, token_path: Path) -> dict:
    """Refresh the local Drive token. Returns the fresh token dict."""
    try:
        import google.oauth2.credentials
        import google.auth.transport.requests
    except ImportError:
        print("[refresh] ERROR: google-auth not installed.")
        print("  Run: pip install google-auth google-auth-oauthlib")
        sys.exit(1)

    if not token_path.exists():
        print(f"[refresh] ERROR: token file not found: {token_path}")
        sys.exit(1)

    print(f"[refresh] Loading token: {token_path}")
    creds = google.oauth2.credentials.Credentials.from_authorized_user_file(
        str(token_path), DRIVE_SCOPES
    )

    if not creds.expired and creds.valid:
        print("[refresh] Token is still valid — refreshing anyway to reset expiry.")

    print("[refresh] Refreshing token...")
    request = google.auth.transport.requests.Request()
    creds.refresh(request)

    # Build the token dict to save and encode
    token_dict = {
        "token":         creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri":     creds.token_uri,
        "client_id":     creds.client_id,
        "client_secret": creds.client_secret,
        "scopes":        list(creds.scopes) if creds.scopes else DRIVE_SCOPES,
        "expiry":        creds.expiry.isoformat() if creds.expiry else None,
    }

    # Write refreshed token back to disk
    token_path.write_text(
        json.dumps(token_dict, indent=2),
        encoding="utf-8",
        newline="\n",
    )
    print(f"[refresh] Local token updated: {token_path}")
    return token_dict


# ── Railway API ─────────────────────────────────────────────────────────────────
def push_to_railway(value_b64: str, dry_run: bool) -> None:
    """Upsert GOOGLE_TOKEN_JSON on Railway via GraphQL API."""
    token   = os.getenv("RAILWAY_TOKEN")
    proj_id = os.getenv("RAILWAY_PROJECT_ID")
    env_id  = os.getenv("RAILWAY_ENVIRONMENT_ID")
    svc_id  = os.getenv("RAILWAY_SERVICE_ID")

    missing = [k for k, v in {
        "RAILWAY_TOKEN":           token,
        "RAILWAY_PROJECT_ID":      proj_id,
        "RAILWAY_ENVIRONMENT_ID":  env_id,
        "RAILWAY_SERVICE_ID":      svc_id,
    }.items() if not v]

    if missing:
        print(f"[refresh] ERROR: missing env vars: {', '.join(missing)}")
        print(f"  Add them to: {ENV_FILE}")
        sys.exit(1)

    mutation = """
mutation variableUpsert(
  $serviceId: String!,
  $environmentId: String!,
  $projectId: String!,
  $name: String!,
  $value: String!
) {
  variableUpsert(
    serviceId: $serviceId,
    environmentId: $environmentId,
    projectId: $projectId,
    name: $name,
    value: $value
  )
}
"""
    variables = {
        "serviceId":     svc_id,
        "environmentId": env_id,
        "projectId":     proj_id,
        "name":          VARIABLE_NAME,
        "value":         value_b64,
    }

    payload = json.dumps({"query": mutation, "variables": variables}).encode("utf-8")

    if dry_run:
        print(f"[refresh] DRY RUN — would push {VARIABLE_NAME} ({len(value_b64)} chars) to Railway")
        print(f"  Service:     {svc_id}")
        print(f"  Environment: {env_id}")
        print(f"  Project:     {proj_id}")
        return

    print(f"[refresh] Pushing {VARIABLE_NAME} to Railway ({len(value_b64)} chars)...")
    req = urllib.request.Request(
        RAILWAY_GQL,
        data=payload,
        headers={
            "Content-Type":  "application/json",
            "Authorization": f"Bearer {token}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            if "errors" in body:
                print(f"[refresh] Railway API error: {body['errors']}")
                sys.exit(1)
            print(f"[refresh] Railway updated. Response: {body.get('data')}")
    except urllib.error.HTTPError as e:
        print(f"[refresh] HTTP {e.code}: {e.read().decode()}")
        sys.exit(1)
    except Exception as e:
        print(f"[refresh] Unexpected error: {e}")
        sys.exit(1)


# ── Main ────────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Refresh Drive token + push to Railway")
    parser.add_argument("--dry-run", action="store_true",
                        help="Refresh local token but do not push to Railway")
    args = parser.parse_args()

    load_dotenv(ENV_FILE)

    creds_path, token_path = load_paths()

    token_dict = refresh_token(creds_path, token_path)

    token_b64 = base64.b64encode(
        json.dumps(token_dict).encode("utf-8")
    ).decode("ascii")

    push_to_railway(token_b64, dry_run=args.dry_run)

    if not args.dry_run:
        print("\n[refresh] Done. Token refreshed locally and Railway updated.")
        print("  Railway will pick up the new value on next deploy or env reload.")
    else:
        print("\n[refresh] Dry run complete. Local token refreshed. Railway not touched.")


if __name__ == "__main__":
    main()
