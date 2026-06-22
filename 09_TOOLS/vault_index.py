"""
vault_index.py — generates the auto-section of the BRAIN_OS navigation page.
Walks the vault, groups .md files by top-level folder, writes [[wikilinks]]
between marker comments in 00_DASHBOARD/Navigation.md. Leaves manual content
above/below the markers untouched.
"""
from pathlib import Path

VAULT_ROOT = Path(r"C:\BRAIN_OS")
NAV_FILE = VAULT_ROOT / "00_DASHBOARD" / "Navigation.md"
START_MARKER = "<!-- AUTO-GENERATED:START -->"
END_MARKER = "<!-- AUTO-GENERATED:END -->"

SKIP_DIRS = {".obsidian", ".git", "node_modules", "__pycache__", "venv"}


def build_auto_section() -> str:
    by_folder: dict[str, list[Path]] = {}
    for md_file in VAULT_ROOT.rglob("*.md"):
        if md_file == NAV_FILE:
            continue
        rel = md_file.relative_to(VAULT_ROOT)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        top = rel.parts[0] if len(rel.parts) > 1 else "_root"
        by_folder.setdefault(top, []).append(rel)

    lines = [START_MARKER, ""]
    for folder in sorted(by_folder):
        files = sorted(by_folder[folder])
        lines.append(f"## {folder}")
        for f in files:
            name = f.stem
            lines.append(f"- [[{name}]]")
        lines.append("")
    lines.append(END_MARKER)
    return "\n".join(lines)


def main() -> None:
    auto_section = build_auto_section()

    if NAV_FILE.exists():
        content = NAV_FILE.read_text(encoding="utf-8")
        if START_MARKER in content and END_MARKER in content:
            before = content.split(START_MARKER)[0]
            after = content.split(END_MARKER)[1]
            new_content = before + auto_section + after
        else:
            print("[vault_index] Markers not found - appending auto-section to end.")
            new_content = content.rstrip() + "\n\n" + auto_section + "\n"
    else:
        print("[vault_index] Navigation.md does not exist - creating with manual header.")
        header = (
            "# BRAIN_OS Navigation\n\n"
            "_Manually curated overview. Auto-generated file index below - "
            "do not edit between the markers, it will be overwritten._\n\n"
        )
        new_content = header + auto_section + "\n"

    NAV_FILE.parent.mkdir(parents=True, exist_ok=True)
    NAV_FILE.write_text(new_content, encoding="utf-8", newline="\n")
    print(f"[vault_index] Wrote {len(auto_section.splitlines())} lines -> {NAV_FILE}")


if __name__ == "__main__":
    main()
