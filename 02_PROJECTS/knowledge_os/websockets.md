---
knowledge_os_machine_key: websockets
knowledge_os_domain: APIs & Protocols
knowledge_os_status: Not Started
knowledge_os_score: 0
knowledge_os_priority: Medium
---
# WebSockets

## What It Is
A WebSocket is a persistent, two-way connection between client and server that stays
open, letting both sides send messages to each other at any time. Where a normal web
request is one-shot, the client asks and the server answers and the connection
closes, a WebSocket holds the line open so the server can push data to the client the
instant something happens, without being asked.

## How It Works
The connection starts as a normal web request that then upgrades into a WebSocket,
switching from the request-response pattern to a persistent open channel. Once open,
either side can send a message whenever it wants, and the other receives it
immediately, full-duplex, meaning both directions are live at once. The connection
stays up until one side closes it, so there is no repeated cost of opening and
closing for each message. This is fundamentally different from polling, where a
client repeatedly asks is there anything new; with a WebSocket the server simply
tells it the moment there is.

## Why It Matters
Some experiences require the server to reach the client in real time, live chat, a
collaborative document updating as others type, a dashboard ticking with live data, a
game. Polling for these is wasteful and laggy; a WebSocket delivers updates instantly
and efficiently over one held-open connection. The tradeoff is that persistent
connections are more complex to manage and scale than stateless requests, so
WebSockets are the right tool specifically when you need live, bidirectional,
low-latency communication, not for ordinary request-response traffic.

## The Pattern
Hold one connection open for instant two-way messaging when you need real-time
push. Reach for it when the server must tell the client the moment something
happens; stick with normal requests otherwise.
