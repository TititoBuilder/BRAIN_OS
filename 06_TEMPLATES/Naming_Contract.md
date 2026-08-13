# Naming Contract

The single naming standard for every file across all three stores:
local disk, Google Drive, and the Obsidian vault. The audit script
measures reality against this document. If a file violates a rule
here, the audit flags it.

This contract is prescriptive. It says what SHOULD exist. Reality is
brought into line with it, not the other way around.

---

## Rule 0 — Every file is one of two classes

Before any other rule, classify the file.

### Machine-key files
A filename that code looks up by exact string match. Renaming it
breaks something downstream.

Examples in this system:
- Drive audio the Read-Along app streams (looked up by `machine_key`)
- GitHub transcripts the app fetches by exact name
- Python modules imported with `from x import y`
- JSON/config keys referenced by other tools

**Rule for machine-key files: STABILITY OVER CLARITY.**
The name is a contract with code. You do not improve it casually.
A rename is a coordinated change across every consumer + a redeploy.
Treated as a migration, never a cleanup.

### Human-readable files
A filename only humans read. Nothing looks it up by exact string.

Examples:
- Vault markdown notes
- Draft scripts and chapter sources not yet imported anywhere
- Documentation, session archives, reference material

**Rule for human-readable files: CLARITY OVER STABILITY.**
Optimize the name for description. Rename freely. Worst case is a
broken wiki-link, which the audit catches.

The audit's first job per file: decide which class it is by scanning
for references to it. No references found anywhere = human-readable.
Any reference found = machine-key, handle with care.

---

## Rule 1 — Canonical filename format

For human-readable files:

    YYYY-MM-DD_descriptive-title.ext      (dated: sessions, logs)
    descriptive-title.ext                 (undated: notes, docs)

- Lowercase, words joined by hyphens inside the title.
- Date prefix only when the file is an event in time.
- No spaces. No version suffixes like `_final`, `_v2`, `_new`.
  Version lives in git, not the filename.
- The name describes the CONTENT, not where it lives or who made it.
  `audio-fingerprinting.md` not `brain-audio-cristian-notes-doc.md`.

For machine-key files: the name is whatever the code already expects.
The contract does not impose a format on these — it freezes them.
A separate migration changes them, with full blast-radius review.

---

## Rule 2 — One canonical copy, everywhere else is a pointer

A given asset has exactly ONE canonical location:

- **Audio (.mp3, .wav)** — canonical home is Google Drive. Never
  committed to git. Already enforced by `.gitignore`.
- **Transcripts / manifests (.json)** — canonical home is the repo
  that the app reads from (GitHub).
- **Knowledge (.md)** — canonical home is the Obsidian vault.
- **Code (.py)** — canonical home is its project repo.

If the same asset exists in two stores, one is canonical and the
other is either a pointer (an index entry, a wiki-link, a manifest
row) or it is a duplicate to be deleted. The audit flags any asset
that physically exists in two places.

---

## Rule 3 — Grouping: files live with their project

Every file belongs to exactly one project. The project owns it.

    soccer-content-generator  (BDF)
    cristian-construction     (CA)
    read-along-app
    resolve-mcp-server
    brain-audio               (shared core)
    book-compiler             (shared core)
    brain-os                  (the vault / system itself)

Shared-core files (`brain-audio`, `book-compiler`) are the explicit
exception: they are owned by no single project and consumed by many.
That is by design (Low Coupling / High Cohesion). The audit treats a
shared-core import as expected, not as blurry coupling.

A file that can't be assigned to one project is orphaned. Orphaned
files get assigned an owner or deleted. Nothing lives nowhere.

---

## Rule 4 — The three stores must agree

The same logical asset is named consistently across stores so a
human (or a script) can trace it end to end:

    vault note            audio-fingerprinting.md
    Drive audio           audio-fingerprinting.wav     (machine-key)
    app manifest entry    "audio-fingerprinting"        (machine-key)

When the machine-key form must differ from the human form (because
code froze an older name), the vault note records the mapping in its
frontmatter:

    machine_key: legacy_fingerprint_v1

So the human-readable side stays clean while the frozen key stays
traceable. The audit verifies every machine-key has a vault note that
declares it.

---

## Rule 5 — No empty files, no dead references

Carried over from existing vault principle. The audit flags:
- Empty `.md` files (no content under the heading)
- Wiki-links pointing to files that don't exist (dead references)
- Manifest entries pointing to Drive files that don't exist (stale)
- Drive files no manifest points to (orphaned audio)

---

## What the audit does NOT do

The audit is read-only. It never renames, moves, or deletes. It
produces a truth map: for every file, its class, its owner project,
its canonical status, and every reference to it. Renames are a
separate, deliberate step taken only after reading that map.
