---
tags: [book, project]
book_project: ca
book_status: active
created: 2026-05-05
updated: 2026-05-05
domain: Creative_Systems
---

# CA Book System

**What This Is:** Automated knowledge compilation pipeline for Cartoon Animator 5 (CA5) work. Identical architecture to BDF Book System — session logs compiled into chapters, stitched into master book, uploaded to Google Drive.

**Why It Exists:** Preserve CA5 rigging, animation, and pipeline knowledge built across sessions.

---

## Pipeline

```
Session log → ca-book run → Claude Opus compiles chapter
→ chapter .md saved → stitch_master_book() → CA_Master_Book.txt
→ sync to Google Drive
```

**Command:** `ca-book run` (run from CA book directory)

---

## File Locations

| Component | Path |
|---|---|
| Compiler | `C:\Knowledge\CA\CA_Book\book_compiler.py` |
| Chapters (canonical) | `C:\Knowledge\CA\CA_Book\chapters\` |
| Session resumes | `C:\Knowledge\CA\Session_Resumes\` |
| Master book (derived) | `CA_Master_Book.txt` (inside CA_Book\) |
| venv | `C:\Knowledge\CA\venv\` |

---

## Architecture

### Canonical Source: Chapters
Chapter `.md` files in `chapters\` are the source of truth. Master book is a **derived artifact** — regenerated on every run. Never edit it directly.

### stitch_master_book()
Same function as BDF. Loops `ch01 → ch10`, reads each `.md` file, concatenates with dividers, writes `CA_Master_Book.txt`. Fires automatically at end of every `ca-book run`. Also uploads to Google Drive immediately after writing.

### Differences vs BDF Book

| Property | BDF Book | CA Book |
|---|---|---|
| Chapter format | `.txt` | `.md` |
| Chapter count | 16 | 10 |
| Compiler location | `C:\Dev\Projects\soccer-content-generator\` | `C:\Knowledge\CA\CA_Book\` |
| Post-processing | Kokoro TTS + Drive | Drive only (no TTS) |
| Master book | `BDF_Master_Book.txt` | `CA_Master_Book.txt` |

---

## Chapter Inventory

| Chapter | Topic | Status |
|---|---|---|
| ch01-ch10 | CA5 rigging, animation, pipeline topics | To be audited |

**Action needed:** Open `C:\Knowledge\CA\CA_Book\chapters\` and audit actual chapter titles.

---

## venv Note

CA has a venv at `C:\Knowledge\CA\venv\` — separate from the BDF venv. This needs to be reconciled with the venv separation task on the backlog (currently CA is sharing BDF venv at `C:\Dev\Projects\soccer-content-generator\venv\`). Clarify which venv `ca-book run` actually uses.

---

## Connected Nodes

- [[BDF_Avatar_Pipeline]] — CA5 rigging pipeline feeds into avatar system
- [[BDF_Book_System]] — sister book, identical architecture
- [[Creative_Systems]] — parent domain
