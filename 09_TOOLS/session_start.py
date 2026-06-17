"""
session_start.py — BRAIN OS Session Orchestrator
Runs automatically when a Claude Code session starts.
Loads project context, runs health check, sends Telegram notification.

Usage:
    python C:/BRAIN_OS/09_TOOLS/session_start.py --project bdf
    python C:/BRAIN_OS/09_TOOLS/session_start.py --project brainos
    python C:/BRAIN_OS/09_TOOLS/session_start.py --project ca
    python C:/BRAIN_OS/09_TOOLS/session_start.py --project construction
    python C:/BRAIN_OS/09_TOOLS/session_start.py --project resolve
    python C:/BRAIN_OS/09_TOOLS/session_start.py  # auto-detects from cwd
"""

import argparse
import os
import sys
import json
import urllib.request
import urllib.error
import subprocess
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Force UTF-8 stdout ? content (CLAUDE.md, archives) contains Unicode that crashes cp1252.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# ── Paths ──────────────────────────────────────────────────────────────────────
BRAIN_OS_ROOT  = Path(r"C:\BRAIN_OS")
ENV_FILE       = Path(r"C:\Dev\Projects\soccer-content-generator\.env")

# ── Project registry ───────────────────────────────────────────────────────────
PROJECTS = {
    "bdf": {
        "name": "BDF Soccer Content Generator",
        "root": Path(r"C:\Dev\Projects\soccer-content-generator"),
        "claude_md": Path(r"C:\Dev\Projects\soccer-content-generator\CLAUDE.md"),
        "context_md": Path(r"C:\BRAIN_OS\02_PROJECTS\graphs\soccer-content-generator.context.md"),
        "venv": Path(r"C:\Dev\Projects\soccer-content-generator\venv\Scripts\python.exe"),
        "emoji": "⚽",
    },
    "brainos": {
        "name": "BRAIN OS",
        "root": BRAIN_OS_ROOT,
        "claude_md": BRAIN_OS_ROOT / "CLAUDE.md",
        "context_md": BRAIN_OS_ROOT / "SYSTEM_MASTER.md",
        "venv": Path(r"C:\Dev\Projects\soccer-content-generator\venv\Scripts\python.exe"),
        "emoji": "🧠",
    },
    "ca": {
        "name": "CA Book System",
        "root": Path(r"C:\Dev\CristianConstruction"),
        "claude_md": Path(r"C:\Dev\CristianConstruction\CLAUDE.md"),
        "context_md": BRAIN_OS_ROOT / "02_PROJECTS" / "graphs" / "ca-book.context.md",
        "venv": Path(r"C:\Knowledge\CA\venv\Scripts\python.exe"),
        "emoji": "📚",
    },
    "construction": {
        "name": "Cristian Construction",
        "root": Path(r"C:\Dev\CristianConstruction"),
        "claude_md": Path(r"C:\Dev\CristianConstruction\CLAUDE.md"),
        "context_md": BRAIN_OS_ROOT / "02_PROJECTS" / "CristianConstruction.md",
        "venv": Path(r"C:\Dev\CristianConstruction\venv\Scripts\python.exe"),
        "emoji": "🔨",
    },
    "resolve": {
        "name": "Resolve MCP Server",
        "root": Path(r"C:\Users\titit\Projects\resolve-mcp-server"),
        "claude_md": Path(r"C:\Users\titit\Projects\resolve-mcp-server\CLAUDE.md"),
        "context_md": BRAIN_OS_ROOT / "02_PROJECTS" / "Resolve_MCP_Server.md",
        "venv": Path(r"C:\Users\titit\Projects\resolve-mcp-server\venv\Scripts\python.exe"),
        "emoji": "🎬",
    },
}

# ── CWD auto-detection ─────────────────────────────────────────────────────────
CWD_MAP = {
    "soccer-content-generator": "bdf",
    "CristianConstruction":     "construction",
    "BRAIN_OS":                 "brainos",
    "resolve-mcp-server":       "resolve",
    "book-compiler":            "ca",
    "brain-audio":              "brainos",
}


def detect_project() -> str:
    cwd = Path.cwd().name
    return CWD_MAP.get(cwd, "brainos")


