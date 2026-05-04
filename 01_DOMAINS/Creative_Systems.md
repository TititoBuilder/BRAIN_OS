---
tags: [domain, creative-systems, video, audio, content, workflows]
created: 2026-05-03
updated: 2026-05-03
domain: Creative Intelligence Layer
---

# Creative Systems — Content & Workflow Brain

**What This Is:** Your content creation, video editing, audio production, and creative automation work.

**Why It Exists:** To see all your creative systems and how you've automated the creative process.

---

## Core Concepts You're Building With

- **Video Editing Automation** - DaVinci Resolve + MCP control
- **Audio Production** - TTS systems for learning content
- **Content Repurposing** - One source → multiple formats
- **Streaming Workflows** - OBS recording and streaming
- **Creative Pipelines** - Automated media processing
- **Visual Storytelling** - Soccer highlights, B-roll, editing techniques

---

## Active Projects

### [[Resolve_Workflows]]
**Location:** DaVinci Resolve 20 + MCP Server  
**What:** Automated video editing with AI control  
**Status:** 52 tools operational, ready for guitar footage testing  
**Tech:** DaVinci Resolve 20, Python MCP server, pyautogui automation

**Editing Capabilities:**
- **Playback Control** (11 tools): play, pause, stop, forward, reverse, markers
- **Timeline Editing** (15 tools): cut, ripple delete, split, nudge, select clips
- **In/Out Points** (4 tools): set in, set out, clear, delete between
- **Audio Tools** (4 tools): normalize, fade in/out, solo, mute, split audio/video
- **Export Tools** (3 tools): quick export, render queue, start render
- **Color Grading** (9 tools): nodes, grading, copy/paste, bypass
- **Navigation** (6 tools): page switching, zoom, fullscreen

**Workflow Pattern:**
1. **Marking pass** - Watch, drop markers at key moments
2. **Cutting pass** - Go to markers, cut, delete unwanted
3. **Audio pass** - Normalize, add fades, split where needed
4. **Color pass** - Grade clips, add nodes
5. **Export pass** - Quick export or render queue

**Pending:**
- [ ] Practice full workflow on guitar footage
- [ ] Test all 52 tools end-to-end
- [ ] Build jump_to_timecode tool (type timecode to jump)

