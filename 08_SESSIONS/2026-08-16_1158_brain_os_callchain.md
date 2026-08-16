Reading all 8 files in parallel to verify every edge before claiming anything.
`token_sync.py` does not exist. Now checking where `session_close.py` actually lives — the CLAUDE.md says it runs from `soccer-content-generator`, not `09_TOOLS`.
Two copies exist. Reading both plus checking for cross-references.
Now confirming there are no `importlib` usages and no cross-imports between the 8 listed files.
All data verified. Now let me produce the map.

---

## Session-Lifecycle Call Chain — `09_TOOLS`

### Verified edges (every line number confirmed against source)

---

### PHASE 1 — SESSION START

```
1. session_start.py              [entry point — no inbound callers within the 8 files]
   │
   ├─ :170  subprocess.run → graph_maintainer.py  [EXTERNAL — soccer-content-generator/scripts/]
   │                                               [BLOCKING]
   │         └─ (graph_maintainer.py imports graphify, drive_sync, etc. — out of scope)
   │
   ├─ :208  subprocess.run → git status           [BLOCKING — informational only]
   │
   └─ Telegram via urllib.request                 [no subprocess — direct HTTP POST]
```

**Note:** `session_start.py` does NOT import or call any of the other 7 listed files.

---

### PHASE 2 — DURING SESSION (all standalone, invoked on demand)

```
2. task_session.py               [entry point — no inbound callers within the 8 files]
   │
   └─ :139  subprocess.run → clip (Windows clipboard)  [BLOCKING]
            └─ no calls to any other listed module

3. graphify.py                   [entry point — no inbound callers within the 8 files]
   └─ no subprocess calls; pure stdlib + ast/pathlib/json
   └─ no imports of any other listed module

4. subprocess_graph.py           [entry point — no inbound callers within the 8 files]
   └─ no subprocess calls; reads source files with re/pathlib, writes JSON
   └─ no imports of any other listed module

5. compile_session.py            [entry point — no inbound callers within the 8 files]
   │
   ├─ :101  urllib.request → Anthropic API (claude-sonnet-4-6)  [BLOCKING — HTTP]
   │
   ├─ :286  subprocess.run → git add            [BLOCKING]
   ├─ :290  subprocess.run → git pull --rebase  [BLOCKING]
   ├─ :300  subprocess.run → git commit         [BLOCKING]
   └─ :301  subprocess.run → git push           [BLOCKING]
            └─ no calls to any other listed module
```

---

### PHASE 3 — SESSION CLOSE

```
6. session_close.py  (09_TOOLS version)   [entry point — no inbound callers within the 8 files]
   │
   ├─ :71   subprocess.run → git log (per-repo loop)  [BLOCKING]
   │
   ├─ :239  subprocess.run → vault_index.py            [BLOCKING]  ◄── only cross-module edge
   │         └─ vault_index.py regenerates 00_DASHBOARD/Navigation.md; no further subprocess calls
   │
   ├─ :244  subprocess.run → git add Navigation.md     [BLOCKING]
   ├─ :247  subprocess.run → git diff --cached         [BLOCKING]
   ├─ :249  subprocess.run → git commit Navigation.md  [BLOCKING]  (conditional on diff)
   │
   └─ :275  subprocess.Popen → watchdog.py             [BACKGROUND — non-blocking]
                                                        [watchdog.py is OUT OF SCOPE but is real;
                                                         it uses importlib.util at line 15]

7. vault_index.py                          [called only by session_close.py:239]
   └─ no subprocess calls; pure pathlib writes to Navigation.md
```

---

### ORPHAN / REACHABILITY AUDIT

| File | Inbound callers (within the 8) | Status |
|---|---|---|
| `session_start.py` | none | **entry point** (invoked directly by user / CLAUDE.md hook) |
| `task_session.py` | none | **entry point** (invoked manually with `--task` flag) |
| `vault_index.py` | `session_close.py:239` | **reachable** |
| `compile_session.py` | none | **entry point** (invoked manually post-session) |
| `graphify.py` | none | **entry point** (invoked manually; also detectable by `subprocess_graph.py` scan but not spawned by it) |
| `subprocess_graph.py` | none | **entry point** (ad-hoc analysis tool) |
| `session_close.py` | none | **entry point** (run from soccer-content-generator terminal per CLAUDE.md) |
| `token_sync.py` | — | **DOES NOT EXIST** — file is absent from disk |

---

### Key findings

1. **`token_sync.py` is NOT in `09_TOOLS`** — but it DOES exist, at `C:\Dev\Projects\soccer-content-generator\token_sync.py` (verified 2026-08-16). The original "ghost" claim was wrong: it searched only `09_TOOLS` and reported a scoped miss as absence from disk. Out of scope for this audit, not nonexistent.

2. **Only one real cross-module edge** among the 8 files: `session_close.py:239 → vault_index.py` (blocking subprocess).

3. **No `importlib` usage** in any of the 8 listed files. The `importlib` calls in `09_TOOLS` belong to `watchdog.py` (line 15) and `audio_stitcher.py` (line 48) — both out of scope.

4. **`subprocess_graph.py` is a meta-analyzer** — it scans for subprocess edges but spawns nothing itself.

5. **`session_close.py` has two copies** — `09_TOOLS\session_close.py` (the BRAIN_OS closer, calls `vault_index.py` + fires `watchdog.py` in background) and `soccer-content-generator\session_close.py` (the BDF closer, calls `sync_brain.py` instead). CLAUDE.md says to run from `soccer-content-generator`; the `09_TOOLS` copy is the one that hits `vault_index.py`. Both end with `subprocess.Popen(watchdog.py)` [background, non-blocking] at their final lines.

6. **`session_start.py` calls `graph_maintainer.py`** (external — soccer-content-generator/scripts) at line 170, not any of the 8 listed files. This edge crosses the scope boundary.
