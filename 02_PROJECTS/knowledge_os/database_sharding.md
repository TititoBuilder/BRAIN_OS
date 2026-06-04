---
knowledge_os_machine_key: database_sharding
knowledge_os_domain: Systems Design
knowledge_os_status: Not Started
knowledge_os_score: 0
knowledge_os_priority: Low
---
# Database Sharding

## What It Is
Sharding is splitting one database across many machines by dividing the data
itself, so each machine holds only a portion. When a single database server cannot
hold or handle all the data, sharding partitions it, this range of users here, that
range there, so the load and storage spread across many servers that together act
as one larger database.

## How It Works
You choose a shard key, the field that decides which shard a given record lives on,
say user ID, and a rule that maps each key to a shard. A query for a specific
record uses the key to go straight to the right shard. The choice of shard key is
the make-or-break decision: a good key spreads data and load evenly across shards,
while a bad one creates hot spots where one shard gets most of the traffic, defeating
the purpose. Queries that span many shards, or that do not include the shard key,
become expensive because they must hit every shard, so the data layout has to match
how you actually query.

## Why It Matters
Sharding is how databases scale beyond what one machine can do, the data equivalent
of running many service instances behind a load balancer, but harder, because data
has identity and location in a way stateless requests do not. It is also a step you
should avoid until you genuinely need it: it adds real complexity, cross-shard
queries, rebalancing, and the irreversible weight of a shard-key choice. Like
microservices, the lesson is not to reach for it early, a single well-tuned
database serves most systems for a long time.

## The Pattern
Split data across machines by a shard key chosen to spread load evenly, and design
queries to use that key. Powerful for scale, costly in complexity, so shard only
when one machine truly is not enough.
