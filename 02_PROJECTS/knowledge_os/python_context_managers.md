---
knowledge_os_machine_key: python_context_managers
knowledge_os_domain: Python
knowledge_os_status: Learning
knowledge_os_score: 50
knowledge_os_priority: Medium
knowledge_os_last_touched: '2026-04-15'
---
# Python Context Managers

## What It Is
A context manager is a way to guarantee that setup and cleanup always happen
around a block of code, even if something goes wrong inside it. You use one with
the with-statement. The classic case is opening a file: the context manager opens
it when you enter the block and closes it when you leave, whether the block
finished normally or raised an error.

## How It Works
A context manager defines two moments: what happens on entering the block and what
happens on leaving it. The with-statement calls the enter step, runs your block,
then calls the exit step no matter how the block ends. That exit step is the
guarantee: it runs on success, on early return, and on exception. You can build
one as a class with enter and exit methods, or more simply with the contextlib
contextmanager decorator wrapped around a generator, where the code before the
yield is setup and the code after is cleanup.

## Why It Matters
Resources that must be released, files, network connections, database sessions,
locks, are dangerous to manage by hand because an error in the middle can skip
your cleanup and leak the resource. The context manager moves that cleanup into a
place that always runs. It turns easy-to-forget discipline into a structural
guarantee, which is why with open is the standard way to touch a file in Python.

## The Pattern
Pair every acquire with a guaranteed release. If something must be cleaned up,
wrap it in a context manager so the cleanup cannot be skipped, even when the code
inside fails.
