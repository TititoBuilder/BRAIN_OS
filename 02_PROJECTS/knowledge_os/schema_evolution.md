---
knowledge_os_machine_key: schema_evolution
knowledge_os_domain: Data Engineering
knowledge_os_status: Not Started
knowledge_os_score: 0
knowledge_os_priority: Low
---
# Schema Evolution

## What It Is
A schema is the defined structure of your data, its fields and types. Schema
evolution is the discipline of changing that structure over time without breaking
the systems and stored data that depend on the old shape. Real systems always need
to change their data structure eventually; doing it safely is the skill.

## How It Works
The core challenge is that data already stored in the old shape, and code already
written against it, must keep working while you move to the new shape. The safe
approach is backward and forward compatibility: add new fields as optional so old
records and old code still function, and avoid removing or renaming fields abruptly,
since that breaks anything still expecting them. Changes roll out in stages, add the
new field, migrate readers and writers to use it, and only later retire the old one
once nothing depends on it. Migrations, scripts that transform existing stored data
to the new shape, handle the data already at rest.

## Why It Matters
A careless schema change is one of the most dangerous things you can do to a live
system, it can break running code, orphan stored data, or corrupt records that no
longer match what the code expects. This is exactly the migration discipline that
applies to renaming a machine-key: the structure is depended upon, so a change is a
staged migration, not a simple edit. Evolving schemas additively and in stages is
what lets a system grow and change while staying continuously working, rather than
requiring a risky big-bang rewrite.

## The Pattern
Change structure additively and in stages: add optional, migrate, then retire.
Keep old data and old code working throughout. A schema change is a staged
migration, never an abrupt edit.
