# Lesson Queue — Active Directions
Location: C:\BRAIN_OS\02_PROJECTS\LESSON_QUEUE.md
Updated: 2026-08-18

---

## Status

    Lesson 01 — Repo Reconciliation          COMPLETE ✓ 2026-08-10
    Lesson 02 — .env + pathlib pattern       COMPLETE ✓ 2026-08-10
    Direction 3 — gig_tracker split          COMPLETE ✓ 2026-08-10
    Direction 4 — Downloads folder triage    COMPLETE ✓ 2026-08-10
    Direction 1 — resolve-mcp-server archaeology    COMPLETE ✓ 2026-08-12
    Direction 5 — resolve-mcp-server paths              QUEUED
    Direction 6 — gig_tracker imports and category coverage    COMPLETE ✓ 2026-08-12
    Direction 7 — gig_tracker web.py dashboard + automation    IN PROGRESS
    Direction 7b — gig_tracker dashboard debt + chart work     QUEUED
    Direction 8 — gig_tracker calibrate_miles + XLSX      QUEUED
    Direction 9 — read-along-app Wall→Listen + infra      COMPLETE ✓ 2026-08-18
    Direction 10 — read-along-app architecture debt       QUEUED

---

## Direction 1 — Go Deeper into resolve-mcp-server
Status: COMPLETE ✓ 2026-08-12

What it is:
  Phase 2 archaeology on the most complex repo in the stack.
  server_api.py is 1,700 lines. You deleted 45 backup files
  but never read the live code.

What you will do:
  - git log --oneline --graph on resolve-mcp-server
  - Hot-spot churn analysis (which files change most)
  - Shift+F12 on major functions to find dead code
  - Read server_api.py top to bottom with VS Code symbols

What you will learn:
  - Whether the codebase is healthy or carrying technical debt
  - How to read a large unfamiliar file systematically
  - git log --follow -p for file archaeology

---

## Direction 2 — Fix Hardcoded Path Problem Across All Repos
Status: COMPLETE ✓ 2026-08-10

Pattern learned: .env + pathlib
  - BASE_DIR = Path(os.getenv("BASE_DIR", r"fallback\path"))
  - Subdirs built with / operator: BASE_DIR / "chapters"
  - .env.example committed, .env never committed
  - os.getenv second argument is the fallback default
  - int() wrapper needed for numeric env vars

Done:
  [x] custom-agent — ca_audio.py refactored, .env.example added
  [x] soccer-content-generator — PathConfig class added to config.py,
      4 paths wired, .env.example added

Audit command (run inside any repo):
  Select-String -Path .\**\*.py -Pattern "Path\(r" | Select-Object Path, LineNumber, Line

---

## Direction 3 — Reconcile the gig_tracker Split
Status: COMPLETE ✓ 2026-08-10

What was done:
  - Identified OneDrive copy as authoritative (newest database Aug 8)
  - CLAUDE_HANDOFF.md and _generated/ reports committed to real repo
  - BRAIN_OS untracked copy deleted
  - Real repo moved from OneDrive Desktop to C:\Dev\Projects\gig_tracker
  - repo_inventory.txt updated with new path
  - gig_tracker/ added to BRAIN_OS .gitignore

---

## Direction 4 — Downloads Folder Triage
Status: COMPLETE ✓ 2026-08-10

What was done:
  - 82 .md files found in Downloads
  - 9 duplicate (1) files deleted
  - 16 batch files moved to C:\Knowledge\CA\CA_Book\incoming\
  - Lesson files → 05_LEARNING\
  - Guide files → 03_KNOWLEDGE\
  - Templates → 06_TEMPLATES\
  - Tools → 09_TOOLS\
  - Sessions → 08_SESSIONS\
  - Nav files → 02_PROJECTS\
  - BDF files → soccer-content-generator\
  - Downloads .md count: 0

---

## Direction 5 — Fix Hardcoded Paths in resolve-mcp-server
Status: QUEUED

