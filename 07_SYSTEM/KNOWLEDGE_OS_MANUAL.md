# KNOWLEDGE OS — User Manual
**Cristian · v1.0 · Built May 2026**

---

## What Is This?

Knowledge OS is your personal computing encyclopedia and learning tracker. It does three things:

1. **Tracks every technology topic you're learning** — with a score, status, and proof of real usage
2. **Builds audio playlists** — exports a manifest your stitcher uses to create one continuous MP3
3. **Syncs to your Obsidian vault** — writes your scores into vault notes as frontmatter

Think of it as a living map of your brain. Every topic you've touched, every skill you've proven, every gap you still need to fill — all in one place.

---

## The Three Files

| File | Location | What It Does |
|---|---|---|
| `knowledge_os.html` | `C:\BRAIN_OS\09_TOOLS\` | The app — open in Chrome |
| `audio_stitcher.py` | `C:\BRAIN_OS\09_TOOLS\` | Stitches audio files into one MP3 |
| `obsidian_sync.py` | `C:\BRAIN_OS\09_TOOLS\` | Writes scores to Obsidian vault |

---

## Opening the App

Double-click `knowledge_os.html` on your Desktop (or at `C:\BRAIN_OS\09_TOOLS\`). Chrome opens. The app loads in under 2 seconds. No internet required after first load.

Your data saves automatically in Chrome's localStorage. It survives restarts and is never lost unless you clear browser data.

---

## The Three Tabs

### Tab 1 — DASHBOARD

Your knowledge health at a glance.

**Domain Mastery**
Nine colored bars — one per domain. The number is your average score across all topics in that domain. Watch these numbers climb as you study and update your scores.

**Velocity Tracker**
Shows when you last touched each domain. Color-coded:
- GREEN (HOT) — touched in the last 7 days
- AMBER (WARM) — touched in the last 30 days
- RED (COLD) — not touched in over 30 days

Cold domains are the ones going stale. Use this to decide what to study next.

**Focus Now**
Auto-generated list of your highest-priority topics that have no build evidence yet. These are your most important gaps. If a High-priority topic has no evidence, it means you learned it in theory but haven't applied it in real code. That's what you fix next.

**Evidence Portfolio**
Every topic where you've linked real proof — a script, a project, a commit. This is your production portfolio. When someone asks what you know, this is the answer.

---

### Tab 2 — ENCYCLOPEDIA

Your full topic list. 78 topics pre-loaded across 9 domains.

**Filtering**
Use the filter bar at the top to narrow down:
- Search by topic name, machine_key, or evidence text
- Filter by Domain, Status, Priority, or Audio status
- Most useful filter: `Priority: High` + `Status: Not Started` = your critical gaps

**Each row shows:**
- Topic name + machine_key (the file identifier)
- Evidence line (green) — proof of real usage
- Domain badge
- Status badge — Not Started / Learning / Practiced / Mastered
- Priority badge — Low / Medium / High
- Score (0–100) with mini bar
- Audio badge — [NONE] / [READY] / [DONE] + duration in minutes
- Two buttons: `e` (edit) and `+` (add to manifest queue)

**Editing a topic**
Click `e` on any row. A modal opens with:
- All fields editable
- Score slider (drag to set 0–100)
- Build Evidence text field — paste the exact file path or project name where you used this skill
- Audio duration in seconds

Always fill in Build Evidence when you've applied something in real code. That's what makes the score meaningful.

**Adding a new topic**
Click `+ New Topic` in the header (visible in Encyclopedia tab). Fill in name, machine_key (snake_case), domain, priority. Add initial evidence if you already have it.

---

### Tab 3 — MANIFEST BUILDER

Build a custom audio learning session.

**Adding topics to the queue**
Go to Encyclopedia → click `+` on any topic. The button turns green with a checkmark. The topic is now in your queue. Switch to Manifest Builder to see it.

**The queue**
Each queued track shows:
- Track number (01, 02, 03...)
- Topic name + domain + audio status + duration
- Transition text — this is the narration spoken between tracks ("Next: RAG Pipelines.")

Edit the transition text to make it contextual. Instead of "Next: Vector Databases", write "Now let's see how vectors are actually stored."

**Reordering**
Use `^` and `v` buttons to move tracks up or down. Put related topics together. Build a narrative arc — foundations first, then applications.

**Duration display**
The header shows total stitched duration in hours and minutes. This is how long your MP3 will be. A good session is 45–90 minutes. If you're commuting 30 minutes each way, queue 60 minutes.

**Export audio_manifest.json**
Click this button when your queue is ready. A JSON file downloads to your Downloads folder. This file feeds directly into `audio_stitcher.py`.

---

## The Two Export Buttons

Both buttons live in the header, always visible.

### ↓ Obsidian Sync
Exports `obsidian_sync.json` — all 78 topics with current scores, statuses, and evidence. Feed this to `obsidian_sync.py` to update your vault.

### Export audio_manifest.json (Manifest Builder tab)
Exports the current queue as a manifest for `audio_stitcher.py`. Only queued topics are included.

---

## The Full Workflow

### Daily Loop (5 minutes)

```
1. Open knowledge_os.html
2. Update 2-3 scores from yesterday's study session
   → click e on the topic → drag score slider → save