# ── Telegram ───────────────────────────────────────────────────────────────────
def _load_telegram():
    load_dotenv(ENV_FILE)
    return os.getenv("TELEGRAM_BOT_TOKEN"), os.getenv("TELEGRAM_CHAT_ID")


def send_telegram(msg: str):
    token, chat_id = _load_telegram()
    if not token or not chat_id:
        print("[session_start] Telegram not configured — skipping.")
        return
    try:
        payload = json.dumps({
            "chat_id": chat_id,
            "text": msg,
            "parse_mode": "HTML"
        }).encode("utf-8")
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{token}/sendMessage",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        urllib.request.urlopen(req, timeout=10)
    except Exception as e:
        print(f"[session_start] Telegram failed: {e}")


# ── Context loader ─────────────────────────────────────────────────────────────
def load_context(project: dict) -> str:
    """Read CLAUDE.md, latest session archive, and Queue.md ? the full startup bundle."""
    parts = []

    # 1. The contract (full, no truncation)
    for label, path in [("CLAUDE.md", project["claude_md"]),
                        ("Context", project["context_md"])]:
        if path and Path(path).exists():
            content = Path(path).read_text(encoding="utf-8", errors="ignore")
            parts.append(f"=== {label}: {Path(path).name} ===\n{content}")
        else:
            parts.append(f"=== {label}: NOT FOUND ({path}) ===")

    # 2. The timeline ? newest real session archive (08_SESSIONS + 09_TOOLS), by mtime
    candidates = []
    for d in [BRAIN_OS_ROOT / "08_SESSIONS", BRAIN_OS_ROOT / "09_TOOLS"]:
        if d.exists():
            for f in d.glob("*.md"):
                n = f.name.lower()
                # real session archives only: dated bdf_ca_brain_os or session_ prefix
                if "_bdf_ca_brain_os" in n or n.startswith("session_"):
                    candidates.append(f)
    if candidates:
        latest = max(candidates, key=lambda f: f.stat().st_mtime)
        content = latest.read_text(encoding="utf-8", errors="ignore")
        parts.append(f"=== LATEST SESSION: {latest.name} ===\n{content}")
    else:
        parts.append("=== LATEST SESSION: none found ===")

    # 3. The queue ? In Progress section content (not just a count)
    parts.append("=== QUEUE (In Progress) ===\n" + "\n".join(_parse_queue_section()))

    return "\n\n".join(parts)


# ── Health check ───────────────────────────────────────────────────────────────
def run_health_check() -> dict:
    """Run graph_maintainer.py and return key metrics."""
    graph_script = Path(r"C:\Dev\Projects\soccer-content-generator\scripts\graph_maintainer.py")
    venv_py      = Path(r"C:\Dev\Projects\soccer-content-generator\venv\Scripts\python.exe")

    if not graph_script.exists():
        return {"error": "graph_maintainer.py not found"}

    try:
        result = subprocess.run(
            [str(venv_py), str(graph_script)],
            capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=60
        )
        output = result.stdout + result.stderr
        metrics = {
            "alternates": 0,
            "missing": 0,
            "orphaned": 0,
            "healthy_chapters": 0,
            "healthy_sessions": 0,
        }
        for line in output.splitlines():
            if "ALTERNATES:" in line:
                try:
                    metrics["alternates"] = int(line.split(":")[1].strip().split()[0])
                except Exception:
                    pass
            if "MISSING:" in line:
                try:
                    metrics["missing"] = int(line.split(":")[1].strip().split()[0])
                except Exception:
                    pass
            if "HEALTHY:" in line and metrics["healthy_chapters"] == 0:
                try:
                    metrics["healthy_chapters"] = int(line.split(":")[1].strip())
                except Exception:
                    pass
        return metrics
    except Exception as e:
        return {"error": str(e)}


# ── Git status ─────────────────────────────────────────────────────────────────
def check_git_status(root: Path) -> int:
    """Return count of uncommitted files in a repo."""
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "status", "--short"],
            capture_output=True, text=True, encoding="utf-8", errors="replace"
        )
        lines = [l for l in result.stdout.splitlines() if l.strip()]
        return len(lines)
    except Exception:
        return -1


