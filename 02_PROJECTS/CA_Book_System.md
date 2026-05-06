---
tags: [book, project]
book_project: ca
book_status: active
created: 2026-05-05
updated: 2026-05-05
domain: Creative_Systems
---

# CA Book System

**What This Is:** Automated knowledge compilation pipeline for the Custom Agent (CA) business. Identical architecture to BDF Book System — session logs compiled into chapters, stitched into master book, uploaded to Google Drive.

**Why It Exists:** Preserve CA business knowledge — origin story, system design, leads, pricing, deployment, and lessons learned.

---

## Pipeline

```
Session log → ca-book run → Claude Opus compiles chapter
→ chapter .md saved → stitch_master_book() → CA_Master_Book.txt
→ sync to Google Drive
```

**Command:**
```powershell
cd C:\Knowledge\CA\CA_Book
# Activate CA venv
C:\Knowledge\CA\venv\Scripts\Activate.ps1
python book_compiler.py           # process incoming + stitch
python book_compiler.py --status  # check current state
```

---

## File Locations

| Component | Path |
|---|---|
| Compiler | `C:\Knowledge\CA\CA_Book\book_compiler.py` |
| Chapters (canonical) | `C:\Knowledge\CA\CA_Book\chapters\` |
| Session resumes | `C:\Knowledge\CA\Session_Resumes\` |
| Master book (derived) | `C:\Knowledge\CA\CA_Book\CA_Master_Book.txt` |
| venv | `C:\Knowledge\CA\venv\` |

---

## Architecture

### Canonical Source: Chapters
Chapter `.md` files in `chapters\` are the source of truth. Master book is a **derived artifact** — regenerated on every run. Never edit it directly.

### stitch_master_book()
Same function as BDF. Loops `ch01 → ch10`, reads each `.md` file, concatenates with dividers, writes `CA_Master_Book.txt`. Also uploads to Google Drive immediately after writing.

### Differences vs BDF Book

| Property | BDF Book | CA Book |
|---|---|---|
| Chapter format | `.txt` | `.md` |
| Chapter count | 27 files (dupes present) | 10 files (clean) |
| Compiler location | `C:\Dev\Projects\soccer-content-generator\` | `C:\Knowledge\CA\CA_Book\` |
| venv | BDF dev venv | `C:\Knowledge\CA\venv\` (independent) |
| Post-processing | Kokoro TTS + Drive | Drive only (no TTS) |
| Master book | `BDF_Master_Book.txt` | `CA_Master_Book.txt` |

---

## Chapter Inventory

| File | Topic | Size |
|---|---|---|
| ch01_origin | Origin — how CA was conceived and built in South CA | 12 KB |
| ch02_system | System design | 16 KB |
| ch03_leads | Leads pipeline | 16 KB |
| ch04_agents | Agent architecture | 19 KB |
| ch05_pricing | Pricing strategy | 16 KB |
| ch06_brand | Brand | 14 KB |
| ch07_deployment | Deployment | 9 KB |
| ch08_relationships | Relationships | 14 KB |
| ch09_finance | Finance | 18 KB |
| ch10_lessons | Lessons learned | 15 KB |

**Total: 10 files, no duplicates. Clean numbering. ✅**

---

## GDrive Credentials Note

`book_compiler.py` line 34 references BDF project dir for shared GDrive credentials:
```python
GDRIVE_CREDS_DIR = Path(r"C:\Dev\Projects\soccer-content-generator")
# Uses: gdrive_credentials.json + gdrive_token.json
```
This is intentional — both books share one GDrive auth. Not a bug, just a dependency to be aware of.

---

## venv Note

`C:\Knowledge\CA\venv\` is the correct independent venv for CA book compilation.
Separate issue: `ca_audio.py` (custom-agent) still shares BDF dev venv — tracked on backlog as venv separation task.

---

## Connected Nodes

- [[BDF_Book_System]] — sister book, identical architecture
- [[Creative_Systems]] — parent domain
