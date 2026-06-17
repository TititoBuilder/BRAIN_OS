"""
graph_maintainer.py — Lightweight BDF graph maintenance runner.

Tasks (in order):
  0. Manifest Pre-Flight — check Drive manifest TTL; auto-sync if stale or token changed
  1. Hash Check          — compare live .py files against stored hashes, report changes
  2. Audio Parity        — cross-reference local _TTS.txt source files against Drive manifest
  3. Dependency          — ast-parse changed/new files, report import delta
  4. Brain-Audio         — verify brain_audio importable, then call graphify.py

Usage:
  python scripts/graph_maintainer.py
"""

from __future__ import annotations

import ast
import hashlib
import json
import subprocess
import sys
import argparse
from pathlib import Path
import re
from datetime import datetime, timezone

parser = argparse.ArgumentParser()
parser.add_argument(
    "--config",
    default="C:/BRAIN_OS/02_PROJECTS/graphs/soccer-content-generator.graphify.json"
)
args = parser.parse_args()

CONFIG_PATH = Path(args.config)
GRAPHIFY_PATH = Path(r"C:\BRAIN_OS\09_TOOLS\graphify.py")


# ---------------------------------------------------------------------------
# Shared helpers (duplicated from graphify.py to keep this file standalone)
# ---------------------------------------------------------------------------

def _md5(path: Path, length: int = 12) -> str:
    h = hashlib.md5(path.read_bytes(), usedforsecurity=False)
    return h.hexdigest()[:length]


def _should_skip(path: Path, patterns: list[str]) -> bool:
    s = str(path)
    return any(p in s for p in patterns)


def _parse_imports(path: Path) -> list[str]:
    try:
        tree = ast.parse(path.read_bytes())
    except SyntaxError:
        return []
    names: list[str] = []
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                names.append(node.module)
    return names


def _flat_imports(node: dict) -> set[str]:
    imp = node.get("imports", {})
    return set(imp.get("stdlib", []) + imp.get("internal", []) + imp.get("external", []))


# ---------------------------------------------------------------------------
# Task 1 — Hash Check
# ---------------------------------------------------------------------------

def task_hash_check(
    root: Path,
    skip_patterns: list[str],
    existing_nodes: dict,
) -> tuple[list[str], list[str], list[str], list[str]]:
    """Returns (changed, new_files, deleted, unchanged)."""
    live: dict[str, Path] = {}
    for f in root.rglob("*.py"):
        if not _should_skip(f, skip_patterns):
            rel = str(f.relative_to(root)).replace("\\", "/")
            live[rel] = f

    changed, new_files, unchanged = [], [], []
    for rel, f in sorted(live.items()):
        h = _md5(f)
        if rel not in existing_nodes:
            new_files.append(rel)
        elif existing_nodes[rel].get("hash") != h:
            changed.append(rel)
        else:
            unchanged.append(rel)

    deleted = [rel for rel in existing_nodes if rel not in live]

    print("=" * 60)
    print("Task 1 — Hash Check")
    print("=" * 60)
    print(f"  CHANGED:   {len(changed)}")
    print(f"  NEW:       {len(new_files)}")
    print(f"  DELETED:   {len(deleted)}")
    print(f"  UNCHANGED: {len(unchanged)}")
    if deleted:
        print("\n  Deleted files:")
        for rel in sorted(deleted):
            print(f"    - {rel}")

    return changed, new_files, deleted, unchanged


# ---------------------------------------------------------------------------
# Task 3 — Dependency Mapping
# ---------------------------------------------------------------------------

def task_dependency_mapping(
    root: Path,
    changed: list[str],
    new_files: list[str],
    existing_nodes: dict,
) -> None:
    affected = [("CHANGED", rel) for rel in changed] + [("NEW", rel) for rel in new_files]
    if not affected:
        return

    print()
    print("=" * 60)
    print("Task 3 — Dependency Mapping (changed / new files)")
    print("=" * 60)

    for label, rel in affected:
        f = root / rel.replace("/", "\\")
        new_imports = set(_parse_imports(f))
        old_imports = _flat_imports(existing_nodes.get(rel, {}))

        gained = new_imports - old_imports
        lost = old_imports - new_imports
        print(f"\n  [{label}] {rel}")
        if gained:
            print(f"    + gained: {', '.join(sorted(gained))}")
        if lost:
            print(f"    - lost:   {', '.join(sorted(lost))}")
        if not gained and not lost:
            print("    (content changed, imports unchanged)")


