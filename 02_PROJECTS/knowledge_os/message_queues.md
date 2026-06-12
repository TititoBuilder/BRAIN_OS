---
knowledge_os_machine_key: message_queues
knowledge_os_domain: Software Architecture
knowledge_os_status: Learning
knowledge_os_score: 40
knowledge_os_priority: Medium
knowledge_os_evidence: General concept; not yet applied to a system component
knowledge_os_last_touched: '2026-06-11'
---
# Message Queues
## What It Is
A message queue is a buffer that sits between two parts of a system so they do
not have to talk to each other directly or at the same time. One part, the
producer, drops a message into the queue. Another part, the consumer, picks it up
when it is ready. The queue holds the message in between. This lets the two sides
run at their own pace and stay decoupled, so neither has to wait on the other to
keep working.
## How It Works
The producer writes a message and hands it to the queue, then moves on without
waiting for a result. The queue stores messages in order, usually first in, first
out, until a consumer is free to process them. The consumer reads a message, does
its work, and acknowledges completion, at which point the queue removes it. If no
consumer is available, messages wait safely in the queue rather than being lost.
If a consumer fails mid-task, an unacknowledged message can be redelivered.
Common implementations include RabbitMQ, Redis, and cloud services like AWS SQS,
but the pattern is the same regardless of the tool.
## Why It Matters
Queues absorb bursts. When work arrives faster than it can be processed, the
queue holds the backlog instead of overwhelming the consumer or dropping
requests. They also provide a failure boundary: if the consumer crashes, the
producer keeps running and the messages wait, so one component failing does not
cascade into the other. This is the same decoupling principle that keeps any
well-architected system from turning a single fault into a system-wide outage.
## The Pattern
Reach for a message queue when one part of a system produces work faster or less
predictably than another part can consume it, or when you want the two sides to
fail independently. Do not add one where a direct, synchronous call is simpler and
the volume is low, because a queue adds a moving part to operate and monitor. The
decision is the same as any decoupling choice: introduce the boundary only when
the coupling it removes is actually causing pain.
