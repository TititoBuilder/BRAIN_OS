"""
learning_path_builder.py — BRAIN OS Learning Path Sequencer
Organizes all audio files into a Phase 1-6 sequential learning path.
Creates a manifest JSON + Drive folder structure plan.

Usage:
    python learning_path_builder.py --dry-run
    python learning_path_builder.py --export manifest
    python learning_path_builder.py --export m3u
"""

import argparse
import json
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────────
PROJECT_ROOT  = Path(r"C:\Dev\Projects\soccer-content-generator")
CONVERTED_DIR = PROJECT_ROOT / "converted"
VAULT_AUDIO   = CONVERTED_DIR / "vault_audio"
OUTPUT_DIR    = PROJECT_ROOT / "converted"

# ── Learning Path Definition ───────────────────────────────────────────────────
LEARNING_PATH = [
    {
        "phase": 1,
        "title": "Orientation — Who Am I, What Did I Build",
        "description": "Start here. Understand Cristian's system, principles, and projects before anything else.",
        "tracks": [
            # Vault audio — system overview
            {"file": "vault_audio/cristian_principles_audio.mp3",    "title": "Cristian's Principles"},
            {"file": "vault_audio/project_directory_audio.mp3",       "title": "Project Directory"},
            {"file": "vault_audio/ai_engineering_audio.mp3",          "title": "AI Engineering Domain"},
            {"file": "vault_audio/creative_systems_audio.mp3",        "title": "Creative Systems Domain"},
            # BRAINOS guides
            {"file": "brainos_chapters/guide_brain_os_audio.mp3",  "title": "BRAIN OS Guide"},
        ]
    },
    {
        "phase": 2,
        "title": "Architecture — How Everything Connects",
        "description": "The wiring of the system. Triggers, agents, MCP, session protocol.",
        "tracks": [
            {"file": "vault_audio/trigger_architecture_audio.mp3",           "title": "Trigger Architecture"},
            {"file": "vault_audio/session_protocol_audio.mp3",               "title": "Session Protocol"},
            {"file": "vault_audio/master_control_audio.mp3",                 "title": "Master Control"},
            {"file": "vault_audio/mcp_registry_audio.mp3",                   "title": "MCP Registry"},
            {"file": "vault_audio/tools_registry_audio.mp3",                 "title": "Tools Registry"},
            {"file": "vault_audio/active_environments_audio.mp3",            "title": "Active Environments"},
            {"file": "vault_audio/knowledge_ingestion_protocol_v2_audio.mp3","title": "Knowledge Ingestion Protocol"},
            {"file": "vault_audio/memory_index_audio.mp3",                   "title": "Memory Index"},
            {"file": "vault_audio/lancedb_vector_store_audio.mp3",           "title": "LanceDB Vector Store"},
            # Trigger deep dives
            {"file": "vault_audio/trigger_session_close_audio.mp3",          "title": "Trigger: Session Close"},
            {"file": "vault_audio/trigger_render_complete_audio.mp3",        "title": "Trigger: Render Complete"},
            {"file": "vault_audio/trigger_bdf_queue_check_audio.mp3",        "title": "Trigger: BDF Queue Check"},
        ]
    },
    {
        "phase": 3,
        "title": "BDF Pipeline — Deep Dive",
        "description": "The soccer content pipeline from clip to Twitter post.",
        "tracks": [
            # Project overview first
            {"file": "vault_audio/bdf_agent_pipeline_audio.mp3",     "title": "BDF Agent Pipeline"},
            {"file": "vault_audio/bdf_book_system_audio.mp3",        "title": "BDF Book System"},
            # Chapters in logical order
            {"file": "ch01_pipeline_architecture_anchor.mp3",        "title": "ch01 Pipeline Architecture ★"},
            {"file": "ch02_predator_setup_anchor.mp3",               "title": "ch02 Predator Setup ★"},
            {"file": "ch03_tts_audio_anchor.mp3",                    "title": "ch03 TTS Audio ★"},
            {"file": "ch04_lancedb_rag_anchor.mp3",                  "title": "ch04 LanceDB RAG ★"},
            {"file": "ch05_telegram_twitter_anchor.mp3",             "title": "ch05 Telegram Twitter ★"},
            {"file": "ch06_obs_clips_anchor.mp3",                    "title": "ch06 OBS Clips ★"},
            {"file": "ch07_dashboard_ui_anchor.mp3",                 "title": "ch07 Dashboard UI ★"},
            {"file": "ch08_methodology_anchor.mp3",                  "title": "ch08 Methodology ★"},
            {"file": "ch09_roadmap_anchor.mp3",                      "title": "ch09 Roadmap ★"},
            {"file": "ch10_cartoon_animator_anchor.mp3",             "title": "ch10 Cartoon Animator ★"},
            {"file": "ch11_image_gallery_anchor.mp3",                "title": "ch11 Image Gallery ★"},
            {"file": "ch12_terminology_glossary_anchor.mp3",         "title": "ch12 Terminology Glossary ★"},
            {"file": "ch13_evolution_decisions_anchor.mp3",          "title": "ch13 Evolution Decisions ★"},
            {"file": "ch14_ideas_discoveries_anchor.mp3",            "title": "ch14 Ideas Discoveries ★"},
            {"file": "ch15_learning_discoveries_anchor.mp3",         "title": "ch15 Learning Discoveries ★"},
            {"file": "ch16_cost_tracking_anchor.mp3",                "title": "ch16 Cost Tracking ★"},
            {"file": "ch16_knowledge_enricher_anchor.mp3",           "title": "ch16 Knowledge Enricher ★"},
            {"file": "ch17_clip_name_parser_anchor.mp3",             "title": "ch17 Clip Name Parser ★"},
            {"file": "ch18_competition_detection_anchor.mp3",        "title": "ch18 Competition Detection ★"},
            {"file": "ch19_export_pipeline_anchor.mp3",              "title": "ch19 Export Pipeline ★"},
            {"file": "ch20_format_b_path_resolution_anchor.mp3",     "title": "ch20 Format B Path ★"},
            {"file": "ch21_library_routing_anchor.mp3",              "title": "ch21 Library Routing ★"},
        ]
    },
    {
        "phase": 4,
        "title": "Agents & Workflows — The Automation Layer",
        "description": "Who does what and how. Agents, workflows, Resolve MCP.",
        "tracks": [
            {"file": "vault_audio/content_orchestrator_audio.mp3",   "title": "Content Orchestrator"},
            {"file": "vault_audio/data_orchestrator_audio.mp3",      "title": "Data Orchestrator"},
            {"file": "vault_audio/video_orchestrator_audio.mp3",     "title": "Video Orchestrator"},
            {"file": "vault_audio/bdf_memory_agent_audio.mp3",       "title": "BDF Memory Agent"},
            {"file": "vault_audio/resolve_editing_agent_audio.mp3",  "title": "Resolve Editing Agent"},
            {"file": "vault_audio/davinci_resolve_mcp_audio.mp3",    "title": "DaVinci Resolve MCP"},
            {"file": "vault_audio/resolve_mcp_server_audio.mp3",     "title": "Resolve MCP Server"},
            {"file": "vault_audio/bdf_video_production_flow_audio.mp3","title": "BDF Video Production Flow"},
            {"file": "vault_audio/bdf_knowledge_build_flow_audio.mp3","title": "BDF Knowledge Build Flow"},
            # Resolve deep dive chapters
            {"file": "ch01_resolve_free_tier_nils_anchor.mp3",       "title": "ch01 Resolve Free Tier ★"},
            {"file": "ch02_bridge_reload_discipline_anchor.mp3",     "title": "ch02 Bridge Reload ★"},
            {"file": "ch03_windows_encoding_patterns_anchor.mp3",    "title": "ch03 Windows Encoding ★"},
            {"file": "ch04_mcp_bridge_architecture_anchor.mp3",      "title": "ch04 MCP Bridge ★"},
            {"file": "ch11_first_end_to_end_export_anchor.mp3",      "title": "ch11 First Export ★"},
            {"file": "ch12_nuclear_clear_tool_anchor.mp3",           "title": "ch12 Nuclear Clear ★"},
            {"file": "ch13_deploy_discipline_anchor.mp3",            "title": "ch13 Deploy Discipline ★"},
            {"file": "ch14_async_export_pattern_anchor.mp3",         "title": "ch14 Async Export ★"},
            {"file": "ch15_clip_type_system_anchor.mp3",             "title": "ch15 Clip Type System ★"},
        ]
    },
    {
        "phase": 5,
        "title": "Programming Fundamentals",
        "description": "Code concepts, tools, and patterns — explained through your own codebase.",
        "tracks": [
            # BRAINOS guides
            {"file": "brainos_chapters/programming_terminology_reference_audio.mp3", "title": "Programming Terminology"},
            {"file": "brainos_chapters/guide_venv_audio.mp3",                        "title": "Virtual Environments"},
            {"file": "brainos_chapters/guide_lancedb_audio.mp3",                     "title": "LanceDB Guide"},
            {"file": "brainos_chapters/guide_mcp_ecosystem_audio.mp3",               "title": "MCP Ecosystem"},
            {"file": "brainos_chapters/guide_obsidian_claude_audio.mp3",             "title": "Obsidian + Claude"},
            {"file": "brainos_chapters/claudeguide_mcp_setup_audio.mp3",             "title": "Claude MCP Setup"},
            {"file": "brainos_chapters/claudeguide_prompting_architecture_audio.mp3","title": "Prompting Architecture"},
            {"file": "brainos_chapters/claudeguide_skills_system_audio.mp3",         "title": "Skills System"},
            {"file": "brainos_chapters/claudeguide_claude_md_standards_audio.mp3",   "title": "CLAUDE.md Standards"},
            {"file": "brainos_chapters/resolve_mcp_guide_audio.mp3",                 "title": "Resolve MCP Guide"},
        ]
    },
    {
        "phase": 6,
        "title": "Session Archive — Build History",
        "description": "Raw session recordings. Listen to understand how the system evolved.",
        "tracks": [
            {"file": "_session_20260331_1354_combined_af_heart_audio.mp3", "title": "Session 2026-03-31 1354"},
            {"file": "_session_20260331_1435_combined_af_heart_audio.mp3", "title": "Session 2026-03-31 1435"},
            {"file": "_session_20260331_1445_combined_af_heart_audio.mp3", "title": "Session 2026-03-31 1445"},
            {"file": "_session_20260331_1457_combined_af_heart_audio.mp3", "title": "Session 2026-03-31 1457"},
            {"file": "_session_20260331_1511_combined_af_heart_audio.mp3", "title": "Session 2026-03-31 1511"},
        ]
    },
]


