---
knowledge_os_machine_key: python_type_hints
knowledge_os_domain: Python
knowledge_os_status: Learning
knowledge_os_score: 40
knowledge_os_priority: Medium
knowledge_os_last_touched: '2026-04-10'
---
# Python Type Hints

## What It Is
Type hints are annotations that say what type a variable, argument, or return
value is expected to be. Python does not enforce them at runtime, the code runs
the same with or without them, but they document intent for humans and let tools
catch type mistakes before the program ever runs.

## How It Works
You annotate an argument by following its name with a colon and a type, and a
return value with an arrow and a type after the signature. Beyond simple types you
can express richer shapes: a list of strings, a dictionary from string to integer,
a value that may be a type or None, a value that could be one of several types.
The interpreter ignores these at runtime, but a static checker like mypy reads
them and flags any place where the types do not line up, before you run anything.
Editors use the same information to power autocomplete and inline warnings.

## Why It Matters
On a small script types are optional comfort. On a growing codebase they are how
you keep it from rotting: they catch the bug where a function gets a string but
expected a number, they document what a function actually accepts so you do not
have to read its body, and they make refactoring safe because the checker tells
you everywhere a change breaks. They turn a class of runtime crashes into errors
you see while editing.

## The Pattern
Annotate the boundaries, function arguments and returns, where misunderstandings
between caller and callee live. Let a static checker read the hints and catch the
mismatches before they become runtime bugs.
