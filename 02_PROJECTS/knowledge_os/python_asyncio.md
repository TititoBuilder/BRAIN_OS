---
knowledge_os_machine_key: python_asyncio
knowledge_os_domain: Python
knowledge_os_status: Learning
knowledge_os_score: 45
knowledge_os_priority: High
knowledge_os_evidence: watchdog.py partial async
knowledge_os_last_touched: '2026-05-22'
---
# Python Asyncio

## What It Is
Asyncio is Python's way of doing many things that involve waiting, all at once,
on a single thread. It is built for work that spends most of its time idle,
waiting on a network reply, a file, a database, where the bottleneck is not the
processor but the waiting. Instead of blocking on each wait, async code hands
control back so other work can run during the idle time.

## How It Works
You mark a function async, which makes it a coroutine, and inside it you use the
await keyword at the points where it would otherwise wait. Await means pause this
coroutine here and let the event loop run something else until this is ready. The
event loop is the scheduler at the center: it keeps a set of coroutines and, every
time one awaits, switches to another that is ready to make progress. Nothing runs
in parallel in the threading sense, it is one thread, but because the waits
overlap, a hundred network calls that each take a second can finish in about a
second total instead of a hundred.

## Why It Matters
For input-output-bound work, web servers handling many connections, scraping many
pages, calling many APIs, asyncio gives huge throughput without the cost and
complexity of threads or processes. The key boundary to understand is that it
helps when you are waiting, not when you are computing. Heavy number-crunching
does not benefit, because there is no idle time to fill. Knowing which kind of
work you have tells you whether async is the right tool.

## The Pattern
Async is for waiting, not for crunching. When the program spends its time waiting
on other systems, let those waits overlap on one thread. When it spends its time
computing, reach for processes instead.
