"""
category: Vault & Sync
trigger_index.py — Regenerate the tables in Trigger_Architecture.md from node frontmatter.

Reads every 08_TRIGGERS/Trigger_*.md, parses type, project, fires_when and
implemented_by, and rewrites the region between the TRIGGER_INDEX:START and
TRIGGER_INDEX:END markers. Section counts are derived, so they cannot drift
the way a hand-maintained count does.

A node whose project field names two projects, separated by a slash, is
listed under both in Coverage by Project.

Usage:
    python C:/BRAIN_OS/09_TOOLS/trigger_index.py
    python C:/BRAIN_OS/09_TOOLS/trigger_index.py --dry-run
"""

import argparse
import re
from pathlib import Path

BRAIN_OS = Path(r"C:\BRAIN_OS")
TRIGGERS = BRAIN_OS / "08_TRIGGERS"
TARGET = BRAIN_OS / "07_SYSTEM" / "Trigger_Architecture.md"

START = "<!-- TRIGGER_INDEX:START -->"
END = "<!-- TRIGGER_INDEX:END -->"

TYPE_ORDER = ["TIME", "EVENT", "STATE", "MANUAL"]
COLUMN = {"TIME": "Schedule", "EVENT": "Source", "STATE": "Condition", "MANUAL": "How"}


def read_node(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    fields = {}
    for line in text.splitlines():
        s = line.strip()
        if s == "---" and fields:
            break
        m = re.match(r"^(type|project|fires_when|implemented_by):\s*(.+)$", s)
        if m:
            fields[m.group(1)] = m.group(2).strip().strip('"')
    fields["name"] = path.stem
    return fields


def build(nodes: list[dict]) -> str:
    out = [START, ""]
    for t in TYPE_ORDER:
        group = sorted((n for n in nodes if n.get("type") == t), key=lambda n: n["name"])
        if not group:
            continue
        out.append(f"## {t} — {len(group)} triggers")
        out.append(f"| Trigger | Project | {COLUMN[t]} | Implemented by |")
        out.append("|---|---|---|---|")
        for n in group:
            out.append(
                f"| [[{n['name']}]] | {n.get('project', '?')} "
                f"| {n.get('fires_when', '?')} | {n.get('implemented_by', '?')} |"
            )
        out.append("")

    out.append("## Coverage by Project")
    out.append("| Project | Triggers |")
    out.append("|---|---|")
    by_project: dict[str, list[str]] = {}
    for n in nodes:
        for proj in [p.strip() for p in n.get("project", "?").split("/")]:
            by_project.setdefault(proj, []).append(n["name"])
    for proj in sorted(by_project):
        links = " ".join(f"[[{x}]]" for x in sorted(by_project[proj]))
        out.append(f"| {proj} | {links} |")
    out.append("")
    out.append(END)
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser(description="Regenerate the Trigger_Architecture tables")
    ap.add_argument("--dry-run", action="store_true", help="Print the block, write nothing")
    args = ap.parse_args()

    nodes = [read_node(p) for p in sorted(TRIGGERS.glob("Trigger_*.md"))]
    if not nodes:
        raise SystemExit("ERROR: no trigger nodes found")

    block = build(nodes)
    if args.dry_run:
        print(block)
        return

    text = TARGET.read_text(encoding="utf-8")
    if START in text and END in text:
        head = text.split(START)[0]
        tail = text.split(END, 1)[1]
        new = head + block + tail
    else:
        raise SystemExit(
            f"ERROR: markers not found in {TARGET.name}.\n"
            f"  Add {START} and {END} around the region this tool owns."
        )

    TARGET.write_text(new, encoding="utf-8", newline="\n")
    types = len({n.get("type") for n in nodes})
    print(f"[trigger_index] wrote {len(nodes)} triggers across {types} types.")


if __name__ == "__main__":
    main()
