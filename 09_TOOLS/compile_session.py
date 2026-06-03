"""
compile_session.py  —  Option C Knowledge Ingestion Pipeline
=============================================================
Reads the latest session archive, runs it through the Knowledge
Ingestion Protocol V2, auto-handles routine updates, flags complex
cases to Telegram + ingestion_flags.md, then git commits.

Usage:
    python C:\\BRAIN_OS\\09_TOOLS\\compile_session.py
    python C:\\BRAIN_OS\\09_TOOLS\\compile_session.py --session 2026-05-28_0607_bdf_ca_brain_os.md
    python C:\\BRAIN_OS\\09_TOOLS\\compile_session.py --dry-run
"""

import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

# ── Config ────────────────────────────────────────────────────────────────────

BRAIN_OS      = Path(r"C:\BRAIN_OS")
SESSIONS_DIR  = BRAIN_OS / "08_SESSIONS"
FLAGS_FILE    = BRAIN_OS / "08_SESSIONS" / "ingestion_flags.md"
PROTOCOL_FILE = BRAIN_OS / "07_SYSTEM" / "KNOWLEDGE_INGESTION_PROTOCOL_V2.md"
ENV_FILE      = Path(r"C:\Dev\Projects\soccer-content-generator\.env")

load_dotenv(ENV_FILE)
ANTHROPIC_KEY  = os.getenv("ANTHROPIC_API_KEY", "").strip()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
TELEGRAM_CHAT  = os.getenv("TELEGRAM_CHAT_ID", "").strip()
MODEL          = "claude-sonnet-4-6"

# ── Structured output prompt ──────────────────────────────────────────────────

ANALYSIS_SYSTEM = """You are the BRAIN_OS Knowledge Ingestion Engine operating in Option C (Hybrid) mode.

Your job: analyze a session archive and produce a structured JSON ingestion plan.

Rules from the Knowledge Ingestion Protocol V2:
- AUTO-HANDLE: simple appends, clear corrections, duplicates (skip), single-node updates
- FLAG: conflicts, multi-node (3+), architecture pivots, financial changes, archival decisions, cross-domain

Output ONLY valid JSON with this exact structure:
{
  "summary": "one sentence describing the session",
  "auto_handle": [
    {
      "action": "APPEND|REPLACE|SKIP|UPDATE",
      "target": "relative/path/from/BRAIN_OS/root.md",
      "section": "section name to target",
      "content": "exact content to apply",
      "reason": "brief reason"
    }
  ],
  "flags": [
    {
      "type": "CONFLICT|MULTI_NODE|ARCHITECTURE|FINANCIAL|ARCHIVAL|CROSS_DOMAIN",
      "priority": "HIGH|MEDIUM|LOW",
      "nodes": ["relative/path.md"],
      "description": "clear description of the issue",
      "suggested_resolution": "what you recommend",
      "old_content": "existing content (if conflict)",
      "new_content": "proposed content"
    }
  ],
  "metrics": {
    "pieces_found": 0,
    "auto_count": 0,
    "flag_count": 0
  }
}

Critical safeguards — ALWAYS FLAG (never auto-handle):
- Financial/cost/pricing information
- Architecture pivots or tool replacements
- Anything affecting 3+ nodes simultaneously"""


# ── Helpers ───────────────────────────────────────────────────────────────────

def find_latest_session(session_name: str | None) -> Path:
    if session_name:
        p = SESSIONS_DIR / session_name
        if not p.exists():
            sys.exit(f"ERROR: session not found: {p}")
        return p
    files = sorted(SESSIONS_DIR.glob("*.md"), key=lambda f: f.stat().st_mtime, reverse=True)
    files = [f for f in files if f.name != "ingestion_flags.md"]
    if not files:
        sys.exit(f"ERROR: no session files found in {SESSIONS_DIR}")
    return files[0]


