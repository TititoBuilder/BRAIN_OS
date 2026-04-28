---
tags: [api, live]
---

# API: Google Drive API

## Purpose
Syncs generated audio chapter files and session recordings to Google Drive after TTS generation.

## Used by projects
- BDF (book_compiler.py), CA (shared credentials)

## Limits and rules
- Rate limits: standard Drive API quotas (10,000 requests/100 seconds per user)
- Cost: $0 (within free tier storage)
- Legal constraints: OAuth2 consent screen must be verified; tokens expire and auto-refresh

## Credentials
- No single env var key — uses OAuth2 flow
- Credential files (stored at project root alongside book_compiler.py):
  - `gdrive_credentials.json` — OAuth2 client secrets (downloaded from Google Cloud Console)
  - `gdrive_token.json` — cached access + refresh token (auto-generated on first auth)
- Same Google account shared between BDF and CA projects

## Connected agents
- [[BDF_Memory_Agent]]

## Inputs
- SCOPES: `["https://www.googleapis.com/auth/drive.file"]`
- Library: `google.oauth2.credentials` + `googleapiclient.discovery.build("drive", "v3")`
- Creates remote folders on first run: `chapters/` and `sessions/` under Drive root
- Uploads: WAV/MP3 audio files produced by book_compiler.py TTS pipeline

## Outputs
- Drive file IDs returned per upload; logged locally
- Files accessible at `drive.google.com` under the authenticated account's root
