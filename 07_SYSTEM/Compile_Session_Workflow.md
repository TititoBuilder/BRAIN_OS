---
tags: [system, workflow, compile, reference]
status: live
updated: 2026-05-01
parent: "[[Project_Directory]]"
---

# Compile Session Workflow

Standard end-of-chat procedure for capturing session content into
the BDF and CA knowledge books.

---

## Step-by-Step

**1. Trigger compile inside Claude chat**

Type `compile session` — Claude produces one or more compile files:

| Content type | Output file | Rule |
|---|---|---|
| BDF content | `session_compile_bdf.txt` | Multi-section OK in one file |
| CA content | `session_compile_ca_chXX.txt` | **ONE FILE PER CHAPTER** — CA compiler stops at first `#chXX` tag |

Save all files to `C:\Users\titit\Downloads\`.

**2. Route and compile BDF**

```powershell
bdf-compile "session_compile_bdf.txt"
bdf-book
```

Normal cost: **$1–2.50**. Batching multiple BDF files = $7–8. Never batch.

**3. Route and compile CA (one pair per chapter)**

```powershell
ca-compile "session_compile_ca_ch01.txt"
ca-book

ca-compile "session_compile_ca_ch02.txt"
ca-book
```

After each `ca-book` run: chapter .wav + `CA_Master_Book.txt`
auto-sync to Google Drive `CA_Book_Audio/` — **no extra steps**.

**4. Bulk CA Drive sync (after major multi-chapter expansion only)**

```powershell
cd C:\Dev\Projects\soccer-content-generator
& .\venv\Scripts\Activate.ps1
python "$env:USERPROFILE\Downloads\ca_bulk_[upload.py](http://upload.py)"
```

Uploads all 10 chapter .wav files (skips `test_` files) + `CA_Master_Book.txt`.
Script lives at `C:\Users\titit\Downloads\ca_bulk_[upload.py](http://upload.py)` (uses BDF venv).

---

## Rules

- Mixed-project chats → **separate compile files per book**, never cross-contaminate.
- One CA compile file per chapter — the CA compiler stops at the first `#chXX` tag.
- Always state estimated cost before running any compiler.
- Plain ASCII only in compile files — no emoji, no Unicode in PowerShell-consumed content.

---

## Connected to

- [[PowerShell_Aliases]]
- [[BDF_Canvas]]
- [[Custom_Agent]]
- [[Project_Directory]]
