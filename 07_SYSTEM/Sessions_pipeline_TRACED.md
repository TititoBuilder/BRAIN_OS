# Sessions Pipeline — TRACE COMPLETE (append to Sessions_Tab_Design_Notes.md)

## The third pipeline — FOUND

The resume audio is made by a TWO-STAGE chain (both your code, soccer project):

1. converter.py  -> reads a source .md, produces a `{name}_TTS.txt`
   (narration-ready text: strips frontmatter/markdown, expands for speech)
2. tts_local.py  -> reads the `_TTS.txt`, produces `{name}.mp3`
   Kokoro-82M, default voice af_heart, CUDA on the Predator GPU.
   Location: C:\Dev\Projects\soccer-content-generator\tts_local.py
   Usage: python tts_local.py converted/<name>_TTS.txt --voice af_heart

Then (separately) the .mp3 is uploaded to Drive + indexed — same pipeline we
used for the 50 topics (upload_file -> id: entry in drive_index.json).

## The source content — FOUND

Resumes are narrated versions of LIVE SYSTEM DOCS, not purpose-written lessons:
  master_control       <- 07_SYSTEM\Master_Control.md
  cristian_principles  <- 07_SYSTEM\Cristian_Principles.md
  project_directory    <- 07_SYSTEM\Project_Directory.md
  ...etc

So the Sessions/Resumes content SOURCE = 07_SYSTEM + 02_PROJECTS docs.
This means resumes are REGENERATABLE and AUTO-UPDATABLE: edit the system doc,
re-run converter.py -> tts_local.py -> upload. Not static artifacts.

## Bonus finding: the {key}_audio twins explained

The ~21 `{key}_audio.mp3` staging duplicates (e.g. master_control.mp3 +
master_control_audio.mp3) are TWO generation passes of the same source doc
under different output-naming. Harmless residue. The hygiene cleanup is now
understood: keep the indexed name, delete the other. (Still a separate pass.)

## Sessions tab — now fully scoped

- SOURCE: 07_SYSTEM + 02_PROJECTS system/project docs
- PIPELINE: converter.py -> tts_local.py (Kokoro af_heart) -> upload -> index
  (same proven flow as the 50-topic batch)
- GROUPING: by project, reuse session_close.py _PROJECT_KEYWORDS
  {BDF, CA, BRAIN_OS, MCP, Resolve} — do NOT invent new taxonomy
- STATE: the 31 are already generated/uploaded/indexed; they need (a) a
  project tag the backend can read, and (b) a view (Sessions tab or 3rd LISTEN
  section) grouped by project.

## Remaining build steps (future session)
1. Decide project-tagging source for the 31 (mirror _PROJECT_KEYWORDS in a
   small map the backend reads; do not pollute obsidian_sync — these aren't
   learning topics).
2. Backend: expose type="session" + project for these entries.
3. Frontend: Sessions view grouped by project (reuse Scheme C pattern + CSS).
4. Optional: wire converter.py -> tts_local.py as a "regenerate resume" step so
   editing a 07_SYSTEM doc can refresh its audio.
