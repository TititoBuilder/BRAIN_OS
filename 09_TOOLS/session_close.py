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
import subprocess
from datetime import datetime
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────

BRAIN_OS_ROOT   = Path(r"C:\BRAIN_OS")
SESSIONS_DIR    = BRAIN_OS_ROOT / "08_SESSIONS"
TELEGRAM_TOKEN  = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT   = os.environ.get("TELEGRAM_CHAT_ID")

_PROJECT_KEYWORDS: dict[str, list[str]] = {
    "BDF":      ["bdf", "soccer", "drive_sync", "graph_maintainer", "distill", "book_compiler",
                 "drive_cleanup", "bdf_drive", "parity"],
    "CA":       ["ca", "construction", "ca-book"],
    "BRAIN_OS": ["brain_os", "brainos", "obsidian", "session_close", "graphify",
                 "system_master", "brain_os_config", "vocabulary"],
    "MCP":      ["mcp_book", "resolve_bridge", "server_api"],
    "Resolve":  ["resolve", "davinci"],
}

# ── Git log helpers ───────────────────────────────────────────────────────────

def _discover_repos(max_depth: int = 2) -> list[Path]:
    """Find git repos up to max_depth levels under C:\\Dev, C:\\BRAIN_OS, and C:\\Knowledge."""
    found: list[Path] = []

    def _scan(path: Path, depth: int) -> None:
        if (path / ".git").is_dir():
            found.append(path)
            return
        if depth == 0:
            return
        try:
            for child in path.iterdir():
                if child.is_dir():
                    _scan(child, depth - 1)
        except PermissionError:
            pass

    for base in (Path(r"C:\Dev"), Path(r"C:\BRAIN_OS"), Path(r"C:\Knowledge")):
        if base.exists():
            _scan(base, max_depth)
    return found


def _git_accomplishments(hours: int = 72) -> list[str]:
    """Return prefixed commit subjects from all repos touched in the last N hours, deduplicated."""
    seen: set[str] = set()
    items: list[str] = []
    for repo in _discover_repos():
        label = repo.name
        try:
            result = subprocess.run(
                ["git", "-C", str(repo), "log", "--oneline", f"--since={hours} hours ago"],
                capture_output=True, text=True, encoding="utf-8", timeout=10,
            )
            for line in result.stdout.strip().splitlines():
                parts = line.split(" ", 1)
                msg = parts[1] if len(parts) == 2 else line
                if msg not in seen:
                    seen.add(msg)
                    items.append(f"[{label}] {msg}")
        except Exception:
            pass
    return items


# ── Helpers ───────────────────────────────────────────────────────────────────

def _detect_projects(commit_messages: list[str]) -> list[str]:
    """Return project names whose keywords appear in commit_messages."""
    combined = " ".join(commit_messages).lower()
    detected = [
        project
        for project, keywords in _PROJECT_KEYWORDS.items()
        if any(kw in combined for kw in keywords)
    ]
    return detected or ["General"]


def _sanitize_filename_part(text: str) -> str:
    """Return a filesystem-safe version of text for use in a filename."""
    text = text.split("\n", 1)[0]          # first line only
    for ch in r'\/:*?"<>|':
        text = text.replace(ch, "")
    return text.strip()


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
    projects: list[str],
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
        f"**Projects:** {', '.join(projects)}",
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
    projects: list[str],
    accomplished: list[str],
    pending: list[str],
    timestamp: datetime,
) -> str:
    date_str = timestamp.strftime("%Y-%m-%d %H:%M")
    acc_text = "\n".join(f"  ✅ {i}" for i in accomplished) or "  (none)"
    pnd_text = "\n".join(f"  🔜 {i}" for i in pending)     or "  (none)"
    return (
        f"*BRAIN OS Session Closed*\n"
        f"📁 Projects: {', '.join(projects)}\n"
        f"🕒 {date_str}\n\n"
        f"*Done:*\n{acc_text}\n\n"
        f"*Next:*\n{pnd_text}"
    )


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="BRAIN OS session compiler")
    parser.add_argument("--silent", action="store_true", help="Skip Telegram notification")
    args = parser.parse_args()

    now = datetime.now()
    print("\n╔══════════════════════════════════╗")
    print("║   BRAIN OS — Session Compiler    ║")
    print(f"║   {now.strftime('%Y-%m-%d  %H:%M')}               ║")
    print("╚══════════════════════════════════╝")

    # Accomplishments — pre-fill from git log
    print("\nFetching recent git commits (last 72 hours)...")
    accomplished = _git_accomplishments()

    # Auto-detect projects from commit messages
    projects = _detect_projects(accomplished)
    print(f"Projects detected: {', '.join(projects)}")

    if accomplished:
        print(f"\n  Pre-filled from git log ({len(accomplished)} commit(s)):")
        for item in accomplished:
            print(f"  • {item}")
    else:
        print("  (no commits found in the last 72 hours)")
    print("\nAdd anything else? (blank to finish)")
    while True:
        line = input("  > ").strip()
        if not line:
            break
        accomplished.append(line)

    pending = prompt_block("What is PENDING for next session?", "tasks to continue, known issues, open questions")

    print("\nExtra notes? (single line, or press Enter to skip)")
    notes = input("  > ").strip()

    # Build archive
    archive_md   = build_archive(projects, accomplished, pending, notes, now)
    date_slug    = now.strftime("%Y-%m-%d_%H%M")
    _parts       = [_sanitize_filename_part(p).lower().replace(" ", "_") for p in projects]
    project_slug = "_".join(p for p in _parts if p) or "general"
    filename     = f"{date_slug}_{project_slug}.md"

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
        msg = build_telegram_message(projects, accomplished, pending, now)
        send_telegram(msg)
    elif not args.silent:
        print("[Telegram] Skipped — TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set")

    print("\nSession closed. Good work.\n")

    subprocess.Popen(
        [sys.executable, r"C:\BRAIN_OS\09_TOOLS\watchdog.py", "--check", "session"]
    )


if __name__ == "__main__":
    main()
