# MCP Consolidation Plan — mcp_protocol → model_context_protocol

**Status:** PLAN ONLY. Nothing executed. Approve before any edit.
**Source of truth:** live trace (findstr + transcript compare), 2026-06-06.
NOT the prior Domain_Taxonomy notes — those were incomplete (missed refs).

---

## Decision (confirmed by transcript, not by doc claim)

`mcp_protocol` and `model_context_protocol` are the SAME lesson. Verified:
both transcripts explain "MCP stands for Model Context Protocol... lets Claude
Code connect to external systems (Obsidian, GitHub, DaVinci Resolve)."

Differences are cosmetic only:
- `mcp_protocol` transcript: "Cloud Code" (Whisper error), len 2199
- `model_context_protocol` transcript: "Claude code" (correct), len 2074
- Different section headers; minor phrasing.

**Canonical keeper = `model_context_protocol`** (accurate transcription +
correct full-name header). `mcp_protocol` is the loser, to be removed.

Underlying audio files (both path-based, both real, NOT yet deleted):
- LOSER  source: BRAIN_OS_Handbook/.../Phase_02_Architecture/mcp_registry_audio.mp3
- KEEPER source: BRAIN_OS_Handbook/.../Phase_05_Programming_Fundamentals/resolve_mcp_guide.wav

---

## Full blast radius — 7 references + 1 generated artifact

(From live findstr /s /i across *.py *.json *.html in 09_TOOLS)

| # | File | Line | Role | Action |
|---|------|------|------|--------|
| 1 | drive_browser.py | 81 | source map "mcp_setup" -> "mcp_protocol" | repoint value -> model_context_protocol |
| 2 | drive_download.py | 38 | downloads "mcp_protocol.mp3" | remove line (keeper has own download) |
| 3 | drive_index.json | 4 | live index entry mcp_protocol | DELETE entry (via Python) |
| 4 | knowledge_os.html | 98 | encyclopedia row (metadata) | change key cell -> model_context_protocol; merge/drop dup row |
| 5 | knowledge_os.html | 132 | DRIVE_INDEX JS object | delete "mcp_protocol" key |
| 6 | learning_paths.json | 13 | your_system path topics[] | replace "mcp_protocol" -> "model_context_protocol" |
| 7 | obsidian_sync.json | 464 | vault sync node machine_key | repoint -> model_context_protocol |
| + | path_manifests\your_system.json | 32 | BUILT manifest | regenerate after #6 (build_path_manifests.py) |

NOTE: knowledge_os.html already contains BOTH keys (line 132 DRIVE_INDEX). So
the app currently shows two encyclopedia entries for one lesson — consolidation
removes the duplicate the user can see.

---

## STAGE A — pure edits (NO GPU, fully reversible via git)

Makes the *individual topic* canonical everywhere. Order:

A1. drive_index.json — delete "mcp_protocol" entry. PYTHON ONLY (never
    PowerShell ConvertTo-Json). Keeper entry model_context_protocol untouched.
A2. learning_paths.json — your_system topics[]: mcp_protocol ->
    model_context_protocol. PYTHON ONLY.
A3. obsidian_sync.json line 464 — machine_key -> model_context_protocol.
    PYTHON ONLY. (Check: does keeper already have a node? If yes, merge not add.)
A4. drive_browser.py line 81 — source map value -> model_context_protocol.
    Text edit, BOM-free.
A5. drive_download.py line 38 — remove "mcp_protocol.mp3" line. Text edit.
A6. knowledge_os.html lines 98 + 132 — repoint key, drop duplicate row/key.
    BOM-free write ([System.IO.File]::WriteAllText). Close Obsidian if it
    touches vault config (it doesn't here, but html is git-tracked).
A7. Regenerate path_manifests\your_system.json via build_path_manifests.py.
A8. Verify: python -c check that "mcp_protocol" returns ZERO hits in index +
    learning_paths. Re-run findstr to confirm only intended refs remain.
A9. git add + commit + push affected repos (BRAIN_OS; read-along-app if backend
    transcripts copied). Atomic commit, descriptive message.

After Stage A: the topic is clean. BUT the your_system STITCHED PATH AUDIO is
now stale — it still contains mcp_protocol's audio segment. Karaoke for that
path will mismatch until Stage B. This is expected and acceptable as an
interim state (documented, not "for now" debt — it has a definite fix in B).

---

## STAGE B — GPU re-stitch (separate session, at the machine)

B1. Re-stitch your_system path with model_context_protocol audio replacing the
    old mcp_protocol segment. Tool: audio_stitcher.py (Kokoro af_heart path).
B2. GPU-transcribe the new stitched path for karaoke. transcribe_batch.py.
B3. Re-upload stitched path to Drive (_paths/), capture Drive ID.
B4. Update path index entry via PYTHON. git push.
B5. Verify: transcript_integrity.py shows 0 dupe sets.
B6. Verify /audio-local for the your_system path returns 200 + correct karaoke.

---

## Safety invariants (apply to every step)
- READ-ONLY until each step approved. Drive has no undo. Audio is expensive.
- JSON edits via Python json lib ONLY. No PowerShell ConvertTo-Json/Set-Content.
- BOM-free writes via [System.IO.File]::WriteAllText for any text/html.
- drive_sync.py --delete-files is the ONLY deleter (not needed in Stage A —
  we're deleting an INDEX entry, not a Drive file; the loser audio
  mcp_registry_audio.mp3 stays in Drive unless we explicitly choose to remove
  it — DEFER that decision, low priority, harmless orphan).
- Commit per stage; git is the rollback net.

## Open question deferred to Stage A execution
- A3: does model_context_protocol already have an obsidian_sync node? If so,
  line 464 is a MERGE (drop mcp_protocol node), not a repoint. Check before edit.
- Loser audio file mcp_registry_audio.mp3 in Drive: leave as orphan for now,
  or remove in a later Drive-cleanup pass. NOT part of this consolidation.
