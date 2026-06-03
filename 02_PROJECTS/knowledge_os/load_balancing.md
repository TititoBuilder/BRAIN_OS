---
knowledge_os_machine_key: load_balancing
knowledge_os_domain: Systems Design
knowledge_os_status: Not Started
knowledge_os_score: 0
knowledge_os_priority: Low
---
# Load Balancing

## What It Is
Load balancing is the practice of spreading incoming requests across several
copies of a service so no single copy gets overwhelmed. When one machine cannot
handle all the traffic, you run several and put a load balancer in front to
distribute the work among them. It is the mechanism that turns many servers into
what looks like one strong service.

## How It Works
The load balancer sits between clients and your pool of identical server
instances. Each request that arrives gets sent to one of the instances according
to a strategy: round-robin cycles through them in turn, least-connections sends
to whichever is least busy, others account for server capacity. Crucially, the
balancer runs health checks, it regularly tests each instance and stops sending
traffic to any that fail, routing around the dead one until it recovers. This is
why load balancing also delivers reliability, not just capacity: a failed
instance is simply taken out of rotation.

## Why It Matters
Load balancing is how systems scale horizontally, you add capacity by adding more
identical instances rather than buying one bigger machine, and how they stay
available, since the failure of one instance does not take the service down. It is
also what makes statelessness pay off: because any instance can handle any
request, the balancer is free to send a request anywhere. The two ideas reinforce
each other, stateless services plus a load balancer give you both scale and
resilience.

## The Pattern
Run many identical instances behind a balancer that distributes work and routes
around failures. Scale by adding copies, survive by removing sick ones, and keep
the service stateless so any copy can serve any request.