# ── Queue check ───────────────────────────────────────────────────────────────
def _parse_queue_section() -> list[str]:
    """Return lines of the '## In Progress' section from Queue.md (header line included)."""
    queue_path = BRAIN_OS_ROOT / "00_DASHBOARD" / "Queue.md"
    if not queue_path.exists():
        return []
    content = queue_path.read_text(encoding="utf-8", errors="ignore")
    lines, grab = [], False
    for line in content.splitlines():
        if line.startswith("## In Progress"):
            grab = True
            lines.append(line)
            continue
        if grab and line.startswith("## "):
            break
        if grab:
            lines.append(line)
    return lines


def check_queue() -> int:
    """Count unchecked items in Queue.md ## In Progress section."""
    return sum(1 for line in _parse_queue_section() if "- [ ]" in line)


# ── Context printer ───────────────────────────────────────────────────────────
def print_context_header(project_key: str, project: dict, metrics: dict,
                         git_dirty: int, queue_blocked: int):
    """Print session context to stdout for Claude Code to read."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    emoji = project["emoji"]

    print("\n" + "=" * 70)
    print(f"  {emoji}  BRAIN OS SESSION START — {project['name']}")
    print(f"  {now}")
    print("=" * 70)

    # Health
    if "error" not in metrics:
        print(f"\n  AUDIO LIBRARY")
        print(f"    Chapters healthy : {metrics.get('healthy_chapters', '?')}")
        print(f"    Alternates       : {metrics.get('alternates', 0)}")
        print(f"    Missing          : {metrics.get('missing', 0)}")
    else:
        print(f"\n  [health] {metrics['error']}")

    # Git
    if git_dirty == -1:
        print(f"\n  GIT: check failed")
    elif git_dirty > 0:
        print(f"\n  GIT: {git_dirty} uncommitted file(s) in {project_key}")
    else:
        print(f"\n  GIT: clean")

    # Queue
    if queue_blocked > 0:
        print(f"\n  QUEUE: {queue_blocked} blocked item(s) in In Progress")
    else:
        print(f"\n  QUEUE: clear")

    print("\n" + "=" * 70)
    print("  CONTEXT LOADED — paste below into Claude Code session")
    print("=" * 70 + "\n")


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="BRAIN OS Session Orchestrator — loads context + health check"
    )
    parser.add_argument(
        "--project", "-p",
        choices=list(PROJECTS.keys()),
        default=None,
        help="Project to load context for (auto-detected from cwd if omitted)"
    )
    parser.add_argument(
        "--no-telegram",
        action="store_true",
        help="Skip Telegram notification"
    )
    parser.add_argument(
        "--no-health",
        action="store_true",
        help="Skip graph_maintainer health check (faster startup)"
    )
    parser.add_argument(
        "--context-only",
        action="store_true",
        help="Print context files only, skip health check and Telegram"
    )
    args = parser.parse_args()

    # Detect project
    project_key = args.project or detect_project()
    project     = PROJECTS[project_key]

    print(f"[session_start] Project: {project['name']} ({project_key})")

    # Load context
    context = load_context(project)

    if args.context_only:
        print(context)
        return

    # Health check
    metrics = {}
    if not args.no_health:
        print("[session_start] Running health check...")
        metrics = run_health_check()

    # Git status
    git_dirty = check_git_status(project["root"])

    # Queue
    queue_blocked = check_queue()

    # Print header
    print_context_header(project_key, project, metrics, git_dirty, queue_blocked)

    # Print context
    print(context)

    # Telegram
    if not args.no_telegram:
        emoji = project["emoji"]
        name  = project["name"]
        issues = []
        if metrics.get("alternates", 0) > 0:
            issues.append(f"⚠️ {metrics['alternates']} ALTERNATES")
        if metrics.get("missing", 0) > 0:
            issues.append(f"⚠️ {metrics['missing']} MISSING")
        if git_dirty > 0:
            issues.append(f"⚠️ {git_dirty} uncommitted files")
        if queue_blocked > 0:
            issues.append(f"⚠️ {queue_blocked} blocked queue items")

        if issues:
            msg = f"{emoji} SESSION STARTED — {name}\n" + "\n".join(issues) + "\n→ Run: cc"
        else:
            msg = f"{emoji} SESSION STARTED — {name}\n✅ System clean. Good to go."

        send_telegram(msg)
        print(f"[session_start] Telegram sent.")


if __name__ == "__main__":
    main()
