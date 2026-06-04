---
knowledge_os_machine_key: token_based_auth
knowledge_os_domain: Security
knowledge_os_status: Not Started
knowledge_os_score: 0
knowledge_os_priority: Medium
---
# Token Based Authentication

## What It Is
Token-based authentication proves who you are on each request by presenting a
token, a signed credential issued when you logged in, rather than re-sending a
password or relying on server-stored sessions. Once you have the token, you attach
it to your requests and the server trusts it without looking anything up.

## How It Works
You authenticate once, and the server issues a token, often a JWT, a JSON Web
Token, which packs your identity and some claims into a string that is
cryptographically signed. On each later request you send the token, and the server
verifies the signature to confirm it is genuine and unaltered, then trusts the
identity inside it. The crucial property is that the token is self-contained: the
server does not need to store session state or hit a database to validate it,
because the signature alone proves authenticity. Tokens carry an expiry so a stolen
one is not valid forever.

## Why It Matters
This statelessness is what lets authentication scale: because any server can
validate a token by checking its signature, with no shared session store, you can
run many servers behind a load balancer and any of them can handle any
authenticated request. It is the same statelessness principle that makes horizontal
scaling work, applied to identity. The tradeoff to respect is that a self-contained
token cannot be easily un-issued before it expires, which is why tokens are
short-lived and why protecting them in transit and storage matters.

## The Pattern
Issue a signed, self-contained, expiring token at login; verify its signature on
each request instead of storing sessions. Stateless validation is what lets auth
scale across many servers.
