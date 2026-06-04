---
knowledge_os_machine_key: stream_processing
knowledge_os_domain: Data Engineering
knowledge_os_status: Not Started
knowledge_os_score: 0
knowledge_os_priority: Medium
---
# Stream Processing

## What It Is
Stream processing handles data continuously, one record at a time as it arrives,
rather than collecting it into batches and processing it later. Where batch asks
process everything accumulated since yesterday, streaming asks process each event
the moment it happens. It is how systems react in real time instead of on a
schedule.

## How It Works
Data flows as an unbounded stream of events, and processors subscribe to that
stream, handling each event as it comes through, often transforming it, aggregating
it with recent events, or triggering an action. Because the stream never ends, many
operations work over windows, the last five minutes, the last hundred events, since
you cannot wait for all the data to compute a total. This connects to event-driven
architecture: events flow through a channel and processors react, and to
generators, which produce a stream of values lazily rather than building the whole
collection at once.

## Why It Matters
Some problems demand immediacy, detecting fraud as it happens, updating a live
dashboard, reacting to a sensor, where waiting for a nightly batch is useless. Stream
processing is what makes real-time response possible, and its windowing model is the
key mental shift: you reason about recent slices of an endless flow rather than
complete datasets. The tradeoff against batch is real, streaming is more complex and
batch is simpler and fine when immediacy is not needed, so the choice follows whether
the problem actually requires reacting now.

## The Pattern
Process each event as it arrives, reason over windows of an endless flow, react in
real time. Choose streaming when immediacy is required and batch when a schedule
will do.
