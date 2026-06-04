---
knowledge_os_machine_key: data_modeling
knowledge_os_domain: Data Engineering
knowledge_os_status: Learning
knowledge_os_score: 45
knowledge_os_priority: Medium
knowledge_os_last_touched: '2026-04-20'
---
# Data Modeling

## What It Is
Data modeling is deciding how to structure your data, what the entities are, what
fields they hold, and how they relate, before you store it. It is the blueprint
that determines whether your data is easy to query and keep correct, or a tangle
that fights you at every turn. The model shapes everything built on top of it.

## How It Works
You identify the real-world things your system tracks, a user, an order, a
document, and define each as an entity with its attributes. Then you define the
relationships: one user has many orders, one order belongs to one customer. A
central decision is normalization versus denormalization. Normalized data stores
each fact once and links to it, which keeps it consistent and avoids contradictory
duplicates, but requires joining tables to answer queries. Denormalized data
duplicates facts to make reads fast and simple, at the cost of having to keep the
copies in sync. The right choice depends on whether the workload is write-heavy and
needs consistency, or read-heavy and needs speed.

## Why It Matters
The data model is one of the hardest things to change later, because everything,
queries, code, other systems, comes to depend on its shape. A good model makes
correct queries natural and bad states impossible to represent; a poor one makes
every feature a struggle and lets inconsistent data creep in. The
normalize-versus-denormalize choice directly echoes the read-versus-write
separation in CQRS: structure for consistency where you write, structure for speed
where you read. Getting the model right early pays back over the whole life of the
system.

## The Pattern
Model entities, attributes, and relationships deliberately before storing.
Normalize for consistency, denormalize for read speed, and choose based on the real
workload. The model is expensive to change, so design it with care.
