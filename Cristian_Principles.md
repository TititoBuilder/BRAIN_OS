The Principle of Verified Reality (The Sync Rule)
Context: Any system bridging local logic and remote state.

Global Pulse Check — Use account-level Change Tokens (changes().getStartPageToken()), not folder modifiedTime, to detect out-of-band drift. Folder timestamps are shallow and don't propagate. The token is a single lightweight API call that acts as a global dirty flag.
Session-Anchor TTL — TTL values are not magic numbers. Derive them from Max_Session_Duration + Buffer. For BRAIN_OS: 4 hours (3h max session + 1h buffer). One fresh sync per session, zero interruptions mid-flow.
Config Centralization — System sensitivity constants (TTL, token storage) belong in C:\BRAIN_OS\BRAIN_OS_CONFIG.json, not buried in project scripts. Global constants at the OS root; logic at the project root.

Proof: bdf_drive_manifest.json is a Security Log, not Ground Truth. It is only as reliable as its last sync. The TTL and Pulse Check together define when "cached" becomes "ghost."

---

The Principle of Single Canonical Authority (Stale Copy Elimination)
Context: Any tool or script that exists in multiple locations.

Stale copies of book_compiler.py exist at:
- C:\Dev\Projects\soccer-content-generator\book_compiler.py
- C:\Knowledge\CA\CA_Book\book_compiler.py
Canonical is C:\Dev\shared\book-compiler\. Both stale copies must be deleted — ACTION: delete this session or next.

Proof: Two copies diverge silently. A fix applied to the canonical never reaches the stale copy; the stale copy gets used by habit. The canonical wins only when it is the only one.

---

The Principle of Existence-First Operations (Skip-Existing Pattern)
Context: Any bulk generation operation (TTS, exports, compilations).

Never run bulk operations without first checking whether the output already exists. Always gate generation on absence:
```powershell
Where-Object { -not (Test-Path <expected_output_path>) }
```

Proof: Bulk regeneration wastes GPU/CPU time, risks overwriting known-good files, and obscures whether a run produced new work or redundant work. The skip-existing check costs nothing and prevents all three failure modes.

---

The Principle of Same-Session Triage (_review/ files)
Context: Any automated routing system that places files in a review queue.

Files landing in _review/ must be triaged within the same session they arrive — never left unreviewed across sessions. A tagged file in _review/ is a decision deferred, not a decision made. Accumulation turns a queue into a graveyard.

Proof: Stale _review/ files lose context. The session that produced them had the intent; the next session has to reconstruct it. Triage while the session is live costs minutes; triage after the session closes costs the full context reconstruction.
