---
knowledge_os_machine_key: auth_patterns
knowledge_os_domain: Security
knowledge_os_status: Learning
knowledge_os_score: 40
knowledge_os_priority: Medium
knowledge_os_last_touched: '2026-04-10'
---
# Authentication Patterns

## What It Is
Authentication patterns are the common, proven ways systems answer two distinct
questions: who are you, authentication, and what are you allowed to do,
authorization. They are different questions often confused, and getting the
distinction right is the foundation of access control.

## How It Works
Authentication establishes identity, by password, by token, by a third party
through OAuth, by an API key for a program. Authorization, which comes after, checks
whether that established identity may perform a given action, usually through roles
or permissions: this user is an admin, this token has read-only scope, this service
account may write to storage. A recurring principle across patterns is least
privilege, granting each identity only the access it actually needs and no more, so
a compromised credential does the least possible damage. Another is keeping the
authentication step with a trusted authority and passing along a scoped credential,
rather than spreading password checks everywhere.

## Why It Matters
Confusing authentication with authorization causes real security holes, a system
that verifies who you are but never checks what you may do will let any logged-in
user reach anything. Separating them, and applying least privilege to the
authorization side, is what contains damage when something is compromised: a leaked
read-only token cannot write, a scoped service account cannot roam. These patterns
are the structure behind every secure system, and the least-privilege habit is the
single most protective default.

## The Pattern
Separate who you are from what you may do, and grant the minimum access needed.
Authenticate once against a trusted authority, authorize every action by scoped
permission, default to least privilege.
