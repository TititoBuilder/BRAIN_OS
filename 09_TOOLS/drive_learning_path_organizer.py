"""
drive_learning_path_organizer.py — Organize Drive audio into Phase 1-6 folders
Creates subfolders under each Drive folder and moves files according to learning path.

Usage:
    python drive_learning_path_organizer.py --dry-run
    python drive_learning_path_organizer.py
"""

import argparse
import sys
import json
from pathlib import Path
from dotenv import load_dotenv

ENV_FILE     = Path(r"C:\Dev\Projects\soccer-content-generator\.env")
MANIFEST     = Path(r"C:\BRAIN_OS\02_PROJECTS\graphs\bdf_drive_manifest.json")
TOKEN_FILE   = Path(r"C:\Dev\Projects\soccer-content-generator\gdrive_token.json")

# ── Phase folder names ─────────────────────────────────────────────────────────
PHASES = {
    1: "Phase_01_Orientation",
    2: "Phase_02_Architecture",
    3: "Phase_03_BDF_Pipeline",
    4: "Phase_04_Agents_Workflows",
    5: "Phase_05_Programming_Fundamentals",
    6: "Phase_06_Session_Archive",
}

# ── File → Phase mapping ───────────────────────────────────────────────────────
# Key = manifest key, Value = phase number
FILE_PHASE_MAP = {
    # Phase 1 — Orientation
    "cristian_principles":        1,
    "project_directory":          1,
    "ai_engineering":             1,
    "creative_systems":           1,
    "guide_brain_os":             1,

    # Phase 2 — Architecture
    "trigger_architecture":              2,
    "session_protocol":                  2,
    "master_control":                    2,
    "mcp_registry":                      2,
    "tools_registry":                    2,
    "active_environments":               2,
    "knowledge_ingestion_protocol_v2":   2,
    "memory_index":                      2,
    "lancedb_vector_store":              2,
    "trigger_session_close":             2,
    "trigger_render_complete":           2,
    "trigger_bdf_queue_check":           2,

    # Phase 3 — BDF Pipeline
    "bdf_agent_pipeline":         3,
    "bdf_book_system":            3,
    "ch01_pipeline_architecture": 3,
    "ch02_predator_setup":        3,
    "ch03_tts_audio":             3,
    "ch04_lancedb_rag":           3,
    "ch05_telegram_twitter":      3,
    "ch06_obs_clips":             3,
    "ch07_dashboard_ui":          3,
    "ch08_methodology":           3,
    "ch09_roadmap":               3,
    "ch10_cartoon_animator":      3,
    "ch11_image_gallery":         3,
    "ch12_terminology_glossary":  3,
    "ch13_evolution_decisions":   3,
    "ch14_ideas_discoveries":     3,
    "ch15_learning_discoveries":  3,
    "ch16_cost_tracking":         3,
    "ch16_knowledge_enricher":    3,
    "ch17_clip_name_parser":      3,
    "ch18_competition_detection": 3,
    "ch19_export_pipeline":       3,
    "ch20_format_b_path_resolution": 3,
    "ch21_library_routing":       3,

    # Phase 4 — Agents & Workflows
    "read_along_app":             4,
    "cristianconstruction":       2,
    "content_orchestrator":       4,
    "data_orchestrator":          4,
    "video_orchestrator":         4,
    "bdf_memory_agent":           4,
    "resolve_editing_agent":      4,
    "davinci_resolve_mcp":        4,
    "resolve_mcp_server":         4,
    "bdf_video_production_flow":  4,
    "bdf_knowledge_build_flow":   4,
    "ch01_resolve_free_tier_nils":    4,
    "ch02_bridge_reload_discipline":  4,
    "ch03_windows_encoding_patterns": 4,
    "ch04_mcp_bridge_architecture":   4,
    "ch11_first_end_to_end_export":   4,
    "ch12_nuclear_clear_tool":        4,
    "ch13_deploy_discipline":         4,
    "ch14_async_export_pattern":      4,
    "ch15_clip_type_system":          4,


    # Phase 5 — Programming Fundamentals
    "programming_terminology_reference": 5,
    "guide_venv":                        5,
    "guide_lancedb":                     5,
    "guide_mcp_ecosystem":               5,
    "guide_obsidian_claude":             5,
    "claudeguide_mcp_setup":             5,
    "claudeguide_prompting_architecture":5,
    "claudeguide_skills_system":         5,
    "claudeguide_claude_md_standards":   5,
    "resolve_mcp_guide":                 5,

    # Phase 6 — Session Archive
    "20260331_1354": 6,
    "20260331_1435": 6,
    "20260331_1445": 6,
    "20260331_1457": 6,
    "20260331_1511": 6,
    "20260331_1517": 6,
    "20260331_1534": 6,
    "20260331_2029": 6,
    "20260401_0732": 6,
    "20260401_1115": 6,
    "20260401_1231": 6,
    "20260401_1322": 6,
    "20260401_1430": 6,
    "20260401_1440": 6,
    "20260401_1459": 6,
    "20260401_1513": 6,
    "20260401_1618": 6,
    "20260401_2239": 6,
    "20260402_0554": 6,
    "20260402_2003": 6,
    "20260404_1046": 6,
    "20260404_1211": 6,
    "20260404_1534": 6,
    "20260407_0827": 6,
    "20260414_1730": 6,
    "20260415_1149": 6,
    "20260426_2019": 6,
    "20260426_2043": 6,
    "20260514_1902": 6,
    "20260517_0725": 6,
    "BDF_Session_Summary_March18_2026": 6,
    "BDF_Session_Resume_March28_2026":  6,
}


