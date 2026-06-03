---
type: session-record
date: 2026-06-02
project: brain-os
domain_relevance: "[[software_architecture]]"
topics:
  - file-organization-audit
  - naming-contract
  - knowledge-graph-modeling
  - tts-pipeline-debug
---
# Session Record — 2026-06-02: Organizing Without Breaking Code

## Goal
Combine, organize, and rename files across three stores (Google Drive,
Obsidian vault, Read-Along app) without breaking a deployed application.
Constraint: TIME, not understanding — learning must convert to durable
structure.

## What was built

### 1. The audit + cleanup loop
A read-only auditor (`audit_files.py`) scans all project roots and classifies
every file as **machine-key** (code looks it up by exact string — frozen) or
**human-readable** (safe to rename). It finds machine-keys by scanning for
references: any code/config reference = machine-key, only wiki-links or none
= human-readable. A second tool (`cleanup_proposer.py`) proposes safe
RENAME/TRASH actions, refuses anything code-referenced, defaults to dry-run,
and asks per-file before acting. Trash is a recoverable move, never a delete.

Iterative debugging hardened the auditor: generic-name collisions
(`settings.json` across projects), self-contamination (the audit's own JSON
output listing every filename), and a `_trash` folder being re-scanned were
each found and fixed. Lesson: a tool that writes output into the territory it
scans contaminates its next run — keep tool output outside scanned roots.

### 2. The Naming Contract
A prescriptive standard saved to the vault. Core rule (Rule 0): classify every
file as machine-key (stability over clarity — frozen, renaming is a migration)
or human-readable (clarity over stability — rename freely). Other rules: one
canonical copy per asset; derivatives encode what they're derived FOR
(`name.tts-processed.txt`, not an inherited source name); files live with
their project; stores agree on names.

### 3. The Domain Taxonomy
`01_DOMAINS` is a personal map of computer science. Five fields, standard
names: ai_engineering, software_architecture, data_science, creative_systems,
systems_operations (the last discovered by finding ~15 files that fit no
existing domain). Top-level split: `01_DOMAINS` = declarative knowledge
("what I know," universal, timeless) vs `02_PROJECTS` = operational records
("what I did," local, time-stamped). Sorting test: "Would this be true if I'd
never built any of my projects?" Yes = domain; No = project.

## Key principles learned

**Granularity** — a link or category should point at the most specific true
node, not a vague container. Appeared three times (filenames, wiki-links,
domain taxonomy) as one underlying law.

**Identity vs. location (the stub pattern)** — a graph node can *represent* a
thing without *containing* it. Code lives on disk; the vault holds a stub that
describes and points at it. Resolves the contradiction between "be specific"
and "don't duplicate the code."

**Typed, directed edges** — frontmatter relationships (`enforces`,
`enforced_by`) turn a plain graph into a directed semantic web: edges carry
meaning and direction a machine can query, not just connectivity.

**Functional cohesion** — sort by what a thing *builds*, not what it *is*. Four
"orchestrators" went to four different domains because the domain is defined by
their output, not by the shared word "orchestrator."

**The Map Principle** — standard field names are automatic sorting keys the
whole world already uses. They connect personal knowledge to global knowledge,
reveal gaps (a field's known sub-topics show what you haven't learned), and let
principles transfer across fields. Mapped learning compounds: each named
concept makes the next cheaper to learn.

## The TTS content-mismatch investigation

Found a live-app bug: five transcripts had the correct `machine_key` but the
wrong `text` (a copy of another topic's content). Users tapping a topic heard
the wrong lecture.

Investigation trail: timestamps showed canonical files in a 5/28 batch and bad
copies in a 5/30 batch. Internal keys matched filenames (ruling out a file-copy
bug). `transcribe_batch.py` was exonerated — it binds key and text to one audio
path, so no misroute is possible there. The bad audio itself was wrong. Traced
to `gen_tts_staging.py`: after an exact-path miss it fell back to a fuzzy glob
(`*{name}*_TTS.txt`) and took `candidates[0]` from a shared, never-purged
directory — selecting a stale leftover from a prior topic's run. Right key,
wrong audio body.

Deeper cause: the `.md` sources were near-empty stubs (~70 chars: title +
"auto-created by Knowledge OS"). ~75 of ~78 topics are unwritten. The glob bug
was masking a missing-content problem. Fix: removed the glob fallback (fail
loud on exact-path miss). The remaining work is authoring content, a content
project, not a code fix.

Lesson: fail-loud beats guess-wrong. A silent fuzzy fallback turned "this file
is missing" into "play the wrong file." The same discipline as the auditor
refusing rather than assuming.

## Outcome
Every project went through the audit → propose → verify → apply loop.
`knowledge/` cleaned, `brain-os` and `soccer-content-generator` cleaned (safe
sets), the contract and taxonomy grounded in the vault, the TTS bug traced and
documented, the generator hardened. Deferred by design: authoring the ~75 stub
topics, a link-aware rename tool for wiki-linked vault files, and trashing
mislabeled transcript duplicates once real audio exists.
