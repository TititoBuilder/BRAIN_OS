"""
session_close.py — BRAIN OS Session Compiler
Captures session work, writes a dated archive, and optionally notifies via Telegram.

Usage:
    python session_close.py
    python session_close.py --project BDF
    python session_close.py --silent   (skip Telegram even if configured)
"""

import os
import sys
import argparse
from datetime import datetime
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────

BRAIN_OS_ROOT   = Path(r"C:\BRAIN_OS")
SESSIONS_DIR    = BRAIN_OS_ROOT / "08_SESSIONS"
TELEGRAM_TOKEN  = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT   = os.environ.get("TELEGRAM_CHAT_ID")

# ── Helpers ───────────────────────────────────────────────────────────────────

def prompt_block(label: str, hint: str = "") -> list[str]:
    """Collect multi-line input until the user enters a blank line."""
    print(f"\n{label}")
    if hint:
        print(f"  ({hint})")
    print("  Enter each item on its own line. Blank line to finish.")
    items = []
    while True:
        line = input("  > ").strip()
        if not line:
            break
        items.append(line)
    return items


def send_telegram(message: str) -> None:
    """Fire-and-forget Telegram message. Fails silently."""
    try:
        import urllib.request, urllib.parse, json
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = json.dumps({"chat_id": TELEGRAM_CHAT, "text": message, "parse_mode": "Markdown"}).encode()
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=5)
        print("[Telegram] Session summary sent.")
    except Exception as e:
        print(f"[Telegram] Failed to send: {e}")


def build_archive(
    project: str,
    accomplished: list[str],
    pending: list[str],
    notes: str,
    timestamp: datetime,
) -> str:
    """Render the session archive as a markdown string."""
    date_str  = timestamp.strftime("%Y-%m-%d")
    time_str  = timestamp.strftime("%H:%M")

    lines = [
        f"# Session Archive — {date_str} {time_str}",
        f"**Project:** {project}",
        "",
        "## Accomplished",
    ]
    for item in accomplished:
        lines.append(f"- {item}")

    lines += ["", "## Pending / Next Session"]
    for item in pending:
        lines.append(f"- {item}")

    if notes.strip():
        lines += ["", "## Notes", notes.strip()]

    lines += ["", "---", f"*Compiled by session_close.py at {time_str}*"]
    return "\n".join(lines)


def build_telegram_message(
    project: str,
    accomplished: list[str],
    pending: list[str],
    timestamp: datetime,
) -> str:
    date_str = timestamp.strftime("%Y-%m-%d %H:%M")
    acc_text = "\n".join(f"  ✅ {i}" for i in accomplished) or "  (none)"
    pnd_text = "\n".join(f"  🔜 {i}" for i in pending)     or "  (none)"
    return (
        f"*BRAIN OS Session Closed*\n"
        f"📁 Project: {project}\n"
        f"🕒 {date_str}\n\n"
        f"*Done:*\n{acc_text}\n\n"
        f"*Next:*\n{pnd_text}"
    )


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="BRAIN OS session compiler")
    parser.add_argument("--project", default="", help="Project name (e.g. BDF, CA, CristianConstruction)")
    parser.add_argument("--silent",  action="store_true", help="Skip Telegram notification")
    args = parser.parse_args()

    now = datetime.now()
    print("\n╔══════════════════════════════════╗")
    print("║   BRAIN OS — Session Compiler    ║")
    print(f"║   {now.strftime('%Y-%m-%d  %H:%M')}               ║")
    print("╚══════════════════════════════════╝")

    # Project
    project = args.project.strip()
    if not project:
        project = input("\nProject name (e.g. BDF, CA, General): ").strip() or "General"

    # Content
    accomplished = prompt_block("What was ACCOMPLISHED this session?", "tasks completed, files built, problems solved")
    pending      = prompt_block("What is PENDING for next session?",   "tasks to continue, known issues, open questions")

    print("\nExtra notes? (single line, or press Enter to skip)")
    notes = input("  > ").strip()

    # Build archive
    archive_md  = build_archive(project, accomplished, pending, notes, now)
    date_slug   = now.strftime("%Y-%m-%d_%H%M")
    project_slug = project.lower().replace(" ", "_")
    filename    = f"{date_slug}_{project_slug}.md"

    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
    archive_path = SESSIONS_DIR / filename
    archive_path.write_text(archive_md, encoding="utf-8")

    print(f"\n✅ Archive saved: {archive_path}")

    # Print summary to terminal
    print("\n" + "─" * 44)
    print(archive_md)
    print("─" * 44)

    # Telegram
    if not args.silent and TELEGRAM_TOKEN and TELEGRAM_CHAT:
        msg = build_telegram_message(project, accomplished, pending, now)
        send_telegram(msg)
    elif not args.silent:
        print("[Telegram] Skipped — TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set")

    print("\nSession closed. Good work.\n")


if __name__ == "__main__":
    main()