def count_tracks(path: dict) -> tuple[int, int]:
    """Return (total_tracks, existing_files)."""
    total, exists = 0, 0
    for phase in path:
        for track in phase["tracks"]:
            total += 1
            p = CONVERTED_DIR / track["file"]
            if p.exists():
                exists += 1
    return total, exists


def export_manifest(path: dict, output: Path):
    """Export full manifest as JSON."""
    manifest = []
    for phase in path:
        for i, track in enumerate(phase["tracks"], 1):
            p = CONVERTED_DIR / track["file"]
            manifest.append({
                "phase":    phase["phase"],
                "phase_title": phase["title"],
                "track":    i,
                "title":    track["title"],
                "file":     track["file"],
                "exists":   p.exists(),
                "size_mb":  round(p.stat().st_size / 1024 / 1024, 1) if p.exists() else None,
            })
    output.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"[learning_path] Manifest saved: {output}")


def export_m3u(path: dict, output: Path):
    """Export M3U playlist per phase."""
    output.mkdir(parents=True, exist_ok=True)
    for phase in path:
        m3u_path = output / f"Phase_{phase['phase']:02d}_{phase['title'][:30].replace(' ', '_')}.m3u"
        lines = ["#EXTM3U", f"# Phase {phase['phase']}: {phase['title']}"]
        for track in phase["tracks"]:
            p = CONVERTED_DIR / track["file"]
            lines.append(f"#EXTINF:-1,{track['title']}")
            lines.append(str(p))
        m3u_path.write_text("\n".join(lines), encoding="utf-8")
        print(f"  ✅ {m3u_path.name} ({len(phase['tracks'])} tracks)")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--export",  choices=["manifest", "m3u", "both"], default="both")
    args = parser.parse_args()

    total, exists = count_tracks(LEARNING_PATH)

    print(f"\n{'='*60}")
    print(f"  BRAIN OS LEARNING PATH")
    print(f"{'='*60}")

    for phase in LEARNING_PATH:
        phase_exists = sum(1 for t in phase["tracks"]
                          if (CONVERTED_DIR / t["file"]).exists())
        pct = int(100 * phase_exists / len(phase["tracks"]))
        bar = "█" * (pct // 10) + "░" * (10 - pct // 10)
        print(f"\n  Phase {phase['phase']}: {phase['title']}")
        print(f"  [{bar}] {phase_exists}/{len(phase['tracks'])} files ({pct}%)")
        if args.dry_run:
            for t in phase["tracks"]:
                p = CONVERTED_DIR / t["file"]
                status = "✓" if p.exists() else "·"
                print(f"    [{status}] {t['title']}")

    print(f"\n{'='*60}")
    print(f"  TOTAL: {exists}/{total} files ready ({int(100*exists/total)}%)")
    print(f"{'='*60}\n")

    if args.dry_run:
        return

    if args.export in ("manifest", "both"):
        export_manifest(LEARNING_PATH, OUTPUT_DIR / "learning_path_manifest.json")

    if args.export in ("m3u", "both"):
        print("\n  Generating M3U playlists...")
        export_m3u(LEARNING_PATH, OUTPUT_DIR / "playlists")


if __name__ == "__main__":
    main()
