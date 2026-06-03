---
knowledge_os_machine_key: python_decorators
knowledge_os_domain: Python
knowledge_os_status: Learning
knowledge_os_score: 55
knowledge_os_priority: Medium
knowledge_os_last_touched: '2026-04-20'
---
# Python Decorators

## What It Is
A decorator is a function that wraps another function to add behavior without
changing the wrapped function's own code. You mark it with an at-sign line
directly above a function definition. The decorator takes the original function,
returns a new version of it, and from then on every call goes through the
wrapper. It is reusable behavior you bolt onto any function by adding one line.

## How It Works
Under the hood, a decorator is just a function that takes a function and returns
a function. When you write the at-sign name above a definition, Python passes the
function you defined into the decorator and rebinds the name to whatever the
decorator returns. The wrapper usually does something before the call, calls the
original, then does something after. To pass arguments through cleanly, the
wrapper accepts star-args and star-star-kwargs and forwards them. The
functools.wraps helper copies the original name and docstring onto the wrapper so
the function still identifies itself correctly.

## Why It Matters
Decorators let you write a behavior once and apply it everywhere: timing how long
a function runs, logging its inputs, caching results, checking permissions,
retrying on failure. Without them you would copy that boilerplate into every
function. With them the logic lives in one place and the functions stay clean and
focused on their real job. This is the open-closed idea in practice: extend
behavior without editing the thing you are extending.

## The Pattern
A decorator separates what a function does from the cross-cutting concerns around
it. Keep the function pure; push the timing, logging, and guarding into a wrapper
you can reuse anywhere.
