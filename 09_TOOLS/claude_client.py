"""
category: System Utilities
claude_client.py — Shared Anthropic API access for 09_TOOLS.

Extracted from session_compiler.py so the distill and narrate halves can be
split without copying the API plumbing into both.

Credential order: BDF's .env first, then the vault's 03_APIS/.env. The key
lives in both and rotation means updating both files. The order matters:
the vault's .env also holds ANTHROPIC_ADMIN_KEY for cost monitoring, which
is a different credential and not interchangeable with this one.

Import as a sibling:
    from claude_client import load_api_key, call_claude

Known wart: both functions sys.exit() on failure rather than raising. That is
script behaviour in a module and removes the caller's ability to recover. Kept
identical to the original on extraction; see FLAGS.txt.
"""

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

from dotenv import load_dotenv

BDF_ENV_FILE = Path(r"C:\Dev\Projects\soccer-content-generator\.env")
BRAIN_ENV_FILE = Path(r"C:\BRAIN_OS") / "03_APIS" / ".env"

MODEL = "claude-sonnet-4-6"


def load_api_key() -> str:
    load_dotenv(BDF_ENV_FILE)
    key = os.getenv("ANTHROPIC_API_KEY")
    if not key:
        load_dotenv(BRAIN_ENV_FILE)
        key = os.getenv("ANTHROPIC_API_KEY")
    if not key:
        sys.exit(f"ERROR: ANTHROPIC_API_KEY not found in {BDF_ENV_FILE} or {BRAIN_ENV_FILE}")
    return key


def call_claude(api_key: str, system: str, prompt: str, max_tokens: int) -> str:
    payload = {
        "model": MODEL,
        "max_tokens": max_tokens,
        "system": system,
        "messages": [{"role": "user", "content": prompt}],
    }
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["content"][0]["text"].strip()
    except urllib.error.HTTPError as e:
        sys.exit(f"ERROR: Claude API {e.code}: {e.read().decode()[:500]}")
    except Exception as e:
        sys.exit(f"ERROR: unexpected API error: {e}")


if __name__ == "__main__":
    print("MODEL:", MODEL)
    print("key loaded:", bool(load_api_key()))
