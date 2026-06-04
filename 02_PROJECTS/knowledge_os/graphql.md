---
knowledge_os_machine_key: graphql
knowledge_os_domain: APIs & Protocols
knowledge_os_status: Not Started
knowledge_os_score: 0
knowledge_os_priority: Low
---
# GraphQL

## What It Is
GraphQL is a query language for APIs that lets the client ask for exactly the data
it wants, in one request, and get back exactly that, no more, no less. Where a
traditional REST API gives you whatever a fixed endpoint returns, GraphQL flips
control to the client: it describes the precise shape of data it needs, and the
server fulfills that shape.

## How It Works
The server publishes a schema, a typed description of all the data available and how
it connects. The client sends a query that mirrors the shape of the response it
wants, naming exactly the fields it needs, including nested related data, and the
server returns a JSON object in that same shape. A single query can pull data that
would take several REST calls, because the client can traverse relationships in one
request: give me this user, and their last five orders, and each order's items. The
typed schema also means tools can validate queries and autocomplete them before they
run.

## Why It Matters
Two common REST frustrations are over-fetching, getting more data than you need, and
under-fetching, needing several round-trips to assemble one screen. GraphQL targets
both by letting the client specify precisely what it wants in one call. The tradeoff
is added server-side complexity and new concerns like preventing expensive
deeply-nested queries. So GraphQL shines when clients have varied, evolving data
needs, mobile and web wanting different slices, and REST remains simpler and often
better when the data needs are uniform and predictable.

## The Pattern
Let the client request exactly the data shape it needs against a typed schema, in
one round-trip. Solves over- and under-fetching; worth its complexity when client
needs are varied, not when they are simple and fixed.
