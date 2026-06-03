---
knowledge_os_machine_key: event_driven_architecture
knowledge_os_domain: Systems Design
knowledge_os_status: Learning
knowledge_os_score: 48
knowledge_os_priority: High
knowledge_os_evidence: watchdog.py 3-mode triggers
knowledge_os_last_touched: '2026-05-20'
---
# Event Driven Architecture

## What It Is
Event-driven architecture is a style where parts of a system communicate by
announcing that something happened rather than by calling each other directly.
One component emits an event, an order was placed, a file was uploaded, a render
finished, and any other component that cares reacts to it. The emitter does not
know or care who is listening. It just broadcasts the fact.

## How It Works
Producers publish events to a channel, a queue or an event bus, and consumers
subscribe to the kinds of events they care about. The channel sits in the middle
so the producer and consumer never talk directly and do not even need to be
running at the same moment, the event waits in the queue until a consumer picks it
up. This is asynchronous: the producer fires the event and moves on without
waiting for anyone to handle it. Adding a new reaction to an event means adding a
new subscriber, with no change to the producer at all.

## Why It Matters
This decoupling is the whole point. In a directly-wired system, the caller must
know every component that needs to react, and adding a reaction means editing the
caller. With events, the producer stays ignorant of its consumers, so you extend
the system by adding listeners rather than modifying existing code. It also
absorbs bursts, the queue buffers a flood of events for consumers to work through
at their own pace, and it isolates failure, a slow or broken consumer does not
block the producer. Your own triggers, on render complete, on queue ready, are
this pattern.

## The Pattern
Announce facts, do not command handlers. Emit an event and let whoever cares
subscribe, so the producer never needs to know who is listening and the system
grows by adding reactions, not editing callers.
