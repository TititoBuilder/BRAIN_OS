# Taxonomy Decision — Two Intentional Lenses (not a divergence to collapse)

**Decided:** June 9 2026, after mapping all three schemes against real files.
**Status:** DECISION MADE. One execution item deferred (fill 2 shells = authoring).

## The finding

The system has TWO domain taxonomies at different granularities. They are NOT
parent/child and do NOT cleanly nest — they answer different questions:

### Lens A — 5-Layer architecture encyclopedia (`01_DOMAINS/`)
A *builder's* view: "what kind of engineering is this?" Top-level architectural
layers. Current state:
- ai_engineering      — 1067 words, 11 backlinks  [RICH, real]
- creative_systems    — 1262 words, 20 backlinks  [RICH, real]
- data_science        —  966 words,  9 backlinks  [RICH, real]
- software_architecture — 19 words, 0 backlinks   [EMPTY SHELL]
- systems_operations    — 18 words, 0 backlinks   [EMPTY SHELL]

### Lens B — 9 learning/browsing domains (obsidian_sync.json -> app)
A *learner's* view: "what topic do I want to listen to?" 77 topics tagged:
AI/ML(15), Systems Design(12), Python(10), Data Engineering(8), Cloud&DevOps(8),
APIs&Protocols(7), Audio&Media(6), Knowledge Systems(6), Security(5).

## The decision

**Keep BOTH. They are intentional, coexisting views — NOT a mess to reconcile.**
- Lens A organizes the knowledge ENCYCLOPEDIA (architectural layers).
- Lens B organizes LEARNING CONTENT (browsable audio topics).
- They don't nest because they measure different things. Python/Security/APIs
  span all architectural layers — that's expected, not a bug.

**Do NOT collapse to one scheme.** Forcing the 9 into the 5 (or vice versa) would
destroy a lens you actively use. The 3 rich Layer files prove the architecture
view has real value. The 9 are proven by 77 tagged topics + the live app.

**This document IS the reconciliation** — naming the intent so future-you or any
AI does not "fix" the divergence by destroying one scheme.

## Execution item (deferred — AUTHORING, Cristian's work)

The 2 empty shells (software_architecture, systems_operations) are INCOMPLETE,
not wrong. They have real topic content under Lens B (Systems Design is 12
topics) but no top-level encyclopedia entry written. FILL them (≈1000-word
backlinked entries like the other 3), don't delete them. This is authoring work.

## Note: a cluster of authoring work is emerging
Three deferred items are all AUTHORING (Cristian's knowledge work, not pipeline):
1. Fill software_architecture + systems_operations encyclopedia entries
2. Author 3 topic lessons: edge_tts, kokoro_tts, message_queues
3. (then voice #2 via converter.py -> tts_local.py)
Suggest a dedicated AUTHORING session for these, separate from systems/cleanup.

## On the external analysis that surfaced this
The prompt that raised the "taxonomy mismatch" was ~40% accurate: its DRY/
frontmatter-as-source principle was right (already applied via obsidian_sync),
but its "filename mismatch" root cause and "moved cristian_construction out of
01_DOMAINS" claim did NOT match the real filesystem (construction lives in
02_PROJECTS, always did; the real gap was the 5-vs-9 scheme split). Lesson:
verify any external analysis against the filesystem before acting — confident
prose can describe a system that isn't yours.
