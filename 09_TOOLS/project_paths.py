r"""
project_paths.py — single source for resolving project roots from the manifest.
Reads C:\BRAIN_OS\02_PROJECTS\graphs\projects.manifest.json (the one declared
source of truth for project roots) and resolves a project's root or a script
path within it. Replaces hardcoded absolute paths in 09_TOOLS callers.
"""
import json
from pathlib import Path

MANIFEST = Path(r"C:\BRAIN_OS\02_PROJECTS\graphs\projects.manifest.json")

def _load():
    return json.loads(MANIFEST.read_text(encoding="utf-8"))

def project_root(name: str) -> Path:
    """Return the root Path for a project by its manifest 'name'. Raises if absent."""
    for p in _load().get("projects", []):
        if p.get("name", "").lower() == name.lower():
            return Path(p["root"])
    raise KeyError(f"project '{name}' not found in {MANIFEST}")

def project_script(name: str, *parts: str) -> Path:
    """Return root(name) joined with sub-path parts, e.g. project_script('BDF','scripts','graph_maintainer.py')."""
    return project_root(name).joinpath(*parts)


def project_venv_python(name: str) -> Path:
    """Return the venv python.exe Path for a project, or None if venv is null."""
    for proj in _load().get("projects", []):
        if proj.get("name", "").lower() == name.lower():
            v = proj.get("venv")
            return Path(v) / "Scripts" / "python.exe" if v else None
    raise KeyError(f"project '{name}' not found")

if __name__ == "__main__":
    # self-test: prove resolution works before any caller depends on this
    print("BDF root        :", project_root("BDF"))
    print("graph_maintainer:", project_script("BDF", "scripts", "graph_maintainer.py"))
    print("tts_local       :", project_script("BDF", "tts_local.py"))
    gm = project_script("BDF", "scripts", "graph_maintainer.py")
    tts = project_script("BDF", "tts_local.py")
    print("graph_maintainer exists:", gm.exists())
    print("tts_local exists       :", tts.exists())