### [[Read_Along_App]]
**Location:** `C:\Users\titit\Projects\read-along-app\`  
**What:** Whisper-powered transcription app with sync  
**Status:** MVP complete, venv rebuilt (2026-04-18)  
**Tech:** Python, Whisper, PyTorch CUDA, FastAPI, React frontend

**Components:**
- Backend: Whisper transcription (GPU-accelerated)
- Frontend: React UI with sync playback
- CUDA: PyTorch 2.11.0+cu128 on RTX 5070 Ti
- FFmpeg: Audio processing

**Venv rebuilt (April 18):**
- Issue: Corrupted .exe launchers from folder move
- Fix: Deleted old venv, created fresh at new location
- Lesson: Venvs hardcode paths, can't be moved

**Pending:**
- [ ] Install fastapi, uvicorn, python-multipart
- [ ] Create requirements.txt
- [ ] Test full transcription workflow

### [[Audio_Systems]]
**Location:** Multiple systems for different purposes  
**What:** Two complementary TTS systems  
**Status:** Both operational, documented, clarified

**System 1: Kokoro TTS (CA Book Audio)**
- **Voice:** af_heart (American English, warm female)
- **Cost:** $0 (100% FREE, local GPU)
- **Format:** WAV (lossless)
- **Automation:** HIGH - one command `ca-audio ch01`
- **Use:** CA Book chapter audio generation
- **Location:** `C:\Dev\Projects\custom-agent\ca_audio.py`

**System 2: Edge TTS (Learning Guides)**
- **Voice:** en-US-GuyNeural (male, slightly slower)
- **Cost:** $0 (100% FREE, Microsoft service)
- **Format:** MP3
- **Automation:** LOW - 3 manual steps (generate → run → upload)
- **Use:** One-off learning guides, documentation
- **Created:** April 18, 2026

**Files Created (Edge TTS):**
- Claude Code Extended Guide (~25-30 min, 6 chapters)
- Claude AI Platform Extended Guide (~25-30 min, 11 chapters)
- Project Regrouping Guide (9 chapters)
- Project Cheatsheet Guide (10 chapters)
- Resolve MCP Guide (11 chapters)

**Decision Framework:**
- Repetitive chapter generation → Kokoro (automated)
- One-off learning guides → Edge TTS (natural voice)

### [[OBS_Setup]]
**Location:** OBS Studio (streaming software)  
**What:** Recording and streaming workflows  
**Status:** Installed, not yet integrated with MCP  
**Tech:** OBS Studio, potential MCP server

**Not to confuse with:** Obsidian (note-taking app)

**Pending:**
- [ ] Document OBS recording workflow
- [ ] Explore OBS MCP integration
- [ ] Test streaming configurations

---

## Media & Asset Management

### Current Structure
```
C:\Media\
├── GuitarProject\
│   ├── originals\
│   │   └── cristian_guitar_01.MOV (54 MB)
│   ├── exports\
│   └── resolve_projects\
```

### BDF Content Pipeline
```
C:\Knowledge\BDF\
├── chapters\ - Book content
├── images\ - Generated graphics
└── videos\ - Highlight compilations
```

### Audio Library
```
C:\Knowledge\CA\CA_Book\audio\ - CA Book audio files
C:\Knowledge\Claudeguide\ - Learning guide MP3s
C:\Knowledge\ResolveMCP\ - Resolve guide audio
```

---

## Creative Workflows

### Soccer Highlight Production (BDF)
1. **Source:** Match footage
2. **Edit:** DaVinci Resolve
3. **Graphics:** Python-generated player cards
4. **Audio:** Commentary/music
5. **Export:** Social media formats
6. **Distribute:** Multiple platforms

**Automation Level:** Medium-High

### Learning Guide Production
1. **Claude generates** narration script (.txt)
2. **Claude generates** Python TTS script (.py)
3. **User runs** generator → MP3 created
4. **User uploads** to Google Drive

**Automation Level:** Medium

### Book Audio Production (CA Book)
1. **User runs** `ca-audio ch01_title`
2. **System reads** markdown chapter
3. **Kokoro generates** audio (WAV)
4. **System uploads** to Google Drive
5. **Telegram alert** sent

**Automation Level:** High

---

## Pending Tasks (Creative Systems)

### Critical (Do Soon)
- [ ] Practice full Resolve editing workflow
- [ ] Test all 52 MCP tools on guitar footage
- [ ] Install FastAPI for Read-Along backend

### Important (Next)
- [ ] Build jump_to_timecode for Resolve
- [ ] Document OBS recording workflow
- [ ] Create Read-Along requirements.txt

### Someday/Maybe
- [ ] Explore OBS MCP integration
- [ ] Build automated B-roll workflow
- [ ] Research: music pipeline automation

---

## Knowledge Base (Compiled Sessions)

**Sessions documenting creative work:**
- [[2026-04-18_Resolve_MCP_Expansion]] - 11 → 52 tools
- [[2026-04-18_Edge_TTS_Learning_System]] - Audio guide creation
- [[2026-04-18_Read_Along_Venv_Rebuild]] - Venv corruption fix
- More sessions to compile from 09_TOOLS/ and past chats

---

## Book Content Candidates

**For CA Book (Personal Development):**
- Audio learning guide creation
- Building hands-on learning systems
- Creative automation for knowledge work

**For BDF Book (Soccer + Technology):**
- Automated highlight production
- AI-powered content creation
- Video editing workflows
- Creative systems for content creators

---

## Learning Journey

**What you've built without realizing:**
- Complete video editing automation (52 Resolve tools)
- Dual audio production systems (Kokoro + Edge TTS)
- Transcription pipeline (Whisper + React)
- Media asset management
- Creative workflow automation

**Terms you now understand:**
- Timeline editing, markers, in/out points
- Ripple delete, split clips, audio normalization
- Color grading nodes, GPU acceleration
- TTS (text-to-speech), voice synthesis
- CUDA, PyTorch, FFmpeg
- Venv isolation, dependency management

---

## Connected Domains
- [[AI_Engineering]] - Automation tools, MCP servers
- [[Data_Science]] - Asset organization, workflow optimization

---

## Tools That Connect Here
- [[Resolve_MCP]] - Video editing automation
- [[Audio_Systems_Comparison]] - TTS system selection
- [[Edge_TTS_Learning_System]] - Learning guide creation
- [[Custom_Agent_TTS]] - CA Book audio generation
