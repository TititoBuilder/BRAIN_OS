---
knowledge_os_machine_key: knowledge_graph_design
knowledge_os_domain: Knowledge Systems
knowledge_os_status: Practiced
knowledge_os_score: 72
knowledge_os_priority: High
knowledge_os_evidence: Federated Graph System, soccer-content-generator.graphify.json
knowledge_os_last_touched: '2026-05-22'
---
# Knowledge Graph Design

## What It Is
A knowledge graph represents what you know as a network of nodes and the
relationships between them, rather than as a hierarchy of folders or a flat list of
files. Designing one well is about deciding what counts as a node, what the
meaningful relationships are, and how to keep the graph navigable as it grows so it
stays a map of your knowledge rather than a tangle.

## How It Works
Each node represents one concept, document, or entity, and edges represent
relationships between them. A key design choice is granularity, what deserves to be
its own node, since too coarse loses structure and too fine fragments meaning, the
right grain is the most specific true unit. Edges can be plain connections or typed
and directed, where the link itself carries meaning and direction, this enforces
that, this is enforced by that, turning a graph of mere connectivity into a queryable
semantic web. A node can represent something without containing it, holding a
describing stub that points to where the real thing lives, which separates identity
from location.

## Why It Matters
A folder hierarchy forces each thing into one place, but real knowledge connects in
many directions at once, which a graph captures and a tree cannot. Designing the
graph deliberately, right granularity, typed edges, identity separated from location,
is what makes it a tool you can actually navigate and query rather than a sprawl.
This is the architecture of your own vault, and the design choices determine whether
it reveals how your knowledge connects or just stores files in a fancier way. The
graph is the map; its design is whether the map is readable.

## The Pattern
Model knowledge as nodes and meaningful, typed relationships at the right grain, and
let nodes represent things without containing them. Design the graph as a navigable
map, not a folder tree; the structure is what makes it usable.
