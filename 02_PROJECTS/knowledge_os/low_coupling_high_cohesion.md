---
knowledge_os_machine_key: low_coupling_high_cohesion
knowledge_os_domain: Systems Design
knowledge_os_status: Practiced
knowledge_os_score: 75
knowledge_os_priority: High
knowledge_os_evidence: brain-audio package design across 3 venvs
knowledge_os_last_touched: '2026-05-13'
---
# Low Coupling, High Cohesion

## What It Is
These are two paired principles for how to divide a system into parts. High cohesion
means each part does one closely-related job, everything inside it belongs together.
Low coupling means parts depend on each other as little as possible, so each can
change without disturbing the others. Together they describe a well-divided system:
focused pieces that are loosely connected.

## How It Works
High cohesion is achieved by grouping things by responsibility, a module, a service,
a component holds one clear job and nothing unrelated, so you always know where a
given concern lives. Low coupling is achieved by minimizing and cleaning the
connections between parts: they talk through narrow, well-defined interfaces rather
than reaching into each other's internals, so one can be replaced or changed behind
its interface without the others noticing. A shared core package that many projects
depend on through a clean interface is the pattern in action, one cohesive source,
loosely depended upon, so a fix propagates without entangling the consumers.

## Why It Matters
A system with low cohesion scatters one concern across many places, so a change means
hunting through the whole codebase; a system with high coupling means touching one
part breaks others unpredictably. Both make systems fragile and hard to change.
Aiming for high cohesion and low coupling is what keeps a system maintainable as it
grows, you can find code by what it does, and change a part without a cascade. It is
the structural foundation under modular design, shared packages, and the whole idea
of building loosely-joined pieces rather than one tangled mass.

## The Pattern
Group by single responsibility for cohesion; connect through narrow interfaces for
low coupling. Focused parts, loosely joined, so you can find code easily and change
one piece without breaking the rest.
