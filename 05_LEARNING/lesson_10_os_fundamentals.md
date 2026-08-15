---
knowledge_os_machine_key: os_fundamentals
knowledge_os_domain: Systems Operations
knowledge_os_status: Learning
knowledge_os_score: 70
knowledge_os_priority: High
knowledge_os_evidence: Learned during gig_tracker session Aug 14 2026
knowledge_os_last_touched: '2026-08-14'
---

# Lesson 10 — OS Fundamentals: From Hardware to Your Code

## The Full Stack (Bottom to Top)

Hardware → Kernel → Process → Fork/Exec → Threads → Virtual Environment → Sandbox → Your Python code

## Hardware — The Three Operations

Every computer does exactly three things:
- COMPUTE — CPU transforms data
- STORE — RAM holds temporarily, Disk holds permanently
- MOVE — Bus moves data between components

When Python runs conn.execute: Disk → RAM → CPU → RAM → Python variable.
conn.commit() is the moment data crosses from RAM to disk permanently.

## Kernel — The Gatekeeper

The Kernel manages CPU time, memory, disk, and devices.
Your Python code NEVER talks to hardware directly — it asks the Kernel.
Time slicing: CPU switches between programs every 1ms — feels simultaneous.

## Process

Every program the Kernel manages is a Process with its own code, memory space, state, and PID. Processes cannot read each other's memory — Kernel enforces this wall.

## Stack vs Heap

Stack — temporary scratchpad. Fast, automatic. Local variables pushed on function call, destroyed on return.
Heap — shared storage. Persistent. Objects live until nothing points to them.
Garbage collector: when reference count hits 0, object deleted, memory freed.

Analogy Stack: Stack of plates at a buffet — cleared instantly when meal ends.
Analogy Heap: Public storage facility — locker stays until everyone throws away their key.

## Fork and Exec

session_close.py calling subprocess.run:
1. FORK — Kernel clones the process
2. EXEC — clone replaces itself with new program
3. WAIT — parent waits for child
4. READ — gets exit code (0=success, 1=error, 2=unavailable)

Exit code is the ONLY communication channel after exec. This is the BRAIN_OS tool contract.

## Thread

One process, multiple threads. Threads share heap, each has private stack.
FastAPI Read-Along: Thread 1 handles User A, Thread 2 handles User B — same heap, private stacks.
Analogy: Restaurant (Process) — chefs (Threads) share pantry (Heap), each has own cutting board (Stack).

## Virtual Environment

A venv is a path redirect, not a separate Python.
Wrong venv = ModuleNotFoundError — Python layer failure, not Kernel failure.

## Sandbox

Process + Venv + File permissions + Network rules = Sandbox.
Railway runs Read-Along in a container — all four walls enforced.

## Connected to Your Projects

Stack/Heap — every function in gig.py and web.py
Garbage collector — Flask request/response cycle
Fork/Exec — session_close.py calling compile_session.py
Exit codes 0/1/2 — BRAIN_OS tool contract
Process isolation — Railway sandbox for Read-Along
Venv — 8 environments across all projects
Time slicing — FastAPI concurrent requests
