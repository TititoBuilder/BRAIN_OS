---
knowledge_os_machine_key: webhook_design
knowledge_os_domain: APIs & Protocols
knowledge_os_status: Learning
knowledge_os_score: 50
knowledge_os_priority: Medium
knowledge_os_evidence: Telegram alerts in watchdog.py
knowledge_os_last_touched: '2026-05-22'
---
# Webhook Design

## What It Is
A webhook is how one service notifies another over the web the instant something
happens, by sending it an HTTP request. Instead of you repeatedly asking a service
are we there yet, the service calls you when the event occurs. It is event-driven
communication across the boundary between two separate systems on the internet.

## How It Works
The receiving side stands up a URL that accepts incoming requests. You register
that URL with the sending service and tell it which events you care about. When
such an event happens, the sender makes an HTTP POST to your URL with details of
the event in the body. Your endpoint receives it, does its work, and returns a
success status quickly so the sender knows it was received. Because the request
comes from outside, two concerns are essential: verifying it genuinely came from
the expected sender, usually via a shared secret signature, and handling the same
event arriving twice, since senders retry when unsure, so your handler should be
safe to run more than once on the same event.

## Why It Matters
Webhooks replace polling, the wasteful pattern of asking over and over whether
something changed. Polling burns requests and adds delay; a webhook delivers the
news immediately and only when there is news. This is how services integrate in
real time, a payment processor telling you a charge succeeded, a repository
telling you code was pushed. The design discipline, verify the signature and
tolerate duplicates, is what separates a webhook endpoint that is secure and
reliable from one that is exploitable or corrupts data on a retry.

## The Pattern
Expose a URL, let the other system call it when something happens, verify the
sender, and make the handler safe to run twice. Be notified, do not poll; trust
nothing unsigned; survive the retry.
