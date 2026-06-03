---
knowledge_os_machine_key: circuit_breaker_pattern
knowledge_os_domain: Systems Design
knowledge_os_status: Not Started
knowledge_os_score: 0
knowledge_os_priority: Medium
---
# Circuit Breaker Pattern

## What It Is
The circuit breaker is a pattern that stops a system from repeatedly calling a
service that is already failing. Named after the electrical safety device, it
trips when failures pile up, cutting off further calls for a while so a struggling
dependency is not hammered and the caller is not left hanging on calls that will
not succeed.

## How It Works
The breaker wraps calls to a remote service and watches the outcomes. Normally it
is closed and calls pass through. When failures cross a threshold, too many errors
in a short span, it opens: further calls fail instantly without even attempting the
remote service, so the caller gets a fast failure instead of a slow timeout. After
a cooldown the breaker goes half-open and lets a trial call through; if it
succeeds the breaker closes and normal traffic resumes, if it fails the breaker
opens again for another cooldown. So it automatically probes for recovery without
flooding the recovering service.

## Why It Matters
In a distributed system, one failing service can drag down everything that depends
on it: callers pile up waiting on timeouts, exhaust their own resources, and the
failure cascades. The circuit breaker contains that cascade. It fails fast so
callers are not blocked, it gives the struggling service room to recover instead of
piling on, and it restores traffic automatically once health returns. It is a core
piece of building systems that degrade gracefully rather than collapsing when one
part breaks.

## The Pattern
Trip when a dependency is failing, fail fast instead of hanging, probe gently for
recovery, then restore. Protect the caller from slow failures and the failing
service from a pile-on.
