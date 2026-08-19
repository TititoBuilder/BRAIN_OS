# Read-Along App — Deploy Architecture (Ground Truth)

Last verified: 2026-08-19. Written after a full deploy debug, updated after the
2026-08-14 Railway->Render migration. Everything here is CONFIRMED by direct
inspection, not assumed.

## The system: 3 pieces, 1 source of truth

| Piece | Where | Deploys via |
|---|---|---|
| Frontend (React/Vite/TS) | `frontend/` subdir | Vercel (auto on push to main) |
| Backend (FastAPI) | `backend/backend.py` | Render (auto on push to main) |
| Index + path defs | BRAIN_OS repo `09_TOOLS/` | git push (read via GitHub raw) |

Audio lives on **Google Drive**. Transcripts live in `backend/transcripts/`
(committed to the read-along repo). The app stitches these together at runtime.

## CRITICAL CONFIG (the things that broke, now documented)

### 1. Vercel Root Directory = `frontend` (NOT `./`)
The code is in the `frontend/` subdir. Vercel's Root Directory MUST be set to
`frontend` (Settings > Build and Deployment > Root Directory). The project was
originally LINKED from frontend/ (see frontend/.vercel/project.json).
SYMPTOM if wrong (set to ./): build fails "sh: vite: command not found"
(exit 127) because Vercel builds in repo root where there's no package.json.
FIX: Root Directory = frontend. This is the durable fix, NOT npx-patching the
build command.

### 2. Two separate Google Drive tokens (local vs Render)
There are TWO copies of the Drive OAuth token, and BOTH expire (~weekly):
- LOCAL: C:\Dev\Projects\soccer-content-generator\gdrive_token.json
  Refresh by running populate_staging.py — its OAuth flow mints a fresh
  token at FULL drive scope. backend.py:1000 names this path in its
  scope-mismatch error.
- RENDER: env var GOOGLE_TOKEN_JSON (base64 of the token JSON).
  Used by the deployed backend's _get_drive_service(). Refreshing the LOCAL
  token does NOT update Render. Must separately:
  base64-encode the fresh local token -> paste into Render's GOOGLE_TOKEN_JSON.
  PowerShell to clipboard:
    $b=[Convert]::ToBase64String([IO.File]::ReadAllBytes($tok)); $b|Set-Clipboard
  THEN click Manual Deploy. Render reads env vars ONCE at process start —
  saving a variable does NOT reliably trigger a redeploy. Confirm the new
  timestamp in the Events tab before testing (2026-08-18: a stale token
  survived three checks because of this).
SCOPE: mint at ["https://www.googleapis.com/auth/drive"], not drive.readonly.
Google refuses to widen scope on refresh — a narrow token must be re-minted.
SYMPTOM if expired: /audio-local/* returns 500 "invalid_grant".
SYMPTOM if narrow:  /audio-local/* returns 500 "invalid_scope" on every key.

### 3. drive_index.json = SINGLE SOURCE OF TRUTH (GitHub only)
Backend reads it from GitHub raw:
  raw.githubusercontent.com/TititoBuilder/BRAIN_OS/main/09_TOOLS/drive_index.json
(backend.py /topics line ~744, _get_drive_index line ~782).
DELETED the Railway env var DRIVE_INDEX_JSON (2026-06-04) — it was a stale
SECOND source that shadowed the GitHub file and caused path 404s. Do NOT
re-add it. To update the index now: edit drive_index.json + git push. One place.
SYMPTOM if env override existed & stale: new keys return 404 even though
GitHub has them.

### 4. Editing drive_index.json — use PYTHON, never PowerShell ConvertTo-Json
PowerShell `ConvertTo-Json -Depth | Set-Content` MANGLED the file and added a
BOM (broke parsing). Always edit via Python's json lib:
  python -c "import json; d=json.load(open(p)); d['index'][k]='id:'+fid; json.dump(d,open(p,'w'),indent=2,ensure_ascii=False)"

## HOW AUDIO RESOLVES (backend.py /audio-local/{key})
1. Look up key in drive_index 'index' object -> get drive_path value.
2. If value starts "id:" -> fetch that Drive file ID directly (preferred, fast).
3. Else -> treat as a path/name, search Drive by filename.
Both topics and learning-paths use this SAME endpoint, keyed by machine_key /
path_id. Paths were uploaded to Knowledge_OS/ root, indexed as "id:..." entries.

## DEPLOY CHECKLIST (when shipping changes)
1. Frontend change -> commit + push read-along repo -> Vercel auto-builds
   (verify Root Directory = frontend). Hard-refresh browser (Ctrl+Shift+R) to
   clear cached old bundle.
2. Backend change -> same push -> Render auto-builds.
3. New audio (topic or path):
   a. Generate mp3 (Kokoro af_heart) + transcribe (GPU Whisper).
   b. Upload mp3 to Drive via drive_browser.py --upload (capture Drive ID).
      (Refresh local token first if it's >~5 days old.)
   c. Add "key":"id:FILEID" to drive_index.json VIA PYTHON. git push BRAIN_OS.
   d. Copy transcript json to backend/transcripts/. Commit + push read-along.
4. If Render can't reach Drive (500 invalid_grant) -> refresh GOOGLE_TOKEN_JSON,
   then Manual Deploy (see section 2).

## KNOWN, ACCEPTED ARTIFACTS (not bugs)
- Karaoke text can differ slightly from narration: transcripts are
  Whisper-generated, and Whisper mis-hears some tech terms (asyncio->Ascensio,
  GraphQL->Graphical, Git->Get). Word-timing tracks the right region but isn't
  always word-perfect. Fixing = hand-correcting transcripts (not worth it).

## ENVIRONMENT GOTCHAS
- Desktop is OneDrive-redirected: use [Environment]::GetFolderPath("Desktop")
  = C:\Users\titit\OneDrive\Desktop. NOT $env:USERPROFILE\Desktop (doesn't exist).
- Venv map: GPU/Whisper + Google API = soccer-content-generator\venv (BDF).
  pydub/stitching = C:\Knowledge\CA\venv. Both have CUDA. Triton warning is
  a harmless fallback, not CUDA failure.
- Telegram "invalid TELEGRAM_CHAT_ID" in Render logs = harmless placeholder
  env var, unrelated to audio.

## KEY FILES / IDS
- Frontend: read-along-app-psi.vercel.app | Backend: read-along-app.onrender.com
- Vercel project: read-along-app (prj_MOIIrsQ5upC1pvWclJJgM5OFBC6n)
- Repos: github.com/TititoBuilder/read-along-app + /BRAIN_OS