# ---------------------------------------------------------------------------
# Task 4 — Brain-Audio Sync + graphify update
# ---------------------------------------------------------------------------

def task_brain_audio_sync() -> None:
    print()
    print("=" * 60)
    print("Task 4 — Brain-Audio Sync")
    print("=" * 60)

    try:
        import brain_audio  # type: ignore[import]
        version = getattr(brain_audio, "__version__", "unknown")
        print(f"  brain_audio {version} — Shared System Dependency — OK")
    except ImportError:
        print("  WARNING: brain_audio not found in venv")
        print(r"  Run: pip install -e C:\Dev\shared\brain-audio")

    print()
    print(f"  Calling graphify.py --config {CONFIG_PATH} ...")
    result = subprocess.run(
        [sys.executable, str(GRAPHIFY_PATH), "--config", str(CONFIG_PATH)],
        capture_output=True,
        text=True,
    )
    if result.stdout:
        for line in result.stdout.rstrip().splitlines():
            print(f"  {line}")
    if result.stderr:
        preview = result.stderr.rstrip()[:600]
        print(f"  [stderr] {preview}")
    if result.returncode != 0:
        print(f"  [graph] graphify.py exited with code {result.returncode}")


# ---------------------------------------------------------------------------
# Parity check constants
# ---------------------------------------------------------------------------

_PROJECT_ROOT      = Path(r"C:\Dev\Projects\soccer-content-generator")
_MANIFEST_PATH     = Path(r"C:\BRAIN_OS\02_PROJECTS\graphs\bdf_drive_manifest.json")
_BRAIN_OS_CONFIG   = Path(r"C:\BRAIN_OS\BRAIN_OS_CONFIG.json")
_VENV_PYTHON       = _PROJECT_ROOT / ".venv" / "Scripts" / "python.exe"
_DRIVE_SYNC        = Path(__file__).parent / "drive_sync.py"


# ---------------------------------------------------------------------------
# Task 0 — Manifest Pre-Flight
# ---------------------------------------------------------------------------