What it is:
  46 hardcoded paths across 9 files. Two roots: C:\BDF\ and C:\Users\titit\
  resolve_bridge.py runs inside Resolve's Python console — cannot import
  from config.py. Needs a different path strategy than Directions 2-3.

What you will do:
  - Apply PathConfig to server_api.py, mcp_ingest.py, memory.py,
    cleanup_config.py, cleanup_plan.py, promote_server.py, seed_knowledge.py
  - Solve resolve_bridge.py separately — .env read directly at runtime
    without imports, using pathlib.Path and os.environ

What you will learn:
  - How to handle path configuration when you can't use standard imports
  - os.environ vs os.getenv vs load_dotenv — three ways to read env vars
  - Why runtime context determines your architecture choices

---

## Direction 6 — gig_tracker: Complete Imports + Automation
Status: COMPLETE ✓ 2026-08-12

What it is:
  AMEX still at 0 transactions. Other category at 26% — target is under 15%.
  Expired offer alerts cluttering day-start. Category rules need refinement.

What you will do:
  - Import AMEX statement
  - Run merchants command to find remaining Other merchants
  - Add targeted rules until Other under 15%
  - Fix expired offer auto-cleanup in alerts command
  - Explore web.py dashboard — connect spending data to visual output

What you will learn:
  - Flask routes and template rendering
  - How web.py connects to the same db.py layer
  - SQLite query optimization for dashboard queries

---

## Direction 7 — gig_tracker: web.py Dashboard + Automation
Status: IN PROGRESS

What it is:
  584 transactions live across 7 cards. web.py is a Flask dashboard
  that connects all imported data to a visual interface. The dashboard
  should show spending trends, Prop 22 status, and card balances in real time.

What you will do:
  [x] Read web.py architecture — Flask routes, template rendering
  [x] Fix hardcoded payment due dates (_DUE_DAYS → DB migration)
  [x] Build balance.py quick balance updater
  [x] Organize downloaded statements into data/statements/
  - Connect spending data to visual charts
  - Explore automation: auto-import statements on schedule

What you will learn:
  - Flask request/response cycle
  - Jinja2 templates
  - How web.py shares db.py with gig.py (same data layer)
  - Scheduled tasks vs event-driven automation

---

## Direction 7b — gig_tracker: Dashboard debt + chart work
Status: COMPLETE ✓ 2026-08-13

What you will do:
  [x] Add Citi card 6936 to cards table → confirmed closed, excluded
  [x] Import transaction CSVs from data/statements/
  [x] Module C: Chart.js spending bar chart
  [x] Add DashboardData TypedDict schema

Commits:
  9199af9 - credit limits + citi 6936 closed
  de51f38 - AMEX importer profile
  9bf6074 - Capital One English profile
  70ef60b - Chart.js spending chart
  044bdc6 - DashboardData TypedDict

---

## Direction 7c — gig_tracker: Importer cleanup + category rules
Status: COMPLETE ✓ 2026-08-13

What you will do:
  [x] Add ANTHROPIC → subscriptions category rule
  [x] Add AMAZON → shopping category rule
  [x] Recategorize existing rows — 119 rows moved out of other
  [x] Add subscriptions and shopping categories
  [x] Run preflight.py — no blocking issues

Commits:
  9d430b4 - subscriptions + shopping category rules
  596c223 - expanded category rules (13 merchants)
  DB only  - 119 rows recategorized

---

## Direction 7d — gig_tracker: Config + dashboard polish
Status: COMPLETE ✓ 2026-08-13

What you will do:
  [x] Move van target dates from hardcoded to van_config.json
  [x] calibrate_miles — deferred, needs 2+ paid-in-full periods
  [x] Populate 11 Obsidian vault docs in BRAIN_OS/02_PROJECTS/gig_tracker/
  [x] Dashboard polish — Chart.js live, balances correct, cash_balance.py built
  [x] Run preflight clean — no blocking issues

