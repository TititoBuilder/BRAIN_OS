"""
borrowed_audio_worklist.py — Borrowed Audio Re-voice Worklist Generator
========================================================================
Identifies drive_index.json entries with path-format values (not id:)
and looks them up in the Drive manifest to find their drive_id.

Outputs a worklist showing what needs to be re-voiced with its own .md.

Usage:
    python C:\\BRAIN_OS\\09_TOOLS\\borrowed_audio_worklist.py
"""

import json
from pathlib import Path

DRIVE_INDEX = Path(r"C:\BRAIN_OS\09_TOOLS\drive_index.json")
MANIFEST    = Path(r"C:\BRAIN_OS\02_PROJECTS\graphs\bdf_drive_manifest.json")
OUTPUT_FILE = Path(r"C:\BRAIN_OS\09_TOOLS\borrowed_audio_worklist.txt")

MANIFEST_CATEGORIES = (
    "chapters", "sessions", "bdf_anchors", "bdf_combined",
    "brainos_chapters", "brainos_sessions",
)


def _build_filename_index(manifest: dict) -> dict:
    """Build a flat filename → {drive_id, category, manifest_key} lookup across all categories."""
    index = {}
    for category in MANIFEST_CATEGORIES:
        for key, entry in manifest.get(category, {}).items():
            filename = entry.get("filename", "")
            if filename:
                index[filename] = {
                    "drive_id":     entry["drive_id"],
                    "category":     category,
                    "manifest_key": key,
                }
    return index


def main() -> None:
    if not DRIVE_INDEX.exists():
        print(f"ERROR: drive_index.json not found at {DRIVE_INDEX}")
        return

    index_data = json.loads(DRIVE_INDEX.read_text(encoding="utf-8"))
    index = index_data.get("index", {})

    path_format = {k: v for k, v in index.items() if not str(v).startswith("id:")}

    print(f"Total entries in drive_index.json : {len(index)}")
    print(f"Path-format entries (not id:)     : {len(path_format)}")

    if not path_format:
        print("Nothing to do — all entries use id: format.")
        return

    manifest_lookup = {}
    if MANIFEST.exists():
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        manifest_lookup = _build_filename_index(manifest)
    else:
        print(f"WARNING: manifest not found at {MANIFEST} — drive_id lookup will show UNMATCHED")

    matched = 0
    unmatched = 0
    col_key  = 40
    col_val  = 65
    col_id   = 36

    lines = [
        "# Borrowed Audio Re-voice Worklist",
        f"# Total path-format entries: {len(path_format)}",
        "#",
        f"# {'KEY':<{col_key}} | {'CURRENT VALUE':<{col_val}} | {'MANIFEST DRIVE_ID':<{col_id}} | ACTION",
        "# " + "-" * (col_key + col_val + col_id + 12),
    ]

    for key, value in sorted(path_format.items()):
        filename = Path(str(value)).name
        match = manifest_lookup.get(filename)

        if match:
            drive_id = match["drive_id"]
            action   = f"Re-voice {key}.md → publish via populate_staging.py"
            matched += 1
        else:
            drive_id = "UNMATCHED"
            action   = "Manual lookup needed — filename not in manifest"
            unmatched += 1

        lines.append(
            f"  {key:<{col_key}} | {str(value):<{col_val}} | {drive_id:<{col_id}} | {action}"
        )

    lines += [
        "",
        f"# SUMMARY: {matched} matched in manifest / {unmatched} unmatched",
        f"# Next step: re-voice each topic from its own .md, then run populate_staging.py.",
        f"# The id: format is written automatically once re-voiced and uploaded.",
    ]

    OUTPUT_FILE.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print(f"\nWorklist written → {OUTPUT_FILE}")
    print(f"  Matched in manifest : {matched}")
    print(f"  Unmatched           : {unmatched}")
    print()
    print("Next step: re-voice each topic from its own .md, then run populate_staging.py.")


if __name__ == "__main__":
    main()
