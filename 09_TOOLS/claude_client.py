"""
category: System Utilities
claude_client.py — Shared Anthropic API access for 09_TOOLS.

Extracted from session_compiler.py so the distill and narrate halves can be
split without copying the API plumbing into both.

Credential order: BDF's .env first, then the vault's 03_APIS/.env. The key
lives in both and rotation means updating both files. Verified 2026-09-01:
both files hold ANTHROPIC_API_KEY, so the BDF-first order is convention
rather than necessity. No ANTHROPIC_ADMIN_KEY exists in either file.

Import as a sibling:
    from claude_client import load_api_key, call_claude

Known wart: both functions sys.exit() on failure rather than raising. That is
script behaviour in a module and removes the caller's ability to recover. Kept
identical to the original on extraction; see FLAGS.txt.
"""

import json
from datetime import datetime
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

from dotenv import load_dotenv
import net_prefer_ipv4  # noqa: F401  -- forces IPv4, see its docstring

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


INPUT_COST_PER_M = 3.00
OUTPUT_COST_PER_M = 15.00
USAGE_LOG = Path(r"C:\BRAIN_OS\05_MEMORY\claude_usage.jsonl")


def _log_usage(usage: dict) -> None:
    """Append one line per API call. Never raises - a logging failure must not
    break the call it is measuring. Token counts are Anthropic's, not an
    estimate, so the cost figure is exact for the model in MODEL."""
    try:
        i = int(usage.get("input_tokens", 0))
        o = int(usage.get("output_tokens", 0))
        cost = (i / 1_000_000) * INPUT_COST_PER_M + (o / 1_000_000) * OUTPUT_COST_PER_M
        row = {
            "ts": datetime.now().isoformat(timespec="seconds"),
            "caller": Path(sys.argv[0]).name or "unknown",
            "model": MODEL,
            "input_tokens": i,
            "output_tokens": o,
            "cost_usd": round(cost, 6),
        }
        USAGE_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(USAGE_LOG, "a", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps(row) + "\n")
    except Exception:
        pass


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
            _log_usage(data.get("usage", {}))
            return data["content"][0]["text"].strip()
    except urllib.error.HTTPError as e:
        sys.exit(f"ERROR: Claude API {e.code}: {e.read().decode()[:500]}")
    except Exception as e:
        sys.exit(f"ERROR: unexpected API error: {e}")


if __name__ == "__main__":
    print("MODEL:", MODEL)
    print("key loaded:", bool(load_api_key()))
