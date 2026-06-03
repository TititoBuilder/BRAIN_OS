---
knowledge_os_machine_key: python_subprocess
knowledge_os_domain: Python
knowledge_os_status: Practiced
knowledge_os_score: 80
knowledge_os_priority: High
knowledge_os_evidence: book_compiler.py â†’ ca_audio.py via subprocess
knowledge_os_last_touched: '2026-05-08'
---
# Python Subprocess

## What It Is
Subprocess is how a Python program runs another program, a command-line tool, a
script, any executable, and works with its result. It is the bridge between your
Python code and everything else installed on the machine that is not a Python
library, letting you script tools like ffmpeg, git, or another Python interpreter
from inside your own code.

## How It Works
The core call is subprocess.run, which you give a list where the first item is the
program and the rest are its arguments, passed as separate list items rather than
one big string. It launches the program, waits for it to finish, and returns a
result object holding the exit code and, if you asked to capture them, the
program's output and error text. A zero exit code means success; anything else
means failure, which you check rather than assuming it worked. Passing arguments
as a list, not a single shell string, is the safe default because it avoids the
shell reinterpreting special characters, which is both a correctness and a
security concern.

## Why It Matters
Much real automation is gluing existing tools together, and subprocess is that
glue. Your audio pipeline calling ffmpeg to stitch files, a script invoking a
different venv's Python, a build step running git, all go through subprocess. The
discipline that matters is checking the exit code and reading the captured error
when something fails, so a silent failure in the called program does not become a
mysterious failure in yours.

## The Pattern
Pass arguments as a list, check the exit code, capture the output. Treat the
called program as a function with a return value you must inspect, not a command
you fire and assume worked.
