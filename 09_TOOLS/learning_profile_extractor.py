r"""
learning_profile_extractor.py — Learning Profile Distiller
=============================================================
Reads Cristian_Principles.md (earned-knowledge source) plus every session
archive in 08_SESSIONS\, and calls the Claude API to distill a meta-level
"Learning Profile": patterns in how Cristian learns, works, decides, and
corrects course — evidenced across the principles doc and the session
history, not a restatement of either.

Usage:
    python C:\BRAIN_OS\09_TOOLS\learning_profile_extractor.py --dry-run
    python C:\BRAIN_OS\09_TOOLS\learning_profile_extractor.py
    python C:\BRAIN_OS\09_TOOLS\learning_profile_extractor.py --force

Output:
    C:\BRAIN_OS\07_SYSTEM\Learning_Profile.md
"""

import argparse
import json
import sys
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

from dotenv import load_dotenv
import os

# ── Config ──────────────────────────────────────────────────────────────────
BRAIN_OS       = Path(r"C:\BRAIN_OS")
PRINCIPLES     = BRAIN_OS / "07_SYSTEM" / "Cristian_Principles.md"
SESSIONS_DIR   = BRAIN_OS / "08_SESSIONS"
OUTPUT_FILE    = BRAIN_OS / "07_SYSTEM" / "Learning_Profile.md"
# ANTHROPIC_API_KEY lives in the BDF project's .env, not BRAIN_OS's
# (BRAIN_OS's 03_APIS/.env holds ANTHROPIC_ADMIN_KEY for cost monitoring only).
BDF_ENV_FILE   = Path(r"C:\Dev\Projects\soccer-content-generator\.env")
BRAIN_ENV_FILE = BRAIN_OS / "03_APIS" / ".env"
MODEL          = "claude-sonnet-4-6"
MAX_OUTPUT_TOKENS = 6000

SYSTEM_PROMPT = """You are analyzing two sources about a developer named Cristian:

1. His personal Principles document — hard-won mental models, proven only after
   completing real work (never theoretical).
2. Chronological session archive logs — dated bullet lists of what he accomplished
   in each coding session, across his projects (BDF, CristianConstruction, BRAIN_OS,
   Read-Along App, Resolve MCP Server).

Your job is NOT to summarize either source. Your job is a meta-analysis: extract
patterns in HOW Cristian learns, works, makes decisions, and corrects course —
patterns that are only visible by looking ACROSS the principles and the session
history together.

Look for things like:
- What kinds of mistakes recur, and how he fixes them (not just what the fix was)
- How his workflow / tooling evolves over time (session to session)
- What he chooses to automate vs. do manually, and why
- How he reacts when something breaks (debugging instincts)
- What he values enough to write a principle about — and what that reveals
- Signs of iteration speed, session rhythm, batching behavior
- How rigorously he verifies before writing/acting
- What "done" means to him — where he draws scope lines

Be concrete. Cite specific evidence (principle names, session dates, commit-style
bullet phrasing) rather than making generic claims. Only include a section if you
found real evidence for it — omit empty categories entirely. Write in third person,
as a reference profile, not a letter to Cristian.

Organize the output into these sections (only include sections with actual evidence):

## Core Working Style
## How He Learns
## Decision-Making Patterns
## Correction Patterns
## Values & Priorities
## Session Rhythm
## Collaboration Preferences (with AI assistants)

Output only the markdown body starting at the first "## " heading — no top-level
title, no preamble, no closing remarks."""

EXTRACTION_PROMPT = """Cristian's Principles document:

{principles}

---

Session archives, chronological ({count} sessions, earliest to latest):

{sessions}

---

Produce the Learning Profile now."""


def load_principles() -> str:
    if not PRINCIPLES.exists():
        sys.exit(f"ERROR: Principles file not found: {PRINCIPLES}")
    return PRINCIPLES.read_text(encoding="utf-8")


def load_sessions() -> tuple[str, int]:
    """Return (concatenated session text, count) in chronological filename order."""
    files = sorted(
        f for f in SESSIONS_DIR.glob("*.md") if f.name != "ingestion_flags.md"
    )
    if not files:
        sys.exit(f"ERROR: no session archives found in {SESSIONS_DIR}")
    parts = []
    for f in files:
        parts.append(f"### {f.name}\n{f.read_text(encoding='utf-8', errors='replace')}")
    return "\n\n".join(parts), len(files)


def call_claude(api_key: str, principles: str, sessions: str, count: int) -> str:
    payload = {
        "model": MODEL,
        "max_tokens": MAX_OUTPUT_TOKENS,
        "system": SYSTEM_PROMPT,
        "messages": [{
            "role": "user",
            "content": EXTRACTION_PROMPT.format(
                principles=principles, sessions=sessions, count=count
            ),
        }],
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


def build_document(body: str) -> str:
    today = date.today().isoformat()
    header = (
        "---\n"
        "tags: [personal, learning, profile, meta]\n"
        f"updated: {today}\n"
        "---\n\n"
        "# Cristian's Learning Profile\n\n"
        "Distilled from [[Cristian_Principles]] and the 08_SESSIONS archive history.\n"
        "This is a meta-analysis of patterns in how Cristian learns and works —\n"
        "not a restatement of the principles themselves. Regenerate with\n"
        "`learning_profile_extractor.py` as new sessions accumulate.\n\n"
    )
    return header + body + "\n"


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(
        description="Distill Cristian_Principles.md + 08_SESSIONS archives into Learning_Profile.md"
    )
    parser.add_argument("--dry-run", action="store_true", help="Print the result, do not write the file")
    parser.add_argument("--force", action="store_true", help="Overwrite existing Learning_Profile.md without prompting")
    args = parser.parse_args()

    # ── Read-only verification pass ──────────────────────────────────────────
    print("── Verifying sources ───────────────────────────────────")
    principles = load_principles()
    sessions, count = load_sessions()
    print(f"  Principles : {PRINCIPLES}  ({len(principles):,} chars)")
    print(f"  Sessions   : {count} archives in {SESSIONS_DIR}  ({len(sessions):,} chars)")
    print(f"  Output     : {OUTPUT_FILE}")
    print()

    if OUTPUT_FILE.exists() and not args.dry_run and not args.force:
        answer = input(f"  {OUTPUT_FILE.name} already exists. Overwrite? [y/N] ").strip().lower()
        if answer != "y":
            print("  Aborted — nothing written.")
            return

    load_dotenv(BDF_ENV_FILE)
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        load_dotenv(BRAIN_ENV_FILE)
        api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        sys.exit(f"ERROR: ANTHROPIC_API_KEY not found in {BDF_ENV_FILE} or {BRAIN_ENV_FILE}")

    print(f"── Calling Claude ({MODEL})... ──────────────────────────")
    body = call_claude(api_key, principles, sessions, count)
    document = build_document(body)

    if args.dry_run:
        print("\n" + "-" * 60)
        print("DRY RUN — would write:")
        print("-" * 60)
        print(document)
        print("-" * 60)
        print("\n[dry-run] Nothing written.")
        return

    OUTPUT_FILE.write_text(document, encoding="utf-8", newline="\n")
    print(f"\n  Written -> {OUTPUT_FILE}")
    print(f"  {len(document.splitlines())} lines, {len(document):,} chars")


if __name__ == "__main__":
    main()
