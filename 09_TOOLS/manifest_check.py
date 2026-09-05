"""
category: System Utilities
manifest_check.py — Validate projects.manifest.json against disk.

Read-only. The manifest is becoming the single source of project identity,
which makes a typo in it able to break every consumer. This is the check
that makes that safe.

Exit codes follow the 09_TOOLS contract:
    0  every project valid
    1  at least one ERROR - a declared path does not exist, or a field is malformed
    2  the manifest itself could not be read or parsed

WARN does not change the exit code. A missing context_md is a gap to decide
on, not a failure.

Usage:
    python C:/BRAIN_OS/09_TOOLS/manifest_check.py
    python C:/BRAIN_OS/09_TOOLS/manifest_check.py --quiet   (errors only)
"""

import argparse
import json
import sys
from pathlib import Path

MANIFEST = Path(r"C:\BRAIN_OS\02_PROJECTS\graphs\projects.manifest.json")

BUCKETS = {"Content", "Business", "Operations", "Personal"}
STATUSES = {"active", "parked", "archived"}


def check() -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warns: list[str] = []

    try:
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"ERROR: cannot read {MANIFEST}: {e}")
        raise SystemExit(2)

    projects = data.get("projects")
    if not isinstance(projects, list):
        print("ERROR: 'projects' is not a list")
        raise SystemExit(2)

    seen_names: dict[str, int] = {}
    seen_aliases: dict[str, str] = {}

    for i, p in enumerate(projects):
        name = p.get("name")
        tag = name or f"entry[{i}]"

        if not name:
            errors.append(f"{tag}: no name")
        elif name in seen_names:
            errors.append(f"{name}: duplicate name, also at entry[{seen_names[name]}]")
        else:
            seen_names[name] = i

        for a in p.get("aliases", []):
            if a in seen_aliases:
                errors.append(f"{tag}: alias '{a}' already used by {seen_aliases[a]}")
            else:
                seen_aliases[a] = tag
            if a in seen_names:
                errors.append(f"{tag}: alias '{a}' collides with a project name")

        root = p.get("root")
        if not root:
            errors.append(f"{tag}: no root")
        elif not Path(root).is_dir():
            errors.append(f"{tag}: root does not exist -> {root}")

        venv = p.get("venv")
        if venv is not None and not Path(venv).exists():
            errors.append(f"{tag}: venv declared but missing -> {venv}")

        ctx = p.get("context_md")
        if ctx is None:
            warns.append(f"{tag}: no context_md declared")
        elif not Path(ctx).is_file():
            warns.append(f"{tag}: context_md declared but missing -> {ctx}")

        cmd = p.get("claude_md")
        if cmd is None:
            warns.append(f"{tag}: no claude_md declared")
        elif not Path(cmd).is_file():
            warns.append(f"{tag}: claude_md declared but missing -> {cmd}")

        b = p.get("bucket")
        if b is None:
            warns.append(f"{tag}: no bucket")
        elif b not in BUCKETS:
            errors.append(f"{tag}: bucket '{b}' not one of {sorted(BUCKETS)}")

        s = p.get("status")
        if s is None:
            warns.append(f"{tag}: no status")
        elif s not in STATUSES:
            errors.append(f"{tag}: status '{s}' not one of {sorted(STATUSES)}")

    return errors, warns


def main() -> None:
    ap = argparse.ArgumentParser(description="Validate projects.manifest.json against disk")
    ap.add_argument("--quiet", action="store_true", help="Print errors only")
    args = ap.parse_args()

    errors, warns = check()

    if warns and not args.quiet:
        print(f"-- WARN ({len(warns)}) " + "-" * 40)
        for w in warns:
            print(f"  {w}")
    if errors:
        print(f"-- ERROR ({len(errors)}) " + "-" * 39)
        for e in errors:
            print(f"  {e}")
        print(f"\n{len(errors)} error(s), {len(warns)} warning(s).")
        raise SystemExit(1)

    print(f"\nOK. 0 errors, {len(warns)} warning(s).")


if __name__ == "__main__":
    main()
