---
knowledge_os_machine_key: cap_theorem
knowledge_os_domain: Systems Design
knowledge_os_status: Not Started
knowledge_os_score: 0
knowledge_os_priority: Medium
---
# CAP Theorem

## What It Is
The CAP theorem is a foundational rule about distributed systems, systems whose data
lives across multiple machines. It says that when a network failure splits those
machines so they cannot all talk to each other, you can have either consistency or
availability, but not both at the same time. You must choose which to sacrifice when
the network breaks.

## How It Works
The three letters are Consistency, every read sees the latest write, all nodes agree;
Availability, every request gets a response; and Partition tolerance, the system keeps
working even when the network splits nodes into groups that cannot communicate. In a
distributed system partitions are not optional, networks fail, so partition tolerance
is a given. That forces the real choice between the other two during a partition: if
two nodes cannot sync, you either refuse some requests to avoid serving stale data,
choosing consistency, or you answer anyway with possibly out-of-date data, choosing
availability. There is no third option when the network is split.

## Why It Matters
CAP names a tradeoff you cannot engineer away, only choose deliberately based on what
your system needs. A banking ledger leans toward consistency, better to reject a
transaction than allow two conflicting ones; a social feed leans toward availability,
better to show slightly stale posts than show nothing. Understanding CAP stops you
from chasing the impossible, a distributed system that is perfectly consistent and
perfectly available under all failures, and points you instead at the honest
question: when the network breaks, which do I give up?

## The Pattern
In a distributed system under a network partition, choose consistency or
availability, not both. The tradeoff is unavoidable; pick the one your use case
needs and design for it deliberately.