def call_claude(session_content: str) -> dict:
    if not ANTHROPIC_KEY:
        sys.exit("ERROR: ANTHROPIC_API_KEY not set")

    # Truncate if very large
    if len(session_content) > 12000:
        session_content = session_content[:12000] + "\n\n[...truncated...]"

    vault_files = []
    for ext in ["*.md"]:
        for p in BRAIN_OS.rglob(ext):
            rel = p.relative_to(BRAIN_OS)
            parts = rel.parts
            if parts[0] not in ("venv", ".git", "_archive", "audio_staging"):
                vault_files.append(str(rel.as_posix()))
    vault_index = "\n".join(sorted(vault_files)[:150])

    payload = {
        "model": MODEL,
        "max_tokens": 4096,
        "system": ANALYSIS_SYSTEM,
        "messages": [{
            "role": "user",
            "content": f"Analyze this session archive and produce the ingestion JSON:"
                       f"\n\nACTUAL VAULT FILES (use ONLY these paths for target field):\n{vault_index}\n\nSession:\n{session_content}"
        }]
    }

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type":      "application/json",
            "x-api-key":         ANTHROPIC_KEY,
            "anthropic-version": "2023-06-01",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
            raw  = data["content"][0]["text"].strip()
            # Strip markdown fences if present
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            return json.loads(raw.strip())
    except urllib.error.HTTPError as e:
        sys.exit(f"ERROR: Claude API {e.code}: {e.read().decode()[:300]}")
    except json.JSONDecodeError as e:
        sys.exit(f"ERROR: Claude returned invalid JSON: {e}")


def apply_auto_handle(items: list[dict], dry_run: bool) -> list[str]:
    """Apply auto-handle queue to vault files. Returns list of changed files."""
    changed = []

    PATH_CORRECTIONS = {
        "03_KNOWLEDGE/Cristian_Principles.md": "07_SYSTEM/Cristian_Principles.md",
        "BRAIN_OS/principles.md": "07_SYSTEM/Cristian_Principles.md",
    }

    for item in items:
        action  = item.get("action", "SKIP").upper()
        target  = item.get("target", "")
        target  = PATH_CORRECTIONS.get(target, target)
        section = item.get("section", "")
        content = item.get("content", "")
        reason  = item.get("reason", "")

        if action == "SKIP":
            print(f"  SKIP  {target} — {reason}")
            continue

        vault_path = BRAIN_OS / target
        if not vault_path.exists():
            print(f"  ⚠    {target} not found — skipping {action}")
            continue

        print(f"  {action:<8} {target}")
        if reason:
            print(f"           → {reason}")

        if dry_run:
            continue

        file_text = vault_path.read_text(encoding="utf-8")

        if action == "APPEND":
            if content.strip() and content.strip() in file_text:
                print(f"           ↩ already present — skipped")
                continue
            ts    = datetime.now().strftime("%Y-%m-%d")
            entry = f"\n\n<!-- auto-ingested {ts} -->\n{content}\n"
            preview = content.strip()[:80].replace("\n", " ")
            print(f"           + {preview}{'...' if len(content.strip()) > 80 else ''}")
            vault_path.write_text(file_text + entry, encoding="utf-8")
            changed.append(target)

        elif action in ("REPLACE", "UPDATE"):
            if section and section in file_text:
                # Replace section content
                ts      = datetime.now().strftime("%Y-%m-%d")
                note    = f"<!-- updated {ts}: {reason} -->"
                new_text = file_text.replace(section, f"{section}\n{note}\n{content}", 1)
                vault_path.write_text(new_text, encoding="utf-8")
            else:
                # Append as fallback
                if content.strip() and content.strip() in file_text:
                    print(f"           ↩ already present — skipped")
                    continue
                ts    = datetime.now().strftime("%Y-%m-%d")
                entry = f"\n\n<!-- auto-updated {ts} -->\n{content}\n"
                preview = content.strip()[:80].replace("\n", " ")
                print(f"           + {preview}{'...' if len(content.strip()) > 80 else ''}")
                vault_path.write_text(file_text + entry, encoding="utf-8")
            changed.append(target)

    return changed


def write_flags_file(flags: list[dict], session_name: str, dry_run: bool):
    if not flags:
        return

    ts    = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        f"# Ingestion Flags — {session_name}",
        f"Generated: {ts}",
        f"Items: {len(flags)}",
        "",
        "---",
        "",
    ]

    for i, flag in enumerate(flags, 1):
        lines += [
            f"## Flag {i} of {len(flags)} — {flag.get('type')} [{flag.get('priority')}]",
            "",
            f"**Description:** {flag.get('description', '')}",
            "",
            f"**Nodes:** {', '.join(flag.get('nodes', []))}",
            "",
        ]
        if flag.get("old_content"):
            lines += [f"**Old:** {flag['old_content']}", ""]
        if flag.get("new_content"):
            lines += [f"**New:** {flag['new_content']}", ""]
        lines += [
            f"**Suggested resolution:** {flag.get('suggested_resolution', '')}",
            "",
            "**Decision:** [ ] Approve  [ ] Modify  [ ] Skip",
            "",
            "---",
            "",
        ]

    if not dry_run:
        FLAGS_FILE.write_text("\n".join(lines), encoding="utf-8")
        print(f"\n  Flags written → {FLAGS_FILE.name}")
    else:
        print("\n  [dry-run] Flags would be written to ingestion_flags.md")


