#chBDF_PLATFORM Session Compile — April 18-19, 2026

## SESSION OVERVIEW
This was a major organizational and infrastructure session spanning two days. Four main threads: Claude learning system creation, Read-Along App venv rebuild, Resolve MCP Server expansion from 11 to 52 tools, and establishing the project cheatsheet handoff system.

---

## THREAD 1: CLAUDE LEARNING SYSTEM (Audio Guides)

### What Was Built
A complete audio learning library using Edge TTS (en-US-GuyNeural voice, rate="-5%"). The workflow: Claude generates a narration script (.txt) and a Python generator script (.py). Cristian runs the generator on his Predator to produce natural-sounding MP3s. Files are saved to C:\Knowledge\[TopicFolder]\ and backed up to Google Drive via drag-and-drop.

### Audio Guides Created
1. Claude Code Extended Guide (~25-30 min) — 6 chapters covering what Claude Code is, 12 key terms, Windows installation, first session walkthrough, advanced patterns, and common mistakes.

2. Claude AI Platform Extended Guide (~25-30 min) — 11 chapters covering the LLM system, memory system, all skills, all tools, artifacts, context window, past conversation search, user preferences, plans/pricing, and advanced terminology.

3. Project Regrouping Guide — 9 chapters mapping all projects, pending tasks, file locations, and how everything connects.

4. Project Cheatsheet Guide — 10 chapters covering all 4 projects with April 18 updates, the session handoff workflow, and complete rules.

5. Resolve MCP Guide — 11 chapters covering the MCP architecture, pyautogui workaround, all terminology, startup sequence, file structure, and next steps.

### System Saved to Memory
Trigger phrase: "Create a learning guide for [topic] using my audio learning system"

### Key Decision: gTTS vs Edge TTS
- gTTS tried first but sounds robotic
- espeak tried as fallback — even worse
- Edge TTS with en-US-GuyNeural was the solution — clear, natural, human-sounding
- Edge TTS is installed globally: pip install edge-tts

## THREAD 2: PROJECT CHEATSHEET SYSTEM

### Problem
Claude kept losing track of project state between conversations. Cristian wasted time re-explaining what had been built.

### Solution: Individual Project Cheatsheets
Split the master cheatsheet into individual files to save tokens.

### Workflow
- START of every Claude chat: upload the project file + rules.txt
- END of sessions where things changed: ask Claude to update the cheatsheet

### Rules Added
- Rule 11: Always where.exe python, never where python in PowerShell
- Rule 12: Never put Python projects or venvs inside OneDrive
- Rule 13: Upload cheatsheet at START of every new Claude chat

## THREAD 3: READ-ALONG APP VENV REBUILD

### Problem
The Read-Along App backend venv had corrupted .exe launchers. The shebang paths pointed to old location. Every pip command failed.

### Fix Applied
1. Deleted old venv
2. Created fresh venv at correct path
3. Installed PyTorch 2.11.0+cu128 from CUDA wheels
4. Verified CUDA: RTX 5070 Ti detected
5. Confirmed FFmpeg and Whisper installed

### Key Lesson
Python venvs hardcode absolute paths. Moving the folder breaks those paths. Always delete and recreate the venv at the new location.

## THREAD 4: RESOLVE MCP SERVER EXPANSION (11 → 52 TOOLS)

### Starting State
11 tools: play_pause, cut_at_playhead, ripple_delete, add_marker, go_to_start, save, undo, zoom_fit, go_to_edit_page, go_to_color_page, go_to_deliver_page.

### Expansion Phase 1: Core Editing Tools (11 → 31)
Added: stop, play_reverse, play_forward, go_to_end, next_marker, prev_marker, next_clip, prev_clip, nudge_forward, nudge_back, select_clip_at_playhead, delete_selected, redo, zoom_in, zoom_out, fullscreen_preview, go_to_media_page, go_to_cut_page, go_to_fusion_page, go_to_fairlight_page.

### Expansion Phase 2: Audio & Export Tools (31 → 43)
Added: set_in_point, set_out_point, clear_in_out, delete_between_in_out, normalize_audio, add_fade_in, solo_audio_track, mute_audio_track, split_audio_video, quick_export, add_to_render_queue, start_render, loop_playback.

### Expansion Phase 3: Color Page Tools (43 → 52)
Added: add_serial_node, add_parallel_node, add_layer_node, reset_grade, copy_grade, paste_grade, toggle_bypass, next_node, prev_node.

### Git Initialized
Initial commit: 1dbece3

### MCP Connection Notes
- Server uses stdio transport (no ports, no network)
- Startup order matters: Resolve first, then Claude Desktop
- After updating server.py, must fully quit Claude Desktop and relaunch

### Editing Workflow Explained
Markers are reference points (bookmarks), not cuts. The editing workflow:
1. Marking pass — watch video, drop markers at important moments
2. Cutting pass — go to each marker, make cuts, delete unwanted sections
3. In/out points define a range for looping, exporting, or bulk deletion
4. Ripple delete removes clips AND closes gaps; regular delete leaves black space

## MACHINE STATE AFTER THIS SESSION

### Environment Verified
- Python 3.12.10 (system)
- PyTorch 2.11.0+cu128 (Read-Along venv, CUDA verified)
- FFmpeg installed system-wide
- Whisper installed (Read-Along venv)
- Edge TTS installed globally
- Git for Windows installed
- DaVinci Resolve 20 running

### Active Venvs
- BDF: C:\Dev\Projects\soccer-content-generator\venv\ (mature, production)
- CA: C:\Dev\CristianConstruction\venv\ (functional)
- Read-Along: C:\Users\titit\Projects\read-along-app\backend\venv\ (REBUILT 4/18, CUDA verified, needs FastAPI)
- Resolve MCP: C:\Users\titit\Projects\resolve-mcp-server\venv\ (mcp, pyautogui, pywinauto)
