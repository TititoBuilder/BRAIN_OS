---
knowledge_os_machine_key: rest_api_design
knowledge_os_domain: APIs & Protocols
knowledge_os_status: Practiced
knowledge_os_score: 72
knowledge_os_priority: High
knowledge_os_evidence: server_api.py in resolve-mcp-server
knowledge_os_last_touched: '2026-05-05'
---
# REST API Design

## What It Is
REST is a style for designing web APIs around resources and standard operations.
A resource is a thing your system manages, a user, an order, a document, and REST
says you expose those resources at clean addresses and act on them with a small
fixed set of verbs. It is the dominant convention for how programs talk to each
other over the web because it is predictable and uses the web's own machinery.

## How It Works
Each resource gets a URL, and the HTTP method says what you are doing to it: GET
to read, POST to create, PUT or PATCH to update, DELETE to remove. The same
address with a different method means a different action, so the structure is
learnable. Responses carry a status code that tells the caller what happened: the
two hundreds mean success, the four hundreds mean the caller made a mistake, the
five hundreds mean the server failed. Data usually travels as JSON. A key
principle is that requests are stateless, each one carries everything needed to
handle it, so the server does not have to remember previous calls.

## Why It Matters
A consistent REST design means anyone consuming your API can guess how it works
from a few examples, which lowers the cost of every integration. Using the right
status codes matters because callers make decisions on them, a four-oh-four and a
five hundred demand different responses from the client. Statelessness is what lets
an API scale horizontally, since any server can handle any request without shared
session memory. Good design here is the difference between an API people adopt
easily and one they fight.

## The Pattern
Model resources as addresses, actions as standard verbs, outcomes as status codes,
and keep each request self-contained. Predictability is the feature; surprise is
the defect.
