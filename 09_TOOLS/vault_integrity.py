#!/usr/bin/env python3
"""
category: System Utilities
vault_integrity.py -- Read-only integrity scan for the BRAIN_OS vault.

Four independent, informational-only checks. None of these block anything --
same "dirty tree != block" lesson gig_tracker's preflight.py already learned.
Run this, read the report, decide what (if anything) to fix by hand.

    1. Duplicate basenames   -- two files sharing an exact filename. Splits
       byte-identical forks (real drift risk) from mere name collisions
       (different content, may be intentional) and excludes known-legitimate
       patterns (nested CLAUDE.md, _archive/_processed/_generated pairs,
       small pointer-stub notes).
    2. Broken [[wikilinks]]  -- link targets with no matching note anywhere
       in the vault. Flags targets that look like tool filenames (.py/.json/
       etc.) separately -- that's the specific failure mode found in
       software_architecture.md (a note wikilinking a script as if a note
       about it exists).
    3. Secrets outside 03_APIS/.env -- same pattern families as gig_tracker's
       scan_secrets.py, reused as ideas not code (this vault has no .py/.ts
       source to scan, just notes). 03_APIS/.env is the DESIGNATED key store
       and is hard-excluded; anything elsewhere that matches is a real leak.
       Never prints the matched value, only file:line.
    4. Cross-note numeric contradictions -- same entity + same unit word,
       different number, in two different notes (e.g. "delivery_runs 67
       rows" vs "delivery_runs 688 rows"). This detects DISAGREEMENT, not
       INCORRECTNESS -- it cannot tell which note is right, only that they
       disagree. Deliberately narrow: only counts phrased as
       "<entity> <number> <rows|commands|entries|files>". Free-form dollar
       figures are NOT checked here -- matching arbitrary dollar amounts
       without category context produces too much noise to be reliable.
       A vault tool cannot safely verify against gig_tracker's own DB either
       -- that would couple two repos that already deliberately don't share
       code across their boundary (see doc_integrity.py's own docstring).

USAGE:
    python vault_integrity.py
    python vault_integrity.py --json report.json
    python vault_integrity.py --vault C:\\BRAIN_OS
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------

DEFAULT_VAULT = Path(__file__).resolve().parents[1]  # 09_TOOLS/.. == C:\BRAIN_OS

SKIP_DIRS = {".git", ".obsidian", "__pycache__", ".venv", "venv", "node_modules"}

# Path segments that mark a separate namespace -- a same-named file here is
# not vault drift, it's an intentional artifact of a known pipeline/archive.
NAMESPACE_SEGMENTS = {"_archive", "_processed", "_generated"}

# Filenames that are never flagged as duplicates -- a per-directory
# convention (Claude Code scopes a nested CLAUDE.md to its own subtree),
# not vault content drift.
DUPLICATE_EXEMPT_NAMES = {"claude.md"}

STUB_MAX_BYTES = 300  # a note this small that just points elsewhere is a redirect, not a fork

WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)")
CODE_EXTS = {".py", ".json", ".js", ".ts", ".jsx", ".tsx", ".ps1", ".sh"}

# Content types actually worth scanning for secrets / numeric claims.
# (No .py/.ts source lives in the vault the way it does in a code repo --
# this is markdown, txt, and vault config, not code.)
SCAN_EXTS = {".md", ".txt", ".json"}

SECRET_PATTERNS = [
    ("Anthropic API key", re.compile(r"sk-ant-[A-Za-z0-9\-_]{20,}")),
    ("GitHub token", re.compile(r"gh[pousr]_[A-Za-z0-9]{36,}")),
    ("AWS access key ID", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("Google API key", re.compile(r"AIza[0-9A-Za-z\-_]{35}")),
    ("Telegram bot token", re.compile(r"\d{8,10}:[A-Za-z0-9_-]{35}")),
    ("Private key block", re.compile(r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----")),
]

# "<entity> <number> <unit>" -- the exact shape of every known drift incident
# (delivery_runs 67 rows / gig.py 24 commands / other-category NN rows).
COUNT_CLAIM_RE = re.compile(
    r"\b([A-Za-z_][\w.\-]{2,30})\s+(?:has\s+|contains\s+)?(\d[\d,]*)\s+"
    r"(rows?|commands?|entries|files?)\b",
    re.IGNORECASE,
)

# Determiners/quantifiers the regex can capture as "entity" (e.g. "all 321
# rows") that are not actually a named entity -- excluded to avoid flagging
# two unrelated tables as if they made the same claim. Found live: "all 321
# rows" (marker taxonomy) vs "all 462 rows" (an unrelated food_fast table).
ENTITY_STOPWORDS = {
    "all", "the", "this", "these", "those", "some", "each", "both", "any",
    "no", "a", "an", "our", "its", "their", "his", "her", "my", "your",
    "another", "more", "most", "many", "few", "several",
}
# NOTE: "other" is deliberately NOT in this list -- it's the exact category
# name in one of the known drift incidents ("other category" 78->39->16
# rows), a specific DB category, not a generic determiner in that context.


# ---------------------------------------------------------------------------
# DISCOVERY
# ---------------------------------------------------------------------------

def iter_notes(vault_root: Path):
    for p in vault_root.rglob("*.md"):
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        yield p


def iter_scannable(vault_root: Path):
    for p in vault_root.rglob("*"):
        if p.is_dir():
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.suffix.lower() in SCAN_EXTS:
            yield p


def read_text(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


# ---------------------------------------------------------------------------
# CHECK 1 -- duplicate basenames
# ---------------------------------------------------------------------------

def find_duplicate_basenames(vault_root: Path, notes: list[Path]) -> list[dict]:
    groups: dict[str, list[Path]] = defaultdict(list)
    for p in notes:
        groups[p.name.lower()].append(p)

    results = []
    for name, paths in groups.items():
        if len(paths) < 2:
            continue

        rel_paths = [str(p.relative_to(vault_root)) for p in paths]

        if name in DUPLICATE_EXEMPT_NAMES:
            results.append({
                "name": paths[0].name, "paths": rel_paths, "identical": None,
                "excluded": True, "reason": "per-directory CLAUDE.md convention",
            })
            continue

        if any(seg in NAMESPACE_SEGMENTS for p in paths for seg in p.parts):
            results.append({
                "name": paths[0].name, "paths": rel_paths, "identical": None,
                "excluded": True,
                "reason": "one copy lives under _archive/_processed/_generated -- separate namespace",
            })
            continue

        texts = [read_text(p) for p in paths]
        stems = {p.stem.lower() for p in paths}
        is_stub_pair = any(
            len(t.encode("utf-8", "ignore")) < STUB_MAX_BYTES
            and WIKILINK_RE.search(t)
            and any(target.strip().lower() in stems for target in WIKILINK_RE.findall(t))
            for t in texts
        )
        if is_stub_pair:
            results.append({
                "name": paths[0].name, "paths": rel_paths, "identical": None,
                "excluded": True, "reason": "small pointer-stub note redirecting to the other copy",
            })
            continue

        hashes = {hashlib.sha256(t.encode("utf-8", "ignore")).hexdigest() for t in texts}
        identical = len(hashes) == 1
        results.append({
            "name": paths[0].name, "paths": rel_paths, "identical": identical,
            "excluded": False,
            "reason": "byte-identical fork -- drift risk" if identical
                      else "same name, different content -- name collision, not verified as a fork",
        })
    return results


# ---------------------------------------------------------------------------
# CHECK 2 -- broken wikilinks
# ---------------------------------------------------------------------------

def find_broken_wikilinks(vault_root: Path, notes: list[Path]) -> list[dict]:
    resolvable: set[str] = set()
    for p in notes:
        resolvable.add(p.name.lower())
        resolvable.add(p.stem.lower())

    results = []
    for p in notes:
        text = read_text(p)
        for lineno, line in enumerate(text.splitlines(), start=1):
            for target in WIKILINK_RE.findall(line):
                target = target.strip()
                if not target or target.lower() in resolvable:
                    continue
                looks_like_code = Path(target).suffix.lower() in CODE_EXTS
                results.append({
                    "file": str(p.relative_to(vault_root)),
                    "line": lineno,
                    "target": target,
                    "looks_like_tool_file": looks_like_code,
                })
    return results


# ---------------------------------------------------------------------------
# CHECK 3 -- secrets outside 03_APIS/.env
# ---------------------------------------------------------------------------

def scan_secrets(vault_root: Path) -> list[dict]:
    env_path = (vault_root / "03_APIS" / ".env").resolve()
    results = []
    for p in iter_scannable(vault_root):
        if p.resolve() == env_path:
            continue
        text = read_text(p)
        for lineno, line in enumerate(text.splitlines(), start=1):
            for label, pattern in SECRET_PATTERNS:
                if pattern.search(line):
                    results.append({
                        "file": str(p.relative_to(vault_root)),
                        "line": lineno,
                        "pattern": label,
                    })
    return results


# ---------------------------------------------------------------------------
# CHECK 4 -- cross-note numeric contradictions
# ---------------------------------------------------------------------------

def find_numeric_contradictions(vault_root: Path, notes: list[Path]) -> list[dict]:
    # key = (entity.lower(), unit.lower()) -> list of (value, file, line)
    claims: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for p in notes:
        text = read_text(p)
        for lineno, line in enumerate(text.splitlines(), start=1):
            for m in COUNT_CLAIM_RE.finditer(line):
                entity, number, unit = m.group(1), m.group(2), m.group(3)
                if entity.lower() in ENTITY_STOPWORDS:
                    continue
                key = (entity.lower(), unit.lower().rstrip("s"))
                claims[key].append({
                    "value": int(number.replace(",", "")),
                    "file": str(p.relative_to(vault_root)),
                    "line": lineno,
                })

    results = []
    for (entity, unit), occurrences in claims.items():
        distinct_values = {o["value"] for o in occurrences}
        distinct_files = {o["file"] for o in occurrences}
        if len(distinct_values) > 1 and len(distinct_files) > 1:
            results.append({
                "entity": entity, "unit": unit, "occurrences": occurrences,
            })
    return results


# ---------------------------------------------------------------------------
# REPORT
# ---------------------------------------------------------------------------

def build_report(vault_root: Path) -> dict:
    notes = list(iter_notes(vault_root))
    return {
        "vault": str(vault_root),
        "note_count": len(notes),
        "duplicate_basenames": find_duplicate_basenames(vault_root, notes),
        "broken_wikilinks": find_broken_wikilinks(vault_root, notes),
        "secrets": scan_secrets(vault_root),
        "numeric_contradictions": find_numeric_contradictions(vault_root, notes),
    }


def print_report(report: dict) -> None:
    print(f"Vault: {report['vault']}  ({report['note_count']} notes scanned)\n")

    print("=" * 70)
    print("1. DUPLICATE BASENAMES")
    print("=" * 70)
    dups = report["duplicate_basenames"]
    active = [d for d in dups if not d["excluded"]]
    excluded = [d for d in dups if d["excluded"]]
    if not dups:
        print("  none found")
    for d in active:
        tag = "IDENTICAL FORK" if d["identical"] else "NAME COLLISION"
        print(f"  [{tag}] {d['name']}")
        for p in d["paths"]:
            print(f"      {p}")
        print(f"      -> {d['reason']}")
    if excluded:
        print(f"\n  ({len(excluded)} excluded as known-legitimate: "
              + ", ".join(f"{d['name']} [{d['reason']}]" for d in excluded) + ")")
    print()

    print("=" * 70)
    print("2. BROKEN [[WIKILINKS]]")
    print("=" * 70)
    links = report["broken_wikilinks"]
    if not links:
        print("  none found")
    for l in links:
        flag = "  <- looks like a tool filename, not a note" if l["looks_like_tool_file"] else ""
        print(f"  {l['file']}:{l['line']}  [[{l['target']}]]{flag}")
    print()

    print("=" * 70)
    print("3. SECRETS OUTSIDE 03_APIS/.env")
    print("=" * 70)
    secrets = report["secrets"]
    if not secrets:
        print("  none found")
    for s in secrets:
        print(f"  {s['file']}:{s['line']}  possible {s['pattern']} (value not printed)")
    print()

    print("=" * 70)
    print("4. CROSS-NOTE NUMERIC CONTRADICTIONS")
    print("=" * 70)
    print("  NOTE: this detects DISAGREEMENT between notes, not INCORRECTNESS.")
    print("  It cannot tell you which number is right -- only that two notes")
    print("  assert different values for what looks like the same claim.")
    print("  Verify against the source (e.g. the live DB) before trusting either.\n")
    contras = report["numeric_contradictions"]
    if not contras:
        print("  none found")
    for c in contras:
        print(f"  '{c['entity']}' {c['unit']}s -- values disagree:")
        for o in c["occurrences"]:
            print(f"      {o['value']}  ({o['file']}:{o['line']})")
    print()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--vault", default=str(DEFAULT_VAULT), help="Vault root (default: this script's own vault)")
    parser.add_argument("--json", default=None, help="Also write machine-readable report to this path")
    args = parser.parse_args()

    vault_root = Path(args.vault).resolve()
    report = build_report(vault_root)
    print_report(report)

    if args.json:
        Path(args.json).write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(f"JSON report written to {args.json}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
