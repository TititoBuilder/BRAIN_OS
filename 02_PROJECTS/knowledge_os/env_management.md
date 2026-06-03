---
knowledge_os_machine_key: env_management
knowledge_os_domain: Cloud & DevOps
knowledge_os_status: Mastered
knowledge_os_score: 85
knowledge_os_priority: High
knowledge_os_evidence: Venv separation + $PROFILE PowerShell functions
knowledge_os_last_touched: '2026-05-24'
---
# Environment Management

## What It Is
Environment management on this system means two things: dotenv files that hold
secrets for Python scripts, and PowerShell profile functions that expose aliases
and paths to every terminal session. Together they form the boundary layer
between hard-coded configuration and runtime context.

## How It Works
Python scripts load secrets via python-dotenv, which reads a dot-env file and
injects its contents into the process environment at startup. Two canonical
dot-env files exist. The soccer-content-generator project root file is primary —
it holds the Telegram bot token and chat ID, Twitter API keys, Anthropic API
key, and LanceDB path. The BRAIN OS file under 03 underscore APIs holds the
Anthropic Admin key and budget thresholds for the cost monitor. Scripts that
need Telegram alerts try the soccer file first and fall back to the BRAIN OS
file, so they work regardless of which directory they are launched from.
PowerShell aliases live in two profile files that must be kept identical: the
VSCode profile and the standalone PowerShell profile. Divergence causes aliases
like bdf-compile or ca-audio to work in one terminal context and silently fail
in another.

## Why It Matters
One hard-won rule: never run Anthropic API calls with Surfshark VPN active.
McAfee and the VPN both intercept SSL traffic, producing connection reset errors
at the Windows socket layer. The env file cannot fix this, but knowing the cause
means the fix is immediate — pause the VPN. Environment files also enforce the
single notification standard: every project reads the same Telegram bot token
from a shared env, so there is no drift toward a second notification channel.

## The Pattern
One dot-env per project, multi-path fallback for shared scripts, values are
keys only — never print or log their contents. Profile files must stay identical
between VSCode and standalone PowerShell or aliases become unreliable.

