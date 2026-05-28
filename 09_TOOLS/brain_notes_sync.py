"""
brain_notes_sync.py  —  Sync Railway Q&As → BRAIN_OS vault
===========================================================
Pulls brain_notes.md from BRAIN_OS GitHub repo, parses new Q&A
entries, appends them to dated vault notes, marks as processed,
commits back to GitHub.

Usage:
    python C:\\BRAIN_OS\\09_TOOLS\\brain_notes_sync.py
    python C:\\BRAIN_OS\\09_TOOLS\\brain_notes_sync.py --dry-run
"""

import argparse
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────

BRAIN_OS        = Path(r"C:\BRAIN_OS")
NOTES_FILE      = BRAIN_OS / "02_PROJECTS" / "knowledge_os" / "brain_notes.md"
VAULT_NOTES_DIR = BRAIN_OS / "06_NOTES"
PROCESSED_TAG   = "<!-- synced -->"


# ── Git helpers ───────────────────────────────────────────────────────────────

def git(args: list, check: bool = True):
    return subprocess.run(
        ["git", "-C", str(BRAIN_OS)] + args,
        capture_output=True, text=True, encoding="utf-8", check=check
    )


def git_pull():
    r = git(["pull"])
    print(f"  git pull: {r.stdout.strip() or 'up to date'}")


def git_commit_push(message: str):
    git(["add", str(NOTES_FILE), str(VAULT_NOTES_DIR)])
    r = git(["commit", "-m", message], check=False)
    if r.returncode != 0 and "nothing to commit" in r.stdout + r.stderr:
        print("  Nothing to commit.")
        return
    git(["push"])
    print(f"  Committed: {message}")


# ── Parse brain_notes.md ──────────────────────────────────────────────────────

def parse_new_entries(content: str) -> list[dict]:
    """
    Expects entries in this format (written by Railway /note endpoint):

        ## 2026-05-28 06:30 | topic_key

        **Q:** question text

        **A:** answer text

        ---
    """
    entries = []
    blocks = re.split(r'\n(?=## )', "\n" + content.strip())

    for block in blocks:
        block = block.strip()
        if not block.startswith("##"):
            continue
        if PROCESSED_TAG in block:
            continue

        header  = re.match(r'^## (.+)', block)
        q_match = re.search(r'\*\*Q:\*\*\s*(.+?)(?=\*\*A:\*\*)', block, re.DOTALL)
        a_match = re.search(r'\*\*A:\*\*\s*(.+?)(?=---|$)', block, re.DOTALL)

        if header and q_match and a_match:
            entries.append({
                "header":   header.group(1).strip(),
                "question": q_match.group(1).strip(),
                "answer":   a_match.group(1).strip(),
                "raw":      block,
            })

    return entries


# ── Write to vault ────────────────────────────────────────────────────────────

def save_to_vault(entry: dict, dry_run: bool):
    VAULT_NOTES_DIR.mkdir(parents=True, exist_ok=True)
    today     = datetime.now().strftime("%Y-%m-%d")
    note_file = VAULT_NOTES_DIR / f"QA_Notes_{today}.md"

    block = (
        f"\n## {entry['header']}\n\n"
        f"**Q:** {entry['question']}\n\n"
        f"**A:** {entry['answer']}\n\n"
        f"---\n"
    )

    if dry_run:
        print(f"    → would append to {note_file.name}")
        print(f"      Q: {entry['question'][:80]}")
        return

    # Create file with header if new
    if not note_file.exists():
        note_file.write_text(f"# Q&A Notes — {today}\n", encoding="utf-8")

    with open(note_file, "a", encoding="utf-8") as f:
        f.write(block)


# ── Mark processed ────────────────────────────────────────────────────────────

def mark_processed(content: str, entries: list[dict]) -> str:
    for entry in entries:
        tagged = entry["raw"] + f"\n{PROCESSED_TAG}"
        content = content.replace(entry["raw"], tagged)
    return content


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Sync Railway Q&As to BRAIN_OS vault")
    parser.add_argument("--dry-run", action="store_true", help="Show plan, no writes")
    args = parser.parse_args()

    print("\n[brain_notes_sync] Starting...\n")

    # Pull latest (notes committed by Railway land here)
    if not args.dry_run:
        print("── git pull ─────────────────────────────────────────────")
        git_pull()
        print()

    # Check notes file
    if not NOTES_FILE.exists():
        print(f"[brain_notes_sync] brain_notes.md not found at:\n  {NOTES_FILE}")
        print("  No notes have been saved from the app yet.")
        sys.exit(0)

    content = NOTES_FILE.read_text(encoding="utf-8")
    entries = parse_new_entries(content)

    if not entries:
        print("[brain_notes_sync] No new entries — all notes already synced.")
        sys.exit(0)

    print(f"── Processing {len(entries)} new Q&A entries ─────────────────")
    for i, entry in enumerate(entries, 1):
        print(f"\n  [{i}/{len(entries)}] {entry['header']}")
        save_to_vault(entry, dry_run=args.dry_run)

    if args.dry_run:
        print(f"\n[dry-run] {len(entries)} entries would be saved. No changes made.")
        return

    # Mark entries as processed in brain_notes.md
    updated = mark_processed(content, entries)
    NOTES_FILE.write_text(updated, encoding="utf-8")

    # Commit vault notes + updated brain_notes.md
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"\n── git commit ───────────────────────────────────────────────")
    git_commit_push(f"sync: {len(entries)} Q&A notes — {today}")

    print(f"\n{'='*56}")
    print(f"  DONE  |  {len(entries)} entries saved to {VAULT_NOTES_DIR.name}/")
    print(f"{'='*56}\n")


if __name__ == "__main__":
    main()
