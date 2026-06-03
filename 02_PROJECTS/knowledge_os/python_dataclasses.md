---
knowledge_os_machine_key: python_dataclasses
knowledge_os_domain: Python
knowledge_os_status: Not Started
knowledge_os_score: 0
knowledge_os_priority: Medium
---
# Python Dataclasses

## What It Is
A dataclass is a shortcut for writing a class whose main job is to hold data. You
declare the fields and their types, add one decorator, and Python generates the
repetitive boilerplate for you: the constructor, a readable string
representation, and equality comparison. It turns a dozen lines of mechanical
code into a few clear field declarations.

## How It Works
You apply the dataclass decorator above a class and list each field as a name with
a type annotation. From those annotations Python writes an init method that
accepts and assigns every field, a repr that prints the object with its values,
and an eq method that compares two instances field by field. You can give fields
default values, mark the class frozen so instances are immutable, and use the
field helper for defaults that need to be created fresh each time, like an empty
list. The type hints are required because they are how the decorator knows what
the fields are.

## Why It Matters
Most classes that just carry data are written wrong by hand: people forget to
update the repr, get equality subtly wrong, or write a long error-prone
constructor. Dataclasses make the correct version the easy version. The code
becomes a clear declaration of what the data is, the boilerplate is generated and
always consistent, and frozen dataclasses give you safe immutable records for
free.

## The Pattern
When a class exists mostly to bundle fields, declare the fields and let the
decorator write the plumbing. Say what the data is; do not hand-write the
constructor and comparisons.