3. Click "↓ Obsidian Sync" → obsidian_sync.json saved to Downloads
4. Run sync:
   C:\Knowledge\CA\venv\Scripts\python C:\BRAIN_OS\09_TOOLS\obsidian_sync.py `
     --input "C:\Users\titit\Downloads\obsidian_sync.json" `
     --vault "C:\BRAIN_OS"
```

### Audio Session Build (10 minutes)

```
1. Open knowledge_os.html → Encyclopedia tab
2. Filter: Audio = Raw Audio Ready
3. Click + on 4-6 topics you want to study
4. Switch to Manifest Builder tab
5. Reorder tracks — put foundations before applications
6. Edit transition text to create narrative flow
7. Click "Export audio_manifest.json"
8. Run stitcher:
   C:\Knowledge\CA\venv\Scripts\python C:\BRAIN_OS\09_TOOLS\audio_stitcher.py `
     --manifest "C:\Users\titit\Downloads\audio_manifest.json" `
     --audio-dir "C:\BRAIN_OS\BrainOS_Book\audio" `
     --output "C:\BRAIN_OS\audio_out\session_today.mp3"
9. Load session_today.mp3 on phone
10. Drive / gym / commute — one file, no tapping
```

### Weekly Review (15 minutes)

```
1. Open Dashboard tab
2. Check Velocity Tracker — any RED (cold) domains?
3. Check Focus Now — which High-priority gaps have no evidence?
4. Pick ONE gap to close this week
5. Study it → build something with it → update the score → add evidence
6. Export obsidian_sync.json → run obsidian_sync.py
```

---

## Scoring Guide

Be honest. Scores only help you if they're accurate.

| Score | What It Means |
|---|---|
| 0 | Never touched it |
| 1–30 | Aware of the concept, no hands-on |
| 31–50 | Read about it, followed a tutorial |
| 51–70 | Built something small with it |
| 71–85 | Used it in a real project, could explain it |
| 86–95 | Mastered — built multiple things, could teach it |
| 96–100 | Expert — you go to for this topic |

The score only moves up when you have **build evidence** — a real file path or project name proving you used it. Theory without application stays below 50.

---

## Status Guide

| Status | When To Use |
|---|---|
| Not Started | Never looked at it |
| Learning | Actively reading / watching / studying |
| Practiced | Built something real with it at least once |
| Mastered | Multiple real builds, can explain it without notes |

---

## Audio Status Guide

| Badge | Meaning |
|---|---|
| [NONE] | No audio file exists for this topic |
| [READY] | A raw audio chapter file exists — can be stitched |
| [DONE] | Already included in a stitched session |

---

## The Concept: Build the Loop

The reason this system works is because it's a closed loop — not isolated tools.

```
Study something
    ↓
Apply it in real code (BDF, CA Book, resolve-mcp, etc.)
    ↓
Update score + add evidence in Knowledge OS app
    ↓
Export obsidian_sync.json → run obsidian_sync.py
    ↓
Vault reflects current knowledge state
    ↓
Queue related audio topics → export manifest → run audio_stitcher.py
    ↓
Listen on commute → deepen understanding
    ↓
Apply again → score goes up → loop continues
```

Every tool feeds the next one. The app is the source of truth. The vault is the map. The audio is the teacher. The code is the proof.

---

## File Reference

| What You Export | File Name | Goes Into |
|---|---|---|
| Audio playlist | `audio_manifest.json` | `audio_stitcher.py --manifest` |
| Vault scores | `obsidian_sync.json` | `obsidian_sync.py --input` |

| What Gets Created | Location |
|---|---|
| Stitched MP3 | `C:\BRAIN_OS\audio_out\` |
| Vault stubs | `C:\BRAIN_OS\02_PROJECTS\knowledge_os\` |

---

## Quick Command Reference

**Stitch audio:**
```powershell
C:\Knowledge\CA\venv\Scripts\python C:\BRAIN_OS\09_TOOLS\audio_stitcher.py `
  --manifest "C:\Users\titit\Downloads\audio_manifest.json" `
  --audio-dir "C:\BRAIN_OS\BrainOS_Book\audio" `
  --output "C:\BRAIN_OS\audio_out\session.mp3"
```

**Sync to Obsidian:**
```powershell
C:\Knowledge\CA\venv\Scripts\python C:\BRAIN_OS\09_TOOLS\obsidian_sync.py `
  --input "C:\Users\titit\Downloads\obsidian_sync.json" `
  --vault "C:\BRAIN_OS"
```

**Dry-run (preview only):**
Add `--dry-run` to either command.

**Create vault stubs for unmatched topics:**
Add `--create` to `obsidian_sync.py`.

---

*Knowledge OS — Built session by session. Every score is earned.*
