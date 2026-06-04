---
knowledge_os_machine_key: owasp_top10
knowledge_os_domain: Security
knowledge_os_status: Not Started
knowledge_os_score: 0
knowledge_os_priority: Medium
---
# OWASP Top 10

## What It Is
The OWASP Top Ten is a widely-referenced list of the most critical web application
security risks, maintained by a security community and updated periodically. It is
not an exhaustive catalog but a prioritized starting point: the categories of
vulnerability that cause the most real-world damage and that every developer should
know to defend against.

## How It Works
The list names recurring classes of flaw rather than specific bugs. Recurring
themes include injection, where untrusted input is interpreted as a command,
classically SQL injection, defended by never building commands from raw input;
broken access control, where users reach things they should not, defended by
checking authorization on every action; cryptographic failures, where sensitive
data is unprotected, defended by proper encryption and not rolling your own;
security misconfiguration, like default credentials or exposed settings; and
vulnerable dependencies, where a flaw in a library you use becomes your flaw. Each
category comes with the defensive practice that addresses it.

## Why It Matters
Most security breaches are not novel, they exploit the same well-known categories
year after year, which is exactly why a prioritized list of them is so useful: it
tells you where to spend defensive effort for the most protection. For a developer,
knowing these categories turns vague worry into concrete checks, validate and
parameterize input, enforce authorization everywhere, encrypt sensitive data, avoid
default configurations, keep dependencies patched. It is the difference between
hoping a system is secure and knowing which specific, common doors you have closed.

## The Pattern
Defend against the known common categories first, injection, broken access control,
crypto failures, misconfiguration, vulnerable dependencies, because that is where
most real attacks live. Prioritized defense beats scattered worry.
