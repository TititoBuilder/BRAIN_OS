# Session Summary — 2026-08-31 → 2026-09-01

Orientation document. Written at the end of two long sessions. Every number
here was measured, not recalled.

---

## 1. What FLAGS.txt is

Three things at once, which is why it was confusing:

- **`FLAGS_MANUAL.md`** defines it as a ledger — 7 columns, 11 TYPEs
- **`STUDY_SYSTEM.md`** defines it as Layer 3, *"your syllabus"* — log a
  CONCEPT flag when you hit something you half-understand
- In practice it also held work items

There was no way to tell a finding from a task from a study note. That
ambiguity is itself an open flag: *flags means 4 different things in this
system*.

**Fixed by the marker taxonomy**, now applied to all 321 rows:

| Marker | Meaning | Action |
|---|---|---|
| `FIXED` | Done | none |
| `LOG` | A record of what happened | none |
| `DECIDED` | A decision, not an action | none |
| `DUP L<n>` | Duplicate of row n | none |
| *(unmarked)* | **The actual to-do list** | work |

**The rule: whatever has no marker is the work.**

### Backlog as of 2026-09-01

| | Count |
|---|---|
| Total rows | 321 |
| **Unmarked — real backlog** | **104** |

| TYPE | Open |
|---|---|
| DESIGN | 45 |
| DATA | 31 |
| RISK | 11 |
| BUG | 7 |
| CONCEPT | 6 |
| SECURITY | 2 |
| FEAT | 1 |
| TOOL | 1 |

Before this session the count read ~220 and included comprehension notes,
duplicates, and items already fixed on disk. **104 is the first honest
number this ledger has produced.**

---

## 2. Queues — where they stand

Seven queue files exist. They were never surfaced because nothing links them.