def send_telegram(message: str):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT:
        print("  [Telegram] Not configured — skipping notification")
        return
    url     = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = json.dumps({"chat_id": TELEGRAM_CHAT, "text": message, "parse_mode": "Markdown"}).encode()
    req     = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            resp.read()
        print("  Telegram notification sent")
    except Exception as e:
        print(f"  [Telegram] Failed: {e}")


def git_commit(changed_files: list[str], session_name: str):
    if not changed_files:
        return
    for f in changed_files:
        subprocess.run(["git", "-C", str(BRAIN_OS), "add", f], check=True)
    subprocess.run(["git", "-C", str(BRAIN_OS), "add", str(FLAGS_FILE)], check=False)

    # Pull remote changes before committing to avoid push rejection
    pull = subprocess.run(
        ["git", "-C", str(BRAIN_OS), "pull", "--rebase", "origin", "main"],
        capture_output=True,
        text=True,
    )
    if pull.returncode != 0:
        print(f"WARNING: git pull --rebase failed:\n{pull.stderr}")
        print("Proceeding anyway — resolve conflicts manually if push fails.")

    msg = f"ingest: auto-handle {len(changed_files)} nodes — {Path(session_name).stem}"
    subprocess.run(["git", "-C", str(BRAIN_OS), "commit", "-m", msg], check=True)
    subprocess.run(["git", "-C", str(BRAIN_OS), "push"], check=True)
    print(f"  Committed: {msg}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Option C knowledge ingestion pipeline")
    parser.add_argument("--session",  help="Specific session filename (default: latest)")
    parser.add_argument("--dry-run",  action="store_true", help="Analyze only, no writes")
    args = parser.parse_args()

    print(f"\n{'='*58}")
    print(f"  COMPILE SESSION — Option C Ingestion")
    print(f"{'='*58}\n")

    # ── Find session ──────────────────────────────────────────────────────────
    session_path = find_latest_session(args.session)
    print(f"Session: {session_path.name}\n")

    session_content = session_path.read_text(encoding="utf-8", errors="ignore")

    # ── Analyze with Claude ───────────────────────────────────────────────────
    print("── Analyzing session with Claude... ────────────────────")
    plan = call_claude(session_content)

    summary      = plan.get("summary", "")
    auto_handle  = plan.get("auto_handle", [])
    flags        = plan.get("flags", [])
    metrics      = plan.get("metrics", {})

    print(f"\n  Summary: {summary}")
    print(f"  Pieces found:    {metrics.get('pieces_found', len(auto_handle) + len(flags))}")
    print(f"  Auto-handle:     {len(auto_handle)}")
    print(f"  Flags:           {len(flags)}")
    print()

    # ── Auto-handle queue ─────────────────────────────────────────────────────
    print("── Auto-handle queue ───────────────────────────────────")
    changed = apply_auto_handle(auto_handle, dry_run=args.dry_run)
    print()

    # ── Flag queue ────────────────────────────────────────────────────────────
    if flags:
        print("── Flag queue ──────────────────────────────────────────")
        for i, flag in enumerate(flags, 1):
            print(f"  [{i}] {flag.get('type')} [{flag.get('priority')}] — {flag.get('description', '')[:70]}")
        write_flags_file(flags, session_path.name, dry_run=args.dry_run)
        print()

    # ── Git commit ────────────────────────────────────────────────────────────
    if not args.dry_run:
        print("── Git commit ──────────────────────────────────────────")
        git_commit(changed, session_path.name)
        print()

    # ── Telegram notification ─────────────────────────────────────────────────
    print("── Telegram ────────────────────────────────────────────")
    tg_msg = (
        f"🧠 *Session Ingested*\n"
        f"📄 `{session_path.name}`\n\n"
        f"_{summary}_\n\n"
        f"✅ Auto-handled: {len(changed)} nodes\n"
        f"⚠️ Flags: {len(flags)} items\n"
    )
    if flags:
        tg_msg += f"\nReview: `08_SESSIONS/ingestion_flags.md`"
    if not args.dry_run:
        send_telegram(tg_msg)
    else:
        print("  [dry-run] Telegram skipped")

    # ── Summary ───────────────────────────────────────────────────────────────
    print(f"\n{'='*58}")
    print(f"  DONE")
    print(f"  Auto-handled: {len(changed)} vault nodes updated")
    print(f"  Flags: {len(flags)} items → ingestion_flags.md")
    if args.dry_run:
        print(f"  [dry-run] No files were modified")
    print(f"{'='*58}\n")


if __name__ == "__main__":
    main()
