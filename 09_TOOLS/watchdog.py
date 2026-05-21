"""
watchdog.py — Unified BRAIN OS System Watchdog
===============================================
Three modes:
    --check morning  : 7:15am daily health check (run via Task Scheduler)
    --check bdf      : on-demand BDF pipeline check
    --check session  : post-session close check (called by session_close.py)

Telegram config: loaded from C:\\Dev\\Projects\\soccer-content-generator\\.env
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# Ensure emoji survive the Windows cp1252 console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ── Paths ─────────────────────────────────────────────────────────────────────
BDF_ROOT      = Path(r"C:\Dev\Projects\soccer-content-generator")
BRAIN_OS_ROOT = Path(r"C:\BRAIN_OS")
ENV_PATH      = BDF_ROOT / ".env"
QUEUE_JSON    = BDF_ROOT / "src" / "queue" / "content_queue.json"
QUEUE_MD      = BRAIN_OS_ROOT / "00_DASHBOARD" / "Queue.md"
SESSIONS_DIR  = BRAIN_OS_ROOT / "08_SESSIONS"
PATCH_PATH    = BRAIN_OS_ROOT / "09_TOOLS" / "graph_maintainer_patch.py"

PROJECTS: dict[str, Path] = {
    "BRAIN_OS":                 BRAIN_OS_ROOT,
    "soccer-content-generator": BDF_ROOT,
    "CristianConstruction":     Path(r"C:\Dev\CristianConstruction"),
    "book-compiler":            Path(r"C:\Dev\shared\book-compiler"),
}

# ── Env loader ────────────────────────────────────────────────────────────────

def _load_telegram_config() -> tuple[str, str]:
    token = chat_id = ""
    if not ENV_PATH.exists():
        return token, chat_id
    for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        if key == "TELEGRAM_BOT_TOKEN":
            token = val
        elif key == "TELEGRAM_CHAT_ID":
            chat_id = val
    return token, chat_id


# ── Telegram ──────────────────────────────────────────────────────────────────

def _send_telegram(msg: str) -> None:
    token, chat_id = _load_telegram_config()
    if not token or not chat_id:
        print("[watchdog] Telegram not configured — skipping notification.")
        return
    url     = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = json.dumps({"chat_id": chat_id, "text": msg}).encode("utf-8")
    req     = urllib.request.Request(
        url, data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10):
            pass
    except Exception as e:
        print(f"[watchdog] Telegram send failed: {e}")


# ── Graph parity (via graph_maintainer_patch) ─────────────────────────────────

def _run_parity_check() -> dict | None:
    """Dynamically import audio_parity_check from graph_maintainer_patch.py."""
    if not PATCH_PATH.exists():
        return None
    spec = importlib.util.spec_from_file_location("graph_maintainer_patch", PATCH_PATH)
    mod  = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.audio_parity_check()


# ── Git helpers ───────────────────────────────────────────────────────────────

def _git_uncommitted(repo: Path) -> int:
    if not repo.exists():
        return 0
    try:
        out = subprocess.check_output(
            ["git", "status", "--porcelain"],
            cwd=repo, text=True, stderr=subprocess.DEVNULL,
        )
        return sum(1 for line in out.splitlines() if line.strip())
    except subprocess.CalledProcessError:
        return 0


# ── Queue helpers ─────────────────────────────────────────────────────────────

def _count_queue_md_unchecked() -> int:
    if not QUEUE_MD.exists():
        return 0
    return sum(
        1 for line in QUEUE_MD.read_text(encoding="utf-8").splitlines()
        if "- [ ]" in line
    )


def _count_queue_json_pending() -> int:
    if not QUEUE_JSON.exists():
        return 0
    try:
        items = json.loads(QUEUE_JSON.read_text(encoding="utf-8"))
        return sum(
            1 for item in items
            if item.get("status") in ("pending", "telegram_pending")
        )
    except (json.JSONDecodeError, TypeError):
        return 0


# ── Bot process check ─────────────────────────────────────────────────────────

def _is_bot_running() -> bool:
    try:
        import psutil
    except ImportError:
        print("[watchdog] psutil not installed — cannot check bot_service.py status.")
        return True  # assume running so we don't false-alarm
    for proc in psutil.process_iter(["cmdline"]):
        try:
            if "bot_service.py" in " ".join(proc.info["cmdline"] or []):
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return False


# ── Session archive check ─────────────────────────────────────────────────────

def _session_archive_recent(window_seconds: int = 600) -> bool:
    """Return True if any file in SESSIONS_DIR was modified within window_seconds."""
    if not SESSIONS_DIR.exists():
        return False
    cutoff = datetime.now(timezone.utc).timestamp() - window_seconds
    return any(
        f.is_file() and f.stat().st_mtime >= cutoff
        for f in SESSIONS_DIR.iterdir()
    )


# ── MODE 1: Morning ───────────────────────────────────────────────────────────

def check_morning() -> None:
    issues: list[str] = []

    # 1. Audio parity (graph_maintainer)
    parity = _run_parity_check()
    if parity is None:
        issues.append("⚠️ Graph: graph_maintainer_patch.py not found")
    elif "error" in parity:
        issues.append(f"⚠️ Graph: {parity['error']}")
    else:
        alternates = (
            len(parity["chapters"]["stale"]) + len(parity["sessions"]["stale"])
        )
        missing = (
            len(parity["chapters"]["missing"]) + len(parity["sessions"]["missing"])
        )
        orphaned = (
            len(parity["chapters"]["orphaned"]) + len(parity["sessions"]["orphaned"])
        )
        if alternates:
            issues.append(f"⚠️ Graph: {alternates} ALTERNATES detected")
        if missing:
            issues.append(f"⚠️ Graph: {missing} MISSING")
        if orphaned:
            issues.append(f"⚠️ Graph: {orphaned} ORPHANED")

    # 2. Queue.md unchecked items
    unchecked = _count_queue_md_unchecked()
    if unchecked:
        issues.append(f"⚠️ Queue: {unchecked} blocked items")

    # 3. BRAIN_OS git status
    brain_dirty = _git_uncommitted(BRAIN_OS_ROOT)
    if brain_dirty:
        issues.append(f"⚠️ Git: {brain_dirty} uncommitted files in BRAIN_OS")

    if issues:
        lines = ["🟡 BRAIN OS — 7:15am Health Check"] + issues + ["→ Run: cc (Claude Code)"]
    else:
        lines = ["✅ BRAIN OS — 7:15am clean. Good morning."]

    msg = "\n".join(lines)
    print(msg)
    _send_telegram(msg)


# ── MODE 2: BDF ───────────────────────────────────────────────────────────────

def check_bdf() -> None:
    issues: list[str] = []

    # 1. content_queue.json pending
    pending = _count_queue_json_pending()
    if pending:
        issues.append(f"⚠️ Queue: {pending} items pending approval")

    # 2. bot_service.py running
    if not _is_bot_running():
        issues.append("⚠️ Bot: bot_service.py NOT running")

    # 3. Audio parity Task 2 — per-category ALTERNATES
    parity = _run_parity_check()
    if parity is None:
        issues.append("⚠️ Audio: graph_maintainer_patch.py not found")
    elif "error" in parity:
        issues.append(f"⚠️ Audio: {parity['error']}")
    else:
        ch_stale = len(parity["chapters"]["stale"])
        se_stale = len(parity["sessions"]["stale"])
        if ch_stale:
            issues.append(f"⚠️ Audio: {ch_stale} ALTERNATES in bdf_chapters")
        if se_stale:
            issues.append(f"⚠️ Audio: {se_stale} ALTERNATES in bdf_sessions")

    if issues:
        lines = ["🟡 BDF — Pipeline Check"] + issues + ["→ Run: cc (Claude Code)"]
    else:
        lines = ["✅ BDF — Pipeline clean."]

    msg = "\n".join(lines)
    print(msg)
    _send_telegram(msg)


# ── MODE 3: Session ───────────────────────────────────────────────────────────

def check_session() -> None:
    issues: list[str] = []

    # 1. Git status across all 4 projects
    for name, path in PROJECTS.items():
        dirty = _git_uncommitted(path)
        if dirty:
            issues.append(f"⚠️ Uncommitted: {name} ({dirty} files)")

    # 2. Session archive created in last 10 minutes
    archive_ok = _session_archive_recent()

    if issues:
        lines = ["🟡 SESSION CLOSED"] + issues
        lines.append("✅ Session archive: confirmed" if archive_ok else "⚠️ Session archive: NOT found")
        lines.append("→ Commit before ingestion")
    else:
        lines = ["✅ SESSION CLOSED — all projects committed."]
        lines.append("✅ Session archive confirmed." if archive_ok else "⚠️ Session archive: NOT found")
        lines.append("→ Run KNOWLEDGE_INGESTION_PROTOCOL_V2")

    msg = "\n".join(lines)
    print(msg)
    _send_telegram(msg)


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="BRAIN OS System Watchdog")
    parser.add_argument(
        "--check",
        choices=["morning", "bdf", "session"],
        required=True,
        help="Which check to run: morning | bdf | session",
    )
    args = parser.parse_args()

    {"morning": check_morning, "bdf": check_bdf, "session": check_session}[args.check]()


if __name__ == "__main__":
    main()
