SESSION START - BRAIN_OS / Read-Along App (continuing)

Continuation. Load context first:
  cd C:\BRAIN_OS
  python 09_TOOLS\session_start.py
(Run bare - docstring claims a --project flag the parser lacks. This script dumps ALL context every run; trimming it is the first study target.)

HOW TO WORK WITH ME:
- I run every command in Win+X PowerShell 5.1; you write them, I paste output. Full absolute paths always.
- VERIFY against the filesystem BEFORE writing. Confident text is NOT truth until checked. Core lesson - nearly every problem came from a gap between what something claimed and what was true.
- File edits: here-string -> .py script -> run -> delete. NEVER python -c with nested quotes, NEVER triple-quoted strings through PowerShell, NEVER Set-Content/ConvertTo-Json on JSON/text (BOM/null corruption). Always Python encoding="utf-8", newline="\n".
- Stale-download trap bit 4x: browser saves file (1).tsx; verify the SOURCE file content by exact name before installing.
- git add by explicit filename, never -A. Verify git status before commit. .gitignore check in BRAIN_OS (audio never commits).
- Declare each task finish line BEFORE starting. Discoveries -> QUEUE.
- State settled decisions directly. Guide me; reserve questions for genuine forks. Explain mechanics first time. I decide session start/end.

SYSTEM TRUTH:
- BRAIN_OS = knowledge graph/vault at C:\BRAIN_OS (git TititoBuilder/BRAIN_OS), NOT a project. Projects hang off it: CristianConstruction (income), BDF/soccer-content-generator, Read-Along App, resolve/obs MCP. Constraint is TIME not understanding.
- Read-Along App: frontend React/Vite/TS on Vercel (read-along-app-psi.vercel.app), backend FastAPI Railway (read-along-app-production.up.railway.app). Frontend C:\Users\titit\Projects\read-along-app\frontend\src\. Git TititoBuilder/read-along-app.
- App 4 layers: vault .md (02_PROJECTS/knowledge_os/{key}.md) -> Drive mp3 -> index (09_TOOLS/drive_index.json from GitHub raw; id: = correct audio, path-string = borrowed/wrong) -> app. Paths in 09_TOOLS/learning_paths.json (9 paths). NODES auto-derives by status (Learning+).
- Deploy: cd frontend; npm run build then cd ..; npx vercel --prod from REPO ROOT. Hard-refresh Ctrl+Shift+R. Verify deploy by fetching live JS/CSS bundle and grep CSS class names (minifier renames variables).
- Dev mode (not yet used): npm run dev = live-reload localhost, fast iteration vs slow deploy. Learn it.
- Two Drive tokens expire ~weekly, refreshed SEPARATELY: local C:\Dev\Projects\soccer-content-generator\gdrive_token.json + Railway env GOOGLE_TOKEN_JSON. Expiry symptom: audio 500 invalid_grant. Fix: refresh local -> base64 -> paste Railway Variables GOOGLE_TOKEN_JSON -> redeploy.
- Venvs: GPU/Whisper+Drive = soccer-content-generator\venv; TTS = C:\Knowledge\CA\venv. Kokoro af_heart. Model claude-sonnet-4-6 never Opus.

LIVE NOW: PATHS tab is a guided course (default tab): pick path -> lessons play in sequence -> auto-advance on end -> Lesson N of M -> large driving controls (big play, prev/next lesson, +/-15s seek, square restart). Committed + deployed.

QUEUE (priority, full list in 00_DASHBOARD/Queue.md):
1. GOLD CAPSTONE LESSON - author entire project lessons as ONE linear reinforced sequence, then voice it. Cover deploy crisis (3 root causes), token fragility, verify-before-write, declared-start-finish, derive-dont-duplicate, four pillars, BOM/encoding, stale-download trap, app 4-layer architecture, for-now-forbidden. Then pipeline author->voice->stage->populate->id:->commit.
2. STUDY CLUSTER - understand my toolchain: read each .py in 09_TOOLS + read-along backend; learn git; learn dev mode + VS Code distinction. FIRST TARGET session_start.py (trim its output).
3. python_asyncio plays borrowed BDF-chapter audio - re-voice from its .md.
4. Convert remaining path-format index entries to id: (low).
5. session_close.py --project flag drift.
6. Telegram env vars not loaded in plain PowerShell.
7. FEATURE: separate Books/Sessions access path.

START HERE: likely #1 or #2. Show me the start/finish line and begin verify-first.
