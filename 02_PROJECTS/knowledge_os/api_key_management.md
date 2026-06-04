---
knowledge_os_machine_key: api_key_management
knowledge_os_domain: Security
knowledge_os_status: Mastered
knowledge_os_score: 85
knowledge_os_priority: High
knowledge_os_evidence: 'Security rule: first 15â€“20 chars only, .env.template standard'
knowledge_os_last_touched: '2026-05-19'
---
# API Key Management

## What It Is
An API key is a secret string that identifies and authorizes a program when it
calls a service. API key management is the discipline of handling those keys
safely, where they are stored, how they reach the code, who can see them, because a
leaked key is a usable credential in anyone's hands.

## How It Works
The core rule is that keys live in the environment, not in the code. You store them
in an environment file or a secrets manager, load them at runtime, and reference
them by variable name in the code, so the actual secret value never appears in a
source file. That environment file is explicitly excluded from version control by
the ignore rules, so it cannot be committed. When a key is exposed, the only safe
response is to revoke and reissue it immediately, since once a secret has been seen
it must be treated as compromised forever. Keys should also be scoped to the
minimum access they need, so a leak is contained.

## Why It Matters
A committed API key is one of the most common and damaging mistakes, it ends up in
history where it persists even after deletion, and automated scanners find exposed
keys within minutes. This is not abstract: an admin key committed to a repository
had to be deleted and reissued, which is exactly the right response and exactly why
the rules exist, never commit the environment file, always verify the ignore rules
before staging, request only a key's prefix when checking it rather than its full
value. The whole discipline exists because the cost of a leak is immediate and
real.

## The Pattern
Keep keys in the environment never in code, exclude the env file from version
control, scope keys minimally, and revoke-and-reissue the instant one is exposed.
A seen secret is a dead secret; rotate it.