def get_service():
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    creds = Credentials.from_authorized_user_file(str(TOKEN_FILE))
    return build("drive", "v3", credentials=creds)


def get_or_create_folder(service, name: str, parent_id: str) -> str:
    """Get existing folder ID or create it under parent."""
    res = service.files().list(
        q=f"name='{name}' and '{parent_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false",
        fields="files(id,name)"
    ).execute()
    if res["files"]:
        return res["files"][0]["id"]
    folder = service.files().create(
        body={"name": name, "mimeType": "application/vnd.google-apps.folder", "parents": [parent_id]},
        fields="id"
    ).execute()
    return folder["id"]


def move_file(service, file_id: str, new_parent_id: str, current_parent_id: str):
    service.files().update(
        fileId=file_id,
        addParents=new_parent_id,
        removeParents=current_parent_id,
        fields="id,parents"
    ).execute()


def match_phase(key: str) -> int:
    """Match a manifest key to a phase number."""
    # Direct match
    if key in FILE_PHASE_MAP:
        return FILE_PHASE_MAP[key]
    # Partial match
    for pattern, phase in FILE_PHASE_MAP.items():
        if pattern in key or key in pattern:
            return phase
    return 0  # unmatched


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    # Load Drive folder IDs from config
    config_path = Path(r"C:\BRAIN_OS\BRAIN_OS_CONFIG.json")
    config = json.loads(config_path.read_text(encoding="utf-8"))
    drive_folders = config.get("drive_folders", {})

    ROOT_FOLDERS = {
        "bdf_chapters":    drive_folders.get("bdf_chapters"),
        "brainos_chapters": drive_folders.get("brainos_chapters"),
        "bdf_sessions":    drive_folders.get("bdf_sessions"),
    }

    if args.dry_run:
        print("\nDRY RUN — files that would be moved:\n")
        for section in ["chapters", "brainos_chapters", "sessions"]:
            for key, meta in manifest.get(section, {}).items():
                phase = match_phase(key)
                if phase:
                    print(f"  Phase {phase} ← [{section}] {key}")
                else:
                    print(f"  [UNMAPPED] {key}")
        return

    service = get_service()

    # Create phase folders under each root Drive folder
    phase_folder_ids = {}
    for folder_key, root_id in ROOT_FOLDERS.items():
        if not root_id:
            print(f"[organizer] No Drive ID for {folder_key} — skipping")
            continue
        phase_folder_ids[folder_key] = {}
        for phase_num, phase_name in PHASES.items():
            fid = get_or_create_folder(service, phase_name, root_id)
            phase_folder_ids[folder_key][phase_num] = fid
            print(f"  ✅ {folder_key}/{phase_name}")

    # Move files
    section_map = {
        "chapters":         ("bdf_chapters",    "bdf_chapters"),
        "brainos_chapters": ("brainos_chapters", "brainos_chapters"),
        "sessions":         ("bdf_sessions",    "bdf_sessions"),
    }

    moved, skipped = 0, 0
    for section, (folder_key, root_key) in section_map.items():
        root_id = ROOT_FOLDERS.get(root_key)
        if not root_id:
            continue
        for key, meta in manifest.get(section, {}).items():
            phase = match_phase(key)
            if not phase:
                print(f"  [UNMAPPED] {key}")
                skipped += 1
                continue
            dest_folder_id = phase_folder_ids[folder_key][phase]
            move_file(service, meta["drive_id"], dest_folder_id, root_id)
            print(f"  → Phase {phase}: {meta['filename']}")
            moved += 1

    print(f"\n{'='*50}")
    print(f"  Moved:   {moved}")
    print(f"  Skipped: {skipped}")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
