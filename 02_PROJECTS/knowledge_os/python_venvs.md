---
knowledge_os_machine_key: python_venvs
knowledge_os_domain: Python
knowledge_os_status: Mastered
knowledge_os_score: 90
knowledge_os_priority: High
knowledge_os_evidence: CA, BDF, read-along venv separation complete
knowledge_os_last_touched: '2026-05-03'
---
# Python Venvs

## What It Is
A Python virtual environment is an isolated copy of the Python interpreter and
its installed packages, scoped to a single project. On this machine, four active
venvs prevent dependency conflicts between a CUDA-heavy AI stack, a full
production pipeline, a DaVinci Resolve bridge, and a lightweight automation
layer.

## How It Works
The BDF venv at soccer-content-generator handles the core pipeline: LanceDB,
Kokoro TTS, Tweepy, FastAPI, and the MCP server package. The Custom Agent venv
at CristianConstruction is minimal by design — FastAPI and Anthropic only —
isolated after May 2026 to prevent package conflicts with the BDF stack. The
Resolve venv at resolve-mcp-server holds pyautogui and pywinauto for Resolve
automation. The canonical AI venv at C colon backslash Knowledge backslash CA
backslash venv is the authoritative environment for any workload that needs
PyTorch — it carries the nightly cu128 build required by the RTX 5070 Ti, which
uses the Blackwell sm underscore one-twenty architecture not yet supported by
stable PyTorch releases. System Python at the AppData Python312 path has no AI
packages and must never be used for inference. Activating a venv on Windows uses
the Activate dot ps1 script in the venv Scripts folder. After activation, verify
the active interpreter with where dot exe python — not the bare where command,
which behaves differently in PowerShell.

## Why It Matters
An accidentally activated wrong venv makes CUDA silently unavailable. PyTorch
falls back to CPU without raising an error unless you explicitly call
torch dot cuda dot is available. On the RTX 5070 Ti this is a meaningful
difference: chapter audio generation that takes seconds on GPU can take minutes
on CPU. Never install CPU-only PyTorch — always use nightly cu128 to preserve
the CUDA path.

## The Pattern
Four venvs, one declared purpose each. The canonical AI venv is the source of
truth for anything touching PyTorch. Verify with where dot exe python after
every activation, not just by assuming activation worked.

