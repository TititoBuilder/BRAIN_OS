"""
category: System Utilities
tools_index.py — regenerates 09_TOOLS_INDEX.md from module docstrings.

Walks every .py in 09_TOOLS, reads each module docstring via ast, groups by the
"category:" line in that docstring, and rewrites the region between the
TOOLS_INDEX:START / TOOLS_INDEX:END markers. Scripts without a category tag land
under "Uncategorized" so the omission is visible rather than silent.

Exit codes: 0 = written or unchanged, 1 = error, 2 = unavailable (index missing).
"""
import ast
import re
import sys
from datetime import date
from pathlib import Path

TOOLS = Path(r"C:\BRAIN_OS\09_TOOLS")
INDEX = TOOLS / "09_TOOLS_INDEX.md"
START = "<!-- TOOLS_INDEX:START -->"
END = "<!-- TOOLS_INDEX:END -->"

ORDER = [
    "Session Management",
    "Graph & Code Analysis",
    "Audio Generation",
    "Google Drive",
    "Learning Path",
    "Vault & Sync",
    "System Utilities",
    "Uncategorized",
]


def describe(path: Path) -> tuple:
    """Return (category, description) for one script."""
    try:
        doc = ast.get_docstring(ast.parse(path.read_text(encoding="utf-8")))
    except SyntaxError as exc:
        return "Uncategorized", f"**[PARSE ERROR line {exc.lineno}]**"
    except Exception as exc:
        return "Uncategorized", f"**[UNREADABLE: {type(exc).__name__}]**"
    if not doc:
        return "Uncategorized", "**[no docstring]**"

    category = "Uncategorized"
    body = []
    for line in doc.strip().splitlines():
        if line.strip().lower().startswith("category:"):
            category = line.split(":", 1)[1].strip()
            continue
        body.append(line.strip())

    text = " ".join(b for b in body if b).strip()
    text = re.sub(r"[=\u2500\u2014_-]{4,}", " ", text)
    text = re.sub(r"\s{2,}", " ", text).strip()
    if text.lower().startswith(path.name.lower()):
        text = text[len(path.name):].lstrip(" -\u2014")
    first = text.split(". ")[0].rstrip(".")
    return category, (first or "**[no description]**")


def main() -> int:
    if not INDEX.exists():
        print(f"[tools_index] {INDEX} not found - skipping.", file=sys.stderr)
        return 2

    groups = {}
    scripts = sorted(TOOLS.glob("*.py"))
    for p in scripts:
        cat, desc = describe(p)
        groups.setdefault(cat, []).append(f"- `{p.name}` \u2014 {desc}")

    lines = [START, "",
             f"_Generated {date.today().isoformat()} from module docstrings by "
             f"`tools_index.py`. Do not edit by hand._", ""]
    for cat in ORDER + sorted(k for k in groups if k not in ORDER):
        if cat in groups:
            lines += [f"## {cat}", ""] + groups[cat] + [""]
    lines += [f"_{len(scripts)} scripts indexed._", "", END]

    src = INDEX.read_text(encoding="utf-8")
    if START not in src or END not in src:
        print("[tools_index] markers missing - run marker insert first.", file=sys.stderr)
        return 1

    new = src[:src.index(START)] + "\n".join(lines) + src[src.index(END) + len(END):]
    if new == src:
        print("[tools_index] unchanged.")
        return 0

    INDEX.write_text(new, encoding="utf-8", newline="\n")
    print(f"[tools_index] wrote {len(scripts)} scripts across {len(groups)} categories.")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    try:
        sys.exit(main())
    except Exception as exc:
        print(f"[tools_index] ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