What you will learn:
  - Config-driven values vs hardcoded constants — when each is right
  - Obsidian vault documentation standards
  - Dashboard data completeness vs display completeness

Commits:
  2b4d7f1 - van dates → van_config.json
  af46c61 - 11 Obsidian vault docs + gitignore fix
  9d430b4 - subscriptions + shopping rules
  596c223 - expanded category rules
  686ddb5 - cash_balance.py + balance.py

---

## Direction 7e — gig_tracker: Importer + mileage
Status: COMPLETE ✓ 2026-08-14

What you will do:
  [x] shopping → van_build category rename complete
  [x] Best Buy is_onetime confirmed
  [x] runway.py fixed — Roadie income from platform_statements
  [x] import_spark_xlsx.py built — 536 trips imported
  [x] delivery_runs 67 → 603 rows
  [x] VALID_SOURCES updated in invariants.py
  [x] Real surplus confirmed: $2,821/month, debt free Mar 2028

  Note: van_build category to be revisited and split after van move-in.
  Post-move: personal shopping gets its own category again.

What you will learn:
  - is_onetime flag — how amortization works for large one-time purchases
  - Baseline calibration — why one data point is never enough
  - Period vs YTD analysis — when each view is misleading

Commits:
  805438d - shopping → van_build importer rule
  DB only  - 16 rows recategorized shopping → van_build
  08c4e09 - runway Roadie fix
  a99f962 - import_spark_xlsx.py
  6afaaf7 - xlsx_import added to VALID_SOURCES

---

## Direction 8 — gig_tracker: Calibrate miles + period analysis
Status: QUEUED — open Monday after period closes Aug 16

What you will do:
  - Download new Spark XLSX after Aug 16 period closes
  - Run import_spark_xlsx.py with new XLSX
  - Run calibrate_miles.py — should now have 2+ paid periods
  - Update mileage baseline if 2+ periods available
  - Patch runs 56-59 engaged_miles
  - Run income_recompute.py — refresh all period figures
  - Run runway.py — verify surplus with updated baseline

What you will learn:
  - How mileage baseline affects Prop 22 floor calculation
  - income_recompute.py — how it rebuilds period aggregates
  - Why provisional baselines exist and when to promote them

Commits this session:
  08c4e09 - runway Roadie fix
  a99f962 - import_spark_xlsx.py
  6afaaf7 - xlsx_import added to VALID_SOURCES

Do not touch FLAGS.txt.
Do not modify gig_income.db directly.
git add by explicit filename only, never -A.

---

## Direction 9 — read-along-app: Wall→Listen + credential archaeology
Status: COMPLETE ✓ 2026-08-18

What it was:
  Clicking a Wall square never loaded audio. Diagnosing it uncovered
  three further failures the broken handoff had been masking — nothing
  downstream of the click had ever been exercised.

What was done:
  [x] Wall→Listen handoff — WallTab declared `key`, /topics returns
      `machine_key`. t.key undefined on every square, so ListenTab's
      effect early-returned on falsy pendingTopic. (21d8dad)
  [x] /topics 404 — Authorization header on public raw.githubusercontent
      URLs. Public raw + bad token = 404, not 401. (f1366b6)
  [x] Two more authenticated raw call sites at backend.py:493 and
      :727. (faab7fb)
  [x] /vault/tree 502 — GitHub PAT expired. New fine-grained token,
      BRAIN_OS only, Contents R/W, expires 2026-11-16.
  [x] /audio-local invalid_scope — gdrive_token.json minted at
      drive.readonly while backend.py:130 requests full drive. Google
      refuses to widen scope on refresh. Re-minted via
      populate_staging.py OAuth flow, GOOGLE_TOKEN_JSON updated.
  [x] $PROFILE shortcuts: ra / bdf / gig / bos
  [x] Vercel production deployed — read-along-app-psi.vercel.app

  Supersedes 2026-08-17 flag "dataclasses not in Drive index" —
  python_dataclasses was always indexed; the invalid_scope 500 was
  misread as a 404.

