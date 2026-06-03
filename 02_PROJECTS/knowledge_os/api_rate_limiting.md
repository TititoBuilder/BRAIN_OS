---
knowledge_os_machine_key: api_rate_limiting
knowledge_os_domain: APIs & Protocols
knowledge_os_status: Learning
knowledge_os_score: 55
knowledge_os_priority: High
knowledge_os_evidence: cost_guard.py $0.75 limit
knowledge_os_last_touched: '2026-05-20'
---
# API Rate Limiting

## What It Is
Rate limiting caps how many requests a caller can make in a given window of time.
It is the control that protects a service from being overwhelmed, whether by an
abusive client, a buggy loop, or simply more demand than the system can safely
handle. It says: you may make this many calls per minute, and no more.

## How It Works
The service tracks how many requests each caller has made recently, usually keyed
by API key or address, and compares that count against a limit over a time window.
A common model is the token bucket: each caller has a bucket that refills at a
steady rate and each request spends a token, so short bursts are allowed but a
sustained flood runs the bucket dry. When a caller exceeds the limit, the service
refuses the extra requests with a specific status code, four-twenty-nine, too many
requests, and often tells the caller how long to wait before trying again. Well
behaved clients read that and back off.

## Why It Matters
Without rate limiting, a single misbehaving caller can degrade the service for
everyone, and costs that scale with usage can run away. It is both a stability
protection and a fairness mechanism, ensuring no one consumer starves the others.
It connects directly to a hard-won lesson about respecting other systems' limits:
when you are the caller, hitting a rate limit is not an error to retry instantly,
it is a signal to slow down and honor the wait the server asked for.

## The Pattern
Cap requests per caller per window, refuse the overflow with a clear retry signal,
and as a caller, honor that signal rather than hammering. Protect the service from
any one consumer; protect every consumer from the greedy one.
