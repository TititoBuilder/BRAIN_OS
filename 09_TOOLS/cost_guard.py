"""
cost_guard.py — Claude Cost Guard
Estimates token cost before running expensive Claude Code tasks.
Sends Telegram warning if estimated cost exceeds threshold.

Usage:
    python cost_guard.py --estimate "your prompt here"
    python cost_guard.py --estimate "your prompt here" --limit 0.50
    python cost_guard.py --file prompt.txt --limit 0.75

Default limit: $0.75 (warns above this, blocks above 2x limit)
"""

import argparse
import os
import sys
import json
import urllib.request
from pathlib import Path
from dotenv import load_dotenv

# ── Config ─────────────────────────────────────────────────────────────────────
ENV_FILE       = Path(r"C:\Dev\Projects\soccer-content-generator\.env")
DEFAULT_LIMIT  = 0.75  # USD — warn above this

# Claude Sonnet 4.6 pricing (per million tokens)
INPUT_COST_PER_M  = 3.00   # $3.00 per 1M input tokens
OUTPUT_COST_PER_M = 15.00  # $15.00 per 1M output tokens

# Rough multipliers for Claude Code overhead
# Claude Code sends system prompts, tool definitions, file reads etc.
# A "simple" task = ~2x your prompt. A "complex" task = ~5-10x.
OVERHEAD_SIMPLE  = 2.0
OVERHEAD_COMPLEX = 6.0


def count_tokens_rough(text: str) -> int:
    """Rough token estimate: ~4 chars per token (industry standard approximation)."""
    return max(1, len(text) // 4)


def estimate_cost(prompt_tokens: int, output_tokens: int = None) -> dict:
    """Estimate cost for input + output tokens."""
    if output_tokens is None:
        # Assume output is ~25% of input for typical tasks
        output_tokens = max(500, prompt_tokens // 4)

    input_cost  = (prompt_tokens  / 1_000_000) * INPUT_COST_PER_M
    output_cost = (output_tokens / 1_000_000) * OUTPUT_COST_PER_M
    total       = input_cost + output_cost

    return {
        "input_tokens":  prompt_tokens,
        "output_tokens": output_tokens,
        "input_cost":    input_cost,
        "output_cost":   output_cost,
        "total":         total,
    }


def send_telegram_warning(msg: str):
    load_dotenv(ENV_FILE)
    token   = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        return
    try:
        payload = json.dumps({
            "chat_id": chat_id,
            "text": msg
        }).encode("utf-8")
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{token}/sendMessage",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        urllib.request.urlopen(req, timeout=10)
    except Exception:
        pass


def format_cost_report(text: str, limit: float) -> dict:
    """Full cost analysis for simple and complex task scenarios."""
    base_tokens = count_tokens_rough(text)

    simple  = estimate_cost(int(base_tokens * OVERHEAD_SIMPLE))
    complex_ = estimate_cost(int(base_tokens * OVERHEAD_COMPLEX))

    return {
        "prompt_tokens": base_tokens,
        "simple":        simple,
        "complex":       complex_,
        "limit":         limit,
        "warn_simple":   simple["total"]  > limit,
        "warn_complex":  complex_["total"] > limit,
        "block":         complex_["total"] > limit * 2,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Estimate Claude Code cost before running expensive tasks."
    )
    parser.add_argument("--estimate", "-e", help="Prompt text to estimate")
    parser.add_argument("--file",     "-f", help="File containing prompt text")
    parser.add_argument(
        "--limit", "-l",
        type=float, default=DEFAULT_LIMIT,
        help=f"Cost limit in USD (default: ${DEFAULT_LIMIT})"
    )
    parser.add_argument(
        "--no-telegram",
        action="store_true",
        help="Skip Telegram warning"
    )
    args = parser.parse_args()

    # Load text
    if args.file:
        p = Path(args.file)
        if not p.exists():
            print(f"[cost_guard] File not found: {args.file}")
            sys.exit(1)
        text = p.read_text(encoding="utf-8", errors="ignore")
    elif args.estimate:
        text = args.estimate
    else:
        # Read from stdin
        print("[cost_guard] Paste your prompt (Ctrl+Z to finish):")
        text = sys.stdin.read()

    report = format_cost_report(text, args.limit)

    # ── Print report ─────────────────────────────────────────────────────────
    print("\n" + "=" * 55)
    print("  CLAUDE CODE COST ESTIMATE")
    print("=" * 55)
    print(f"  Prompt tokens (raw):  ~{report['prompt_tokens']:,}")
    print(f"  Cost limit:           ${args.limit:.2f}")
    print()
    print(f"  SIMPLE task estimate  (~{OVERHEAD_SIMPLE}x overhead):")
    print(f"    Input:   ~{report['simple']['input_tokens']:,} tokens")
    print(f"    Output:  ~{report['simple']['output_tokens']:,} tokens")
    print(f"    Cost:    ~${report['simple']['total']:.4f}")

    if report["warn_simple"]:
        print(f"    ⚠️  ABOVE LIMIT (${args.limit:.2f})")
    else:
        print(f"    ✅ Within limit")

    print()
    print(f"  COMPLEX task estimate (~{OVERHEAD_COMPLEX}x overhead):")
    print(f"    Input:   ~{report['complex']['input_tokens']:,} tokens")
    print(f"    Output:  ~{report['complex']['output_tokens']:,} tokens")
    print(f"    Cost:    ~${report['complex']['total']:.4f}")

    if report["block"]:
        print(f"    🚫 BLOCKED — exceeds 2x limit (${args.limit * 2:.2f})")
    elif report["warn_complex"]:
        print(f"    ⚠️  ABOVE LIMIT (${args.limit:.2f}) — consider breaking into smaller tasks")
    else:
        print(f"    ✅ Within limit")

    print("=" * 55)

    # ── Recommendation ────────────────────────────────────────────────────────
    if report["block"]:
        print("\n  ACTION: BREAK THIS TASK INTO SMALLER PIECES")
        print("  This prompt will likely cost more than")
        print(f"  ${args.limit * 2:.2f} in Claude Code tokens.")
        msg = (
            f"🚫 COST GUARD — BLOCKED\n"
            f"Estimated cost: ~${report['complex']['total']:.3f}\n"
            f"Limit: ${args.limit:.2f}\n"
            f"Action: Break task into smaller pieces before running."
        )
        if not args.no_telegram:
            send_telegram_warning(msg)
        sys.exit(1)

    elif report["warn_complex"]:
        print("\n  ACTION: PROCEED WITH CAUTION")
        print("  Consider breaking into smaller tasks.")
        msg = (
            f"⚠️ COST GUARD — WARNING\n"
            f"Estimated cost: ~${report['complex']['total']:.3f}\n"
            f"Limit: ${args.limit:.2f}\n"
            f"Proceeding — monitor token usage."
        )
        if not args.no_telegram:
            send_telegram_warning(msg)
    else:
        print("\n  ACTION: SAFE TO PROCEED")

    print()


if __name__ == "__main__":
    main()
