#!/usr/bin/env python3
"""
audit_files.py  --  Read-only file audit across the BRAIN_OS ecosystem.

Measures local disk reality against Naming_Contract.md. NEVER renames,
moves, or deletes anything. Produces a truth map: for every file, its
class (machine-key vs human-readable), owner project, and every place
it is referenced.

The reference scan is the safety mechanism: any file referenced by code
or config is flagged MACHINE-KEY (freeze it). Files only referenced by
vault wiki-links, or not referenced at all, are human-readable.

USAGE (run from anywhere, e.g. Win+X -> Terminal):
    python audit_files.py
    python audit_files.py --json report.json     # also write machine-readable
    python audit_files.py --root C:\\Dev          # limit scan to one root

Drive is NOT scanned here (no Drive access from a local script without
the API). Drive parity is a separate pass once we read this local map.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field, asdict
from pathlib import Path

# ---------------------------------------------------------------------------
# CONFIG  --  the stores we scan. Edit these paths if any are wrong.
# ---------------------------------------------------------------------------

PROJECT_ROOTS = {
    "soccer-content-generator": r"C:\Dev\Projects\soccer-content-generator",
    "cristian-construction":    r"C:\Dev\CristianConstruction",
    "read-along-app":           r"C:\Users\titit\Projects\read-along-app",
    "resolve-mcp-server":       r"C:\Users\titit\Projects\resolve-mcp-server",
    "brain-audio":              r"C:\Dev\shared\brain-audio",
    "book-compiler":            r"C:\Dev\shared\book-compiler",
    "brain-os":                 r"C:\BRAIN_OS",
    "knowledge":                r"C:\Knowledge",
}

# File types that are CONTENT we care about classifying.
CONTENT_EXTS = {".md", ".py", ".ts", ".tsx", ".js", ".jsx",
                ".json", ".wav", ".mp3", ".html", ".txt"}

# File types we read to FIND references (where code/config looks things up).
SOURCE_EXTS = {".py", ".ts", ".tsx", ".js", ".jsx", ".json", ".md", ".html"}

# Directories we never descend into.
SKIP_DIRS = {".git", "node_modules", "venv", ".venv", "__pycache__",
             "dist", "build", ".next", "site-packages", ".obsidian",
             "audio_staging", "_trash"}  # audio_staging scanned separately as workshop

# Generic filenames that collide across projects. A cross-project match on
# these is almost always a false positive (every React app has an index.html).
# They only count as machine-key when referenced from within their OWN project.
GENERIC_NAMES = {
    "settings.json", "settings.local.json", "index.html", "index.js",
    "index.ts", "package.json", "package-lock.json", "__init__.py",
    "main.py", "main.jsx", "main.tsx", "config.json", "tsconfig.json",
    "vite.config.js", "eslint.config.js", "app.jsx", "app.tsx",
    "readme.md", "requirements.txt", ".env", "vercel.json", "dockerfile",
}

# Wiki-link pattern for Obsidian: [[note name]] or [[note name|alias]]
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)")

MAX_REF_BYTES = 2_000_000  # don't read source files larger than ~2MB


# ---------------------------------------------------------------------------
# DATA MODEL
# ---------------------------------------------------------------------------

@dataclass
class FileRecord:
    path: str
    name: str
    stem: str               # name without extension
    ext: str
    project: str
    size: int
    cls: str = "unknown"            # machine-key | human-readable
    ref_reason: str = ""            # why it got that class
    code_refs: list = field(default_factory=list)   # files referencing it
    wiki_refs: list = field(default_factory=list)
    contract_flags: list = field(default_factory=list)  # rule violations


# ---------------------------------------------------------------------------
# SCANNING
# ---------------------------------------------------------------------------

def project_for(path: Path, roots: dict[str, Path]) -> str:
    """Return the owning project for a path, or 'ORPHAN' if under no root."""
    for name, root in roots.items():
        try:
            path.relative_to(root)
            return name
        except ValueError:
            continue
    return "ORPHAN"


def walk_files(root: Path):
    """Yield content files under root, skipping noise directories."""
    for p in root.rglob("*"):
        if p.is_dir():
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.suffix.lower() in CONTENT_EXTS:
            yield p


def build_lookup_names(rec: FileRecord) -> set[str]:
    """
    The strings code might use to reference this file. We match on the
    full name, the stem, and a normalized topic key (hyphens/underscores
    interchangeable) so 'audio_fingerprinting' matches 'audio-fingerprinting'.
    """
    names = {rec.name, rec.stem}
    names.add(rec.stem.replace("-", "_"))
    names.add(rec.stem.replace("_", "-"))
    # drop trivially short stems to avoid false-positive matches
    return {n for n in names if len(n) >= 4}


def read_source_text(p: Path) -> str:
    try:
        if p.stat().st_size > MAX_REF_BYTES:
            return ""
        return p.read_text(encoding="utf-8", errors="ignore")
    except (OSError, ValueError):
        return ""


# ---------------------------------------------------------------------------
# MAIN AUDIT
# ---------------------------------------------------------------------------

def run_audit(roots: dict[str, Path]) -> list[FileRecord]:
    print("Phase 1: discovering files...", file=sys.stderr)
    records: list[FileRecord] = []
    for proj, root in roots.items():
        if not root.exists():
            print(f"  WARNING: root missing, skipped: {root}", file=sys.stderr)
            continue
        for p in walk_files(root):
            records.append(FileRecord(
                path=str(p), name=p.name, stem=p.stem,
                ext=p.suffix.lower(),
                project=project_for(p, roots),
                size=p.stat().st_size,
            ))
    print(f"  found {len(records)} content files", file=sys.stderr)

    # Phase 2: build the reference index by reading every source file ONCE.
    print("Phase 2: indexing references (one pass over source files)...",
          file=sys.stderr)
    # Map every lookup-name -> the FileRecords that claim it.
    name_to_records: dict[str, list[FileRecord]] = defaultdict(list)
    for rec in records:
        for n in build_lookup_names(rec):
            name_to_records[n].append(rec)

    source_files = [r for r in records if r.ext in SOURCE_EXTS]
    for src in source_files:
        text = read_source_text(Path(src.path))
        if not text:
            continue
        is_code = src.ext in {".py", ".ts", ".tsx", ".js", ".jsx", ".json", ".html"}
        if not is_code:
            # still need wiki-link handling below for .md
            pass
        else:
            # A reference counts only when the FULL filename (with extension)
            # appears in the source. This kills false positives from generic
            # stems like "settings" or "index" matching unrelated prose/keys.
            for name, targets in name_to_records.items():
                if name not in text:
                    continue
                for tgt in targets:
                    if tgt.path == src.path:
                        continue
                    full = tgt.name in text          # strong: exact filename
                    same_proj = (src.project == tgt.project)
                    generic = tgt.name.lower() in GENERIC_NAMES
                    # Count if: exact filename appears, AND either it's
                    # distinctive OR the reference is within the same project.
                    if full and (not generic or same_proj):
                        tgt.code_refs.append(src.name)
        # Wiki-links (vault): only meaningful in .md
        if src.ext == ".md":
            for m in WIKILINK_RE.finditer(text):
                link = m.group(1).strip()
                for cand in (link, link.replace(" ", "-"), link.replace(" ", "_")):
                    for tgt in name_to_records.get(cand, []):
                        if tgt.path != src.path:
                            tgt.wiki_refs.append(src.name)

    # Phase 3: classify + flag contract violations.
    print("Phase 3: classifying and checking contract...", file=sys.stderr)
    # File types that CAN legitimately be machine-keys (code looks them up).
    # A .md/.txt doc whose name merely appears in a .py is NOT a machine-key;
    # documentation is human-readable even when code mentions the topic.
    KEYABLE_EXTS = {".wav", ".mp3", ".json", ".py", ".ts", ".tsx",
                    ".js", ".jsx", ".html"}
    for rec in records:
        rec.code_refs = sorted(set(rec.code_refs))
        rec.wiki_refs = sorted(set(rec.wiki_refs))
        if rec.code_refs and rec.ext in KEYABLE_EXTS:
            rec.cls = "machine-key"
            rec.ref_reason = f"referenced by code/config: {', '.join(rec.code_refs[:5])}"
        elif rec.code_refs:
            # doc whose topic name appears in code, but a doc is never a
            # machine-key — its name is for humans. Treat as linked.
            rec.cls = "human-readable"
            rec.ref_reason = f"topic mentioned in code (doc stays human-readable)"
        elif rec.wiki_refs:
            rec.cls = "human-readable"
            rec.ref_reason = f"linked from {len(rec.wiki_refs)} vault note(s)"
        else:
            rec.cls = "human-readable"
            rec.ref_reason = "no references found (orphan candidate)"
        classify_contract(rec)
    return records


def classify_contract(rec: FileRecord) -> None:
    """Flag naming-contract violations. Only meaningful for human-readable."""
    flags = rec.contract_flags
    if rec.cls == "machine-key":
        return  # machine-key names are frozen; we do not judge their format
    name = rec.stem
    if " " in name:
        flags.append("has spaces")
    if re.search(r"([_\- ](final\d*|v\d+|new|copy|backup|old))+$", name, re.IGNORECASE):
        flags.append("version/junk suffix in name")
    if rec.ext == ".md" and rec.size < 30:
        flags.append("near-empty file")
    if rec.project == "ORPHAN":
        flags.append("under no known project root")


# ---------------------------------------------------------------------------
# REPORTING
# ---------------------------------------------------------------------------

def print_report(records: list[FileRecord]) -> None:
    by_project: dict[str, list[FileRecord]] = defaultdict(list)
    for r in records:
        by_project[r.project].append(r)

    mk = [r for r in records if r.cls == "machine-key"]
    hr = [r for r in records if r.cls == "human-readable"]
    orphans = [r for r in records
               if "no references found" in r.ref_reason
               and r.ext not in {".py", ".ts", ".tsx", ".js", ".jsx"}]
    flagged = [r for r in records if r.contract_flags]

    print("\n" + "=" * 70)
    print("FILE AUDIT REPORT")
    print("=" * 70)
    print(f"Total content files : {len(records)}")
    print(f"  Machine-key (freeze, code depends on them) : {len(mk)}")
    print(f"  Human-readable (safe to rename)            : {len(hr)}")
    print(f"  Orphan candidates (nothing references)     : {len(orphans)}")
    print(f"  Contract violations flagged                : {len(flagged)}")

    print("\n--- Files per project ---")
    for proj in sorted(by_project):
        rs = by_project[proj]
        mkn = sum(1 for r in rs if r.cls == "machine-key")
        print(f"  {proj:28} {len(rs):4} files   ({mkn} machine-key)")

    print("\n--- MACHINE-KEY FILES (do NOT rename without migration) ---")
    for r in sorted(mk, key=lambda x: x.path)[:60]:
        print(f"  [{r.project}] {r.name}")
        print(f"      <- {r.ref_reason}")
    if len(mk) > 60:
        print(f"  ... and {len(mk) - 60} more (see --json for full list)")

    print("\n--- CONTRACT VIOLATIONS (human-readable, safe to fix) ---")
    for r in sorted(flagged, key=lambda x: x.path)[:60]:
        print(f"  [{r.project}] {r.name}")
        print(f"      ! {'; '.join(r.contract_flags)}")
    if len(flagged) > 60:
        print(f"  ... and {len(flagged) - 60} more")

    print("\n--- ORPHAN CANDIDATES (nothing references them) ---")
    for r in sorted(orphans, key=lambda x: x.path)[:40]:
        print(f"  [{r.project}] {r.name}")
    if len(orphans) > 40:
        print(f"  ... and {len(orphans) - 40} more")
    print("\n" + "=" * 70)
    print("READ-ONLY: nothing was changed. Renames are a separate step.")
    print("=" * 70)


def main() -> int:
    ap = argparse.ArgumentParser(description="Read-only file audit.")
    ap.add_argument("--json", metavar="PATH",
                    help="also write full machine-readable report to PATH")
    ap.add_argument("--root", metavar="PATH",
                    help="limit scan to a single root path")
    args = ap.parse_args()

    if args.root:
        roots = {"single-root": Path(args.root)}
    else:
        roots = {k: Path(v) for k, v in PROJECT_ROOTS.items()}

    records = run_audit(roots)
    print_report(records)

    if args.json:
        Path(args.json).write_text(
            json.dumps([asdict(r) for r in records], indent=2),
            encoding="utf-8")
        print(f"\nFull report written to {args.json}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
