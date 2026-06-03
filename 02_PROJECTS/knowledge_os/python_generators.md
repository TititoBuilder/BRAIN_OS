---
knowledge_os_machine_key: python_generators
knowledge_os_domain: Python
knowledge_os_status: Not Started
knowledge_os_score: 0
knowledge_os_priority: Medium
---
# Python Generators

## What It Is
A generator is a function that produces values one at a time instead of building
a whole list in memory at once. Where a normal function returns a single result
and exits, a generator yields a value, pauses, and resumes from exactly where it
left off when asked for the next one. It is a lazy sequence: values appear only
as you consume them.

## How It Works
The keyword that makes a function a generator is yield. When you call the
function you do not get a result, you get a generator object that has done no work
yet. Each time you ask for the next value, the function runs until it hits a
yield, hands that value back, and freezes its entire state, local variables and
all. Ask again and it thaws and continues. This means a generator can describe an
enormous or even infinite sequence while only ever holding one value in memory at
a time. You iterate it with a for-loop or pull values with next.

## Why It Matters
Generators are how you process data too large to fit in memory: a multi-gigabyte
log file, a stream of records, an endless feed. A list of a million items costs a
million items worth of memory; a generator costs one. They also compose, you can
chain generators so each stage pulls from the one before it, building a pipeline
that streams data through transformations without ever materializing the whole
thing.

## The Pattern
Yield, do not build. When you would otherwise create a big list just to loop over
it once, produce the items lazily instead. Memory stays flat no matter how much
data flows through.