What was learned:
  - raw.githubusercontent.com needs NO auth on a public repo and
    returns 404 (not 401) when sent a bad token. api.github.com
    requires auth and returns 401. One rule does not cover both.
  - A refresh token cannot be widened to a larger scope. invalid_scope
    means re-authorize; invalid_grant means expired. Different fixes.
  - Render reads env vars once at process start. Saving a var does not
    reliably redeploy — always Manual Deploy and confirm the timestamp.
  - One dead credential produced three unrelated-looking symptoms and
    no message named the cause.
  - The hypothesis in the session opener was wrong. ListenTab is
    CSS-hidden, never unmounted. Reading both files before touching
    anything is what caught it.

Commits:
  21d8dad - fix(wall): read machine_key not key from /topics
  f1366b6 - fix(backend): drop auth header on public raw fetches
  faab7fb - fix(backend): drop auth header on remaining raw fetches
  2cc6408 - feat: lesson_10 + lesson_11 audio nodes (drive_index 137)

---

## Direction 10 — read-along-app: architecture debt
Status: QUEUED

What it is:
  Direction 9 fixed symptoms. These are the structural causes, plus
  the observability gaps that made a two-line bug cost a full session.

Priority — do these first:
  - Extract shared Topic interface → frontend/src/types/topic.ts and
    domain constants → frontend/src/constants/domains.ts.
    Direct root cause of the Wall bug.
  - Startup credential check: ping api.github.com/user, log pass/fail.
    backend.py:681 raises 503 for a MISSING token but lets an INVALID
    one fall through to 502.
  - Log which Drive auth source won at startup (GOOGLE_TOKEN_JSON vs
    GDRIVE_TOKEN_PATH) and its scope list.
  - Connect Vercel to the GitHub repo. Render auto-deploys, Vercel
    is manual — production frontend ran pre-fix code all session.

Cleanup:
  - Delete backend/download_legacy.py (dead — /audio-local is served
    from backend.py:825). Its stale drive.readonly constant is what
    made the scope bug hard to read.
  - Consolidate three _GDRIVE_SCOPES declarations.
  - /audio-local: return 502 + detail instead of bare 500.
  - Fix "Railway" strings in populate_staging.py and backend.py:790.
  - read-along-app.context.md is stale (87 days) — refresh.
  - Rewrite .gitignore: `transcripts/` excludes the parent, so
    `!backend/transcripts/` can never work. Also
    `!.claude/settings.jsonbackend/get_ids.py` is two patterns
    collided on a missing newline.

Data and product:
  - ~40 topics carry snake_case domains (creative_systems,
    systems_operations, ai_engineering) absent from DOMAIN_ORDER in
    both tabs — invisible on the Wall. Reconcile against
    obsidian_sync.json.
  - BooksTab "Sessions" header: no documented purpose anywhere in
    read-along-app.context.md. Decide intent or remove.
  - AskTab is stateless — each Ask replaces the last. "Explore next"
    suggestions are generated text with nothing wired. Decide:
    clickable chip (frontend only) or multi-turn (backend change).
  - No gig_tracker audio node exists. Nothing generates one
    automatically — needs a vault note before populate_staging.py
    will see it.

Coupling:
  - populate_staging.py lives in read-along-app/backend but reads
    C:\Dev\Projects\soccer-content-generator\gdrive_token.json.
    Shared by BDF, populate_staging, and the read-along backend.
    Widened readonly → full drive this session.
    Backup: gdrive_token.json.bak-2026-08-17

Calendar:
  - GitHub PAT expires 2026-11-16.
  - Drive token has no expiry but is shared across three consumers.

---

