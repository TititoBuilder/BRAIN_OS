---
knowledge_os_machine_key: monolith_vs_microservices
knowledge_os_domain: Systems Design
knowledge_os_status: Practiced
knowledge_os_score: 78
knowledge_os_priority: High
knowledge_os_evidence: ch07_deployment.md CA Book
knowledge_os_last_touched: '2026-05-13'
---
# Monolith vs Microservices

## What It Is
This is the core decision about how to split a system into deployable pieces. A
monolith is one application: all the code, all the features, built and deployed as
a single unit. Microservices break the same system into many small independent
services, each owning one capability and running on its own. The question is not
which is better in the abstract, but which fits the size and stage of what you
are building.

## How It Works
In a monolith, components talk to each other through ordinary function calls
inside one process, and you deploy the whole thing at once. It is simple to build,
simple to test end to end, and simple to reason about because everything is in one
place. Microservices instead communicate over the network, each service has its
own codebase, its own database, and its own deployment, and they coordinate
through APIs or messages. That independence costs you network calls, distributed
failure handling, and operational complexity, in exchange for letting teams deploy
and scale each piece separately.

## Why It Matters
The common mistake is reaching for microservices too early, paying all their
complexity before having the scale or team size that justifies it. A monolith is
almost always the right place to start: it is faster to build and easier to change
while you are still discovering what the system should do. You split into services
when specific pressures appear, a piece needs to scale independently, separate
teams keep colliding in one codebase, one part needs a different technology. The
split should be a response to real pain, not a default.

## The Pattern
Start with a monolith; extract services only when a concrete pressure demands it.
Distribution is a cost you pay for independence, so do not pay it until you need
what it buys.
