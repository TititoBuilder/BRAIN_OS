"""
task_session.py — focused context launcher for task-specific Claude sessions.

Usage:
    python task_session.py --task [git|audio|fix|build]

Each task reads only the files relevant to that work, builds a compact
context string, prints it, and copies it to the clipboard.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

BRAIN_OS = Path(r"C:\BRAIN_OS")


def _queue_open_items():
    """Return open [ ] lines from the ## In Progress section only."""
    lines = (BRAIN_OS / "00_DASHBOARD" / "Queue.md").read_text(encoding="utf-8").splitlines()
    in_section, items = False, []
    for line in lines:
        if line.startswith("## In Progress"):
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if in_section and line.startswith("- [ ]"):
            items.append(line)
    return items


def _queue_in_progress_section():
    """Return the full ## In Progress section text."""
    lines = (BRAIN_OS / "00_DASHBOARD" / "Queue.md").read_text(encoding="utf-8").splitlines()
    in_section, out = False, []
    for line in lines:
        if line.startswith("## In Progress"):
            in_section = True
            out.append(line)
            continue
        if in_section and line.startswith("## "):
            break
        if in_section:
            out.append(line)
    return "\n".join(out)


def build_git_context():
    parts = ["=== TASK: GIT ===\n"]

    parts.append("--- Open Queue Items ---")
    items = _queue_open_items()
    parts.extend(items or ["(none)"])

    parts.append("\n--- Git Notes ---")
    found = False
    # look in knowledge_os for git* files
    for f in sorted((BRAIN_OS / "02_PROJECTS" / "knowledge_os").glob("git*.md")):
        parts.append(f"\n[{f.name}]")
        parts.append("\n".join(f.read_text(encoding="utf-8").splitlines()[:5]))
        found = True
    # also check 05_LEARNING/git/ if it exists
    learn_git = BRAIN_OS / "05_LEARNING" / "git"
    if learn_git.exists():
        for f in sorted(learn_git.glob("*.md")):
            parts.append(f"\n[{f.name}]")
            parts.append("\n".join(f.read_text(encoding="utf-8").splitlines()[:5]))
            found = True
    if not found:
        parts.append("(no git notes found)")

    return "\n".join(parts)


def build_audio_context():
    parts = ["=== TASK: AUDIO ===\n"]

    parts.append("--- Open Queue Items ---")
    parts.extend(_queue_open_items() or ["(none)"])

    # drive_index summary
    with open(BRAIN_OS / "09_TOOLS" / "drive_index.json", encoding="utf-8") as f:
        idx = json.load(f)["index"]
    total = len(idx)
    path_fmt = sum(1 for v in idx.values() if not v.startswith("id:"))
    parts.append("\n--- drive_index.json ---")
    parts.append(f"Total entries  : {total}")
    parts.append(f"id: format     : {total - path_fmt}")
    parts.append(f"path-format    : {path_fmt}  (flagged for re-voice)")

    # audio_staging file list
    staging = BRAIN_OS / "audio_staging"
    parts.append("\n--- audio_staging/ ---")
    if staging.exists():
        files = sorted(staging.iterdir())
        parts.extend([f"  {f.name}" for f in files] or ["  (empty)"])
    else:
        parts.append("  (folder not found)")

    return "\n".join(parts)


def build_fix_context():
    parts = ["=== TASK: FIX ===\n"]

    parts.append("--- Open Queue Items ---")
    parts.extend(_queue_open_items() or ["(none)"])

    parts.append("\n--- 09_TOOLS_INDEX.md ---")
    idx = BRAIN_OS / "09_TOOLS" / "09_TOOLS_INDEX.md"
    parts.append(idx.read_text(encoding="utf-8") if idx.exists() else "(not found)")

    return "\n".join(parts)


def build_build_context():
    parts = ["=== TASK: BUILD ===\n"]

    parts.append("--- CLAUDE.md ---")
    claude_md = BRAIN_OS / "CLAUDE.md"
    parts.append(claude_md.read_text(encoding="utf-8") if claude_md.exists() else "(not found)")

    ctx = BRAIN_OS / "00_DASHBOARD" / ".context.md"
    if ctx.exists():
        parts.append("\n--- .context.md ---")
        parts.append(ctx.read_text(encoding="utf-8"))

    parts.append("\n--- Queue.md: In Progress ---")
    parts.append(_queue_in_progress_section())

    return "\n".join(parts)


def copy_to_clipboard(text: str) -> None:
    try:
        subprocess.run(["clip"], input=text.encode("utf-8"), check=True)
    except Exception as exc:
        print(f"[clipboard failed: {exc}]", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="Focused task context launcher")
    parser.add_argument("--task", required=True, choices=["git", "audio", "fix", "build"])
    args = parser.parse_args()

    builders = {
        "git":   build_git_context,
        "audio": build_audio_context,
        "fix":   build_fix_context,
        "build": build_build_context,
    }

    context = builders[args.task]()
    print(context)
    copy_to_clipboard(context)


if __name__ == "__main__":
    main()
