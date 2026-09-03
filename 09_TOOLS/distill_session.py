"""
category: Session Management
distill_session.py — Turn a session archive into a reviewable chapter.

Front half of the old session_compiler.py, split at the boundary that tool
already had: --chapter-only stopped here, after the chapter was written to
disk. voice_chapter.py takes it from there and reads the chapter file, so
the two exchange a file rather than shared state.

Usage:
    python C:/BRAIN_OS/09_TOOLS/distill_session.py
    python C:/BRAIN_OS/09_TOOLS/distill_session.py 2026-08-30_2050_ca_brain_os.md
    python C:/BRAIN_OS/09_TOOLS/distill_session.py --dry-run
    python C:/BRAIN_OS/09_TOOLS/distill_session.py --force
"""

import argparse
import re
import sys
from pathlib import Path

from claude_client import load_api_key, call_claude

# ── Config ──────────────────────────────────────────────────────────────────
BRAIN_OS      = Path(r"C:\BRAIN_OS")
SESSIONS_DIR  = BRAIN_OS / "08_SESSIONS"
DISTILLED_DIR = SESSIONS_DIR / "distilled"

CHAPTER_MAX_TOKENS = 4096

# ── Prompts ───────────────────────────────────────────────────────────────────
CHAPTER_SYSTEM_PROMPT = """You are a knowledge distiller for BRAIN_OS, Cristian's personal
knowledge-graph vault. You receive a session archive — a dated log of commit-style
bullet points recording what was built, fixed, and decided across his projects
(BDF, CristianConstruction, BRAIN_OS, Read-Along App, Resolve MCP Server) during one
working session.

Distill it into a clean, reviewable chapter. Write as reference documentation, not
as a conversation recap or a re-listing of every bullet. Group related bullets into
a coherent narrative of what actually happened and why it mattered.

Never use phrases like "Claude said", "you mentioned", or "in this session". Only
include a section if it has real content — omit empty categories entirely. Be
concrete: include exact file names, tool names, and commands where present.
"""

CHAPTER_PROMPT = """Distill this BRAIN_OS session archive into a reviewable chapter.

Organize the output into these sections (only include sections with actual content):

## Summary
One or two sentences: what this session accomplished, at a glance.

## Systems Built
Tools, scripts, or integrations created or extended. Include file names and locations.

## Decisions Made
Choices made and the reasoning behind them.

## Problems Solved
Bugs fixed or blockers removed, with root cause and fix.

## Patterns & Principles Earned
Anything reusable that emerged — a rule of thumb, a corrected assumption, a
principle worth remembering.

## Open Threads
Anything left unresolved or deferred to a future session.

---

Session archive ({filename}):

{content}
"""


# ── Session location ──────────────────────────────────────────────────────────
def find_session(name: str | None) -> Path:
    if name:
        p = Path(name)
        if not p.is_absolute():
            p = SESSIONS_DIR / name
        if not p.exists():
            sys.exit(f"ERROR: session archive not found: {p}")
        return p
    files = sorted(
        (f for f in SESSIONS_DIR.glob("*.md") if f.name != "ingestion_flags.md"),
        key=lambda f: f.stat().st_mtime,
        reverse=True,
    )
    if not files:
        sys.exit(f"ERROR: no session archives found in {SESSIONS_DIR}")
    return files[0]


def session_machine_key(path: Path) -> str:
    """Filename is the machine key source — timestamp is all that's needed."""
    m = re.search(r"(\d{4}-\d{2}-\d{2})_(\d{4})", path.stem)
    if m:
        date_part = m.group(1).replace("-", "")
        return f"session_{date_part}_{m.group(2)}"
    return f"session_{re.sub(r'[^a-z0-9]+', '_', path.stem.lower()).strip('_')}"


def chapter_output_path(machine_key: str) -> Path:
    return DISTILLED_DIR / f"{machine_key}.md"



def distill_chapter(api_key: str, session_path: Path) -> str:
    content = session_path.read_text(encoding="utf-8", errors="replace")
    prompt = CHAPTER_PROMPT.format(filename=session_path.name, content=content)
    return call_claude(api_key, CHAPTER_SYSTEM_PROMPT, prompt, CHAPTER_MAX_TOKENS)




# ── Main ────────────────────────────────────────────────────────────────────
def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Distill a session archive into a chapter")
    parser.add_argument("session_file", nargs="?", help="Filename in 08_SESSIONS (default: most recent)")
    parser.add_argument("--dry-run", action="store_true", help="Print the chapter, write nothing")
    parser.add_argument("--force", action="store_true", help="Overwrite without confirming")
    args = parser.parse_args()

    print("=" * 60)
    print("  SESSION DISTILL")
    print("=" * 60)

    session_path = find_session(args.session_file)
    machine_key = session_machine_key(session_path)
    print(f"\nSession    : {session_path.name}")
    print(f"Machine key: {machine_key}")

    api_key = load_api_key()

    print("\n-- Distilling chapter (Claude) --")
    chapter_body = distill_chapter(api_key, session_path)
    chapter_doc = f"# Session Chapter \u2014 {session_path.name}\n\n{chapter_body}\n"

    if args.dry_run:
        print("\n" + "-" * 60)
        print("DRY RUN \u2014 distilled chapter:")
        print("-" * 60)
        print(chapter_doc)
        print("\n[dry-run] Nothing written.")
        return

    out_chapter = chapter_output_path(machine_key)
    DISTILLED_DIR.mkdir(parents=True, exist_ok=True)
    if out_chapter.exists() and not args.force:
        answer = input(f"  {out_chapter.name} exists. Overwrite? [y/N] ").strip().lower()
        if answer != "y":
            print("  Aborted \u2014 nothing written.")
            return
    out_chapter.write_text(chapter_doc, encoding="utf-8", newline="\n")

    print(f"  Chapter written -> {out_chapter}")
    print("\nNext:")
    print(f"  python C:/BRAIN_OS/09_TOOLS/voice_chapter.py {out_chapter.name}")


if __name__ == "__main__":
    main()
