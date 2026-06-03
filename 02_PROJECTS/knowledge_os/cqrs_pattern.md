---
knowledge_os_machine_key: cqrs_pattern
knowledge_os_domain: Systems Design
knowledge_os_status: Not Started
knowledge_os_score: 0
knowledge_os_priority: Low
---
# CQRS Pattern

## What It Is
CQRS stands for Command Query Responsibility Segregation. It is the idea of
separating the path that changes data, commands, from the path that reads data,
queries, so each can be designed for its own job. Instead of one model serving
both writes and reads, you split them, because what makes writing safe and what
makes reading fast are often different things.

## How It Works
The write side accepts commands, do this, change that, and is built around
correctness: validating, enforcing rules, keeping data consistent. The read side
answers queries and is built around speed and shape: it can use denormalized views,
caches, or a separate data store tuned for exactly the reads your application
makes. The two sides can use different models of the same data, and in more
advanced setups even different databases, with changes from the write side
propagating over to update the read side. The essential move is simply refusing to
force one model to be good at both.

## Why It Matters
In many systems reads vastly outnumber writes and have very different needs: reads
want fast, flexible, pre-shaped data, writes want strict validation and
consistency. A single model trying to serve both ends up compromised at each.
Separating them lets you optimize and scale each independently, scale the read side
out for traffic without touching write logic. The tradeoff is added complexity and
the read side often being slightly behind the write side, so CQRS is worth it when
read and write demands genuinely diverge, not as a default for simple systems.

## The Pattern
Split the write path from the read path so each is built for its real job,
correctness for commands, speed and shape for queries. Apply it when reads and
writes truly diverge, not everywhere by reflex.
