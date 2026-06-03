---
type: contract
enforces: "[[Cristian_Principles]]"
enforced_by:
  - "[[Tools_Registry#audit_files]]"
  - "[[Tools_Registry#cleanup_proposer]]"
---
# Naming Contract

The single naming standard for every file across all three stores:
local disk, Google Drive, and the Obsidian vault. The audit script
(audit_files.py) measures reality against this document.

This contract is prescriptive. It says what SHOULD exist.

---

## Rule 0 - Every file is one of two classes

Classify the file before any other rule.

### Machine-key files
A filename code looks up by exact string. Renaming breaks something.
Examples: Drive audio the Read-Along app streams, GitHub transcripts
the app fetches, Python modules imported by name, config keys.
RULE: STABILITY OVER CLARITY. The name is a contract with code. A
rename is a coordinated migration across every consumer plus redeploy,
never a casual cleanup.

### Human-readable files
A filename only humans read. Nothing looks it up by exact string.
Examples: vault notes, drafts, documentation, session archives.
RULE: CLARITY OVER STABILITY. Optimize for description. Rename freely.

The audit decides class by scanning for references: any code/config
reference = machine-key; only wiki-links or none = human-readable.

---

## Rule 1 - Canonical filename format (human-readable files)

    YYYY-MM-DD_descriptive-title.ext   (dated: sessions, logs)
    descriptive-title.ext              (undated: notes, docs)

Lowercase, hyphen-joined. No spaces. No version suffixes (_final, _v2,
_new, _BACKUP, _OLD) - version lives in git, not the filename. The
name describes CONTENT, not location or author. Machine-key names are
frozen as-is; this format does not apply to them.

---

## Rule 2 - One canonical copy; everything else is a pointer

Each asset has exactly ONE canonical home:
- Audio (.mp3/.wav)        -> Google Drive (never committed to git)
- Transcripts/manifests    -> the repo the app reads (git) [pending audit confirm]
- Knowledge (.md)          -> the Obsidian vault
- Code (.py)               -> its project repo

A file existing in two stores is either a pointer (index entry,
wiki-link, manifest row) or a duplicate to delete. The audit flags any
asset physically present in two places.

---

## Rule 2b - Derivative files encode what they are derived FOR

A file produced by transforming another file is a DERIVATIVE, not a
duplicate. Its name must announce its role via suffix - never inherit
the source name unchanged.

    source:      bdf-complete-reference.txt        (human-readable master)
    TTS-prepped: bdf-complete-reference.tts-processed.txt
    audio:       bdf-complete-reference.wav

Rationale: the TTS pipeline strips punctuation so the voice does not
read "underscore" / "hashtag" aloud, producing a mangled text copy.
That copy looks like a duplicate but is a derived artifact with a
different role. The suffix (.tts-processed, .wav) makes the role
explicit so it is never mistaken for, or merged with, its source.
A derivative is canonical for ITS purpose; the source stays canonical
for reading. Both are kept; neither is junk.

(Future optimization: have the producing script emit the .tts-processed
suffix automatically. Until then, this is a manual naming convention.)

---

## Rule 3 - Files live with their project

Owner projects: soccer-content-generator (BDF), cristian-construction
(CA), read-along-app, resolve-mcp-server, brain-audio (shared core),
book-compiler (shared core), brain-os (the vault/system).
Shared-core files are owned by no single project by design. A file
that cannot be assigned an owner is orphaned: assign or delete.

---

## Rule 4 - The three stores agree

The same logical asset is named consistently across stores. When a
machine-key form must differ from the human form (frozen old name),
the vault note records the mapping in frontmatter:

    machine_key: legacy_fingerprint_v1

---

## Rule 5 - No empty files, no dead references

The audit flags empty .md files, wiki-links to missing files, manifest
entries pointing to missing Drive files, and Drive files no manifest
points to. Orphan != delete: leaf nodes (templates, daily logs,
framework files like package.json) are legitimately unreferenced.

---

## The audit is read-only

audit_files.py never renames, moves, or deletes. cleanup_proposer.py
proposes safe actions (RENAME real content, TRASH garbage to a
recoverable _trash folder) and acts only with --apply, asking y/N per
file. It refuses any machine-key or code-referenced file.