## Backlog — Future Directions

  B1 — Write .env.example for every repo that has a .env
  B2 — Add .gitignore to any repo missing one
  B3 — Write a 10-line README for each repo (CODE flag fix)
  B4 — Learn git log --follow and git show <sha>:path
       (recover any file from resolve-mcp-server history)
  B5 — Understand load_dotenv() internals — write your own
       in 10 lines of Python to cement the pattern

---

## Session Log

  2026-08-10  Lesson 01 — Full repo audit, 12 repos, 5 RISK flags fixed
  2026-08-10  Lesson 02 — .env + pathlib pattern, applied to custom-agent
  2026-08-10  Directions 2-4 — paths refactored, gig_tracker reconciled,
              82 Downloads files triaged and filed
  2026-08-10  Direction 1 — server.py read complete, full architecture mapped, Option B (live test) queued for next session
  2026-08-12  Direction 1 — resolve_bridge.py fully mapped, 23 CONCEPT flags,
              STUDY_SYSTEM.md created, FLAGS.txt sorted and deduplicated (41 entries)
  2026-08-12  gig_tracker deep dive — 555 transactions imported across 5 cards,
              category rules 51 to 84, Other category 90% to 26%,
              financial CSVs removed from GitHub, prop22.py db.py importer.py fully mapped
  2026-08-12  Direction 6 complete — 584 transactions imported across 7 cards,
              category rules 51→84, Other 90%→22%, format detectors fixed,
              financial CSVs removed from GitHub
  2026-08-18  Direction 9 — read-along-app Wall→Listen fixed plus three
              masked failures: raw.githubusercontent auth 404s, expired
              GitHub PAT, Drive scope mismatch. 4 commits, Vercel
              deployed. Direction 10 opened for the structural causes.

<!-- auto-ingested 2026-08-13 -->
## Added 2026-08-13
- FLAGS_MANUAL and LESSON_QUEUE files added to vault
- Study system documented: four layers, domain map, learning principle

## Session 2026-08-26 — Harness Framework, Phase 2 + Phase 3 (partial)

DONE
- Phase 2 discovery complete across C:\Dev, C:\Users\titit\Projects, C:\BRAIN_OS, C:\Knowledge
- HARNESS_DRAFT.md written for BRAIN_OS and custom-agent (1ac4ba3, 5c14112)
- custom-agent .claude\settings.json hardened; 3 of 4 gaps verified in-session
- FLAGS.txt +26 entries (212 total); line 9 updated; format errors corrected
- session_close.py fix attempted (9891bc2) — UNVERIFIED

NEXT — in order

1. CA_Book ingestion pipeline — 34 files in incoming, no _processed\ stage
   - BDF_Book has _processed\ and _rejected\; CA_Book has neither
   - software_architecture.md confirmed processed 6/11 into 01_DOMAINS,
     still sits in incoming indistinguishable from unprocessed drafts
   - Audit all 34 against vault counterparts BEFORE moving anything —
     a VERIFY-marked draft that was never processed is content, not debt
   - Then mirror BDF_Book's structure

2. Verify session_close.py fix (9891bc2) by running a real close
   - Fifth attempt; the "ordering is already correct" claim was asserted,
     not tested. Flag stays open until a close leaves a clean tree.

3. BDF_Canvas.md — still divergent, 65 lines repo vs 152 vault, two repos
   - Not the same case as software_architecture.md; no pipeline involved

4. Canonical lesson folder — knowledge_os vs 05_LEARNING
   - Then file LESSON_HARNESS_01.txt as lesson_13_the_harness.md

5. Map soccer-content-generator, resolve-mcp-server, obs-mcp-server

6. Promote settings.json template — blocked on Bash() pattern-match question

OPEN DECISIONS
- Global ~\.claude\CLAUDE.md is 0.2KB — what belongs in it?
- Two CLAUDE.md in the vault — which wins?
- C:\AI — delete or populate?
- Vault-note-in-repo flow — 3 confirmed misfiles, no correct flow defined yet