---
tags: [audio, tts, learning, edge-tts, free, system]
created: 2026-04-18
updated: 2026-05-03
parent: [[07_SYSTEM]]
---

# Edge TTS Learning System

## Purpose
Generate natural-sounding audio learning guides using Microsoft Edge TTS.
Created April 18, 2026 as the second audio generation system alongside Kokoro.

## System Architecture

**Engine:** Microsoft Edge TTS
**Voice:** en-US-GuyNeural (male, American English)
**Rate:** -5% (slightly slower for learning comprehension)
**Cost:** $0 - 100% FREE Microsoft service
**Format:** MP3

## Workflow

1. **User requests learning guide** on a topic
2. **Claude generates narration script** (.txt file)
3. **Claude generates Python generator** (.py file with Edge TTS calls)
4. **User runs generator** on Predator → MP3 created
5. **User manually uploads** to `C:\Knowledge\[TopicFolder]\`
6. **User drag-and-drop** to Google Drive

### Automation Level
**Low** - 3 manual steps (generate → run → upload)

Contrast with Kokoro: **High** - 1 command (`ca-audio ch01`)

## Evolution Timeline

### April 18, 2026 - Creation
**Problem:** Needed natural-sounding audio for learning guides

**Attempt 1 - gTTS:**
- Google Text-to-Speech (neural voice)
- Result: Too robotic despite being "neural"
- Rejected

**Attempt 2 - espeak:**
- Open-source speech synthesizer
- Result: Even more robotic than gTTS
- Rejected

**Solution - Edge TTS:**
- Microsoft Edge TTS service
- en-US-GuyNeural voice
- Result: ✅ Clear, natural, human-sounding
- **Adopted**

### Installation
```bash
pip install edge-tts
```

## Files Created (April 18, 2026)

All saved to `C:\Knowledge\Claudeguide\`:

1. **claude_code_extended_guide.mp3** (~25-30 min)
   - 6 chapters: What is Claude Code, 12 key terms, installation, first session, advanced patterns, mistakes

2. **claude_ai_platform_extended_guide.mp3** (~25-30 min)
   - 11 chapters: LLM system, memory, skills, tools, artifacts, context window, search, preferences, pricing, terminology

3. **project_regrouping_guide.mp3**
   - 9 chapters: All projects, pending tasks, file locations, connections

4. **project_cheatsheet_guide.mp3**
   - 10 chapters: 4 projects with updates, session handoff, complete rules

5. **resolve_mcp_guide.mp3**
   - 11 chapters: MCP architecture, workarounds, terminology, startup, file structure, next steps

All files also backed up to Google Drive `Claudeguide/` folder.

## When to Use

**Best for:**
- One-off learning guides
- Documentation audio
- Tutorial narration
- Knowledge transfer sessions

**NOT for:**
- Repetitive chapter generation (use Kokoro)
- Batch processing (workflow is manual)
- Automated pipelines (3-step manual process)

## Memory Trigger

**Phrase:** "Create a learning guide for [topic] using my audio learning system"

Claude generates narration script + Python generator using Edge TTS.

## Connected to
- [[Audio_Systems_Comparison]]
- [[Custom_Agent_TTS]]
- [[Knowledge_Management]]
- [[Session_Protocol]]
