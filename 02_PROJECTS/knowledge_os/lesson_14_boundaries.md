# Lesson 14 - Boundaries

Found 2026-08-27 while tracing the BRAIN_OS navigation layer.

## Part 1 - Enforcement levels

Every rule sits at one of three levels. They look identical in a text
editor. You find out which one you have only by violating it.

**Level 1 - Declared.** Written in prose. A human must read it, remember
it, and choose to comply. Nothing checks. Drifts the moment attention
lapses.
Example: the writer field in artifacts.manifest.json. It says who should
write each file. No code reads it. Two of three declared readers of
Queue.md bypass it with hardcoded paths.

**Level 2 - Enforced at runtime.** Encoded in something that executes.
The program stops.
Example: artifact_paths.py line 39 raises AmbiguousArtifact when a bare
kind name is passed. Discovered by tripping it. That is what enforcement
feels like from outside.

**Level 3 - Enforced by a test.** The rule is an executable assertion. It
survives a future editor who does not know why the decision was made.
Example: artifact_paths.py line 108 asserts that queue must stay
ambiguous.

### Why Level 3 is the one that matters

Claude proposed pluralizing the manifest kind values. The reasoning
sounded principled - it would have fixed two collisions at once and
preserved the filename convention. It would also have silently removed a
real safety property.

Prose could not have stopped that. A doc saying keep queue ambiguous is
exactly what a confident editor reads and rationalizes past. The test
would have exited 1 and made the breakage undeniable.

**Tests are not for catching typos. They hold design decisions in a form
that survives the person who did not make them.**

### Where this shows up in BRAIN_OS

- Level 1: the writer field, Active_Environments.md, CLAUDE.md rules, the
  always flag financial info safeguard in compile_session.py
- Level 2: the ambiguity check, the two write-boundary checks
- Level 3: the FLAGS-protected and Principles-open assertions

custom-agent settings.json was already known as the only enforced policy
gate on the machine. This generalizes it: the same gap exists in the data
layer, not just in permissions.

## Part 2 - Trusted base, untrusted piece

    vault_path = BRAIN_OS / target        # compile_session.py:182

BRAIN_OS is a fixed root you control. target is a string that arrived from
a language model at runtime. Joined together, that is the address the
script writes to.

The pattern is general: **a trusted base plus an untrusted piece.**
Whether it is safe depends entirely on what you check about the untrusted
half.

### The check that was there

    if not vault_path.exists():

That verifies the file exists. It does not verify the file is one the
script should be touching. FLAGS.txt exists. Navigation.md exists. Both
were writable. An append to Navigation.md would have survived until the
next vault_index.py run regenerated the file, then vanished with no error.

**Does it exist is not the same question as is it allowed.** Confusing the
two is how the boundary was missed for months.

### What made it invisible

The rule was declared. Line 132 tells the model to use ONLY these paths.
But line 123 sent the first 150 of 396 paths, sorted alphabetically. The
model was following an instruction against a list that did not contain
what it needed, so it guessed.

PATH_CORRECTIONS at lines 165-168 is the fossil record: two hardcoded
fixes for two guessed paths. Someone patched the symptom twice without
finding the truncation.

**A declared rule that cannot be obeyed is worse than no rule, because the
failure looks like disobedience.**

### The fix shape

Two checks, both before the path is built:

1. Is the target a known vault node? Data already computed at line 111 and
   previously discarded.
2. Is it protected? New protected field in the manifest.

Refused items become HIGH priority flags carrying their content, so
blocked material surfaces instead of vanishing.

Derive, don't duplicate: the policy lives in the manifest beside the data,
not hardcoded in the tool. New human-only files need a flag in the
manifest, not an edit to compile_session.py.

Verified by dry run on an ordinary session: the model targeted
Queue_Archive.md and Navigation.md. Both blocked, both flagged.

## Commits

- 809a868 session_start.py crash on ambiguous artifact key
- 4cadcb0 write boundary enforced in compile_session.py
- fa36baf session filter, queue label, vault list truncation
