#!/usr/bin/env python3
"""
obsidian_sync.py -- Knowledge OS Phase 3
=========================================
Reads obsidian_sync.json exported from the Knowledge OS app.
Finds matching .md files in your Obsidian vault by machine_key.
Updates YAML frontmatter with knowledge_os_* fields.

Location : C:\\BRAIN_OS\\09_TOOLS\\obsidian_sync.py
Venv     : C:\\Knowledge\\CA\\venv\\Scripts\\python.exe

Install:
    C:\\Knowledge\\CA\\venv\\Scripts\\pip install pyyaml

Usage:
    python obsidian_sync.py --input obsidian_sync.json
    python obsidian_sync.py --input obsidian_sync.json --dry-run
    python obsidian_sync.py --input obsidian_sync.json --vault C:\\BRAIN_OS

Flags:
    --input      Path to obsidian_sync.json        (required)
    --vault      Obsidian vault root               (default: C:\\BRAIN_OS)
    --dry-run    Preview only, no files written
    --create     Create a new .md stub if no match found
    --create-dir Vault folder for new stubs        (default: 02_PROJECTS\\knowledge_os)
"""

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed.")
    print("  Run: C:\\Knowledge\\CA\\venv\\Scripts\\pip install pyyaml")
    sys.exit(1)


FRONTMATTER_RE = re.compile(r"^---\r?\n(.*?)\r?\n---", re.DOTALL)

KOS_FIELDS = [
    "knowledge_os_status",
    "knowledge_os_score",
    "knowledge_os_priority",
    "knowledge_os_evidence",
    "knowledge_os_last_touched",
    "knowledge_os_machine_key",
    "knowledge_os_domain",
]

SKIP_DIRS = {"_archive", ".obsidian", "__pycache__", ".git", "node_modules"}


# ─── Vault indexing ───────────────────────────────────────────────────────

def index_vault(vault: Path) -> dict[str, Path]:
    """Return {normalized_stem -> Path} for all .md files, skipping archive dirs."""
    files: dict[str, Path] = {}
    for f in vault.rglob("*.md"):
        if any(part in SKIP_DIRS or part.startswith(".") for part in f.parts):
            continue
        norm = _normalize(f.stem)
        if norm not in files:
            files[norm] = f
    return files


