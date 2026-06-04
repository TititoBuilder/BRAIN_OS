---
knowledge_os_machine_key: blast_radius_principle
knowledge_os_domain: Systems Design
knowledge_os_status: Mastered
knowledge_os_score: 85
knowledge_os_priority: High
knowledge_os_evidence: Cristian_Principles.md â€” venv contamination incident
knowledge_os_last_touched: '2026-05-13'
---
# Blast Radius Principle

## What It Is
Blast radius is how far the damage spreads when something changes or fails. The
principle is to understand and limit that reach before you act: before changing a
piece of a system, know everything that depends on it, so you can see how far a
mistake would propagate. A small blast radius means a failure stays contained; a
large one means a single change can break things far away.

## How It Works
You trace dependencies before acting. Before renaming a file, you find everything
that references it; before changing a shared component, you map what relies on it.
That map is the blast radius, the set of things a change could affect. The practice
is to deliberately keep that radius small through how you structure the system,
isolating components so failures cannot cascade, and to expand your awareness of it
before risky changes, checking references rather than assuming a change is local.
When the radius is large, you proceed as a careful staged migration; when it is
small, you can move freely.

## Why It Matters
Most damaging mistakes come from underestimating reach, a change that seemed local
breaks something three systems away because a hidden dependency was missed. This
principle, applied throughout this work, is why a machine-key file is checked for
references before renaming, why a shared-directory change is examined for what else
uses it, why a live-app migration is treated more carefully than an isolated edit.
Knowing the blast radius converts a blind change into an informed one, and
structuring for a small radius is what lets a system grow without becoming fragile.

## The Pattern
Map what depends on a thing before you change it, and structure systems so failures
stay contained. Know the reach before you act; keep the radius small by design.
