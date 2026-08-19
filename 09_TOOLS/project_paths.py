r"""
category: System Utilities
project_paths.py — single source for resolving project attributes from the manifest.
Reads C:\BRAIN_OS\02_PROJECTS\graphs\projects.manifest.json (the one declared
source of truth) and resolves a project's root, venv python, context file, or a
script path within it. Matching is case-insensitive across 'name' and 'aliases',
so "BDF" and "soccer-content-generator" resolve to the same entry.

NOTE: this module is a LIBRARY, imported by other 09_TOOLS scripts. It is a
deliberate exception to the subprocess-only rule — a path resolver must not be
shelled out to. Run directly for a self-test.
"""
import json
import sys
from pathlib import Path

MANIFEST = Path(r"C:\BRAIN_OS\02_PROJECTS\graphs\projects.manifest.json")


def _load():
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def _find(name: str) -> dict:
    """Return the manifest entry matching name or any alias, case-insensitively."""
    key = name.strip().lower()
    for p in _load().get("projects", []):
        if p.get("name", "").lower() == key:
            return p
        if any(a.lower() == key for a in p.get("aliases", [])):
            return p
    known = ", ".join(p.get("name", "?") for p in _load().get("projects", []))
    raise KeyError(f"project {name!r} not found in {MANIFEST}. Known: {known}")


def project_root(name: str) -> Path:
    """Return the root Path for a project. Raises KeyError if absent."""
    return Path(_find(name)["root"])


def project_script(name: str, *parts: str) -> Path:
    """Return root(name) joined with sub-path parts."""
    return project_root(name).joinpath(*parts)


def project_venv_python(name: str) -> Path:
    """Return the venv python.exe Path, or None if the project has no venv."""
    v = _find(name).get("venv")
    return Path(v) / "Scripts" / "python.exe" if v else None


def project_context(name: str) -> Path:
    """Return the declared context_md Path. Raises KeyError if undeclared."""
    entry = _find(name)
    ctx = entry.get("context_md")
    if not ctx:
        raise KeyError(f"project {entry['name']!r} has no context_md declared")
    return Path(ctx)


def project_names() -> list:
    """Return every canonical project name, for CLI help text."""
    return [p["name"] for p in _load().get("projects", [])]


if __name__ == "__main__":
    print(f"manifest: {MANIFEST}")
    print(f"exists  : {MANIFEST.exists()}\n")
    if not MANIFEST.exists():
        sys.exit(1)

    bad = 0
    for entry in _load().get("projects", []):
        n = entry["name"]
        root = project_root(n)
        ctx = project_context(n)
        venv = project_venv_python(n)
        rk = "OK" if root.exists() else "MISS"
        ck = "OK" if ctx.exists() else "MISS"
        vk = "OK" if venv is None or venv.exists() else "MISS"
        if "MISS" in (rk, ck, vk):
            bad += 1
        print(f"{n:<24} root={rk:<5} ctx={ck:<5} venv={vk}")

    print()
    for alias in ("bdf", "soccer-content-generator", "BDF", "vault", "cc"):
        try:
            print(f"  {alias:<26} -> {_find(alias)['name']}")
        except KeyError as exc:
            print(f"  {alias:<26} -> ERROR {exc}")
            bad += 1

    print(f"\n{bad} problem(s)")
    sys.exit(1 if bad else 0)