def _fmt_age(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    return f"{h}h {m}m"


def task_preflight_check() -> bool:
    """Check manifest TTL against BRAIN_OS_CONFIG. Returns stale_flag."""
    print("=" * 60)
    print("Task 0 — Manifest Pre-Flight")
    print("=" * 60)

    if not _MANIFEST_PATH.exists():
        print("  [manifest] not found — run: python scripts/drive_sync.py")
        return False

    ttl_hours = 4  # safe default
    if _BRAIN_OS_CONFIG.exists():
        try:
            cfg = json.loads(_BRAIN_OS_CONFIG.read_text(encoding="utf-8"))
            ttl_hours = cfg["sync"]["SESSION_ANCHOR_TTL_HOURS"]
        except (KeyError, json.JSONDecodeError):
            pass

    manifest     = json.loads(_MANIFEST_PATH.read_text(encoding="utf-8"))
    last_synced  = manifest.get("last_synced", "")
    if not last_synced:
        print("  [manifest] missing last_synced field — treating as stale")
        return True

    python_exe = str(_VENV_PYTHON) if _VENV_PYTHON.exists() else sys.executable

    stored_token = manifest.get("start_page_token", "")
    if stored_token:
        token_result = subprocess.run(
            [python_exe, str(_DRIVE_SYNC), "--get-token"],
            capture_output=True, text=True, check=False,
        )
        if token_result.returncode == 0:
            current_token = token_result.stdout.strip()
            if current_token == stored_token:
                print("  [TOKEN VALID] Drive unchanged — skipping sync")
                return False
            print("  [TOKEN CHANGED] Drive has new content — syncing...")
            sync_result = subprocess.run(
                [python_exe, str(_DRIVE_SYNC)],
                capture_output=True, text=True, check=False,
            )
            if sync_result.returncode != 0:
                print("  [Offline] Token changed but sync failed. Proceeding with STALE manifest.")
                return True
            print("  [Sync OK] Manifest refreshed.")
            return False
        # subprocess failed (offline) — fall through to TTL logic

    synced_dt = datetime.fromisoformat(last_synced.replace("Z", "+00:00"))
    age_secs  = (datetime.now(timezone.utc) - synced_dt).total_seconds()
    age_str   = _fmt_age(age_secs)
    ttl_secs  = ttl_hours * 3600

    if age_secs < ttl_secs:
        print(f"  [TTL Valid] Using cached manifest (Age: {age_str})")
        return False

    print(f"  [TTL Expired] Manifest is {age_str} old. Triggering auto-sync...")
    result = subprocess.run(
        [python_exe, str(_DRIVE_SYNC)],
        capture_output=True, text=True, check=False,
    )
    if result.returncode != 0:
        print("  [Offline] TTL expired but sync failed. Proceeding with STALE manifest.")
        return True

    print("  [Sync OK] Manifest refreshed.")
    return False


# ---------------------------------------------------------------------------
# Task 2 — Audio Parity Check
# ---------------------------------------------------------------------------

KNOWN_ORPHANS = {
    "sessions": {
        "BDF_Session_Summary_March18_2026",
        "BDF_Session_Resume_March28_2026",
    }
}


def _chapter_source_key(filename: str) -> str | None:
    m = re.match(r"(ch\d+_.+?)_TTS\.txt$", filename)
    return m.group(1) if m else None


def _is_alternate_chapter(key: str) -> bool:
    """True when a local chapter key has more than 2 topic segments after chNN.

    ch01_pipeline_architecture  → 2 segments → CORE candidate (MISSING if not on Drive)
    ch01_resolve_free_tier_nils → 4 segments → ALTERNATE
    """
    return len(key.split("_")) - 1 > 2


def _session_source_key(filename: str) -> str | None:
    """
    _session_20260407_0827_combined_TTS.txt
        → 20260407_0827
    BDF_Session_Summary_March18_2026_TTS.txt
        → BDF_Session_Summary_March18_2026
    """
    m = re.match(r"_session_(\d{8}_\d{4})_combined_TTS\.txt$", filename)
    if m:
        return m.group(1)
    m = re.match(r"(BDF_Session_[A-Za-z]+_[A-Za-z]+\d+_\d{4})_TTS\.txt$", filename)
    return m.group(1) if m else None


def audio_parity_check() -> dict:
    """
    Cross-reference local _TTS.txt source files against the Drive manifest.

    Statuses per node:
        HEALTHY  — source and audio both exist; audio is newer than source
        STALE    — source was modified after the audio was generated
        MISSING  — source exists locally but no audio on Drive
        ORPHANED — audio exists on Drive but no local source file
    """
    if not _MANIFEST_PATH.exists():
        return {
            "error": (
                "manifest not found — run: "
                "python scripts/drive_sync.py"
            )
        }

    manifest       = json.loads(_MANIFEST_PATH.read_text(encoding="utf-8"))
    drive_chapters = manifest.get("chapters", {})
    drive_sessions = manifest.get("sessions", {})
    last_synced    = manifest.get("last_synced", "unknown")

    results: dict = {
        "chapters":         {"healthy": [], "stale": [], "missing": [], "alternates": [], "orphaned": []},
        "sessions":         {"healthy": [], "stale": [], "missing": [], "orphaned": []},
        "bdf_anchors":      {"catalogued": []},
        "bdf_combined":     {"catalogued": []},
        "brainos_chapters": {"catalogued": []},
        "brainos_sessions": {"catalogued": []},
        "last_synced": last_synced,
    }

    # ── Chapters ──────────────────────────────────────────────────────────────
    local_chapters: dict[str, Path] = {}
    for f in (_PROJECT_ROOT / "converted").glob("ch*_TTS.txt"):
        key = _chapter_source_key(f.name)
        if key:
            local_chapters[key] = f

    for key, source_path in sorted(local_chapters.items()):
        if key not in drive_chapters:
            if _is_alternate_chapter(key):
                results["chapters"]["alternates"].append(key)
            else:
                results["chapters"]["missing"].append(key)
        else:
            source_mtime = datetime.fromtimestamp(
                source_path.stat().st_mtime, tz=timezone.utc
            )
            audio_mtime = datetime.fromisoformat(
                drive_chapters[key]["modified_time"].replace("Z", "+00:00")
            )
            if source_mtime > audio_mtime:
                results["chapters"]["stale"].append(key)
            else:
                results["chapters"]["healthy"].append(key)

    for key in drive_chapters:
        if key not in local_chapters:
            results["chapters"]["orphaned"].append(key)

    # ── Sessions ──────────────────────────────────────────────────────────────
    local_sessions: dict[str, Path] = {}
    for f in (_PROJECT_ROOT / "converted").glob("_session_*_combined_TTS.txt"):
        key = _session_source_key(f.name)
        if key:
            local_sessions[key] = f

    for key, source_path in sorted(local_sessions.items()):
        if key not in drive_sessions:
            results["sessions"]["missing"].append(key)
        else:
            source_mtime = datetime.fromtimestamp(
                source_path.stat().st_mtime, tz=timezone.utc
            )
            audio_mtime = datetime.fromisoformat(
                drive_sessions[key]["modified_time"].replace("Z", "+00:00")
            )
            if source_mtime > audio_mtime:
                results["sessions"]["stale"].append(key)
            else:
                results["sessions"]["healthy"].append(key)

    for key in drive_sessions:
        if key not in local_sessions and key not in KNOWN_ORPHANS["sessions"]:
            results["sessions"]["orphaned"].append(key)

    # ── BDF Anchors ───────────────────────────────────────────────────────────
    for key in manifest.get("bdf_anchors", {}):
        results["bdf_anchors"]["catalogued"].append(key)

    # ── BDF Combined ──────────────────────────────────────────────────────────
    for key in manifest.get("bdf_combined", {}):
        results["bdf_combined"]["catalogued"].append(key)

    # ── BRAIN_OS Chapters ─────────────────────────────────────────────────────
    for key in manifest.get("brainos_chapters", {}):
        results["brainos_chapters"]["catalogued"].append(key)

    # ── BRAIN_OS Sessions ─────────────────────────────────────────────────────
    for key in manifest.get("brainos_sessions", {}):
        results["brainos_sessions"]["catalogued"].append(key)

    return results


def _print_parity_report(results: dict, stale_flag: bool = False) -> None:
    print("=" * 60)
    print("Task 2 — Audio Parity Check")
    print("=" * 60)

    if "error" in results:
        print(f"  [!] {results['error']}")
        return

    for category in ("chapters", "sessions", "bdf_anchors", "bdf_combined", "brainos_chapters", "brainos_sessions"):
        r = results.get(category)
        if r is None:
            continue

        total = sum(len(v) for v in r.values())
        if total == 0:
            continue

        label = category.upper()
        print(f"  {label}")

        if "catalogued" in r:
            # Drive-only category: no local source to compare against
            print(f"  {'CATALOGUED:':10} {len(r['catalogued']):>3}")
            print()
            continue

        print(f"  {'HEALTHY:':10} {len(r['healthy']):>3}")

        if r["stale"]:
            items = ", ".join(r["stale"])
            print(f"  {'STALE:':10} {len(r['stale']):>3}  ← {items}")
        else:
            print(f"  {'STALE:':10} {len(r['stale']):>3}")

        if r["missing"]:
            items = ", ".join(r["missing"])
            print(f"  {'MISSING:':10} {len(r['missing']):>3}  ← {items}")
        else:
            print(f"  {'MISSING:':10} {len(r['missing']):>3}")

        if "alternates" in r:
            if r["alternates"]:
                items = ", ".join(r["alternates"])
                print(f"  {'ALTERNATES:':10} {len(r['alternates']):>3}  ← {items}")
            else:
                print(f"  {'ALTERNATES:':10} {len(r['alternates']):>3}")

        if r["orphaned"]:
            items = ", ".join(r["orphaned"])
            print(f"  {'ORPHANED:':10} {len(r['orphaned']):>3}  ← {items}")
        else:
            print(f"  {'ORPHANED:':10} {len(r['orphaned']):>3}")

        print()

    synced = results["last_synced"][:19].replace("T", " ")
    stale_suffix = "  [STALE DATA]" if stale_flag else ""
    print(f"[manifest] last synced: {synced} UTC{stale_suffix}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    if not CONFIG_PATH.exists():
        sys.exit(f"[graph] Config not found: {CONFIG_PATH}")

    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    root = Path(config["root"])
    skip_patterns: list[str] = config.get("skip_patterns", [])
    graph_output = Path(config["graph_output"])

    existing_nodes: dict = {}
    if graph_output.exists():
        existing_graph = json.loads(graph_output.read_text(encoding="utf-8"))
        existing_nodes = existing_graph.get("nodes", {})

    # Task 0
    stale_flag = task_preflight_check()

    # Task 1
    changed, new_files, deleted, unchanged = task_hash_check(root, skip_patterns, existing_nodes)

    if not changed and not new_files and not deleted:
        print("\n[graph] up to date")
        # Note: intentional fall-through — audio parity always runs

    # ── Task 2 — Audio Parity Check ──────────────────────────────────────
    parity = audio_parity_check()
    _print_parity_report(parity, stale_flag)

    # Short-circuit for code tasks (dependency mapping + graphify)
    if not changed and not new_files and not deleted:
        return

    # Task 3
    task_dependency_mapping(root, changed, new_files, existing_nodes)

    # Task 4
    task_brain_audio_sync()


if __name__ == "__main__":
    main()
