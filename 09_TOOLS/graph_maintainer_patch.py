"""
graph_maintainer.py — PATCH: Task 2 Audio Parity Check
=======================================================

INTEGRATION INSTRUCTIONS
─────────────────────────
Apply three changes to scripts/graph_maintainer.py:

CHANGE 1 — Add imports at the top of the file (after existing imports):
    import re
    from datetime import datetime, timezone

CHANGE 2 — Add the two functions below (paste anywhere before main()).

CHANGE 3 — Modify the short-circuit and main task sequence.
    Find the early-exit block that currently looks like:

        if changed == 0 and new == 0 and deleted == 0:
            print("[graph] up to date")
            return   # ← REMOVE THIS LINE

    Replace with:

        if changed == 0 and new == 0 and deleted == 0:
            print("[graph] up to date")
            # Note: intentional fall-through — audio parity always runs

    Then after that block (still in main), add:

        # ── Task 2 — Audio Parity Check ──────────────────────────────────────
        parity = audio_parity_check()
        _print_parity_report(parity)

        # Short-circuit for code tasks (dependency mapping + graphify)
        if changed == 0 and new == 0 and deleted == 0:
            return

    This ensures:
    - Audio Parity always runs
    - Dependency Mapping and Graphify only run when code changed
"""

import json
import re
from datetime import datetime, timezone
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────

_PROJECT_ROOT   = Path(r"C:\Dev\Projects\soccer-content-generator")
_MANIFEST_PATH  = Path(r"C:\BRAIN_OS\02_PROJECTS\graphs\bdf_drive_manifest.json")


# ── Key extraction ────────────────────────────────────────────────────────────

def _chapter_source_key(filename: str) -> str | None:
    """
    ch01_pipeline_architecture_TTS.txt
        → ch01_pipeline_architecture
    """
    m = re.match(r"(ch\d+_.+?)_TTS\.txt$", filename)
    return m.group(1) if m else None


def _session_source_key(filename: str) -> str | None:
    """
    _session_20260407_0827_combined_TTS.txt
        → 20260407_0827
    """
    m = re.match(r"_session_(\d{8}_\d{4})_combined_TTS\.txt$", filename)
    return m.group(1) if m else None


# ── Parity check ──────────────────────────────────────────────────────────────

def audio_parity_check() -> dict:
    """
    Cross-reference local _TTS.txt source files against the Drive manifest.

    Statuses per node:
        HEALTHY  — source and audio both exist; audio is newer than source
        STALE    — source was modified after the audio was generated
        MISSING  — source exists locally but no audio on Drive
        ORPHANED — audio exists on Drive but no local source file

    Returns a dict with keys: chapters, sessions, last_synced, error (if any).
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
        "chapters":   {"healthy": [], "stale": [], "missing": [], "orphaned": []},
        "sessions":   {"healthy": [], "stale": [], "missing": [], "orphaned": []},
        "last_synced": last_synced,
    }

    # ── Chapters ──────────────────────────────────────────────────────────────
    local_chapters: dict[str, Path] = {}
    for f in _PROJECT_ROOT.glob("ch*_TTS.txt"):
        key = _chapter_source_key(f.name)
        if key:
            local_chapters[key] = f

    for key, source_path in sorted(local_chapters.items()):
        if key not in drive_chapters:
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
    for f in _PROJECT_ROOT.glob("_session_*_combined_TTS.txt"):
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
        if key not in local_sessions:
            results["sessions"]["orphaned"].append(key)

    return results


# ── Reporter ──────────────────────────────────────────────────────────────────

def _print_parity_report(results: dict) -> None:
    """Print the Task 2 Audio Parity section to stdout."""
    print("=" * 60)
    print("Task 2 — Audio Parity Check")
    print("=" * 60)

    if "error" in results:
        print(f"  [!] {results['error']}")
        return

    for category in ("chapters", "sessions"):
        r = results[category]

        # Skip category entirely if no nodes on either side
        total = sum(len(v) for v in r.values())
        if total == 0:
            continue

        label = category.upper()
        print(f"  {label}")
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

        if r["orphaned"]:
            items = ", ".join(r["orphaned"])
            print(f"  {'ORPHANED:':10} {len(r['orphaned']):>3}  ← {items}")
        else:
            print(f"  {'ORPHANED:':10} {len(r['orphaned']):>3}")

        print()

    synced = results["last_synced"][:19].replace("T", " ")
    print(f"[manifest] last synced: {synced} UTC")
