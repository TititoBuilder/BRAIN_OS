r"""
category: System Utilities
artifact_paths.py — single source for resolving vault artifacts by name or alias.

Reads C:\BRAIN_OS\02_PROJECTS\graphs\artifacts.manifest.json, the declared source
of truth for where each artifact lives, who writes it, and what it is for.
Matching is case-insensitive across 'name' and 'aliases', so "directions",
"lesson queue", and "LESSON_QUEUE" all resolve to the same entry.

An ambiguous ask raises with the candidates listed rather than guessing:
    artifact_path("queue")  ->  AmbiguousArtifact naming all three queues.

NOTE: this module is a LIBRARY, imported by other 09_TOOLS scripts. Same
deliberate exception to the subprocess-only rule as project_paths.py.
Run directly for a self-test.
"""
import json
import sys
from pathlib import Path

MANIFEST = Path(r"C:\BRAIN_OS\02_PROJECTS\graphs\artifacts.manifest.json")


class AmbiguousArtifact(KeyError):
    """Raised when a name matches a kind rather than one artifact."""


def _load():
    d = json.loads(MANIFEST.read_text(encoding="utf-8"))
    return Path(d["root"]), d["artifacts"]


def _find(name: str) -> dict:
    key = name.strip().lower()
    _, arts = _load()

    # Kind check FIRST: a term naming a kind with 2+ members is ambiguous even
    # when it also happens to be one artifact's name ("queue" is both).
    kin = [a for a in arts if a["kind"].lower() == key]
    if len(kin) > 1:
        opts = "\n".join(f"  {a['name']:<20} {a['path']:<45} {a['purpose']}" for a in kin)
        raise AmbiguousArtifact(
            f"{name!r} is a KIND, not one artifact. {len(kin)} match:\n{opts}\n"
            f"Ask for one by name."
        )

    for a in arts:
        if a["name"].lower() == key or any(x.lower() == key for x in a["aliases"]):
            return a

    if kin:
        return kin[0]

    known = ", ".join(a["name"] for a in arts)
    raise KeyError(f"artifact {name!r} not found. Known: {known}")


def artifact(name: str) -> dict:
    """Full manifest entry: path, kind, writer, readers, purpose."""
    return _find(name)


def artifact_path(name: str) -> Path:
    """Absolute Path to the artifact."""
    root, _ = _load()
    return root / _find(name)["path"]


def artifacts_of_kind(kind: str) -> list:
    """Every artifact of a kind: queue, log, index, doctrine, config."""
    _, arts = _load()
    return [a for a in arts if a["kind"].lower() == kind.strip().lower()]


def artifact_names() -> list:
    _, arts = _load()
    return [a["name"] for a in arts]


# Dashboard and doctrine directories. Auto-ingest writes knowledge nodes,
# which live in 01_DOMAINS and 02_PROJECTS. It has no business in these
# four. Enumerating protected files never converged - three consecutive
# dry runs each surfaced a new unlisted target - so the rule is by
# directory. A manifest entry with protected false still wins, which is
# how Cristian_Principles stays writable inside 07_SYSTEM.
PROTECTED_DIRS = ("00_DASHBOARD/", "07_SYSTEM/", "00_NAV/", "05_MEMORY/",
                  "02_PROJECTS/graphs/")


def directory_protection_note(path: str) -> str:
    """Why a path is protected by directory. Empty string if it is not."""
    _, arts = _load()
    for a in arts:
        if a["path"] == path and a.get("protected") is False:
            return ""
    for d in PROTECTED_DIRS:
        if path.startswith(d):
            return f"{d.rstrip('/')} is a dashboard or doctrine directory"
    return ""


def protected_paths() -> set:
    """Relative paths that auto-ingest tools must never write to."""
    _, arts = _load()
    return {a["path"] for a in arts if a.get("protected", False)}


def protection_note(path: str) -> str:
    """Why a path is protected. Empty string if it is not."""
    _, arts = _load()
    for a in arts:
        if a["path"] == path and a.get("protected", False):
            return f"{a['name']} (writer: {a['writer']}) - {a['purpose']}"
    return ""


def unwritten() -> list:
    """Artifacts with no writer - the drift risks."""
    _, arts = _load()
    return [a for a in arts if a["writer"] == "manual" and not a["readers"]]


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    root, arts = _load()
    print(f"manifest: {MANIFEST}\nroot    : {root}\n")

    bad = 0
    print(f"{'ARTIFACT':<22} {'KIND':<10} {'ON DISK':<8} WRITER")
    print("-" * 78)
    for a in arts:
        ok = (root / a["path"]).exists()
        if not ok:
            bad += 1
        print(f"{a['name']:<22} {a['kind']:<10} {'OK' if ok else 'MISS':<8} {a['writer']}")

    print("\nAlias resolution:")
    for q in ("directions", "lesson queue", "todo", "flags", "nav", "principles"):
        try:
            print(f"  {q:<16} -> {_find(q)['name']}")
        except KeyError as exc:
            print(f"  {q:<16} -> ERROR {exc}")
            bad += 1

    print("\nAmbiguity check:")
    try:
        _find("queue")
        print("  ERROR: 'queue' resolved to one artifact - should be ambiguous")
        bad += 1
    except AmbiguousArtifact:
        print("  'queue' correctly raised AmbiguousArtifact")

    print("\nProtection check:")
    prot = protected_paths()
    print(f"  {len(prot)} protected, {len(arts) - len(prot)} open")
    if "FLAGS.txt" not in prot:
        print("  ERROR: FLAGS.txt must be protected - one writer, manual only")
        bad += 1
    else:
        print("  FLAGS.txt correctly protected")
    if "07_SYSTEM/Cristian_Principles.md" in prot:
        print("  ERROR: Cristian_Principles must stay open - ingest targets it")
        bad += 1
    else:
        print("  Cristian_Principles correctly open")

    print("\nReference check:")
    tools = MANIFEST.parent.parent.parent / "09_TOOLS"
    stale = []
    for a in arts:
        for r in a["readers"]:
            if not (tools / r).exists():
                stale.append(f"{a['name']} reader {r}")
        w = a["writer"]
        if w != "manual" and "/" not in w and not (tools / w).exists():
            stale.append(f"{a['name']} writer {w}")
    if stale:
        for line in stale:
            print(f"  ERROR: {line} is not a file in 09_TOOLS")
            bad += 1
    else:
        print(f"  all bare readers and writers resolve in 09_TOOLS")

    orphans = unwritten()
    print(f"\nNo writer, no reader ({len(orphans)}):")
    for a in orphans:
        print(f"  {a['name']:<22} {a['path']}")

    print(f"\n{len(arts)} artifacts, {bad} problem(s)")
    sys.exit(1 if bad else 0)