| Queue | Location | State |
|---|---|---|
| Master queue | `00_DASHBOARD\Queue.md` | Active. Holds scoped-but-unexecuted plans |
| Queue archive | `00_DASHBOARD\Queue_Archive.md` | Closed items |
| Lesson queue | `02_PROJECTS\LESSON_QUEUE.md` | Not reviewed this session |
| Content queue | `05_MEMORY\Content_Queue.md` | Not reviewed this session |
| BDF content queue | `soccer-content-generator\src\queue\content_queue.json` | **21 items pending approval** |
| message_queues.md | `02_PROJECTS\knowledge_os\` and `03_KNOWLEDGE\` | Duplicate pair, unflagged |

### Why you never heard about the 21 items

`watchdog.py --check bdf` checks the queue, formats a report, and sends it
to Telegram. Telegram was dropping ~20% of sends because of an IPv6 routing
fault. The check worked; the result never arrived.

**Fixed today.** Telegram now delivers (verified, message ID 542). The
7:30am scheduled task will report from tomorrow.

**But BDF is parked**, so 21 pending approvals is evidence the channel was
dead, not a queue to clear. Once notifications work, that number arrives
every morning and manufactures urgency for work you chose not to do. The
recommended fix is a `parked: true` flag in `projects.manifest.json` with
watchdog skipping parked projects — not processing the queue, not deleting
the check.

---

## 3. The trigger layer — surfaced, not wired

`07_SYSTEM\Trigger_Architecture.md` plus 13 nodes in `08_TRIGGERS\`. Four
types: TIME (Calendar), EVENT (file change), STATE (condition), MANUAL.

Fully specified. **No tool reads `08_TRIGGERS` to decide anything.** The
only code references are the audio pipeline treating three trigger notes as
narration source material.

Two conditions are implemented independently, unaware the nodes exist:

- `graph_maintainer.py:222` reads `SESSION_ANCHOR_TTL_HOURS` — that is
  `Trigger_Graph_TTL_Expired`
- `watchdog.py` checks the content queue — that is `Trigger_BDF_Queue_Check`

**Verdict (Fable's, and I agree): leave it as documentation, make the
documentation true. Do not build a runner.** The runtime already exists in
three pieces. A `trigger_runner.py` would be a fourth layer on top of three
silent failures.

Cheapest version, ~90 minutes: add one `implemented_by:` line to each of
the 13 nodes, and turn `Trigger_Architecture.md` into a status table. That
becomes the audit surface that would have caught a STATE trigger whose
action had been a no-op for weeks.

---

## 4. What Fable produced

Ran in parallel on the same artifacts. Cost ~$17.

**Genuinely valuable:**

- **The marker taxonomy** — FIXED / LOG / DECIDED / DUP, with row lists for
  160 markers. Applied. This is what turned a 220-row backlog into a
  104-row one, and it is the single most useful output.
- **A dependency graph of fixes** — F0 through F10, showing what blocks
  what. Identified that decisions cost nothing but unblock six fixes.
- **A six-phase plan** with hours, verification commands, and risk notes.
- **Three things not to do** — the discipline of naming what looks worth
  fixing and is not.
- **The trigger verdict.**
- **Three probe scripts** — Telegram transport, ledger markers, credential
  status. The transport probe is what led to the IPv6 discovery.

**Its errors, for calibration:**

- Left a `<name from C6>` placeholder inside a runnable block
- Took a path from `artifacts.manifest.json` as fact — the exact ground
  rule the prompt had given it
- Its marker script wrote with `utf-8-sig`, adding a BOM to FLAGS.txt

Net: the planning and clustering were strong, the executable output needed
the same verification as anything else.

---

## 5. What was achieved

### Security

| | |
|---|---|
| gig_tracker bank statements | 13 CSVs purged from git history with filter-repo, force-pushed, verified empty. Repo confirmed private throughout. Mirror retained at `C:\Dev\_backups\` |
| PowerShell profiles | GitHub PAT and HF token removed from both OneDrive-synced profiles. `generate_profile.py` now emits a read from `.env` instead of the value |
| custom-agent | Two deny entries added for `git push origin main --force`, which the existing patterns missed |
| **Outstanding** | **Both tokens are still unrotated. Also `RAILWAY_TOKEN` is live for a dead service** |

### Root causes found and fixed

| Bug | Root cause |
|---|---|
| `WinError 10054`, open since 08-30 | **IPv6 address selection.** Telegram and Hugging Face resolve IPv6-first and reset ~1 in 5 connections. Measured 2/10 failures default, 0/10 forced IPv4. Every tool makes one request and exits, so it looked random |
| `[Offline]` at every session start | A missing `drive_sync.py`, reported as a network failure because three subprocess calls discarded stderr |
| Watchdog phantom warning since 08-19 | `audio_parity_check` imported from a file deleted after verifying its *destination* but not its *callers* |
| `graph_maintainer` un-importable | argparse ran at module level, consuming the importing process's argv |
| Drive auth stranding callers | A regression I introduced this session, found by reading a BDF comment recording the same bug in June |

### Shared modules built

Five now, following the `artifact_paths.py` pattern:

| Module | Consumers | Bugs fixed as a side effect |
|---|---|---|
| `drive_service.py` | 9 | 4 tools that could not survive a token expiry |
| `claude_client.py` | 4 | 2 tools with no HTTP timeout |
| `vault_paths.py` | 2 | closed 2 duplicate DESIGN flags |
| `net_prefer_ipv4.py` | 6 | the 10054 root cause |
| `drive_sync.py` | ported from BDF | restored the manifest sync |

~170 lines of duplicated Drive auth removed. One model string in the whole
toolchain, down from four.

### Renames and documentation

- `compile_session.py` → `ingest_session.py`, atomic across the file, the
  subprocess caller, four comments, both PowerShell profiles, and the shell
  function
- All 37 tool descriptions now honest. `tools_index.py` splits at the first
  period-space, so every title needed one — `watchdog.py` was swallowing its
  entire usage block into its index entry
- `category: library` distinguishes the 5 libraries from the 32 programs
- Eleven verification rules written into `~\.claude\CLAUDE.md`, loaded by
  every Claude Code session in all 12 repos

### Deliberately not done

Two duplications turned out to be load-bearing:

- **The Drive OAuth token stays with BDF** — issued per Google Cloud
  project, cannot be duplicated. Now documented in `CLAUDE.md`
- **`ingest_session.py` keeps its own HTTP block** — its exit codes
  (0 success, 1 error, 2 unavailable) carry meaning the shared client does
  not, and `session_close.py` branches on them

---

## 6. Things discovered that no sweep had found

Both were invisible to code-first mapping because neither has callers:

- **`08_TRIGGERS`** — 13 nodes, a full event architecture
- **`07_SYSTEM\Navigation_Shortcuts.md`** — 20 KB covering five projects
  terminal-by-terminal, aliases, folder tree, VS Code workspaces, git repos,
  troubleshooting, and common navigation mistakes. **`SYSTEM_MASTER.md` does
  not mention it, and nothing links `00_NAV`.** Seventeen navigation
  documents exist; the problem was never missing documentation
- **`C:\BRAIN_OS\scripts\`** — one abandoned stub, now deleted

---

## 7. Next, in order

1. **Rotate the tokens.** GitHub, Hugging Face, and revoke `RAILWAY_TOKEN`.
   Three files now instead of six: `03_APIS\.env`,
   `soccer-content-generator\.env`, `.claude.json:2337`
2. **File the GitHub GC ticket** for gig-tracker so the purged objects are
   removed server-side
3. **Check tomorrow's 7:30am report arrives** — first full unattended run
4. **The `implemented_by:` pass** on the 13 trigger nodes, ~90 minutes
5. **Link `Navigation_Shortcuts.md`** from `SYSTEM_MASTER.md` and add a
   `nav` shortcut via the alias table, not by hand
6. **`session_compiler.py` split** into distill and voice halves — now safe,
   the shared modules mean a split no longer duplicates anything

---

## 8. The pattern worth carrying

Every bug found today was hiding behind a message that named a **cause**
instead of a **symptom**. `[Offline]` for a missing file. "not found" for a
deleted import. Silence for a dropped send.

Each one stopped an investigation, because once a message asserts a
diagnosis nobody looks further. The change that unlocked everything else
was making one tool print what actually happened.

**Error messages should report the symptom. The reader draws the
conclusion.**

Second pattern, from the ledger itself: **it was systematically
pessimistic.** Nine flags were already fixed on disk. Fixes get applied and
not marked. Verify before working any flag — the backlog reads worse than
reality on the rows it has, and better than reality on the rows it does not.
