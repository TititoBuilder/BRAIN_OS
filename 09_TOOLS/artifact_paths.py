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

    orphans = unwritten()
    print(f"\nNo writer, no reader ({len(orphans)}):")
    for a in orphans:
        print(f"  {a['name']:<22} {a['path']}")

    print(f"\n{len(arts)} artifacts, {bad} problem(s)")
    sys.exit(1 if bad else 0)