def _normalize(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")


# ─── Matching ─────────────────────────────────────────────────────────────

def find_match(topic: dict, index: dict[str, Path]) -> Path | None:
    key = _normalize(topic["machine_key"])
    name = _normalize(topic["topic"])

    # 1. Exact machine_key
    if key in index:
        return index[key]

    # 2. Exact normalized topic name
    if name in index:
        return index[name]

    # 3. machine_key is a substring of a vault filename (or vice versa)
    for norm, path in index.items():
        if key in norm or norm in key:
            return path

    # 4. Partial word overlap (>=2 words match)
    key_words = set(key.split("_")) - {"the", "a", "an", "of", "and", "or"}
    for norm, path in index.items():
        norm_words = set(norm.split("_"))
        if len(key_words & norm_words) >= 2:
            return path

    return None


# ─── Frontmatter I/O ──────────────────────────────────────────────────────

def read_frontmatter(content: str) -> tuple[dict, str]:
    m = FRONTMATTER_RE.match(content)
    if m:
        try:
            fm = yaml.safe_load(m.group(1)) or {}
        except yaml.YAMLError:
            fm = {}
        return fm, content[m.end():]
    return {}, content


def write_frontmatter(fm: dict, body: str) -> str:
    fm_str = yaml.dump(fm, default_flow_style=False, allow_unicode=True, sort_keys=False).strip()
    return f"---\n{fm_str}\n---{body}"


def apply_topic(topic: dict, vault_file: Path, dry_run: bool) -> bool:
    """Write knowledge_os_* fields to file frontmatter. Returns True if changed."""
    try:
        content = vault_file.read_text(encoding="utf-8")
    except Exception as e:
        print(f"    [FAIL] Could not read file: {e}")
        return False

    fm, body = read_frontmatter(content)

    # Snapshot for change detection
    old_kos = {k: fm.get(k) for k in KOS_FIELDS}

    fm["knowledge_os_machine_key"]  = topic["machine_key"]
    fm["knowledge_os_domain"]       = topic["domain"]
    fm["knowledge_os_status"]       = topic["status"]
    fm["knowledge_os_score"]        = topic["score"]
    fm["knowledge_os_priority"]     = topic["priority"]
    if topic.get("evidence"):
        fm["knowledge_os_evidence"] = topic["evidence"]
    if topic.get("last_touched"):
        fm["knowledge_os_last_touched"] = topic["last_touched"]

    new_kos = {k: fm.get(k) for k in KOS_FIELDS}
    changed = old_kos != new_kos

    if changed and not dry_run:
        new_content = write_frontmatter(fm, body)
        try:
            vault_file.write_text(new_content, encoding="utf-8")
        except Exception as e:
            print(f"    [FAIL] Write error: {e}")
            return False

    return changed


def create_stub(topic: dict, stub_dir: Path, dry_run: bool) -> Path:
    """Create a minimal .md stub for a topic with no vault match."""
    stub_dir.mkdir(parents=True, exist_ok=True)
    path = stub_dir / f"{topic['machine_key']}.md"

    fm = {
        "knowledge_os_machine_key":  topic["machine_key"],
        "knowledge_os_domain":       topic["domain"],
        "knowledge_os_status":       topic["status"],
        "knowledge_os_score":        topic["score"],
        "knowledge_os_priority":     topic["priority"],
    }
    if topic.get("evidence"):
        fm["knowledge_os_evidence"] = topic["evidence"]
    if topic.get("last_touched"):
        fm["knowledge_os_last_touched"] = topic["last_touched"]

    body = f"\n\n# {topic['topic']}\n\n> Auto-created by Knowledge OS Obsidian Sync.\n\n"
    content = write_frontmatter(fm, body)

    if not dry_run:
        path.write_text(content, encoding="utf-8")

    return path


# ─── Main ─────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Knowledge OS Phase 3 -- Obsidian Sync",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python obsidian_sync.py --input obsidian_sync.json
  python obsidian_sync.py --input obsidian_sync.json --dry-run
  python obsidian_sync.py --input obsidian_sync.json --create
        """
    )
    parser.add_argument("--input",      required=True,                       help="Path to obsidian_sync.json")
    parser.add_argument("--vault",      default="C:\\BRAIN_OS",              help="Vault root (default: C:\\BRAIN_OS)")
    parser.add_argument("--dry-run",    action="store_true",                 help="Preview only, no writes")
    parser.add_argument("--create",     action="store_true",                 help="Create .md stubs for unmatched topics")
    parser.add_argument("--create-dir", default="02_PROJECTS\\knowledge_os", help="Subfolder for new stubs")
    args = parser.parse_args()

    input_path = Path(args.input)
    vault      = Path(args.vault)
    stub_dir   = vault / args.create_dir

    # Load topics
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    topics = data if isinstance(data, list) else data.get("topics", [])

    print()
    print("=" * 62)
    print("  Knowledge OS -- Obsidian Sync")
    print(f"  Topics : {len(topics)}")
    print(f"  Vault  : {vault}")
    print(f"  Mode   : {'DRY RUN -- no files written' if args.dry_run else 'WRITE'}")
    if args.create:
        print(f"  Create : {stub_dir}")
    print("=" * 62)
    print()

    index = index_vault(vault)
    print(f"  Indexed {len(index)} vault files\n")

    matched   = 0
    updated   = 0
    unchanged = 0
    created   = 0
    missed    = []

    for topic in topics:
        name = topic.get("topic", topic.get("machine_key"))
        vault_file = find_match(topic, index)

        if vault_file:
            rel     = vault_file.relative_to(vault)
            changed = apply_topic(topic, vault_file, args.dry_run)
            tag     = "UPDATE" if changed else "NO-CHG"
            print(f"  [{tag}] {name}")
            print(f"         {rel}")
            matched += 1
            if changed:
                updated += 1
            else:
                unchanged += 1
        elif args.create:
            path = create_stub(topic, stub_dir, args.dry_run)
            rel  = path.relative_to(vault)
            print(f"  [CREATE] {name}")
            print(f"          {rel}")
            created += 1
        else:
            print(f"  [MISS]  {name}  [{topic.get('machine_key')}]")
            missed.append(topic.get("machine_key", "?"))

    print()
    print("=" * 62)
    print(f"  Matched   : {matched}/{len(topics)}")
    print(f"  Updated   : {updated}")
    print(f"  Unchanged : {unchanged}")
    if args.create:
        print(f"  Created   : {created}")
    print(f"  Missed    : {len(missed)}")
    if missed:
        sample = ", ".join(missed[:6]) + ("..." if len(missed) > 6 else "")
        print(f"  Keys      : {sample}")
    if args.dry_run:
        print()
        print("  [DRY RUN] No files were written.")
    print("=" * 62)
    print()


if __name__ == "__main__":
    main()
